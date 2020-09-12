import os
from flask import Flask, render_template, request, url_for, session, redirect, flash
from flask_pymongo import PyMongo
import bcrypt
if os.path.exists('env.py'):
    import env

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'login'
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/logged_in')
def logged_in():
    if 'username' in session:
        return render_template('loggedin.html')


#################################LOGIN#################################

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']).encode('utf-8') == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('logged_in'))

    return 'Incorrct Username/Password'

#################################REGISTER#################################
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return render_template('userexists.html')

    return render_template('loggedin.html')


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)