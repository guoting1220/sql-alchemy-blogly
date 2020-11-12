"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post, Tag, PostTag
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
    """Home page showing the 5 most recent posts"""

    # posts = Post.query.order_by("created_at".desc()).limit(5).all()
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template("posts/home.html", posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404


#====================================================
# users routes

@app.route('/users')
def list_users():
    """List users and show the add user button"""

    users = User.query.all()
    return render_template("users/index.html", users=users)


@app.route('/users/new')
def show_add_user_form():
    """Show the Add New User form"""

    return render_template("users/new.html")


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
    flash(f"User {new_user.full_name} added!")

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    """Show the user detail, including edit and delete button"""

    user = User.query.get_or_404(user_id)

    return render_template("users/detail.html", user=user)


@app.route('/users/<int:user_id>/edit')
def edit(user_id):
    """Show the user edit form, including cancel and save button"""

    user = User.query.get_or_404(user_id)

    return render_template("users/edit.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def handle_edit(user_id):
    """Handle the edit of the current user"""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form['firstName']
    user.last_name = request.form['lastName']
    user.image_url = request.form['imgURL']

    db.session.add(user)
    db.session.commit()

    flash(f"User {user.full_name} edited!")

    return redirect('/users')
   

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Handle the delete of the current user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)  
    db.session.commit()
    flash(f"User {user.full_name} deleted!")

    return redirect('/users')


#=============================================================
# posts routes

@app.route('/users/<int:user_id>/posts/new')
def show_add_post_form(user_id):
    """Show the Add Post form"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template("posts/new.html", user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def handle_add_post_form(user_id):
    """handle the Add post"""
    
    title = request.form["title"]
    content = request.form["content"]

    post = Post(title=title, content=content, user_id=user_id)
    
    tag_ids = request.form.getlist("tags")

    for tag_id in tag_ids:
        tag = Tag.query.get_or_404(tag_id)
        post.tags.append(tag)

    db.session.add(post)
    db.session.commit()

    flash(f"Post '{post.title}' added!")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """ show the detail of the post """

    post = Post.query.get_or_404(post_id)

    return render_template("posts/show.html", post=post)


@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """ show edit post form """

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template("posts/edit.html", post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def handle_edit_post(post_id):
    """ handle editing post """

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    post.tags = []   # Do I need to do this?

    tag_ids = request.form.getlist("tags")

    for tag_id in tag_ids:
        tag = Tag.query.get_or_404(tag_id)
        post.tags.append(tag)

    db.session.add(post)
    db.session.commit()

    flash(f"Post edited!")

    return redirect(f"/posts/{post.id}")


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def handle_delete_post(post_id):
    """ handle delete post """

    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    # Post.query.filter_by(id=post_id).delete()
    db.session.delete(post)
    db.session.commit()

    flash(f"Post '{post.title}' deleted!")

    return redirect(f"/users/{user_id}")


#================================================
# tags routes

@app.route("/tags")
def list_tags():
    """ list all the tags """

    tags = Tag.query.all()

    return render_template("tags/index.html", tags=tags)


@app.route("/tags/new")   
def show_add_tag_form():
    """ show the add new tag form """

    posts = Post.query.all()

    return render_template("tags/new.html", posts=posts) 


@app.route("/tags/new", methods=['POST'])
def handle_add_tag():
    """ handle adding new tag """

    tag = Tag(name = request.form["tagName"])
    post_ids = request.form.getlist("posts") 

    for post_id in post_ids:
        tag.posts.append(Post.query.get_or_404(post_id))

    db.session.add(tag)
    db.session.commit()

    flash(f"Tag '{tag.name}' added!")

    return redirect("/tags")


@app.route("/tags/<int:tag_id>")
def tag_detail(tag_id):
    """ show the tag detail with edit and delete button"""

    tag = Tag.query.get_or_404(tag_id)
    
    return render_template("tags/show.html", tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """ show edit tag form """

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()

    return render_template("tags/edit.html", tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def handle_edit_tag(tag_id):
    """ handle editing tag """

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["tagName"]
    tag.posts = []
    post_ids = request.form.getlist("posts")

    for post_id in post_ids:
        tag.posts.append(Post.query.get_or_404(post_id))

    db.session.add(tag)
    db.session.commit()

    flash(f"Tag edited!")

    return redirect(f"/tags/{tag.id}")


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def handle_delete_tag(tag_id):
    """ handle deleting tag """

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    flash(f"Tag deleted!")

    return redirect("/tags")
