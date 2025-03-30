import sqlite3

connection = None

def initialize(database_file):
    global connection
    connection = sqlite3.connect(database_file, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    create_tables()

def create_tables():
    cursor = connection.cursor()
    
    # Create Department table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Department (
            DepartmentID INTEGER PRIMARY KEY,
            DeptName TEXT,
            Location TEXT
        )
    """)
    
    # Create Position table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Position (
            PositionID INTEGER PRIMARY KEY,
            PositionName TEXT,
            DepartmentID INTEGER,
            FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
        )
    """)
    
    # Create Attendance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Attendance (
            AttendanceID INTEGER PRIMARY KEY,
            EmployeeID INTEGER,
            Date DATE,
            Status TEXT
        )
    """)
    
    # Create Leave table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Leave (
            LeaveID INTEGER PRIMARY KEY,
            EmployeeID INTEGER,
            StartDate DATE,
            EndDate DATE,
            Reason TEXT,
            Status TEXT
        )
    """)
    
    # Create Project table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Project (
            EmployeeID INTEGER,
            TeamID INTEGER,
            ProjectID TEXT UNIQUE,
            Task TEXT,
            Status TEXT,
            Sprint INTEGER,
            PRIMARY KEY (EmployeeID, TeamID)
        )
    """)
    
    # Create Payroll table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Payroll (
            PayrollID INTEGER PRIMARY KEY,
            EmployeeID INTEGER,
            Month TEXT,
            BasicPay DECIMAL(10,2),
            Deductions DECIMAL(10,2),
            Netpay DECIMAL(10,2)
        )
    """)
    
    # Create Employee_details table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Employee_details (
            EmployeeID INTEGER PRIMARY KEY,
            EmployeeName TEXT,
            HireDate DATE,
            Experience TEXT,
            Position TEXT,
            Gender TEXT,
            DepartmentID INTEGER,
            Email TEXT,
            Phone TEXT,
            Status TEXT,
            DOB TEXT,
            Salary TEXT,
            TeamID INTEGER,
            FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID),
            FOREIGN KEY (Position) REFERENCES Position(PositionName)
        )
    """)
    
    connection.commit()

# Employee CRUD operations
def get_employees():
    cursor = connection.cursor()
    cursor.execute("""
        SELECT e.*, d.DeptName, p.PositionName 
        FROM Employee_details e
        LEFT JOIN Department d ON e.DepartmentID = d.DepartmentID
        LEFT JOIN Position p ON e.Position = p.PositionName
    """)
    employees = cursor.fetchall()
    return [dict(emp) for emp in employees]

def get_employee(id):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT e.*, d.DeptName, p.PositionName 
        FROM Employee_details e
        LEFT JOIN Department d ON e.DepartmentID = d.DepartmentID
        LEFT JOIN Position p ON e.Position = p.PositionName
        WHERE e.EmployeeID = ?
    """, (id,))
    employee = cursor.fetchone()
    return dict(employee) if employee else None

def create_employee(data):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Employee_details (
            EmployeeName, HireDate, Experience, Position, Gender, 
            DepartmentID, Email, Phone, Status, DOB, Salary, TeamID
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["EmployeeName"], data["HireDate"], data["Experience"], 
        data["Position"], data["Gender"], data["DepartmentID"], 
        data["Email"], data["Phone"], data["Status"], 
        data["DOB"], data["Salary"], data["TeamID"]
    ))
    connection.commit()

def update_employee(id, data):
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Employee_details SET 
            EmployeeName = ?, HireDate = ?, Experience = ?, Position = ?, 
            Gender = ?, DepartmentID = ?, Email = ?, Phone = ?, 
            Status = ?, DOB = ?, Salary = ?, TeamID = ?
        WHERE EmployeeID = ?
    """, (
        data["EmployeeName"], data["HireDate"], data["Experience"], 
        data["Position"], data["Gender"], data["DepartmentID"], 
        data["Email"], data["Phone"], data["Status"], 
        data["DOB"], data["Salary"], data["TeamID"], id
    ))
    connection.commit()

def delete_employee(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Employee_details WHERE EmployeeID = ?", (id,))
    connection.commit()

# Department CRUD operations
def get_departments():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Department")
    return [dict(dept) for dept in cursor.fetchall()]

def get_department(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Department WHERE DepartmentID = ?", (id,))
    dept = cursor.fetchone()
    return dict(dept) if dept else None

def create_department(data):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Department (DeptName, Location) 
        VALUES (?, ?)
    """, (data["DeptName"], data["Location"]))
    connection.commit()

