from unittest import TestCase

from app import app
from models import db, User, Post, connect_db

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

connect_db(app)

db.drop_all()
db.create_all()

# Post.query.delete()
# User.query.delete()

user = User(first_name='Tony', last_name="Wilson",
            image_url='https://images.unsplash.com/photo-1482482097755-0b595893ba63?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2734&q=80')

post = Post(title="hello",
            content="This is my first post!",
            user_id=1)

db.session.add(user)
db.session.commit()
db.session.add(post)
db.session.commit()

class UserViewsTestCase(TestCase):
    """Tests for views for User."""

    # def tearDown(self):
    #     """Clean up any fouled transaction."""

    #     db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Tony', html)

    def test_add_new_user(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('First Name', html)

    def test_user_detail(self):
        with app.test_client() as client:
            resp = client.get(f"/users/1")
            # resp = client.get("/users/1")  #?????
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Tony', html)
            self.assertIn('Posts', html)

    def test_homepage(self):
        with app.test_client() as client:
            resp = client.get("/")           
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Recent Posts', html)

    def test_add_new_post(self):
        with app.test_client() as client:
            resp = client.get(f"/users/1/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add Post for', html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/1")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('hello', html)
    
    def test_edit_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/1/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit Post', html)

    # def test_delete_post(self):
    #     with app.test_client() as client:
    #         resp = client.post(f"/posts/1/delete")
    #         html = resp.get_data(as_text=True)

    #         # self.assertEqual(resp.status_code, 200)
    #         self.assertIn('Tony', html)
    #         self.assertIn('Posts', html)
