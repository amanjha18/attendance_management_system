import logging
from flask import request, jsonify
from app import app, mysql


import random
import string
from flask import Flask
# from flask_mysql import MySQL
from werkzeug.security import generate_password_hash

# Set up logging to track the application's activity and errors
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



# Utility function to generate a random password
def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

# Check if the users table is empty, and if so, create a user
def create_user_if_needed():
    # Check if there are any users in the table
    result = execute_query("SELECT * FROM users", fetch=True)
    if not result:  # No users found, create one
        username = 'admin'
        password = generate_random_password()  # Generate a random password
        hashed_password = generate_password_hash(password)  # Hash the password

        # Insert the new user into the database
        execute_query("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))

        # Log the username and password (only for initial user creation, be cautious in production)
        logger.info(f"Initial user created - Username: {username}, Password: {password}")
    else:
        logger.info("Users already exist in the database, skipping user creation.")

# Create user on app startup
@app.before_first_request
def before_first_request():
    create_user_if_needed()


# Utility function for handling database operations with error handling and logging
def execute_query(query, params=None, fetch=False):
    try:
        cur = mysql.connection.cursor()  # Get cursor to execute MySQL queries
        logger.debug(f"Executing query: {query}, with params: {params}")  # Log query execution
        cur.execute(query, params) if params else cur.execute(query)  # Execute query with or without params
        if fetch:  # If fetching data, return the results
            result = cur.fetchall()
            logger.debug(f"Query result: {result}")
            return result, None  # Return result without error
        mysql.connection.commit()  # Commit changes to the database
        logger.info("Query executed and committed successfully")  # Log successful execution
        return None, None  # No result, but no error either
    except Exception as e:
        logger.error(f"Error executing query: {e}")  # Log any errors during query execution
        return None, str(e)  # Return error message

# 1. Get all departments
@app.route('/departments', methods=['GET'])
def get_departments():
    logger.info("Fetching all departments")  # Log the action
    departments, error = execute_query("SELECT * FROM departments", fetch=True)  # Fetch departments
    if error:  # If an error occurs
        logger.error(f"Error fetching departments: {error}")  # Log the error
        return jsonify({"error": error}), 500  # Return error response
    return jsonify(departments)  # Return departments as JSON response

# 2. Get a specific department by ID
@app.route('/departments/<int:department_id>', methods=['GET'])
def get_department(department_id):
    logger.info(f"Fetching department with ID: {department_id}")  # Log the action
    department, error = execute_query("SELECT * FROM departments WHERE id = %s", (department_id,), fetch=True)  # Fetch department by ID
    if error:  # If an error occurs
        logger.error(f"Error fetching department with ID {department_id}: {error}")  # Log the error
        return jsonify({"error": error}), 500  # Return error response
    if not department:  # If the department is not found
        logger.warning(f"Department with ID {department_id} not found")  # Log warning
        return jsonify({"message": "Department not found"}), 404  # Return not found response
    return jsonify(department[0])  # Return department as JSON response

# 3. Add a new department
@app.route('/departments', methods=['POST'])
def add_department():
    data = request.get_json()  # Get JSON data from the request body
    logger.info("Adding a new department")  # Log the action
    if not data or not data.get('name'):  # Validate input
        logger.warning("Department name is required")  # Log warning
        return jsonify({"error": "Department name is required"}), 400  # Return bad request response
    execute_query("INSERT INTO departments (name) VALUES (%s)", (data['name'],))  # Insert new department
    logger.info(f"Department '{data['name']}' added successfully")  # Log success
    return jsonify({"message": "Department added"}), 201  # Return created response

# 4. Update an existing department by ID
@app.route('/departments/<int:department_id>', methods=['PUT'])
def update_department(department_id):
    data = request.get_json()  # Get JSON data from the request body
    logger.info(f"Updating department with ID: {department_id}")  # Log the action
    if not data or not data.get('name'):  # Validate input
        logger.warning("Department name is required")  # Log warning
        return jsonify({"error": "Department name is required"}), 400  # Return bad request response
    execute_query("UPDATE departments SET name = %s WHERE id = %s", (data['name'], department_id))  # Update department
    logger.info(f"Department with ID {department_id} updated successfully")  # Log success
    return jsonify({"message": "Department updated"})  # Return success response

# 6. Get all students
@app.route('/students', methods=['GET'])
def get_students():
    logger.info("Fetching all students")  # Log the action
    students, error = execute_query("SELECT * FROM students", fetch=True)  # Fetch all students
    if error:  # If an error occurs
        logger.error(f"Error fetching students: {error}")  # Log the error
        return jsonify({"error": error}), 500  # Return error response
    return jsonify(students)  # Return students as JSON response

# 7. Get a specific student by ID
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    logger.info(f"Fetching student with ID: {student_id}")  # Log the action
    student, error = execute_query("SELECT * FROM students WHERE id = %s", (student_id,), fetch=True)  # Fetch student by ID
    if error:  # If an error occurs
        logger.error(f"Error fetching student with ID {student_id}: {error}")  # Log the error
        return jsonify({"error": error}), 500  # Return error response
    if not student:  # If the student is not found
        logger.warning(f"Student with ID {student_id} not found")  # Log warning
        return jsonify({"message": "Student not found"}), 404  # Return not found response
    return jsonify(student[0])  # Return student as JSON response

# 8. Add a new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()  # Get JSON data from the request body
    logger.info("Adding a new student")  # Log the action
    if not data or not data.get('name') or not data.get('course_id'):  # Validate input
        logger.warning("Name and course ID are required")  # Log warning
        return jsonify({"error": "Name and course ID are required"}), 400  # Return bad request response
    execute_query("INSERT INTO students (name, course_id) VALUES (%s, %s)", (data['name'], data['course_id']))  # Insert new student
    logger.info(f"Student '{data['name']}' added successfully")  # Log success
    return jsonify({"message": "Student added"}), 201  # Return created response

# 9. Update an existing student by ID
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()  # Get JSON data from the request body
    logger.info(f"Updating student with ID: {student_id}")  # Log the action
    if not data or not data.get('name') or not data.get('course_id'):  # Validate input
        logger.warning("Name and course ID are required")  # Log warning
        return jsonify({"error": "Name and course ID are required"}), 400  # Return bad request response
    execute_query("UPDATE students SET name = %s, course_id = %s WHERE id = %s", 
                  (data['name'], data['course_id'], student_id))  # Update student
    logger.info(f"Student with ID {student_id} updated successfully")  # Log success
    return jsonify({"message": "Student updated"})  # Return success response

# 11. Log attendance for a student
@app.route('/attendance', methods=['POST'])
def log_attendance():
    data = request.get_json()  # Get JSON data from the request body
    logger.info("Logging attendance")  # Log the action
    if not data or not data.get('student_id') or not data.get('date') or not data.get('status'):  # Validate input
        logger.warning("Student ID, date, and status are required")  # Log warning
        return jsonify({"error": "Student ID, date, and status are required"}), 400  # Return bad request response
    execute_query("INSERT INTO attendance_log (student_id, date, status) VALUES (%s, %s, %s)", 
                  (data['student_id'], data['date'], data['status']))  # Log attendance
    logger.info(f"Attendance for student ID {data['student_id']} on {data['date']} logged successfully")  # Log success
    return jsonify({"message": "Attendance logged"}), 201  # Return created response

# 12. Get attendance for a specific student
@app.route('/attendance/<int:student_id>', methods=['GET'])
def get_attendance(student_id):
    logger.info(f"Fetching attendance for student with ID: {student_id}")  # Log the action
    attendance, error = execute_query("SELECT * FROM attendance_log WHERE student_id = %s", (student_id,), fetch=True)  # Fetch attendance
    if error:  # If an error occurs
        logger.error(f"Error fetching attendance for student with ID {student_id}: {error}")  # Log the error
       
