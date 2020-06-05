from manager.database import db
from manager.book.models import subs

class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    profile_pic=db.Column(db.String(100))
    subscriptions=db.relationship('Book',secondary=subs,
    backref=db.backref('subscribers',lazy='dynamic'))
    user=db.relationship('User',backref='student',uselist=False)

    def __repr__(self):
        return self.name