def update_department(id, data):
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Department SET 
            DeptName = ?, Location = ?
        WHERE DepartmentID = ?
    """, (data["DeptName"], data["Location"], id))
    connection.commit()

def delete_department(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Department WHERE DepartmentID = ?", (id,))
    connection.commit()

# Position CRUD operations
def get_positions():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Position")
    return [dict(pos) for pos in cursor.fetchall()]

def get_position(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Position WHERE PositionID = ?", (id,))
    pos = cursor.fetchone()
    return dict(pos) if pos else None

def create_position(data):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Position (PositionName, DepartmentID) 
        VALUES (?, ?)
    """, (data["PositionName"], data["DepartmentID"]))
    connection.commit()

def update_position(id, data):
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Position SET 
            PositionName = ?, DepartmentID = ?
        WHERE PositionID = ?
    """, (data["PositionName"], data["DepartmentID"], id))
    connection.commit()

def delete_position(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Position WHERE PositionID = ?", (id,))
    connection.commit()

# Attendance CRUD operations
def get_attendances():
    cursor = connection.cursor()
    cursor.execute("""
        SELECT a.*, e.EmployeeName 
        FROM Attendance a
        LEFT JOIN Employee_details e ON a.EmployeeID = e.EmployeeID
    """)
    return [dict(att) for att in cursor.fetchall()]

def get_attendance(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Attendance WHERE AttendanceID = ?", (id,))
    att = cursor.fetchone()
    return dict(att) if att else None

def create_attendance(data):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Attendance (EmployeeID, Date, Status) 
        VALUES (?, ?, ?)
    """, (data["EmployeeID"], data["Date"], data["Status"]))
    connection.commit()

def update_attendance(id, data):
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Attendance SET 
            EmployeeID = ?, Date = ?, Status = ?
        WHERE AttendanceID = ?
    """, (data["EmployeeID"], data["Date"], data["Status"], id))
    connection.commit()

def delete_attendance(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Attendance WHERE AttendanceID = ?", (id,))
    connection.commit()

# Leave CRUD operations
def get_leaves():
    cursor = connection.cursor()
    cursor.execute("""
        SELECT l.*, e.EmployeeName 
        FROM Leave l
        LEFT JOIN Employee_details e ON l.EmployeeID = e.EmployeeID
    """)
    return [dict(leave) for leave in cursor.fetchall()]

def get_leave(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Leave WHERE LeaveID = ?", (id,))
    leave = cursor.fetchone()
    return dict(leave) if leave else None

def create_leave(data):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Leave (EmployeeID, StartDate, EndDate, Reason, Status) 
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["EmployeeID"], data["StartDate"], data["EndDate"], 
        data["Reason"], data["Status"]
    ))
    connection.commit()

def update_leave(id, data):
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Leave SET 
            EmployeeID = ?, StartDate = ?, EndDate = ?, Reason = ?, Status = ?
        WHERE LeaveID = ?
    """, (
        data["EmployeeID"], data["StartDate"], data["EndDate"], 
        data["Reason"], data["Status"], id
    ))
    connection.commit()

def delete_leave(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Leave WHERE LeaveID = ?", (id,))
    connection.commit()

# Project CRUD operations
def get_projects():
    cursor = connection.cursor()
    cursor.execute("""
        SELECT p.*, e.EmployeeName 
        FROM Project p
        LEFT JOIN Employee_details e ON p.EmployeeID = e.EmployeeID
    """)
    return [dict(proj) for proj in cursor.fetchall()]

def get_project(employee_id, team_id):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM Project 
        WHERE EmployeeID = ? AND TeamID = ?
    """, (employee_id, team_id))
    proj = cursor.fetchone()
    return dict(proj) if proj else None

def create_project(data):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Project (EmployeeID, TeamID, ProjectID, Task, Status, Sprint) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["EmployeeID"], data["TeamID"], data["ProjectID"], 
        data["Task"], data["Status"], data["Sprint"]
    ))
    connection.commit()

def update_project(employee_id, team_id, data):
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Project SET 
            ProjectID = ?, Task = ?, Status = ?, Sprint = ?
        WHERE EmployeeID = ? AND TeamID = ?
    """, (
        data["ProjectID"], data["Task"], data["Status"], 
        data["Sprint"], employee_id, team_id
    ))
    connection.commit()

