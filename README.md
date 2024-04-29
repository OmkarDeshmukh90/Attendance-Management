# Attendance-Management
# Student Attendance Management System

This repository contains code for a Student Attendance Management System built using Python and Streamlit. The system allows users to manage student information, record attendance for classes, generate a list of students with low attendance, view student attendance records, and remove students from the database.

## Overview

The Student Attendance Management System consists of the following components:

1. **Add Student**: Add new students to the database or update existing student information.

2. **Record Attendance**: Record attendance for classes by specifying class ID, student ID, attendance status, and optional remarks.

3. **Generate Low Attendance List**: Generate a list of students with attendance less than 75% and download the list as a CSV file.

4. **View Student Attendance**: View student attendance records, including total attendance, present attendance, and attendance percentage.

5. **Remove Student**: Remove a student from the database by entering their roll number.

## Dependencies

Make sure you have the following dependencies installed:

- Python 3
- Streamlit
- Pandas
- MySQL Connector

## Usage

1. Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/student-attendance-management-system.git
```

2. Navigate to the project directory:

```bash
cd student-attendance-management-system
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
streamlit run app.py
```

5. Access the application through your web browser at `http://localhost:8501`.

## Features

- **Student Management**: Add new students, update student information, and remove students from the database.

- **Attendance Recording**: Record attendance for classes with options to specify attendance status and remarks.

- **Attendance Analysis**: Generate a list of students with low attendance and view student attendance records.

## Data

The system uses a MySQL database to store student information and attendance records. Ensure that the database is properly configured and accessible.


