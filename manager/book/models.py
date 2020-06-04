from manager.database import db

class Book(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    price=db.Column(db.Integer)
    author=db.Column(db.String(100))
    filename=db.Column(db.String(100))
    
    def __repr__(self):
        return self.name

subs = db.Table('subs',
        db.Column('book_id',db.Integer,db.ForeignKey('book.id')),
        db.Column('user_id',db.Integer,db.ForeignKey('student.id'))
        )
