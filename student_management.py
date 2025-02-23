import sqlite3
import streamlit as st
import pandas as pd

# Database connection
def connect_db():
    conn = sqlite3.connect('students.db')
    return conn

# Initialize the database
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            grade TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Add a new student
def add_student(name, age, grade):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (name, age, grade)
        VALUES (?, ?, ?)
    ''', (name, age, grade))
    conn.commit()
    conn.close()

# Get all students
def get_students():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Delete a student by ID
def delete_student(student_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()

# Streamlit app
def main():
    st.title("Student Management System")

    menu = ["Add Student", "View Students", "Delete Student"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Student":
        st.subheader("Add Student")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=100)
        grade = st.text_input("Grade")
        if st.button("Add"):
            add_student(name, age, grade)
            st.success(f"Student {name} added successfully!")

    elif choice == "View Students":
        st.subheader("View Students")
        students = get_students()
        df = pd.DataFrame(students, columns=["ID", "Name", "Age", "Grade"])
        st.dataframe(df)

    elif choice == "Delete Student":
        st.subheader("Delete Student")
        student_id = st.number_input("Student ID", min_value=1)
        if st.button("Delete"):
            delete_student(student_id)
            st.success(f"Student with ID {student_id} deleted successfully!")

if __name__ == '__main__':
    init_db()
    main()