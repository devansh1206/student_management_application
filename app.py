from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///data.db"
db = SQLAlchemy(app)
app.config["SECRET_KEY"]="dev1206"

class Student(db.Model):
    __tablename__= "Student"
    RollNo  = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Name = db.Column(db.String,nullable=False)
    Email = db.Column(db.String, nullable=False, unique=True)
    Password = db.Column(db.String, nullable=False)
    PhysicsMarks = db.Column(db.Integer, nullable=True)
    ChemistryMarks = db.Column(db.Integer, nullable=True)
    MathMarks = db.Column(db.Integer, nullable=True)
    

class Teachers(db.Model):
    __tablename__="Teachers"
    T_code = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Tname = db.Column(db.String, nullable=False)
    Temail = db.Column(db.String, nullable=False, unique=True)
    Tpass = db.Column(db.String, nullable=False)

class Admins(db.Model):
    __tablename__="Admins"
    Aid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Aname = db.Column(db.String, nullable=False)
    Aemail = db.Column(db.String, nullable=False, unique=True)
    Apass = db.Column(db.String, nullable=False)

engine = create_engine("sqlite:///data.db", connect_args={'check_same_thread': False})
session = Session(engine)

@app.route("/")
def first():
    return render_template("index.html")

@app.route("/slogin", methods = ["GET", "POST"])
def slogin(msg = ""):
    if request.method=="POST":
        roll = request.form.get("sroll")
        spass = request.form.get("spass")

        inst = session.query(Student).filter(Student.RollNo==roll, Student.Password==spass).first()
        if inst:
            return render_template("sdash.html", st=inst)
        else:
            msg = "Incorrect RollNo/password"
    
    return render_template("slogin.html", msg=msg)

@app.route("/ssess", methods = ["GET", "POST"])
def suser():
    if  "user" in session:
        user = session["user"]
        return render_template("dash.html", userd = user)
    else:
        return redirect(url_for("slogin"))

@app.route("/tlogin", methods = ["GET", "POST"])
def tlogin(msg=""):
    if request.method=="POST":
        tcode = request.form.get("tcode")
        tpass = request.form.get("tpass")

        teach = session.query(Teachers).filter(Teachers.T_code==tcode, Teachers.Tpass==tpass).first()

        if teach:
            return render_template("tdash.html", msg="")
        else:
            msg = "Incorrect Teacher code/Password"
    return render_template("tlogin.html", msg=msg)

@app.route("/viewMarks", methods=["GET", "POST"])
def viewMarks():
    if request.method=="POST":
        roll = request.form.get("roll")
        inst = session.query(Student).filter(Student.RollNo==roll).first()
        if inst:
            return render_template("teacherViewMarks.html", st=inst)
    return render_template("tdash.html", msg = "student does not exist")


@app.route("/alogin", methods = ["GET", "POST"])
def alogin(msg=" "):
    if request.method=="POST":
        aid = request.form.get("id")
        apass = request.form.get("password")
        inst = session.query(Admins).filter(Admins.Aid==aid, Admins.Apass==apass).first()
        if inst:            
            return render_template("adash.html")
        else:
            msg = "Incorrect AdminId/Password"
    return render_template("login.html", msg = msg)

@app.route("/logout", methods = ["GET", "POST"])
def logout():
    session.pop("user", None)
    return redirect(url_for("first"))

@app.route("/addSt", methods=["GET", "POST"])
def addSt():
    if request.method=="POST":
        Name=request.form.get("name")
        Email = request.form.get("email")
        Password = request.form.get("password")
        entry = Student(Name=Name, Email=Email, Password=Password)
        db.session.add(entry)
        db.session.commit()
    return render_template("addst.html")

@app.route("/searchst", methods=["GET", "POST"])
def searchst(msg=""):
    if request.method=="POST":
        roll= request.form.get("roll")
        myst = Student.query.filter(Student.RollNo==roll).first()
        if myst:
            return render_template("stdet.html", st = myst)
        
        return render_template("adash.html", msg="student does not exist")
    return render_template("adash.html", msg="")
    

@app.route("/remSt", methods=["GET", "POST"])
def remSt():
    if request.method=="POST":
        roll=request.form.get("roll")
        Student.query.filter(Student.RollNo==roll).delete()
        db.session.commit()
    return render_template("remst.html")
        
@app.route("/addT", methods=["GET", "POST"])
def addT():
    if request.method=="POST":
        tname=request.form.get(tname)
        temail=request.form.get(temail)
        tpass=request.form.get(tpass)

        entry = Teachers(Tname=tname, Temail=temail, Tpass=tpass)
        db.session.add(entry)
        db.session.commit()
    return render_template("addT.html")

@app.route("/remT", methods=["GET", "POST"])
def remT(tcode):
    if request.method=="POST":
        Teachers.query.filter(T_code=tcode).delete()
        db.session.commit()
    return render_template("remT.html")

@app.route("/addMarks", methods=["GET", "POST"])
def addMarks():
    if request.method=="POST":
        roll = request.form.get("roll")
        pmarks = request.form.get("pmarks")
        cmarks = request.form.get("cmarks")
        mmarks = request.form.get("mmarks")
        
        entry = Student.query.get(roll)
        if entry:
            entry.PhysicsMarks = pmarks
            entry.ChemistryMarks = cmarks
            entry.MathMarks = mmarks
            db.session.commit()

    return render_template("addMarks.html")

if __name__ == "__main__":
    app.run(
        host = "0.0.0.0",
        debug=True,
        port = 8080
    ) 
    
