from flask import Blueprint,request,redirect,render_template,send_from_directory
from flask_uploads import IMAGES, UploadSet
from .models import Student
from manager.book.models import Book
from manager.database import db
from flask import current_app

mod=Blueprint('student',__name__,template_folder='templates',static_folder='static')

dps=UploadSet('dps',IMAGES)

@mod.route('/login')
def login():
    return render_template('login.html')

@mod.route('/signup')
def signup():
    return render_template('signup.html')

@mod.route('/homepage',methods=['POST','GET'])
def index():
    if request.method=='POST':
        student_name=request.form['studentname']
        profile_pic=request.files['profile_pic']
        filename=dps.save(profile_pic)
        newstudent=Student(name=student_name,profile_pic=filename)

        try:
            db.session.add(newstudent)
            db.session.commit()
            return redirect('/student/')
        except:
            return 'There was an issue adding student'
    else:
        students=Student.query.order_by('name').all()
        return render_template('student_index.html', students=students)

@mod.route('/view/<int:id>')
def view(id):
    student=Student.query.get_or_404(id)
    books=Book.query.order_by('name').filter(Book.subscribers.contains(student)).all()
    return render_template('view_subscriptions.html',stu_id=id,books=books)

@mod.route('/displayBooksList/<int:id>')
def display(id):
    student=Student.query.get_or_404(id)
    books=Book.query.order_by('name').filter(~Book.subscribers.contains(student)).all()
    return render_template('display_book_list.html',stu_id=id,books=books)

@mod.route('/subscribe/<int:bk_id>/<int:st_id>',methods=['POST','GET'])
def subscribe(bk_id,st_id):
    book=Book.query.get_or_404(bk_id)
    student=Student.query.get_or_404(st_id)
    student.subscriptions.append(book)
    try:
        db.session.commit()
        return redirect('/student')
    except:
        return 'There was an issue in subscribing'