from flask import Blueprint,request,redirect,render_template,send_from_directory
from flask_uploads import IMAGES, UploadSet
from .models import Book
from manager.database import db
from flask import current_app

mod=Blueprint('book',__name__,template_folder='templates',static_folder='static')

covers=UploadSet('covers',IMAGES)

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
        return render_template('index.html', books=books)

@mod.route('media/covers/<filename>')
def retrieve_cover(filename):
    return send_from_directory(current_app.config['UPLOADED_COVERS_DEST'],filename)