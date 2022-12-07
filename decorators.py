import re
from functools import wraps
from flask import request, jsonify
from database import *


admin_credentials = db.Table('admin_credentials', metadata, autoload=True, autoload_with=engine)
employee_credentials = db.Table('employee_credentials', metadata, autoload=True, autoload_with=engine)


def admin_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "Authorization" not in request.headers:
            return jsonify({"message": "Authorization header not present"}), 401
        auth = request.headers.get("Authorization")
        print(auth)
        admin = session.query(admin_credentials).filter(admin_credentials.c.auth_token == str(auth)).all()
        print('msg',admin)
        if admin:
            return f(*args, **kwargs)
        return jsonify({"message": "you need to be admin"}), 403

    return wrap


def is_email_address_valid(email):
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z-]+)*$", str(email)):
        return False
    return True


def is_password(password):
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$', str(password)):
        return False
    return True


def is_phone_number(phone_number):
    if not re.match("^[0-9]{10}$", str(phone_number)):
        return False
    return True


def all_registered_emp_details():
    query = db.select([employee_credentials])
    result = engine.execute(query)
    res = result.fetchall()
    return jsonify({'All registered employees': [dict(row) for row in res]})