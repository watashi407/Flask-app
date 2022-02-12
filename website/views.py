from queue import Empty
from flask import Blueprint, render_template, request, flash, redirect, url_for , jsonify
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_login import login_required, current_user
from .models import Note
from .models import Member
import json



#other imports

views = Blueprint('views', __name__)


# @views.route('/', methods=['GET', 'POST'])
# def search():
#      q = request.args.get('q')

#      if q:
#          posts=Post.query.filter()

   
            
#      return render_template("home.html", user=current_user)

@views.route('/', methods=['GET', 'POST'])
def home():

    searchs = request.args.get('search')

    # note = Note.query.order_by(Note.date)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user= User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login in successfully', category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.admin'))
            else:
                flash('Incorrect User', category="error")
        else:
                 flash('That thing doesn\`t exist', category="error")



    

    if searchs:
        searched = Note.query.filter(Note.names.contains(searchs) | Note.emails.contains(searchs) )

    else : 
        searched = Note.query.order_by(Note.date)
         
    return render_template("home.html", user=current_user , searched = searched )





@views.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('username already exists.', category='error')
        elif len(username) < 4:
            flash('username must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(
            password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.admin'))
            
    return render_template("signup.html", user=current_user , )


#search



# admin

@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    # if request.method == 'POST':
    #     note = request.form.get('note')
    #     member = request.form.get('Member')

    #     if len(note) < 1:
    #         flash('Note is too short!', category='error')
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash('Note added!', category='success')
    if request.method == 'POST':
        note = request.form.get('note')
        name= request.form.get('name')
        number = request.form.get('number') 
        emails = request.form.get('emails') 
        status = request.form.get('status') 


        email = Note.query.filter_by(emails=emails).first()
        if email:
            flash('email already exists.', category='error')
        elif len(note) < 1:
            flash('Note is too short!', category='error')
        elif len(name) < 3  :
            flash('The name is not valid !', category='error')
        elif len(number) < 10  :
            flash('The number is not valid for PH network!', category='error')
        else:
            new_member = Note(data=note, names=name , numbers=number , emails=emails , statuses = status , user_id=current_user.id)
            db.session.add(new_member)
            db.session.commit()
            flash('Member is succesfully added', category='success')
            return redirect(url_for('views.admin'))

    return render_template("admin.html", user=current_user)

@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
