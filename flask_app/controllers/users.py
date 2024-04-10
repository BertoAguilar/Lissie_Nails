from flask import render_template, redirect, request, session
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash
from flask_app.models.user import User

bcrypt = Bcrypt(app)


@app.route("/")
@app.route("/login_and_register")
def display_login_register():
    users = User.get_users()
    return render_template("login_register.html", users=users)


@app.post("/user/new")
def create_user():
    if not User.validate_new_user(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    print(pw_hash)
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash,
    }
    email = User.get_by_email(data)
    if email != 0:
        flash("Email already in use", "register")
        return redirect("/")
    user_id = User.new_user(data)
    session["user_id"] = user_id
    return redirect("/appointments/all")


@app.post("/user/login")
def login():
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)
    if not User.validate_login(request.form):
        flash("Please Check Your Login Info")
        return redirect("/")
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email/Password")
        return redirect("/")
    session["user_id"] = user_in_db.id
    return redirect("/appointments/all")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please Log In.", "login")
        return redirect("/")
    user = User.get_one_user(session["user_id"])
    return render_template("dashboard.html", user=user)


@app.route("/user/logout")
def logout():
    session.clear()
    return redirect("/")


# ===============EVERYTHIN ABOVE IS FOR THE LOGIN AND REGISTER PART ==============================================================================


@app.get("/edit_user/<int:user_id>")
def edit_user(user_id):
    user = User.get_one_user(user_id)
    return render_template("edit_user.html", user=user)


@app.post("/update_user")
def update_user():
    User.update_user(request.form)
    return redirect("/")
