from flask import Flask,render_template,request,redirect,url_for,session
import config
from models import  User
from exts import  db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    return  render_template('index1.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone,User.password == password).first()
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

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

@app.route('/report/')
def report():
    return render_template('report.html')

if __name__ == '__main__':
    app.run(
      host='127.0.0.1',
      port= 5555,
      debug=True
    )
