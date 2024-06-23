from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db

# Define user model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) # compares the original password to the hashed password
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

# Define task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # establish foreign key relationship, storing id of user in task table
    user = db.relationship('User', backref=db.backref('tasks', lazy=True)) # establishes a correspondence between a task and its associated user
    # uses a back-reference from User model to related tasks, allowing you to access tasks associated with a specific user
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
