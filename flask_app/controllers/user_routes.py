from flask import render_template, redirect, request, session    #Imports flask functionalilty
from flask_app import app   #Imports flask app
from flask import flash
from flask_app.models.user import User #imports user class
from flask_app.models.planets import Planet #imports Planet class
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from datetime import datetime

@app.route('/')
def index_page():           #displays register and login panel
    planets = Planet.get_planets()
    
    return render_template('index.html', planets = planets)

#Rework for specific use
@app.route('/register/user', methods=['POST'])
def register():
    # validate the form here ...
    if not User.validate_user(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # put the pw_hash into the data dictionary
    data = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash,
        "birthday" : request.form['birthday'],
        "abducted" : request.form['abducted'],
        "planet_id" : request.form['planet_id']
    }
    # Call the save @classmethod on User
    user_id = User.save(data)
    # store user id into session
    session['user_id'] = user_id

    return redirect("/dashboard")


@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password", 'login')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", 'login')
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id

    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard_page():
    if session.get('user_id') is None:
        return redirect('/')
    now = datetime.now()
    data = {'id': session['user_id']}
    user = User.get_by_id(data)

    return render_template('dashboard.html', user=user, now=now)

@app.route('/logout')
def user_logout():
    session.clear()

    return redirect('/')
