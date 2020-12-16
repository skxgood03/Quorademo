#模型
from exts import db
from datetime import datetime
#加密模块
#加密 generate_password_hash
#验证 check_password_hash
from werkzeug.security import generate_password_hash,check_password_hash
class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    telephone=db.Column(db.String(40),nullable=False)
    username=db.Column(db.String(40),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    # 密码加密函数
    def __init__(self,*args,**kwargs):
        telephone = kwargs.get('telephone')
        username = kwargs.get('username')
        password = kwargs.get('password')

        self.telephone=telephone
        self.username=username
        self.password=generate_password_hash(password)
    #验证加密密码
    def check_password(self,raw_password):
        result=check_password_hash(self.password,raw_password)#check_password_has后面加（加密密码，输入的密码）
        return result


    
class Question(db.Model):
    __tablename__='question'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.TEXT,nullable=False)
    #now()获取的是服务器第一次运行的时间
    #now获取的是每次创建模型的时候的，的当时时间
    create_time=db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    author = db.relationship('User',backref=db.backref('questions'))

class Answer(db.Model):
    __tablename__='answer'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.TEXT,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    question_id=db.Column(db.Integer,db.ForeignKey('question.id'))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    question=db.relationship('Question',backref=db.backref('comments',order_by=id.desc()))
    author=db.relationship('User',backref=db.backref('comments'))




