from flask import Flask, render_template, abort, request
from forms import LoginForm,SignUpForm

app = Flask(__name__)

import os

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

"""Information regarding the Pets in the System."""
pets = [
    {"id": 1, "name": "Nelly", "age": "5 weeks",
     "bio": "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles."},
    {"id": 2, "name": "Yuki", "age": "8 months", "bio": "I am a handsome gentle-cat. I like to dress up in bow ties."},
    {"id": 3, "name": "Basker", "age": "1 year", "bio": "I love barking. But, I love my friends more."},
    {"id": 4, "name": "Mr. Furrkins", "age": "5 years", "bio": "Probably napping."},
]

users = [{"id": 1, "full_name": "Pet Rescue Team", "email": "team@pawsrescue.co", "password": "adminpass"}]


@app.route("/")
def hello():
    """ Home page. """
    return render_template("home.html", pets=pets)


@app.route("/about")
def about():
    """ About page. """
    return render_template("about.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    fullname = form.fullname.data
    email = form.email.data
    password = form.password.data

    if form.validate_on_submit():
        print('submitted and valid')
        new_user = {"id": len(users) + 1, "full_name": fullname, "email": email, "password": password}
        users.append(new_user)
        return render_template("signup.html", message="successful login")
    else:
        return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    fullname = form.fullname.data
    email = form.email.data
    password = form.password.data
    cpassword = form.confirm.data

    if form.validate_on_submit():
        print('submitted and valid')
        if email in users and users[email] == password and password == cpassword:
            return render_template("login.html", message="successful login")
        else:
            return render_template("login.html", message="invalid users")
    else:
        if request.method == "POST":
            emailerror = form.email.errors[0]
            passworderror = form.password.errors[0]
            return render_template("login.html", form=form, emailerror=emailerror, passworderror=passworderror)

    return render_template("login.html", form=form)


@app.route("/details/<int:id>")
def details(id):
    """ details about specific pet"""
    try:
        if pets[id - 1] is None:
            abort(404, description="No Pet was Found with the given ID")
        else:
            return render_template("details.html", pets=pets[id - 1])
    except Exception as e:
        abort(404, description="No Pet was Found with the given ID")


if __name__ == "__main__":
    app.run(debug=True)
