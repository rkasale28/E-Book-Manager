from manager.database import db

class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    profile_pic=db.Column(db.String(100))
    
    def __repr__(self):
        return '<Student %r>' % self.id