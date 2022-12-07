from flask import Flask

from decorators import *

app = Flask(__name__)


@app.route('/')
def welcome():
    return "welcome to Experience.com"


@app.route('/register', methods=['Get', 'post'])
def register():
    if request.method == 'POST':
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        username = request.args.get('username')
        email = request.args.get('email')
        phone_number = request.args.get('phone_number')
        password = request.args.get('password')
        department = request.args.get('department')
        role = request.args.get('role')

    if not first_name.replace(" ", "").isalpha():
        return jsonify({"message": "first name contains only alphabets"}), 404
    if not last_name.replace(" ", "").isalpha():
        return jsonify({"message": "last name contains only alphabets"}), 404
    if not username.replace(" ", "").isalnum():
        return jsonify({"message": "username contains only alphabets and numbers not special characters"}), 404
    if not is_email_address_valid(email):
        return jsonify({"message": "Please enter a valid email address"}), 404
    if not is_phone_number(phone_number):
        return jsonify({"message": "phone number should contains 10 digits numbers"}), 404
    if not is_password(password):
        return jsonify({"message": "password should be atleast 6 characters. it should contain 1 uppercase alphabet "
                                   "and 1 special character and 1 number "}), 404
    if not department.replace(" ", "").isalpha():
        return jsonify({"message": "department should contains only alphabets"}), 404
    if not role.replace(" ", "").isalpha():
        return jsonify({"message": "role should contains only alphabets"}), 404

    check1 = session.query(employee_credentials).filter(employee_credentials.c.username == username)
    res = check1.all()
    if res:
        return jsonify({"message": 'Account already exists!'}), 403
    else:

        data = employee_credentials.insert().values(first_name=first_name, last_name=last_name, username=username,
                                                    email=email, phone_number=phone_number, password=password,
                                                    department=department, role=role)
        conn.execute(data)

        return jsonify({'message': 'Registered successfully'}), 200


@app.route('/login/<username>/<password>', methods=['GET'])
def login(username, password):
    if request.method == "GET":
        check_emp = session.query(employee_credentials).filter(employee_credentials.c.username == username,
                                                               employee_credentials.c.password == password)
        result = check_emp.all()
        if result:
            return jsonify({"message": 'Employee successfully logged in'}), 200

        else:
            check_admin = session.query(admin_credentials).filter(admin_credentials.c.username == username,
                                                                  admin_credentials.c.password == password)
            res = check_admin.all()
            if res:
                return jsonify({"message": 'Admin successfully logged in'}), 200
            elif not res:
                return jsonify({"message": 'invalid username or password'}), 401


@app.route('/<username>/<password>', methods=['GET'])
def details(username, password):
    if request.method == "GET":
        check_emp = session.query(employee_credentials).filter(employee_credentials.c.username == username,
                                                               employee_credentials.c.password == password)
        result = check_emp.all()
        if result:
            return jsonify({"result": result})
        else:
            check_admin = session.query(admin_credentials).filter(admin_credentials.c.username == username,
                                                                  admin_credentials.c.password == password)
            res = check_admin.all()
            if res:
                return all_registered_emp_details()


@app.route('/add', methods=['POST'])
@admin_login_required
def add_employee():
    return register()


@app.route('/delete_details/<emp_id>', methods=["DELETE"])
@admin_login_required
def delete_details(emp_id):
    if request.method == 'DELETE':
        check1 = session.query(employee_credentials).filter(employee_credentials.c.emp_id == emp_id)
        res = check1.all()
        if not res:
            return jsonify({"message": f'{emp_id} emp_id record is not available'}), 404
        else:
            delete = employee_credentials.delete().where(employee_credentials.c.emp_id == emp_id)
            conn.execute(delete)
            return jsonify({"message": f'{emp_id} emp_id record has been deleted'}), 200


@app.route('/update_details/<emp_id>', methods=["PUT"])
@admin_login_required
def update_details(emp_id):
    if request.method == 'PUT':
        department = request.args.get("department")
        role = request.args.get("role")

    check1 = session.query(employee_credentials).filter(employee_credentials.c.emp_id == emp_id)
    res = check1.all()
    if not res:
        return jsonify({"message": f'{emp_id} emp_id record is not available'}), 404
    else:
        update = employee_credentials.update().where(employee_credentials.c.emp_id == emp_id).values(
            department=department, role=role)
        conn.execute(update)

        return jsonify({'message': f'{emp_id} emp_id details has been updated successfully'}), 200


if __name__ == "__main__":
    app.run(debug=True, port=7009)
