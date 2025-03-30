from flask import Flask, render_template, request, redirect, url_for
import database

# Initialize the database
database.initialize("ems.db")

app = Flask(__name__)

# Employee Routes
@app.route("/", methods=["GET"])
@app.route("/employees", methods=["GET"])
def get_employee_list():
    employees = database.get_employees()
    return render_template("employee_list.html", employees=employees)

@app.route("/employee/create", methods=["GET"])
def get_employee_create():
    departments = database.get_departments()
    positions = database.get_positions()
    return render_template("employee_create.html", departments=departments, positions=positions)

@app.route("/employee/create", methods=["POST"])
def post_employee_create():
    data = dict(request.form)
    database.create_employee(data)
    return redirect(url_for("get_employee_list"))

@app.route("/employee/delete/<id>", methods=["GET"])
def get_employee_delete(id):
    database.delete_employee(id)
    return redirect(url_for("get_employee_list"))

@app.route("/employee/update/<id>", methods=["GET"])
def get_employee_update(id):
    employee = database.get_employee(id)
    departments = database.get_departments()
    positions = database.get_positions()
    return render_template("employee_update.html", employee=employee, departments=departments, positions=positions)

@app.route("/employee/update/<id>", methods=["POST"])
def post_employee_update(id):
    data = dict(request.form)
    database.update_employee(id, data)
    return redirect(url_for("get_employee_list"))

# Department Routes
@app.route("/departments", methods=["GET"])
def get_department_list():
    departments = database.get_departments()
    return render_template("department_list.html", departments=departments)

@app.route("/department/create", methods=["GET"])
def get_department_create():
    return render_template("department_create.html")

@app.route("/department/create", methods=["POST"])
def post_department_create():
    data = dict(request.form)
    database.create_department(data)
    return redirect(url_for("get_department_list"))

@app.route("/department/delete/<id>", methods=["GET"])
def get_department_delete(id):
    database.delete_department(id)
    return redirect(url_for("get_department_list"))

@app.route("/department/update/<id>", methods=["GET"])
def get_department_update(id):
    department = database.get_department(id)
    return render_template("department_update.html", department=department)

@app.route("/department/update/<id>", methods=["POST"])
def post_department_update(id):
    data = dict(request.form)
    database.update_department(id, data)
    return redirect(url_for("get_department_list"))

# Position Routes
@app.route("/positions", methods=["GET"])
def get_position_list():
    positions = database.get_positions()
    return render_template("position_list.html", positions=positions)

@app.route("/position/create", methods=["GET"])
def get_position_create():
    departments = database.get_departments()
    return render_template("position_create.html", departments=departments)

@app.route("/position/create", methods=["POST"])
def post_position_create():
    data = dict(request.form)
    database.create_position(data)
    return redirect(url_for("get_position_list"))

@app.route("/position/delete/<id>", methods=["GET"])
def get_position_delete(id):
    database.delete_position(id)
    return redirect(url_for("get_position_list"))

@app.route("/position/update/<id>", methods=["GET"])
def get_position_update(id):
    position = database.get_position(id)
    departments = database.get_departments()
    return render_template("position_update.html", position=position, departments=departments)

@app.route("/position/update/<id>", methods=["POST"])
def post_position_update(id):
    data = dict(request.form)
    database.update_position(id, data)
    return redirect(url_for("get_position_list"))

# Attendance Routes
@app.route("/attendances", methods=["GET"])
def get_attendance_list():
    attendances = database.get_attendances()
    return render_template("attendance_list.html", attendances=attendances)

@app.route("/attendance/create", methods=["GET"])
def get_attendance_create():
    employees = database.get_employees()
    return render_template("attendance_create.html", employees=employees)

@app.route("/attendance/create", methods=["POST"])
def post_attendance_create():
    data = dict(request.form)
    database.create_attendance(data)
    return redirect(url_for("get_attendance_list"))

@app.route("/attendance/delete/<id>", methods=["GET"])
def get_attendance_delete(id):
    database.delete_attendance(id)
    return redirect(url_for("get_attendance_list"))

