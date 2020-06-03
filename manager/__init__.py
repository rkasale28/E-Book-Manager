from flask import Flask
from flask_migrate import MigrateCommand
from flask_script import Manager
from flask_uploads import configure_uploads, IMAGES, UploadSet

from manager.book.models import db as books_db,migrate as books_migrate
from manager.book.views import mod as book,covers

def create_app():
    app=Flask(__name__)
    app.register_blueprint(book,url_prefix='/books')
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/manager'
    app.config['UPLOADED_COVERS_DEST']='manager/book/static/uploads/covers'
    
    books_db.init_app(app)
    books_migrate.init_app(app, books_db)
    return app
    
app=create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)

configure_uploads(app,covers)