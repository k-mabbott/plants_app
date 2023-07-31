from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DB
from flask_app.models import message_model
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
ALPHA = re.compile(r"^[a-zA-Z]+$") 
ALPHANUMERIC = re.compile(r"^[a-zA-Z0-9]+$") 


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
    
# ------------------------------------------------ SAVE NEW USER
    @classmethod
    def save(cls,data):
        query = """
                INSERT INTO users (first_name, last_name, email, password ) 
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
                """
        return connectToMySQL(DB).query_db(query, data)
    
# ------------------------------------------------ GET BY ID
    @classmethod
    def get_by_id(cls, data):
        query = """
                SELECT * FROM users WHERE id = %(id)s;
                """
        results = connectToMySQL(DB).query_db(query, data)
        print('results!!!! ---', results)
        if results:
            return cls(results[0])
        return False
    
# ------------------------------------------------ GET BY EMAIL
    @classmethod
    def get_by_email(cls, data):
        query = """
                SELECT * FROM users WHERE email = %(email)s;
                """
        results = connectToMySQL(DB).query_db(query, data)
        if results:
            return cls(results[0])
        return False
# ------------------------------------------------ GET ALL
    @classmethod
    def get_all(cls, data):
        query = """
                SELECT * FROM users WHERE id != %(id)s  ORDER BY users.first_name;
                """
        results = connectToMySQL(DB).query_db(query, data)
        if results:
            all_users = []
            for row in results:
                user = cls(row)
                all_users.append(user)
            return all_users
        return False
    

# ------------------------------------------------ VALIDATION CHECK
    @staticmethod
    def validation(data):
        is_valid = True
        # -----------------------------------------First Name
        if len(data['first_name']) < 1 :
            is_valid = False
            flash('Invalid First Name!', 'first_name')
        elif len(data['first_name']) < 2 :
            is_valid = False
            flash('Invalid First Name! * must be 2 characters long', 'first_name')
        elif not ALPHA.match(data['first_name']):
            is_valid = False
            flash('Invalid First Name! * must be letters only ', 'first_name')
        # -----------------------------------------Last Name
        if len(data['last_name']) < 1 :
            is_valid = False
            flash('Invalid last name!', 'last_name')
        elif len(data['last_name']) < 2 :
            is_valid = False
            flash('Invalid last name! * must be 2 characters long', 'last_name')
        elif not ALPHA.match(data['last_name']):
            is_valid = False
            flash('Invalid Last Name!  * must be letters only', 'last_name')
        # -----------------------------------------Email
        if len(data['email']) < 1 :
            is_valid = False
            flash('Invalid Email! * must have email', 'email')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('Invalid Email Address! * check format', 'email')
        else: 
            user_data = {
                'email': data['email']
            }
            potential_user = User.get_by_email(user_data)
            if potential_user:
                is_valid = False
                flash('Email already exists')

        # -----------------------------------------Password
        if len(data['password']) < 1:
            is_valid = False
            flash('Password Required! \n*must be atleast 8 characters long', 'password')
        elif len(data['password']) < 8:
            is_valid = False
            flash('Invalid Password! \n*must be atleast 8 characters long', 'password')
        elif re.search('[0-9]',data['password']) is None:
            is_valid = False
            flash('Invalid Password! \n*must have one number in it', 'password')
        elif re.search('[A-Z]',data['password']) is None:
            is_valid = False
            flash('Invalid Password! \n*must have one capital letter in it', 'password')
        elif data['password'] != data['confirm_password']:
            flash('password must match', 'confirm_password')
            is_valid = False

        return is_valid

