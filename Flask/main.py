from flask import Flask,render_template,request,redirect,url_for,session
import config
from models import User
from exts import db
import re  
app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
@app.route('/')
def index():
    return render_template('index.html')

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
            session['user_id'] = user.id
            #如果３１天都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return 'Wrong Information'


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



if __name__ == '__main__':
    app.run()
