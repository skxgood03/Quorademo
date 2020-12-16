from exts import db
from models import Question
from houpu import app
with app.app_context():
     cla=Question.query.filter(Question.id>=13).delete()
     db.session.commit()