@app.route("/attendance/update/<id>", methods=["GET"])
def get_attendance_update(id):
    attendance = database.get_attendance(id)
    employees = database.get_employees()
    return render_template("attendance_update.html", attendance=attendance, employees=employees)

@app.route("/attendance/update/<id>", methods=["POST"])
def post_attendance_update(id):
    data = dict(request.form)
    database.update_attendance(id, data)
    return redirect(url_for("get_attendance_list"))

# Leave Routes
@app.route("/leaves", methods=["GET"])
def get_leave_list():
    leaves = database.get_leaves()
    return render_template("leave_list.html", leaves=leaves)

@app.route("/leave/create", methods=["GET"])
def get_leave_create():
    employees = database.get_employees()
    return render_template("leave_create.html", employees=employees)

@app.route("/leave/create", methods=["POST"])
def post_leave_create():
    data = dict(request.form)
    database.create_leave(data)
    return redirect(url_for("get_leave_list"))

@app.route("/leave/delete/<id>", methods=["GET"])
def get_leave_delete(id):
    database.delete_leave(id)
    return redirect(url_for("get_leave_list"))

@app.route("/leave/update/<id>", methods=["GET"])
def get_leave_update(id):
    leave = database.get_leave(id)
    employees = database.get_employees()
    return render_template("leave_update.html", leave=leave, employees=employees)

@app.route("/leave/update/<id>", methods=["POST"])
def post_leave_update(id):
    data = dict(request.form)
    database.update_leave(id, data)
    return redirect(url_for("get_leave_list"))

# Project Routes
@app.route("/projects", methods=["GET"])
def get_project_list():
    projects = database.get_projects()
    return render_template("project_list.html", projects=projects)

@app.route("/project/create", methods=["GET"])
def get_project_create():
    employees = database.get_employees()
    return render_template("project_create.html", employees=employees)

@app.route("/project/create", methods=["POST"])
def post_project_create():
    data = dict(request.form)
    database.create_project(data)
    return redirect(url_for("get_project_list"))

@app.route("/project/delete/<employee_id>/<team_id>", methods=["GET"])
def get_project_delete(employee_id, team_id):
    database.delete_project(employee_id, team_id)
    return redirect(url_for("get_project_list"))

@app.route("/project/update/<employee_id>/<team_id>", methods=["GET"])
def get_project_update(employee_id, team_id):
    project = database.get_project(employee_id, team_id)
    employees = database.get_employees()
    return render_template("project_update.html", project=project, employees=employees)

@app.route("/project/update/<employee_id>/<team_id>", methods=["POST"])
def post_project_update(employee_id, team_id):
    data = dict(request.form)
    database.update_project(employee_id, team_id, data)
    return redirect(url_for("get_project_list"))

# Payroll Routes
@app.route("/payrolls", methods=["GET"])
def get_payroll_list():
    payrolls = database.get_payrolls()
    return render_template("payroll_list.html", payrolls=payrolls)

@app.route("/payroll/create", methods=["GET"])
def get_payroll_create():
    employees = database.get_employees()
    return render_template("payroll_create.html", employees=employees)

@app.route("/payroll/create", methods=["POST"])
def post_payroll_create():
    data = dict(request.form)
    database.create_payroll(data)
    return redirect(url_for("get_payroll_list"))

@app.route("/payroll/delete/<id>", methods=["GET"])
def get_payroll_delete(id):
    database.delete_payroll(id)
    return redirect(url_for("get_payroll_list"))

@app.route("/payroll/update/<id>", methods=["GET"])
def get_payroll_update(id):
    payroll = database.get_payroll(id)
    employees = database.get_employees()
    return render_template("payroll_update.html", payroll=payroll, employees=employees)

@app.route("/payroll/update/<id>", methods=["POST"])
def post_payroll_update(id):
    data = dict(request.form)
    database.update_payroll(id, data)
    return redirect(url_for("get_payroll_list"))

if __name__ == "__main__":
    app.run(debug=True)