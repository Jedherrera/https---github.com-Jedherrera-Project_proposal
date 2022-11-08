from mysqlx import Result
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
import re

DB = "mediarys"


class Mediary:

    def __init__(self, mediary):
        self.id = mediary['id']
        self.journal_date = mediary['journal_date']
        self.journal_description = mediary['journal_description']
        self.created_at = mediary['created_at']
        self.updated_at = mediary['updated_at']
        self.user = None

    @classmethod
    def get_by_id(cls, mediary_id):
        print(f"get mediary by id {mediary_id}")
        data = {"id": mediary_id}
        query = """SELECT mediarys.id, mediarys.created_at, mediarys.updated_at, journal_date, journal_description,
                    users.id as user_id, first_name, last_name, email, password, users.created_at as uc, users.updated_at as uu
                    FROM mediarys
                    JOIN users on users.id = mediarys.user_id
                    WHERE mediarys.id = %(id)s;"""

        result = connectToMySQL(DB).query_db(query, data)
        result = result[0]
        mediary = cls(result)

        mediary.user = user.User(
            {
                "id": result["user_id"],
                "first_name": result["first_name"],
                "last_name": result["last_name"],
                "password": result["password"],
                "email": result["email"],
                "created_at": result["uc"],
                "updated_at": result["uu"]
            }
        )

        return mediary

    @classmethod
    def delete_mediary_by_id(cls, mediary_id):

        data = {"id": mediary_id}
        query = "DELETE from mediarys WHERE id = %(id)s;"
        connectToMySQL(DB).query_db(query, data)

        return mediary_id

    @classmethod
    def update_mediary(cls, mediary_dict, session_id):

        mediary = cls.get_by_id(mediary_dict["id"])
        if mediary.user.id != session_id:
            return False

        if not cls.journal_is_valid(mediary_dict):
            return False

        query = """UPDATE mediarys
                    SET journal_date = %(journal_date)s, journal_description = %(journal_description)s,
                    WHERE id = %(id)s;"""

        result = connectToMySQL(DB).query_db(query, mediary_dict)
        mediary = cls.get_by_id(mediary_dict["id"])

        return mediary

    @classmethod
    def get_all(cls):
        query = """SELECT 
                    mediarys.id, mediarys.created_at, mediarys.updated_at, journal_date, journal_description, 
                    users.id as user_id, first_name, last_name, email, password, users.created_at as uc, users.updated_at as uu
                    FROM mediarys
                    JOIN users on users.id = mediarys.user_id;"""
        mediary_data = connectToMySQL(DB).query_db(query)

        mediarys = []

        for mediary in mediary_data:

            mediary_obj = cls(mediary)

            mediary_obj.user = user.User(
                {
                    "id": mediary["user_id"],
                    "first_name": mediary["first_name"],
                    "last_name": mediary["last_name"],
                    "password": mediary["password"],
                    "email": mediary["email"],
                    "created_at": mediary["uc"],
                    "updated_at": mediary["uu"]
                }
            )
            mediarys.append(mediary_obj)

        return mediarys

    @staticmethod
    def journal_is_valid(mediary_dict):
        valid = True

        if len(mediary_dict["journal_description"]) < 10:
            flash("Invalid description")
            valid = False

        if len(mediary_dict["journal_date"]) <= 1:
            flash("Date is required.")

        return valid

    @classmethod
    def create_valid_journal(cls, mediary_dict):
        if not cls.journal_is_valid(mediary_dict):
            return False

        query = """INSERT INTO mediarys (journal_date, journal_description, user_id) VALUES (%(journal_date)s, %(journal_description)s, %(user_id)s);"""
        mediary_id = connectToMySQL(DB).query_db(query, mediary_dict)
        mediary = cls.get_by_id(mediary_id)

        return mediary
