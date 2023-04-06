from flask_app import app
from flask import render_template,session,redirect,request,flash
from flask_app.models.user import User
from flask_app.models.show import Show 
from flask_bcrypt import Bcrypt

bcrypt= Bcrypt(app)

@app.route('/')
def home():
    return render_template("home.html")

#----register-----

@app.route('/register', methods=["POST"])
def register():
    if User.validate(request.form):
        hashed_password = bcrypt.generate_password_hash(request.form['password'])
        user_data ={
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': hashed_password
        }
        session['user_id'] = User.create_user(user_data)
        return redirect('/shows')
    else:
        print("Data is not valid")
        return redirect("/")
    

#----Login----
@app.route('/login', methods=['POST'])
def login():
    #check email existence
    user_exist=User.get_by_email({'email':request.form['email']})
    if user_exist:
        if not bcrypt.check_password_hash(user_exist.password, request.form['password']):
            flash('Wrong Inputs',"login")
            return redirect('/')
        else:
            session['user_id']=user_exist.id
            return redirect('/shows')
    else:
        flash("user does not exist register first","login")
        return redirect('/')
    
@app.route('/shows')
def shows():
    if 'user_id' not in session:
        return redirect('/')
    shows=Show.get_all()
    user=User.get_by_id({'id':session['user_id']})
    return render_template('view_all.html',user=user,all_shows=shows)


#-----Logout---
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

