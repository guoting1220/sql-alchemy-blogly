"""Seed file to make sample data for Blogly db."""
"""not drop the database, but reset everything in the database"""

# Create all tables
from models import db, User, Post, Tag, PostTag
from app import app

db.drop_all()
db.create_all()

# If table isn't empty, empty it
# Why need to delete ?
# Post.query.delete()
# User.query.delete()

# Add sample users
u1 = User(first_name='Tony', last_name="Wilson",
          image_url='https://images.unsplash.com/photo-1503919545889-aef636e10ad4?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80')
u2 = User(first_name='Kevin', last_name="Lee",
          image_url='https://images.unsplash.com/photo-1503023345310-bd7c1de61c7d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1001&q=80')
u3 = User(first_name='Susan', last_name="Vu",
          image_url='https://images.unsplash.com/photo-1520155707862-5b32817388d6?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80')

# Add sample posts
p1 = Post(title="hello",
          content="This is my first post!",    
          user_id=2)
p2 = Post(title="I love SQL",
          content="I enjoy learning SQL!",
          user_id=1)
p3 = Post(title="My first post",
          content="This is my first post!",
          user_id=3)
p4 = Post(title="hello again",
          content="This is my second post!",
          user_id=2)
p5 = Post(title="My second post",
          content="This is my second post!",
          user_id=3)
p6 = Post(title="My third post",
          content="This is my third post!",
          user_id=3)

# Add sample tags
t1 = Tag(name="Fun")
t2 = Tag(name="Bloop")

# Add sample posts_tags
pt1 = PostTag(post_id=1, tag_id=1)
pt2 = PostTag(post_id=1, tag_id=2)
pt3 = PostTag(post_id=2, tag_id=1)
pt4 = PostTag(post_id=5, tag_id=2)
pt5 = PostTag(post_id=4, tag_id=2)


# Add new objects to session, so they'll persist
db.session.add_all([u1, u2, u3])
db.session.commit()

db.session.add_all([p1, p2, p3, p4, p5, p6])
db.session.commit()

db.session.add_all([t1, t2])
db.session.commit()

db.session.add_all([pt1, pt2, pt3, pt4, pt5])
db.session.commit()
