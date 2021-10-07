#from os import name
from os import name
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime

app = Flask(__name__)
app.secret_key = "Online notice board of university of balochitstan"

db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:srebel412@localhost/notice_board"
app.config['SECRET_KEY'] = "Online notice board of university of balochitstan"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

class Notice(db.Model):
    __tablename__="notice"
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(500), nullable=False)
    detail = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # date_created = db.Column(db.DateTime, default=datetime.utcnow())




#         A D M I N
@app.route("/manage_notice", methods=['GET', 'POST'])
def manage_notice():
    if session.get('username'):
                if request.method == "POST":
                    subject = request.form.get("subject")
                    detail = request.form.get("detail")

                    notice = Notice(subject = subject, detail = detail)
                    db.session.add(notice)
                    db.session.commit()
                    
                allnotice = Notice.query.order_by(Notice.id.desc()).all()
                return render_template('admin.html', allnotice = allnotice)
    else:
     return render_template('adminlogin.html')
@app.route("/adminlogin", methods=['POST','GET'])
def adminlogin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if username.lower() == 'rebel' and password =='123':
            session ['username'] = "Rebel"
            allnotice = Notice.query.order_by(Notice.id.desc()).all()
            return render_template('/admin.html',allnotice = allnotice)
        else:
            return render_template('adminlogin.html')
    else:
        return render_template('adminlogin.html')


# if session.get('username'):
#       return render_template('manageusers.html')
#     return render_template("adminlogin.html")

@app.route("/manageusers", methods=['GET', 'POST'])
def manageusers():
        if session.get('username'):
                if request.method == "POST":
                    name = request.form.get("name")
                    email = request.form.get("email")
                    department = request.form.get("department")
                    password = request.form.get("password")

                    user = User(name = name, email = email, department = department, password = password)
                    db.session.add(user)
                    db.session.commit()
                    
                alluser = User.query.all()
                return render_template('manageusers.html', alluser = alluser)
        else:
         return render_template('adminlogin.html')

@app.route("/update/<int:id>", methods=['GET', 'POST'] )
def update(id):
    if request.method =='POST':
        name = request.form.get("name")
        email = request.form.get("email")
        department = request.form.get("department")
        password = request.form.get("password")

        user = User.query.filter_by(id=id).first()
        user.name = name
        user.email = email
        user.department = department
        user.password = password
        db.session.add(user)
        db.session.commit()    
        return redirect("/manageusers")

    user = User.query.filter_by(id=id).first()
    return render_template("/update.html", user = user)    

@app.route("/delete/<int:id>")
def delete(id):
    dell_notice = Notice.query.filter_by(id=id).first()
    db.session.delete(dell_notice)
    db.session.commit()
    return redirect("/manage_notice")

@app.route("/remove/<int:id>")
def remove(id):
    rem_user = User.query.filter_by(id=id).first()
    db.session.delete(rem_user)
    db.session.commit()
    return redirect("/manageusers")



#          U S E R


@app.route("/read_notice/notice_id=<id>", methods=['GET', 'POST'])
def read_notice(id):
    note= Notice.query.filter(Notice.id==id).first()

    return render_template('note.html', note=note)

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/notice", methods=['POST','GET'])
def notice():
    allnotice = Notice.query.order_by(Notice.id.desc()).all()
    return render_template('notice.html', allnotice = allnotice)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))
    

if __name__ == "__main__":
    app.run(debug=True, port=3360)
    