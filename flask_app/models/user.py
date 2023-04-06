from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import show
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
class User:
    def __init__(self,data) :
        self.id= data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email = data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

#*****Read All****
    @classmethod
    def get_all(cls):
        query="SELECT*FROM users"
        return connectToMySQL('tv_shows').query_db(query)
#******Create******
    @classmethod
    def create_user(cls, data):
        query ="INSERT INTO users ( first_name, last_name, email,password) VALUES ( %(first_name)s, %(last_name)s, %(email)s,%(password)s);"
        return connectToMySQL('tv_shows').query_db(query,data)
#********Get One by id/email*****
    @classmethod
    def get_by_id(cls,data):
        query= "SELECT * FROM users WHERE id = %(id)s;"
        results= connectToMySQL("tv_shows").query_db(query,data)
        return cls(results[0])
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('tv_shows').query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])
#*********Validations Register********
    @staticmethod
    def validate(user):
        is_valid=True
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email, check your syntax","register")
            is_valid=False
        elif User.get_by_email({'email':user['email']}):
            flash("Email exist,try to login","register")
            is_valid=False
        if len(user['password'])<8:
            is_valid = False
            flash("Password must be at least 8" ,"register")
        if user['password']!=user['confirm_password']:
            flash("Passwords must match","register")
            is_valid=False
        if len(user['first_name'])<2:
            flash("first name must be at least 2 characters, required*","register")
            is_valid=False
        if len(user['last_name'])<2:
            flash("last name must be at least 2 characters,required*","register")
            is_valid=False
        return is_valid
