from flask import Blueprint,request,redirect,render_template,send_from_directory
from flask_uploads import IMAGES, UploadSet
from .models import Student
from manager.database import db
from flask import current_app

mod=Blueprint('student',__name__,template_folder='templates',static_folder='static')

dps=UploadSet('dps',IMAGES)

@mod.route('/',methods=['POST','GET'])
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