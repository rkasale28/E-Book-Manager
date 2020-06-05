from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import SQLAlchemyUserDatastore, UserMixin, RoleMixin

db = SQLAlchemy()
migrate = Migrate()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))
    student_id = db.Column(db.Integer,db.ForeignKey('student.id'))
    
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    users=db.relationship('User',backref='role')

user_datastore = SQLAlchemyUserDatastore(db, User, Role)