from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config["SECRET_KEY"]=r"\xebr\x17D*t\xae\xd4\xe3S\xb6\xe2\xebP1\x8b"

posts = [
    {
        "author":"Corey Shafer",
        "title":"blog post",
        "content":"april"
    },
    {
        "author":"Steve James",
        "title":"blog post2",
        "content":"july"
    }
]

@app.route("/")
def home():
    return render_template("home.html", posts=posts)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Account created for {0}!".format(form.username.data))
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)


if __name__ == "__main__":
    app.run(debug=True)

