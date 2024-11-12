# Attendance Management System - Flask App

A simple Attendance Management System built with Flask and MySQL.

## Features
- **Departments**: Add, view, update departments.
- **Students**: Add, view, update student records.
- **Attendance**: Log and view attendance for students.

## Setup Instructions

### Prerequisites
- Python 3.6+
- MySQL Server
- Flask
- Flask-MySQL
- werkzeug

### Installing Dependencies
1. Clone the repository:
    ```bash
    git clone https://github.com/amanjha18/attendance-management-flask.git
    cd attendance-management-flask
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your MySQL database and update credentials in `app.py`.

4. Run the app:
    ```bash
    python run.py
    ```

### API Endpoints

- **GET /departments** - Get all departments
- **GET /departments/{id}** - Get department by ID
- **POST /departments** - Add department
- **PUT /departments/{id}** - Update department

- **GET /students** - Get all students
- **GET /students/{id}** - Get student by ID
- **POST /students** - Add student
- **PUT /students/{id}** - Update student

- **POST /attendance** - Log attendance
- **GET /attendance/{student_id}** - Get attendance for a student

### First Time Setup
The app will create an admin user (`admin`) with a random password on the first run, which will be logged in the console.

## License
MIT License
