from flask import Flask, render_template, session, redirect, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.mediary import Mediary
from flask_app.models.medication import Medication
from flask_app.models.appointment import Appointment
from flask import flash


@app.route("/mediarys/home")
def mediarys_home():
    if "user_id" not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect("/")

    user = User.get_by_id(session["user_id"])
    mediarys = Mediary.get_all()

    return render_template("home.html", user=user, mediarys=mediarys)


@app.route("/mediarys/medications")
def medication_medications():
    if "user_id" not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect("/")

    user = User.get_by_id(session["user_id"])
    medications = Medication.get_all()

    return render_template("medications.html", user=user, medications=medications)


@app.route("/mediarys/appointment")
def mediarys_appointment():
    if "user_id" not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect("/")

    user = User.get_by_id(session["user_id"])
    appointments = Appointment.get_all()

    return render_template("appointments.html", user=user,  appointments=appointments)


@app.route("/mediarys/account")
def mediarys_account():
    user = User.get_by_id(session["user_id"])
    mediarys = Mediary.get_all()

    return render_template("account.html", user=user,  mediarys=mediarys)


@app.route("/mediarys/journal/create")
def mediary_create_journal():
    user = User.get_by_id(session["user_id"])
    return render_template("new_journal.html", user=user)


@app.route("/mediarys/<int:mediary_id>")
def mediary_journal(mediary_id):
    user = User.get_by_id(session["user_id"])
    mediary = Mediary.get_by_id(mediary_id)
    return render_template("journal_detail.html", user=user, mediary=mediary)


@app.route("/mediarys/edit/<int:mediary_id>")
def mediary_edit_page(mediary_id):
    mediary = Mediary.get_by_id(mediary_id)
    return render_template("edit_journal.html", mediary=mediary)


@app.route("/mediarys/<int:mediary_id>", methods=["POST"])
def update_mediary(mediary_id):
    valid_mediary = Mediary.update_mediary(request.form, session["user_id"])
    if not valid_mediary:
        return redirect(f"/mediarys/edit/{mediary_id}")

    return redirect(f"/mediarys/{mediary_id}")


@app.route("/mediarys", methods=["POST"])
def create_journal():
    valid_journal = Mediary.create_valid_journal(request.form)
    if valid_journal:
        return redirect(f'/mediarys/{valid_journal.id}')
    return redirect('/mediarys/journal/create')


@app.route("/mediarys/delete/<int:mediary_id>")
def delete_by_id(mediary_id):
    Mediary.delete_mediary_by_id(mediary_id)
    return redirect("/mediarys/home")


@app.route("/mediarys/medication/create")
def mediary_create_medication():
    user = User.get_by_id(session["user_id"])
    return render_template("new_medication.html", user=user)


@app.route("/medication", methods=["POST"])
def create_medication():
    valid_medication = Medication.create_valid_medication(request.form)
    if valid_medication:
        return redirect(f'/medication/{valid_medication.id}')
    return redirect('/mediarys/medication/create')


@app.route("/medication/<int:medication_id>")
def mediary_medication(medication_id):
    user = User.get_by_id(session["user_id"])
    medication = Medication.get_by_id(medication_id)
    return render_template("medication_detail.html", user=user, medication=medication)


@app.route("/medication/delete/<int:medication_id>")
def delete_by_med_id(medication_id):
    Medication.delete_medication_by_id(medication_id)
    return redirect("/mediarys/medications")


@app.route("/mediarys/appointment/create")
def mediary_create_appointment():
    user = User.get_by_id(session["user_id"])
    return render_template("new_appointment.html", user=user)


@app.route("/appointment", methods=["POST"])
def create_appointment():
    valid_appointment = Appointment.create_valid_appointment(request.form)
    if valid_appointment:
        return redirect(f'/appointment/{valid_appointment.id}')
    return redirect('/mediarys/appointment/create')


@app.route("/appointment/<int:appointment_id>")
def mediary_appointment(appointment_id):
    user = User.get_by_id(session["user_id"])
    appointment = Appointment.get_by_id(appointment_id)
    return render_template("appointment_detail.html", user=user, appointment=appointment)


@app.route("/appointment/delete/<int:appointment_id>")
def delete_by_app_id(appointment_id):
    Appointment.delete_appointment_by_id(appointment_id)
    return redirect("/mediarys/appointment")
