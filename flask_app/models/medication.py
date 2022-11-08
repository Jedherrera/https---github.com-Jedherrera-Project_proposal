from mysqlx import Result
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
import re

DB = "mediarys"


class Medication:

    def __init__(self, medication):
        self.id = medication['id']
        self.medication_name = medication['medication_name']
        self.prescribe_by = medication['prescribe_by']
        self.created_at = medication['created_at']
        self.updated_at = medication['updated_at']
        self.user = None

    @classmethod
    def get_by_id(cls, medication_id):
        print(f"get medication by id {medication_id}")
        data = {"id": medication_id}
        query = """SELECT medications.id, medications.created_at, medications.updated_at, medication_name, prescribe_by,
                    users.id as user_id, first_name, last_name, email, password, users.created_at as uc, users.updated_at as uu
                    FROM medications
                    JOIN users on users.id = medications.user_id
                    WHERE medications.id = %(id)s;"""

        result_1 = connectToMySQL(DB).query_db(query, data)
        result_1 = result_1[0]
        medication = cls(result_1)

        medication.user = user.User(
            {
                "id": result_1["user_id"],
                "first_name": result_1["first_name"],
                "last_name": result_1["last_name"],
                "password": result_1["password"],
                "email": result_1["email"],
                "created_at": result_1["uc"],
                "updated_at": result_1["uu"]
            }
        )

        return medication

    @classmethod
    def delete_medication_by_id(cls, medication_id):

        data = {"id": medication_id}
        query = "DELETE from medications WHERE id = %(id)s;"
        connectToMySQL(DB).query_db(query, data)

        return medication_id

    @classmethod
    def get_all(cls):
        query = """SELECT 
                    medications.id, medications.created_at, medications.updated_at, medication_name, prescribe_by,
                    users.id as user_id, first_name, last_name, email, password, users.created_at as uc, users.updated_at as uu
                    FROM medications
                    JOIN users on users.id = medications.user_id;"""
        medication_data = connectToMySQL(DB).query_db(query)

        medications = []

        for medication in medication_data:

            medication_obj = cls(medication)

            medication_obj.user = user.User(
                {
                    "id": medication["user_id"],
                    "first_name": medication["first_name"],
                    "last_name": medication["last_name"],
                    "password": medication["password"],
                    "email": medication["email"],
                    "created_at": medication["uc"],
                    "updated_at": medication["uu"]
                }
            )
            medications.append(medication_obj)

        return medications

    @staticmethod
    def medication_is_valid(medication_dict):
        valid = True

        if len(medication_dict["medication_name"]) < 5:
            flash("Invalid Medication Name")
            valid = False

        if len(medication_dict["prescribe_by"]) <= 1:
            flash("Name is required.")

        return valid

    @classmethod
    def create_valid_medication(cls, medication_dict):
        if not cls.medication_is_valid(medication_dict):
            return False

        query = """INSERT INTO medications (medication_name, prescribe_by, user_id) VALUES (%(medication_name)s, %(prescribe_by)s, %(user_id)s);"""
        medication_id = connectToMySQL(DB).query_db(query, medication_dict)
        medication = cls.get_by_id(medication_id)

        return medication
