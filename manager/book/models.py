from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

class Book(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    price=db.Column(db.Integer)
    author=db.Column(db.String(100))
    filename=db.Column(db.String(100))
    
    def __repr__(self):
        return '<Book %r>' % self.id