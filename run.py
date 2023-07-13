from flask import Flask,render_template,g,jsonify,request
import sqlite3
import os

mp3files="static/budaplz.mp3"

app=Flask(__name__)

DATABASE = "counter.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # Enable foreign key check
        db.execute("PRAGMA foreign_keys = ON")
        db.execute('CREATE TABLE IF NOT EXISTS counterrecord('
               'id INTEGER PRIMARY KEY AUTOINCREMENT, '
               'targetnum INTEGER DEFAULT 0 NOT NULL, '
               'finishednum INTEGER DEFAULT 0 NOT NULL)')
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

# def init_db():
#     if not os.path.isfile(DATABASE):



@app.route('/')
def home():
    defaultData = query_db('select * from counterrecord')[-1]
    print(defaultData)
    return render_template("counter.html",mp3files=mp3files,targetnum = defaultData[1],finishednum = defaultData[2])

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