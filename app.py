import os
from flask import Flask, render_template, abort, request, session
from forms import LoginForm, SignUpForm, PetEditForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

"""Information regarding the Pets in the System."""


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    age = db.Column(db.String)
    bio = db.Column(db.String)
    posted_by = db.Column(db.String, db.ForeignKey('user.id'))


"""Model for Users."""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    pets = db.relationship('Pet', backref='user')


# """Information regarding the Pets in the System."""
# pets = [
#     {"id": 1, "name": "Nelly", "age": "5 weeks",
#      "bio": "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles."},
#     {"id": 2, "name": "Yuki", "age": "8 months", "bio": "I am a handsome gentle-cat. I like to dress up in bow ties."},
#     {"id": 3, "name": "Basker", "age": "1 year", "bio": "I love barking. But, I love my friends more."},
#     {"id": 4, "name": "Mr. Furrkins", "age": "5 years", "bio": "Probably napping."},
# ]


@app.route("/")
def hello():
    """ Home page. """
    pets = Pet.query.all()
    return render_template("home.html", pets=pets)


@app.route("/about")
def about():
    """ About page. """
    return render_template("about.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    signup_template = "signup.html"
    form = SignUpForm()
    fullname = form.fullname.data
    email = form.email.data
    password = form.password.data
    user = User.query.filter_by(email=email, password=password).first()
    if user is not None:
        return render_template(signup_template, message="The email already exists!, please login")
    else:
        if form.validate_on_submit():
            print('submitted and valid')
            new_user = User(full_name=fullname, email=email, password=password)
            try:
                db.session.add(new_user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
            print(User.query.all())
            return render_template(signup_template, message="User created")
        else:
            return render_template(signup_template, form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    email = form.email.data
    password = form.password.data

    if form.validate_on_submit():
        print('submitted and valid')
        user = User.query.filter_by(email=email, password=password).first()

        if user is None:
            return render_template("login.html", form=form, message="invalid users")
        else:
            session['id'] = user.id
            return render_template("login.html", form=form, message="successful login")

    else:
        if request.method == "POST":
            user = User.query.filter_by(email=email, password=password).first()
            if user is None:
                return render_template("login.html", form=form, message="invalid users")
            else:
                session['id'] = user.id
                return render_template("login.html", form=form, message="successful login")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    if 'id' in session:
        session.pop('id')
    return hello()


@app.route("/details/<int:id>", methods=["GET", "POST"])
def details(id):
    """ details about specific pet"""
    pet = Pet.query.filter_by(id=id).first()
    form = PetEditForm()
    try:
        if pet is None:
            abort(404, description="No Pet was Found with the given ID")
        else:
            if request.method == "POST":
                name = form.name.data
                age = form.age.data
                bio = form.bio.data
                pet.name, pet.age, pet.bio = name, age, bio
                db.session.commit()
            return render_template("details.html", pets=pet, form=form)
    except Exception as e:
        abort(404, description="No Pet was Found with the given ID")


@app.route("/delete/<int:id>", methods=["GET","POST"])
def delete(id):
    """ details about specific pet"""
    pet = Pet.query.filter_by(id=id).first()
    try:
        if pet is None:
            abort(404, description="No Pet was Found with the given ID")
        else:
            db.session.delete(pet)
            db.session.commit()
            return hello()
    except Exception as e:
        abort(404, description="No Pet was Found with the given ID")


if __name__ == "__main__":
    app.run(debug=True)
