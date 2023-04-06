from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.show import Show
from flask_app.models.user import User

#******New Show******

@app.route('/shows/new')
def new():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({'id':session['user_id']})
    return render_template('new.html',user=user)
@app.route('/create',methods=['post'])
def create():
    if not Show.validate(request.form):
        return redirect('/shows/new')
    data={
        **request.form,
        'user_id': session['user_id']
    }
    Show.create_show(data)
    return redirect('/shows')

#******Edit Show******
@app.route('/shows/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id":id
    }
    return render_template("edit.html",show=Show.get_by_id(data))
@app.route('/update', methods=['post'])
def update():
    if not Show.validate(request.form):
        show_id=request.form['id']
        return redirect('/shows')
    Show.update(request.form)
    return redirect('/shows')

#*****Delete*****
@app.route('/shows/delete/<int:id>')
def delete(id):
    Show.delete({'id':id})
    return redirect('/shows')
#*****Read one Show*****
@app.route('/shows/<int:id>')
def view(id):
    if 'user_id' not in session:
        return redirect('/')
    show = Show.get_by_id({'id':id})
    user = User.get_by_id({'id':session['user_id']})
    users= User.get_all()
    return render_template("view_one.html", show = show, user = user,users=users)