def delete_project(employee_id, team_id):
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM Project 
        WHERE EmployeeID = ? AND TeamID = ?
    """, (employee_id, team_id))
    connection.commit()

# Payroll CRUD operations
def get_payrolls():
    cursor = connection.cursor()
    cursor.execute("""
        SELECT p.*, e.EmployeeName 
        FROM Payroll p
        LEFT JOIN Employee_details e ON p.EmployeeID = e.EmployeeID
    """)
    return [dict(pay) for pay in cursor.fetchall()]

def get_payroll(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Payroll WHERE PayrollID = ?", (id,))
    pay = cursor.fetchone()
    return dict(pay) if pay else None

def create_payroll(data):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Payroll (EmployeeID, Month, BasicPay, Deductions, Netpay) 
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["EmployeeID"], data["Month"], data["BasicPay"], 
        data["Deductions"], data["Netpay"]
    ))
    connection.commit()

def update_payroll(id, data):
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Payroll SET 
            EmployeeID = ?, Month = ?, BasicPay = ?, Deductions = ?, Netpay = ?
        WHERE PayrollID = ?
    """, (
        data["EmployeeID"], data["Month"], data["BasicPay"], 
        data["Deductions"], data["Netpay"], id
    ))
    connection.commit()

def delete_payroll(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Payroll WHERE PayrollID = ?", (id,))
    connection.commit()

# Test functions
def setup_test_database():
    initialize("test_ems.db")
    cursor = connection.cursor()
    
    # Clear all tables
    cursor.execute("DROP TABLE IF EXISTS Employee_details")
    cursor.execute("DROP TABLE IF EXISTS Department")
    cursor.execute("DROP TABLE IF EXISTS Position")
    cursor.execute("DROP TABLE IF EXISTS Attendance")
    cursor.execute("DROP TABLE IF EXISTS Leave")
    cursor.execute("DROP TABLE IF EXISTS Project")
    cursor.execute("DROP TABLE IF EXISTS Payroll")
    
    # Recreate tables
    create_tables()
    
    # Insert test data
    # Departments
    departments = [
        {"DeptName": "IT", "Location": "Floor 1"},
        {"DeptName": "HR", "Location": "Floor 2"},
        {"DeptName": "Finance", "Location": "Floor 3"}
    ]
    for dept in departments:
        create_department(dept)
    
    # Positions
    positions = [
        {"PositionName": "Developer", "DepartmentID": 1},
        {"PositionName": "Manager", "DepartmentID": 1},
        {"PositionName": "HR Specialist", "DepartmentID": 2},
        {"PositionName": "Accountant", "DepartmentID": 3}
    ]
    for pos in positions:
        create_position(pos)
    
    # Employees
    employees = [
        {
            "EmployeeName": "John Doe", "HireDate": "2020-01-15", 
            "Experience": "5 years", "Position": "Developer", 
            "Gender": "Male", "DepartmentID": 1, "Email": "john@example.com",
            "Phone": "1234567890", "Status": "Active", "DOB": "1990-05-10",
            "Salary": "50000", "TeamID": 1
        },
        {
            "EmployeeName": "Jane Smith", "HireDate": "2019-03-20", 
            "Experience": "6 years", "Position": "Manager", 
            "Gender": "Female", "DepartmentID": 1, "Email": "jane@example.com",
            "Phone": "9876543210", "Status": "Active", "DOB": "1988-11-25",
            "Salary": "70000", "TeamID": 1
        }
    ]
    for emp in employees:
        create_employee(emp)
    
    connection.commit()

if __name__ == "__main__":
    setup_test_database()
    print("Test database created successfully.")