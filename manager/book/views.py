from flask import Blueprint,request,redirect,render_template,send_from_directory
from flask_uploads import IMAGES, UploadSet
from .models import Book
from manager.database import db,User
from flask import current_app
from flask_security.utils import hash_password,verify_password,login_user,logout_user
from flask_security import login_required

mod=Blueprint('book',__name__,template_folder='templates',static_folder='static')

covers=UploadSet('covers',IMAGES)

@mod.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form['username']
        pwd=request.form['pwd']
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not (user.roles[0].name=='Admin') or not verify_password(pwd,user.password):
            return redirect('/books/login') # if user doesn't exist or password is wrong, reload the page
        else: 
            login_user(user)
            return redirect('/books/')
    else:
        return render_template('admin_login.html')

@mod.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        book_name=request.form['bookname']
        book_price=request.form['price']
        book_author=request.form['author']
        cover_page=request.files['cover_page']
        filename=covers.save(cover_page)
        newbook=Book(name=book_name,
        price=book_price,
        author=book_author,
        filename=filename)

        try:
            db.session.add(newbook)
            db.session.commit()
            return redirect('/books/')
        except Exception as e:
            return e
    else:
        books=Book.query.order_by('name').all()
        return render_template('book_index.html', books=books)

@mod.route('/logout')
def logout():
    logout_user()
    return redirect('/books/login')