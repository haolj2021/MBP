from flask import Flask,render_template,request,redirect,url_for,session
from ldap3 import Server , Connection , NTLM
import config
from models import  User,Question
from exts import  db
from sqlalchemy import  or_
from flask_paginate import  Pagination,get_page_parameter

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    # 分页查看https://www.cnblogs.com/donghaoblogs/p/10389673.html
    PER_PAGE = 40 #每页问题数量
    total = Question.query.count()#总共的问题数量
    page = request.args.get(get_page_parameter(),type=int,default=1) #获取页码，默认为第一页
    start = (page - 1)*PER_PAGE #每一页的开始位置
    end = start +  PER_PAGE #每一页的结束位置
    pagination = Pagination(bs_version=3,page=page,total=total) #bootstarp的版本，默认为2，这是使用3
    questions = Question.query.slice(start,end) #对问题进行切片处理
    # questions = Question.query.order_by(Question.create_time.desc()).all()  # 对问题进行切片处理

    ###发布内容按时间排序，mysql版本不一样，这里写法不一样：Question.create_time.desc()
    context = {
       # 'questions': Question.query.order_by(Question.create_time.desc()).all(),
        'pagination': pagination,
        'questions': questions
    }
    return  render_template('index.html',**context)


@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login-bg.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username,User.password == password).first()
        if user:
            session['user_id'] = user.id
            #31天内不需要登录
            session.permanent = True
            return  redirect(url_for('index'))
        else:
            return  '手机号或密码错误，请确认后再登录'


@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #手机号码验证，如果注册后就不能在注册
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return '该手机号码已被注册，请更改手机号码！'
        else:
            #password1要和password2相等才可以注册成功
            if password1 != password2:
                return  '两次密码不同，请核对后再填写'
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                #如果注册册成功，跳转到登录页面
                return  redirect(url_for('login'))

@app.route('/logout/')
def logout():
    session.clear()
    return  redirect(url_for('login'))

@app.route('/question/',methods=['GET','POST'])
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title = title,content = content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return  redirect(url_for('index'))

#性能需求统计：https://www.jianshu.com/p/90b7330806d1
@app.route('/perfxuqiu/',methods=['GET','POST'])
def perfxuqiu():
    if request.method =='GET':
        return render_template('perf-xuqiu.html')
    else:
        pass

#搜索功能
@app.route('/search/',methods=['GET','POST'])
def search():
    #获取前端传过来的要查询的q的值
    q = request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q))).order_by(Question.create_time.desc()).all()
    return render_template('index.html',questions = questions)

@app.route('/autocheck',methods=['GET','POST'])
def autocheck():
    if request.method =='GET':
        return render_template('autocheck.html')
    else:
        pass

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

#2020年11月18日17:23:39
#2020年11月18日17:41:14

if __name__ == '__main__':
    app.run(
      host='172.25.56.86',
      port= 5555,
      debug=True
    )

