#创建所有模型
from exts import  db
from datetime import  datetime

#用户库
class User(db.Model):
    __tablename =  'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)

#发布性能问题库
class Question(db.Model):
    __tablename = 'question'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    #now()第一是获取服务器的时间，now每次获取服务器最新时间
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    author = db.relationship('User',backref = db.backref('question'))

#日报库
class report(db.Model):
    __tablename = 'report'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    pass

