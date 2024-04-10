from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.appointment import Appointment
from flask_app.models.user import User


@app.route("/appointments/all")
def display_all_appointments():
    if "user_id" not in session:
        flash("Please Log In.", "login")
        return redirect("/")
    appointments = Appointment.get_appointments()
    user = User.get_one_user(session["user_id"])
    return render_template("dashboard.html", appointments=appointments, user=user)


@app.route("/appointments/create")
def create_appointment():
    if "user_id" not in session:
        flash("Please Log In.", "login")
        return redirect("/")
    return render_template("new_appointment.html")


@app.post("/submit/appointment")
def new_appointment():
    if not Appointment.validate_appointment(request.form):
        return redirect("/appointments/create")
    Appointment.save(request.form)
    return redirect("/appointments/all")


@app.post("/appointments/destroy/<int:appointment_id>")
def destroy_appointment(appointment_id):
    if "user_id" not in session:
        flash("Please Log In.", "login")
        return redirect("/")
    Appointment.destroy_appointment(appointment_id)
    return redirect("/appointments/all")


# to go back to orig. delete the "_detailed" to go back to appointment.get_one_appointment
@app.get("/appointments/view/<int:appointment_id>")
def view_appointment(appointment_id):
    appointment = Appointment.get_one_appointment_detailed(appointment_id)
    user = User.get_one_user(session["user_id"])
    return render_template("view_appointment.html", appointment=appointment, user=user)


@app.get("/appointments/edit/<int:appointment_id>")
def edit_appointment(appointment_id):
    appointment = Appointment.get_one_appointment(appointment_id)
    return render_template("edit_appointment.html", appointment=appointment)


@app.post("/update_appointment")
def update_appointment():
    appointment_id = request.form["appointment_id"]
    if not Appointment.validate_appointment(request.form):
        return redirect(f"/appointments/edit/{appointment_id}")
    Appointment.update_appointment(request.form)
    return redirect("/appointments/all")
