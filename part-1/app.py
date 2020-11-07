"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

db.create_all()

@app.route('/')
def home_page():
    """Home page redirect to the users list"""

    return redirect("/users")


@app.route('/users')
def list_users():
    """List users and show the add user button"""

    users = User.query.all()
    return render_template("index.html", users=users)


@app.route('/users/new')
def show_add_form():
    """Show the Add New User form"""

    return render_template("new.html")


@app.route('/users/new', methods=['POST'])
def process_add_form():
    """Handle the submition of the Add New User form"""
    
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    image_url = request.form['imgURL']

    new_user = User(first_name=first_name, last_name=last_name,
                    image_url=image_url)

    db.session.add(new_user)    
    db.session.commit() 

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    """Show the user detail, including edit and delete button"""

    user = User.query.get_or_404(user_id)

    return render_template("detail.html", user=user)


@app.route('/users/<int:user_id>/edit')
def edit(user_id):
    """Show the user edit form, including cancel and save button"""

    user = User.query.get_or_404(user_id)

    return render_template("edit.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def handle_edit(user_id):
    """Handle the edit of the current user"""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form['firstName']
    user.last_name = request.form['lastName']
    user.image_url = request.form['imgURL']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')
   

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete(user_id):
    """Handle the delete of the current user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)  
    db.session.commit()

    return redirect('/users')
