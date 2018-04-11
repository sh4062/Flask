from flask import Flask,render_template,request,redirect,url_for,session,flash
import config
from models import User,Blog
from exts import db
import re  
app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
@app.route('/')
def index():
    return render_template('index.html')
#登录
@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        #email verfy
        user = User.query.filter(User.email == email,User.password==password).first()
        if user:
            flash('Logged in successfully.')
            session['user_id'] = user.id
            session['user_name'] = user.username
            #如果３１天都不需要登录
            session.permanent = True
            
            return redirect(url_for('index'))
        else:
            return 'Wrong Information'

#注册
@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #email verfy
        user = User.query.filter(User.email == email).first()
        if user:
            return 'This email has been registed!'
        elif not re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',email):
            return 'Please reset your right Email address!'
        else: 
            if password1 != password2:
               return 'Please input same password'
            else:
                user = User(email = email,username = username, password = password1) 
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
#上下文管理器
@app.context_processor
def my_context_processor():
    user = session.get('user_name')
    if user:
        return {'login_user': user}
    return {}

#注销
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))

#发布
@app.route('/post/',methods=['GET','POST'])
def post():
    user = session.get('user_name')
    if not user:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('post.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        blog = Blog(title = title,content = content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        blog.author = user
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('index'))

#观看
@app.route('/view/',methods=['GET','POST'])
def view():
    context = {'blogs' : Blog.query.all()}
    if request.method == 'GET':
        return render_template('view.html',**context)


if __name__ == '__main__':
    app.run()
