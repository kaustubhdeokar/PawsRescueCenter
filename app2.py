from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, abort, request, session
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    email = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


db.create_all()
#archie = User(email="archie.andrews@email.com", password="football4life")
veronica = User(email="veronica.lodge@email.com", password="fashiondiva")
#db.session.add(archie)
db.session.add(veronica)

try:
    db.session.commit()
except Exception as e:
    db.session.rollback()

### QUERY.

print('all')
print(User.query.all())

print('first')
print(User.query.first())

print('get by primary key')
print(User.query.get("archie.andrews@email.com"))

print('get by filter')
print(User.query.filter_by(password="football4life").first())

## UPDATE.

user = User.query.get("veronica.lodge@email.com")
print(user)

user.email = "veronica@email.com"

try:
    db.session.commit()
except Exception as e:
    db.session.rollback()

print("All Users : ", User.query.all())

user = User.query.get("veronica@email.com")
print(user)

user.email = "veronica.lodge@email.com"

try:
    db.session.commit()
except Exception as e:
    db.session.rollback()

print("All Users : ", User.query.all())

#DELETE


user = User.query.get("veronica.lodge@email.com")
print(user)

db.session.delete(user)

try:
    db.session.commit()
except Exception as e:
    db.session.rollback()

print("All Users : ", User.query.all())

# ADD

veronica = User(email="veronica.lodge@email.com", password="fashiondiva")
db.session.add(veronica)
try:
    db.session.commit()
except Exception as e:
    db.session.rollback()
finally:
    db.session.close()

print(User.query.all())