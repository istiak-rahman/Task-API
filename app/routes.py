from flask import Flask, render_template, jsonify, request, g, abort, redirect, url_for, session, flash
from sqlalchemy import desc
from datetime import datetime, date
from app import auth, db, app
from app.models import User, Task
from functools import wraps

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first!')
            return redirect(url_for('login'))
    return wrap

# Define your routes and functions here
# Login required to access main page
@app.route('/')
@login_required
def index():
    user_id = session.get('user_id')
    tasks = Task.query.filter_by(user_id = user_id).all() # fetch all tasks in database
    return render_template('index.html', tasks = tasks)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()
        if user is None or not user.check_password(password):
            error = 'Invalid credentials. Please try again.'
        else:
            session['user_id'] = user.id
            flash('Logged in successfully!')
            return redirect(url_for('index'))
    return render_template('login.html', error = error)

# if already logged in, you can log out
@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!')
    return redirect(url_for('welcome'))

# Allow users to create an account
@app.route('/register', methods = ['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # if username already exists in the database
        if User.query.filter_by(username = username).first():
            return "Username already exists!"

        user = User(username = username)
        user.set_password(password)

        # Add new user to the database
        db.session.add(user)
        db.session.commit()
        flash("Your account has been successfully created!")
        return redirect(url_for('welcome'))
    return render_template('register.html')

# Allow users to create tasks
@app.route('/create-tasks', methods = ['GET', 'POST'])
def create_tasks():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        created_at = datetime.utcnow()
        due_date_str = request.form['due_date']
        user_id = session.get('user_id')
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            return 'Invalid due date'
        
        task = Task(user_id = user_id, title = title, description = description, created_at = created_at, due_date = due_date)
        # Adds task to the Task database
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_task.html')

@app.route('/delete-tasks/<int:id>', methods = ['POST'])
def delete_tasks(id):
    # query the database for the specific id associated with this task
    task = Task.query.get(id)

    if task is None:
        return 'Task does not exist', 404 # failed request
    if task.user_id != session.get('user_id'):
        return 'Not authorized to delete this task', 403 # unauthorized
    
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

# Verify log in with password
# @auth.verify_password
# def verify_password(username, password):
#     user = User.query.filter_by(username = username).first()
#     if not user or not user.check_password(password):
#         return False
#     g.user = user
#     return True

