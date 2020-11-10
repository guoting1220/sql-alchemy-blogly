"""Models for Blogly."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """model of user"""

    __tablename__ = 'bloguser'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False,
                          default="https://images.unsplash.com/photo-1501426026826-31c667bdf23d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2776&q=80")
    # if a user is deleted, the related posts will be deleted too, by setting 'cascade'
    posts = db.relationship(
        'Post', cascade="all,delete-orphan", backref="user")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """model for post"""

    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, default="-No Title-")
    content = db.Column(db.Text, nullable=False, default="No Content")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("bloguser.id"), nullable=False, )
    # user = db.relationship('User', backref='posts')

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

# datetime.now().strftime("%a %b %d %Y, %I:%M %p")
        return self.created_at.strftime("%a %b %d %Y, %I:%M %p")



