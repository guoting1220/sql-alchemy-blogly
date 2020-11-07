"""Seed file to make sample data for Blogly db."""
"""not drop the database, but reset everything in the database"""


# Create all tables
from models import User, db
from app import app

db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
u1 = User(first_name='Tony', last_name="Wilson",
          image_url='https://images.unsplash.com/photo-1482482097755-0b595893ba63?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2734&q=80')
u2 = User(first_name='Kevin', last_name="Lee",
          image_url='https://images.unsplash.com/photo-1531427186611-ecfd6d936c79?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80')
u3 = User(first_name='Steven', last_name="Vu",
          image_url='https://images.unsplash.com/photo-1520155707862-5b32817388d6?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80')

# Add new objects to session, so they'll persist
db.session.add(u1)
db.session.add(u2)
db.session.add(u3)

# Commit--otherwise, this never gets saved!
db.session.commit()
