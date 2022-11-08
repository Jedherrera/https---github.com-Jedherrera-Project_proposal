from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import mediary
from flask_app.models import medication
from flask_app.models import appointment
import re

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DB = "mediarys"


class User:

    def __init__(self, user):

        self.id = user["id"]
        self.first_name = user["first_name"]
        self.last_name = user["last_name"]
        self.email = user["email"]
        self.password = user["password"]
        self.created_at = user["created_at"]
        self.updated_at = user["updated_at"]

    @classmethod
    def get_by_email(cls, data):

        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query, data)

        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, user_id):

        data = {"id": user_id}
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)

        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * from users;"
        user_data = connectToMySQL(DB).query_db(query)

        users = []
        for user in user_data:
            users.append(cls(user))

        return users

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DB).query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Please enter your email", "register")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must be at least 2 characters", "register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 2 characters", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if user['password'] != user['password_confirmation']:
            flash("Passwords must match", "register")
        return is_valid

    @classmethod
    def save(cls, user):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(DB).query_db(query, user)
