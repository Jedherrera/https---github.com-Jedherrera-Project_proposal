from mysqlx import Result
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
import re

DB = "mediarys"


class Appointment:

    def __init__(self, appointment):
        self.id = appointment['id']
        self.appointment_date = appointment['appointment_date']
        self.appointment_location = appointment['appointment_location']
        self.appointment_description = appointment['appointment_description']
        self.created_at = appointment['created_at']
        self.updated_at = appointment['updated_at']
        self.user = None

    @classmethod
    def get_by_id(cls, appointment_id):
        print(f"get mediary by id {appointment_id}")
        data = {"id": appointment_id}
        query = """SELECT appointments.id, appointments.created_at, appointments.updated_at, appointment_date, appointment_location, appointment_description,
                    users.id as user_id, first_name, last_name, email, password, users.created_at as uc, users.updated_at as uu
                    FROM appointments
                    JOIN users on users.id = appointments.user_id
                    WHERE appointments.id = %(id)s;"""

        result_2 = connectToMySQL(DB).query_db(query, data)
        result_2 = result_2[0]
        appointment = cls(result_2)

        appointment.user = user.User(
            {
                "id": result_2["user_id"],
                "first_name": result_2["first_name"],
                "last_name": result_2["last_name"],
                "password": result_2["password"],
                "email": result_2["email"],
                "created_at": result_2["uc"],
                "updated_at": result_2["uu"]
            }
        )

        return appointment

    @classmethod
    def delete_appointment_by_id(cls, appointment_id):

        data = {"id": appointment_id}
        query = "DELETE from appointments WHERE id = %(id)s;"
        connectToMySQL(DB).query_db(query, data)

        return appointment_id

    @classmethod
    def get_all(cls):
        query = """SELECT 
                    appointments.id, appointments.created_at,appointments.updated_at, appointment_date, appointment_location, appointment_description,
                    users.id as user_id, first_name, last_name, email, password, users.created_at as uc, users.updated_at as uu
                    FROM appointments
                    JOIN users on users.id = appointments.user_id;"""
        appointment_data = connectToMySQL(DB).query_db(query)

        appointments = []

        for appointment in appointment_data:

            appointment_obj = cls(appointment)

            appointment_obj.user = user.User(
                {
                    "id": appointment["user_id"],
                    "first_name": appointment["first_name"],
                    "last_name": appointment["last_name"],
                    "password": appointment["password"],
                    "email": appointment["email"],
                    "created_at": appointment["uc"],
                    "updated_at": appointment["uu"]
                }
            )
            appointments.append(appointment_obj)

        return appointments

    @staticmethod
    def appointment_is_valid(appointment_dict):
        valid = True

        if len(appointment_dict["appointment_date"]) < 0:
            flash("Invalid description")
            valid = False

        if len(appointment_dict["appointment_location"]) <= 1:
            flash("Date is required.")

        if len(appointment_dict["appointment_description"]) <= 10:
            flash("Date is required.")

        return valid

    @classmethod
    def create_valid_appointment(cls, appointment_dict):
        if not cls.appointment_is_valid(appointment_dict):
            return False

        query = """INSERT INTO appointments ( appointment_date, appointment_location, appointment_description, user_id) VALUES (%(appointment_date)s, %(appointment_location)s,
        %(appointment_description)s, %(user_id)s);"""
        appointment_id = connectToMySQL(DB).query_db(query, appointment_dict)
        appointment = cls.get_by_id(appointment_id)

        return appointment
