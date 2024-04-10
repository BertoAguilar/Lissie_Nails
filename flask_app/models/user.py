from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class User:
    db = "lissie_nails_v1"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_users(cls):
        """This Method Selects All Users"""
        query = "SELECT * FROM users;"
        results = connectToMySQL(User.db).query_db(query)
        users = []
        for each_result in results:
            user = User(each_result)
            users.append(user)
        return users

    @classmethod
    def new_user(cls, form_data):
        """This Method Creates a new User"""
        query = """
        INSERT INTO users 
        (first_name, last_name, email, password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        user_id = connectToMySQL(User.db).query_db(query, form_data)
        return user_id

    @staticmethod
    def validate_new_user(user):
        is_valid = True
        if len(user["first_name"]) < 3:
            flash("First name must be at least 3 characters.", "register")
            is_valid = False
        if len(user["last_name"]) < 3:
            flash("Last name must be at least 3 characters.", "register")
            is_valid = False
        if len(user["email"]) == 0:
            flash("Email is Empty!", "register")
            is_valid = False
        elif not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email address!", "register")
            is_valid = False
        if len(user["password"]) < 5:
            flash("Password must be at least 5 characters.", "register")
            is_valid = False
        if len(user["confirm_password"]) == 0:
            flash("Please confirm password.", "register")
            is_valid = False
        elif user["password"] != user["confirm_password"]:
            flash("Password does not match", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user["email"]) == 0:
            flash("Email is Empty!", "login")
            is_valid = False
        if len(user["password"]) < 5:
            flash("Password is Empty!", "login")
            is_valid = False
        elif not EMAIL_REGEX.match(user["email"]):
            flash("Invalid Email Address Format!", "login")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(User.db).query_db(query, data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return User(result[0])

    @classmethod
    def get_one_user(cls, user_id):
        query = "SELECT * FROM users WHERE id= %(user_id)s;"
        data = {"user_id": user_id}
        list_of_dicts = connectToMySQL(User.db).query_db(query, data)
        user = User(list_of_dicts[0])
        return user

    @classmethod
    def update_user(cls, data):
        query = """
        UPDATE users SET 
        customer_name = %(customer_name)s, 
        cookie_type = %(cookie_type)s, 
        numb_of_boxes = %(numb_of_boxes)s
        WHERE id= %(user_id)s;"""
        return connectToMySQL(User.db).query_db(query, data)
