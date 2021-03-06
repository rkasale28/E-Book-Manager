from flask import Blueprint,request,redirect,render_template,send_from_directory
from flask_uploads import IMAGES, UploadSet
from .models import Student
from manager.book.models import Book
from manager.database import db,Role,user_datastore,User
from flask import current_app
from flask_security.utils import hash_password,verify_password,login_user,logout_user
from flask_security import current_user,login_required

mod=Blueprint('student',__name__,template_folder='templates',static_folder='static')

dps=UploadSet('dps',IMAGES)

@mod.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        student_name=request.form['studentname']
        username=request.form['username']
        pwd=hash_password(request.form['pwd'])
        profile_pic=request.files['profile_pic']
        filename=dps.save(profile_pic)
        role=Role.query.get_or_404(2)
        user_datastore.create_user(username=username,password=pwd,roles=[role])
        db.session.commit()
        
        user = User.query.filter_by(username=username).first()
        newstudent=Student(name=student_name,profile_pic=filename,user=user)
        db.session.add(newstudent)
        db.session.commit()
        login_user(user)
        return redirect('/student/')
    else:
        return render_template('signup.html')

@mod.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form['username']
        pwd=request.form['pwd']
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not verify_password(pwd,user.password):
            return redirect('/student/login') # if user doesn't exist or password is wrong, reload the page
        else: 
            login_user(user)
            return redirect('/student/')
    else:
        return render_template('login.html')
        

@mod.route('/',methods=['POST','GET'])
@login_required
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

@mod.route('/displayBooksList')
@login_required
def display():
    books=Book.query.order_by('name').filter(~Book.subscribers.contains(current_user.student)).all()
    return render_template('display_book_list.html',books=books)

@mod.route('/subscribe/<int:bk_id>',methods=['POST','GET'])
@login_required
def subscribe(bk_id):
    book=Book.query.get_or_404(bk_id)
    current_user.student.subscriptions.append(book)
    try:
        db.session.commit()
        return redirect('/student')
    except:
        return 'There was an issue in subscribing'

@mod.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/student/login')