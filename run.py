from flask import current_app,Flask,render_template,g,jsonify,request, url_for, redirect, flash
import sqlite3
import os
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import requests

mp3files="static/budaplz.mp3"

app=Flask(__name__)
config = app.config
app.secret_key = config.get('flask', '730713acad5673b116152920fe534dc6')

login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = '請證明你並非來自黑暗草泥馬界'

DATABASE = "counter.db"
#twitch oauth
# 
#==============


class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(userdata):
    if userdata not in users:
        return

    user = User()
    user.id = userdata
    return user

@login_manager.request_loader
def request_loader(request):
    userdata = request.form.get('user_id')
    if userdata not in users:
        return

    user = User()
    user.id = userdata

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[userdata]['password']

    return user

users = {'root': {'password': '123456'}}


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        errorReason = request.args.get('error')
        code = request.args.get('code')
        scope = request.args.get('scope')
        state = request.args.get('state')
        if errorReason is not None:
            return render_template("login.html")
        elif code is not None:
            url = 'https://id.twitch.tv/oauth2/token'
            myobj = {
                'client_id':'45c2yhxzp8cr8m3p9g9eiuqvqf0ukf',
                'client_secret':'ztg5d71akqjrgrqazgl74rrmrsdz7r',
                'code':code,
                'grant_type':'authorization_code',
                'redirect_uri':'http://localhost:5000/login'
            }

            x = requests.post(url, data = myobj)
            print(x.text)
        else:
            return render_template("login.html")
        
        
        
    
    userdata = request.form['user_id']
    if (userdata in users) and (request.form['password'] == users[userdata]['password']):
        user = User()
        user.id = userdata
        login_user(user)
        flash(f'{userdata}！歡迎加入草泥馬訓練家的行列！')
        return redirect(url_for('home'))

    flash('登入失敗了...')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    userdata = current_user.get_id()
    logout_user()
    flash(f'{userdata}！謝謝今天的練習！')
    return render_template('login.html')

@app.route('/')
# @login_required
def home():
    #select all user's item.
    userdata = current_user.get_id()
    items = query_db('select * from item where id = ?',(userdata,))
    return render_template("index.html",items=items)

@app.route('/musiccounter')
@login_required
def musiccounter():
    defaultData = query_db('select * from item where id = ?',(0,))
    print(defaultData)
    # return render_template("counter.html",mp3files=mp3files,targetnum = defaultData[1],finishednum = defaultData[2])
    return render_template("counter.html")

@app.route('/changetargetnum',methods=['POST'])
def changetargetnum_api():
    data = request.json
    db = get_db()
    # db.execute("UPDATE counterrecord SET targetnum = ? finishednum = ? WHERE id = 1", (new_name, member_role_id))  
    db.execute("INSERT INTO counterrecord(targetnum, finishednum) VALUES(?,?)", (int(data['targetnumber']), int(data['finishednumber'])))
    db.commit()
    return jsonify({'status':'updated'})

@app.route('/changefinishednum',methods=['POST'])
def changefinishednum_api():
    data = request.json
    db = get_db()
    # db.execute("UPDATE counterrecord SET targetnum = ? finishednum = ? WHERE id = 1", (new_name, member_role_id))  
    db.execute("INSERT INTO counterrecord(targetnum, finishednum) VALUES(?,?)", (int(data['targetnumber']), int(data['finishednumber'])))
    db.commit()
    return jsonify({'status':'updated'})

if __name__ == '__main__':
    app.run(debug=True)
    