
import os
from datetime import datetime

from flask import Flask, render_template, request, flash, redirect, url_for, session, Response, jsonify

# from requests import Response
from flaskext.markdown import Markdown
from flask_wtf.csrf  import CSRFProtect

from models import User,Question,Answer
from exts import db
from functools import wraps
from sqlalchemy import or_

import config
app = Flask(__name__)
csrf = CSRFProtect(app)
Markdown(app)
app.config.from_object(config)
app.secret_key='itheima'
db.init_app(app)
#登录限制装饰器
def login_astrict(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            print('sssss')
            return func(*args,**kwargs)

        else:
            print('lalala')
            return redirect(url_for('login'))

    return wrapper


@app.route('/')
def index():
    list = Question.query.order_by(Question.create_time.desc()).all()
    # print(list)
    # print("-------------------------------------------------")
    context={
        'questions': list
    }
    # print(context)

    return render_template('index.html',**context)
@app.route('/login/',methods=['GET','POST'] )
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        telephone=request.form.get('telephone')
        password=request.form.get('password')
        #未加密前验证
        # user=User.query.filter(User.telephone==telephone,User.password==password).first()
        #加密后验证
        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_password(password):
            session['user_id']=user.id
            #如果想在31天免登录
            session.permanent=True

            return redirect(url_for('index'))
        else:
            flash('登陆失败,账号或密码错误')
            return "登陆失败,账号或密码错误"
    # return render_template('login.html')

@app.route('/register/',methods=['GET','POST'] )
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        telephone=request.form.get('telephone')
        username=request.form.get('username')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        #判断手机号是否被注册
        user=User.query.filter(User.telephone == telephone).first()
        if user:
            flash('手机号码已被注册')

        else:#判断两次密码是否相同
            if password1 != password2:
                flash('密码不相同')
            else:
                user=User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
        return redirect(url_for('login'))
@app.route('/logout/')

def logout():
    # session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('login'))
@app.route('/question/',methods=['GET','POST'])
@login_astrict
def question():
    if request.method=='GET':
        return  render_template("question.html")
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question=Question(title=title,content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id==user_id).first()

        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))
@app.route('/detail/<question_id>',methods=['GET','POST'])
def detail(question_id):
    question_model= Question.query.filter(Question.id==question_id).first()

    return render_template('detail.html',question=question_model)




@app.route('/add_answer/',methods=['POST'])
@login_astrict
def add_answer():
    content=request.form.get('answer_comment')
    question_id=request.form.get('question_id')
    answer = Answer(content=content)
    user_id=session['user_id']
    user=User.query.filter(User.id==user_id).first()
    answer.author=user

    question=Question.query.filter(Question.id==question_id).first()
    answer.question=question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))

@app.route('/search/')
def search():
    q=request.args.get('q')
    condition=or_(Question.title.contains(q),Question.content.contains(q))
    questions=Question.query.filter(condition).order_by(Question.create_time.desc())
    # questions=Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q))).first()
    # questions=Question.query.filter(Question.title.contains(q),Question.content.contains(q))

    return render_template('index.html',questions=questions)





@app.context_processor
def my_context_processor():
    user_id=session.get('user_id')
    if user_id:
        user=User.query.filter(User.id==user_id).first()
        if user:
            return {'user':user}
    return {}
@app.route('/upload/', methods=['GET','POST'])
@login_astrict
@csrf.exempt
def upload():
    file = request.files.get('editormd-image-file')
    if not file:
        res = {
            'success': 0,
            'message': '上传失败'
        }
    else:
        ex = os.path.splitext(file.filename)[1]
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + ex
        bodypic_path = 'static/asset/' + filename
        file.save(bodypic_path)
        res = {
            'success': 1,
            'message': '上传成功',
            'url': url_for('.image', name=filename)
        }
    return jsonify(res)
# 隐藏后端静态文件目录的效果
@app.route('/image/<name>', methods=['GET'])
@login_astrict
@csrf.exempt
def image(name):
    current_path = os.path.abspath(os.path.dirname(__file__))
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep)
    filedir = os.path.join(father_path,'project_demo\\static\\asset\\')
    filepath = os.path.join(filedir)
    with open(os.path.join(filepath, name), 'rb') as f:
        resp=Response(f.read(), mimetype="image/jpeg")
        print(resp)
    return resp

if __name__ == '__main__':
    app.run()