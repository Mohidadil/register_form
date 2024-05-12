from flask import Flask,render_template,redirect,request,session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask (__name__)
app.secret_key="secret_key"

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:root@localhost/Login_databases'
db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True )
    name = db.Column(db.String,nullable=False)
    last_name = db.Column(db.String,nullable=False)
    email = db.Column(db.String,unique = True ,nullable=False)
    contact = db.Column(db.String,unique = True ,nullable=False)
    password =db.Column(db.String,nullable=False)
    def __init__(self,name,last_name,email,contact,password):
        self.name = name
        self.email = email
        self.last_name = last_name
        self.contact = contact
        self.password = bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")

    def check_password(self,password):
         return bcrypt.checkpw(password.encode("utf-8"),self.password.encode("utf-8"))
        
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return "i am a home page "

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == "POST":
        name = request.form["First.name"]
        last_name = request.form["last_name"]
        email =request.form["email"]
        contact = request.form["contact"]
        password =request.form["password"]

        new_user = user(name,last_name,email,contact,password)
        db.session.add(new_user)
        db.session.commit()
        db.session.close()
        return redirect('/login')
    return render_template('register.html')
    

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        User = user.query.filter_by(email= email).first()
        if User and user.check_password(User,password):
            session['name'] = User.name
            session['last_name'] = User.last_name
            session['email'] = User.email
            session['contact'] = User.contact
            session['password'] = User.password
            return redirect("/dashboard")
        else:
            return  render_template('/login.html',error='invalid user')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if session["name"]:
        User=user.query.filter_by(email=session["email"]).first()
        return render_template('dashboard.html',User=User)
    return render_template('login.html')

app.run(debug=True,port=5000)
