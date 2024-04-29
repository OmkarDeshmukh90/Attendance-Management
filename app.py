import streamlit as st
import mysql.connector
import pandas as pd

# Connect to MySQL database
def connect_to_database():
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="4578",
            database="student_attendance"
        )
        print("Connected to database successfully!")
        return db_connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Add a new student
def add_or_update_student(roll_number, name, email, department, year, contact_number):
    db_connection = connect_to_database()
    if db_connection:
        cursor = db_connection.cursor()
        try:
            # Check if the student already exists
            cursor.execute("SELECT * FROM Students WHERE student_roll_number = %s", (roll_number,))
            existing_student = cursor.fetchone()
            if existing_student:
                # Update existing student information
                cursor.execute("UPDATE Students SET student_name = %s, student_email = %s, student_department = %s, student_year = %s, student_contact_number = %s WHERE student_roll_number = %s",
                               (name, email, department, year, contact_number, roll_number))
                db_connection.commit()
                st.success("Student information updated successfully!")
            else:
                # Add a new student
                cursor.execute("INSERT INTO Students (student_roll_number, student_name, student_email, student_department, student_year, student_contact_number) VALUES (%s, %s, %s, %s, %s, %s)",
                               (roll_number, name, email, department, year, contact_number))
                db_connection.commit()
                st.success("Student added successfully!")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()
            db_connection.close()

# Remove a student from the database
def remove_student(roll_number):
    db_connection = connect_to_database()
    if db_connection:
        cursor = db_connection.cursor()
        try:
            # Check if the student exists
            cursor.execute("SELECT * FROM Students WHERE student_roll_number = %s", (roll_number,))
            existing_student = cursor.fetchone()
            if existing_student:
                # Remove the student
                cursor.execute("DELETE FROM Students WHERE student_roll_number = %s", (roll_number,))
                db_connection.commit()
                st.success("Student removed successfully!")
            else:
                st.warning("Student not found!")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()
            db_connection.close()

# Record attendance for a class
def record_attendance(class_id, student_id, attendance_status, remarks=None):
    db_connection = connect_to_database()
    if db_connection:
        cursor = db_connection.cursor()
        try:
            cursor.execute("INSERT INTO Attendance (class_id, student_id, attendance_status, attendance_remarks) VALUES (%s, %s, %s, %s)",
                           (class_id, student_id, attendance_status, remarks))
            db_connection.commit()
            st.success("Attendance recorded successfully!")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()
            db_connection.close()

# Generate a list of students with attendance less than 75%


# Fetch data and return as Pandas DataFrame
def fetch_data_as_dataframe():
    db_connection = connect_to_database()
    if db_connection:
        query = """
            SELECT Students.student_id, Students.student_name, Students.student_roll_number,
                   COUNT(Attendance.attendance_id) AS total_attendance, 
                   SUM(CASE WHEN Attendance.attendance_status='Present' THEN 1 ELSE 0 END) AS present_attendance 
            FROM Students 
            LEFT JOIN Attendance ON Students.student_id = Attendance.student_id 
            GROUP BY Students.student_id 
            HAVING (SUM(CASE WHEN Attendance.attendance_status='Present' THEN 1 ELSE 0 END) / COUNT(Attendance.attendance_id)) * 100 < 75
        """
        try:
            df = pd.read_sql_query(query, db_connection)
            return df
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            db_connection.close()

def fetch_student_attendance_data():
    db_connection = connect_to_database()
    if db_connection:
        query = """
            SELECT Students.student_id, Students.student_name, Students.student_department,
                   COUNT(Attendance.attendance_id) AS total_attendance, 
                   SUM(CASE WHEN Attendance.attendance_status='Present' THEN 1 ELSE 0 END) AS present_attendance 
            FROM Students 
            LEFT JOIN Attendance ON Students.student_id = Attendance.student_id 
            GROUP BY Students.student_id, Students.student_name, Students.student_department
        """
        try:
            df = pd.read_sql_query(query, db_connection)
            # Calculate attendance percentage
            df['attendance_percentage'] = (df['present_attendance'] / df['total_attendance']) * 100
            return df[['student_id', 'student_name', 'student_department', 'attendance_percentage']]
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            db_connection.close()

def main():
    st.title("Student Attendance Management System")

    menu_choice = st.sidebar.selectbox("Menu", ["Add Student", "Record Attendance", "Generate Low Attendance List", "View Student Attendance", "Remove Student"])

    if menu_choice == "Add Student":
        st.header("Add Student")
        roll_number = st.text_input("Roll Number")
        name = st.text_input("Name")
        email = st.text_input("Email")
        department = st.text_input("Department")
        year = st.number_input("Year", min_value=1, max_value=5)
        contact_number = st.text_input("Contact Number")
        update_student = st.checkbox("Update Student Information")
        if update_student:
            if st.button("Update"):
                add_or_update_student(roll_number, name, email, department, year, contact_number)

    elif menu_choice == "Record Attendance":
        st.header("Record Attendance")
        class_id = st.text_input("Class ID")
        student_id = st.text_input("Student ID")
        attendance_status = st.selectbox("Attendance Status", ["Present", "Absent", "Late"])
        remarks = st.text_input("Remarks (optional)")
        if st.button("Record"):
            record_attendance(class_id, student_id, attendance_status, remarks)

    elif menu_choice ==("Generate Low Attendance List"):
        st.header("Generate Low Attendance List")
        if st.button("Generate"):
            df = fetch_data_as_dataframe()
            if df is not None and not df.empty:
                st.dataframe(df)
                st.download_button(
                    label="Download Excel",
                    data=df.to_csv().encode(),
                    file_name="low_attendance_list.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data found for students with low attendance.")

    elif menu_choice == "View Student Attendance":
        st.header("View Student Attendance")
        df = fetch_student_attendance_data()
        if df is not None and not df.empty:
            st.dataframe(df)
        else:
            st.warning("No data found for student attendance.")

    elif menu_choice == "Remove Student":
        st.header("Remove Student")
        roll_number_to_remove = st.text_input("Enter Roll Number of Student to Remove")
        if st.button("Remove"):
            remove_student(roll_number_to_remove)

if __name__ == "__main__":
    main()
