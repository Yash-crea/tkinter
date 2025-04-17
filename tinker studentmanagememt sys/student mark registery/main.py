import sqlite3
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox


# Database Setup
def setup_database():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            module TEXT,
            module_id TEXT,
            date_of_entry TEXT,
            gender TEXT,
            cw1 REAL,
            cw2 REAL,
            cw3 REAL
        )
    ''')
    conn.commit()
    conn.close()


# Login Window
def login_window():
    def check_credentials():
        username = username_entry.get()
        password = password_entry.get()
        if username == "admin" and password == "1234":
            messagebox.showinfo("Login Successful", "Welcome to the Student Management System!")
            window.destroy()
            main_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    window = Tk()
    window.title("Login")
    window.geometry("300x150")

    Label(window, text="Username:").grid(row=0, column=0, pady=10, padx=10)
    username_entry = Entry(window)
    username_entry.grid(row=0, column=1)

    Label(window, text="Password:").grid(row=1, column=0, pady=10, padx=10)
    password_entry = Entry(window, show="*")
    password_entry.grid(row=1, column=1)

    Button(window, text="Login", command=check_credentials).grid(row=2, columnspan=2, pady=10)
    window.mainloop()


# Function to visualize student marks
def visualize_marks():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, cw1, cw2, cw3 FROM students")
    data = cursor.fetchall()
    conn.close()

    if not data:
        messagebox.showinfo("No Data", "No students' data available for visualization.")
        return

    # Prepare data for plotting
    names = [entry[0] for entry in data]
    cw1_marks = [entry[1] for entry in data]
    cw2_marks = [entry[2] for entry in data]
    cw3_marks = [entry[3] for entry in data]

    # Create bar chart
    x = range(len(names))
    plt.figure(figsize=(10, 6))
    plt.bar(x, cw1_marks, width=0.2, label='CW1', align='center')
    plt.bar(x, cw2_marks, width=0.2, label='CW2', align='edge')
    plt.bar(x, cw3_marks, width=0.2, label='CW3', align='edge')

    plt.xticks(x, names, rotation=45)
    plt.xlabel('Student Name')
    plt.ylabel('Marks')
    plt.title('Student Marks for CW1, CW2, CW3')
    plt.legend()

    plt.tight_layout()
    plt.show()


# Main Application Window
def main_window():
    def clear_screen():
        for widget in frame_main.winfo_children():
            widget.destroy()

    def add_student():
        clear_screen()

        Label(frame_main, text="First Name:").grid(row=0, column=0, pady=5, padx=5)
        first_name_entry = Entry(frame_main)
        first_name_entry.grid(row=0, column=1, pady=5, padx=5)

        Label(frame_main, text="Last Name:").grid(row=1, column=0, pady=5, padx=5)
        last_name_entry = Entry(frame_main)
        last_name_entry.grid(row=1, column=1, pady=5, padx=5)

        Label(frame_main, text="Module:").grid(row=2, column=0, pady=5, padx=5)
        module_entry = Entry(frame_main)
        module_entry.grid(row=2, column=1, pady=5, padx=5)

        Label(frame_main, text="Module ID:").grid(row=3, column=0, pady=5, padx=5)
        module_id_entry = Entry(frame_main)
        module_id_entry.grid(row=3, column=1, pady=5, padx=5)

        Label(frame_main, text="Date of Entry:").grid(row=4, column=0, pady=5, padx=5)
        date_of_entry_entry = Entry(frame_main)
        date_of_entry_entry.grid(row=4, column=1, pady=5, padx=5)

        Label(frame_main, text="Gender:").grid(row=5, column=0, pady=5, padx=5)
        gender_var = StringVar(value="None")  # Default value
        Radiobutton(frame_main, text="Male", variable=gender_var, value="Male").grid(row=5, column=1, sticky=W)
        Radiobutton(frame_main, text="Female", variable=gender_var, value="Female").grid(row=5, column=2, sticky=W)

        Label(frame_main, text="CW1:").grid(row=6, column=0, pady=5, padx=5)
        cw1_entry = Entry(frame_main)
        cw1_entry.grid(row=6, column=1, pady=5, padx=5)

        Label(frame_main, text="CW2:").grid(row=7, column=0, pady=5, padx=5)
        cw2_entry = Entry(frame_main)
        cw2_entry.grid(row=7, column=1, pady=5, padx=5)

        Label(frame_main, text="CW3:").grid(row=8, column=0, pady=5, padx=5)
        cw3_entry = Entry(frame_main)
        cw3_entry.grid(row=8, column=1, pady=5, padx=5)

        def save_student():
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO students (first_name, last_name, module, module_id, date_of_entry, gender, cw1, cw2, cw3)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                first_name_entry.get(), last_name_entry.get(), module_entry.get(),
                module_id_entry.get(), date_of_entry_entry.get(), gender_var.get(),
                cw1_entry.get(), cw2_entry.get(), cw3_entry.get()
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student added successfully!")
            clear_screen()

        Button(frame_main, text="Save", command=save_student).grid(row=9, columnspan=2, pady=10)

    def update_marks():
        clear_screen()

        Label(frame_main, text="Student ID:").grid(row=0, column=0, pady=5, padx=5)
        student_id_entry = Entry(frame_main)
        student_id_entry.grid(row=0, column=1, pady=5, padx=5)

        Label(frame_main, text="CW1:").grid(row=1, column=0, pady=5, padx=5)
        cw1_entry = Entry(frame_main)
        cw1_entry.grid(row=1, column=1, pady=5, padx=5)

        Label(frame_main, text="CW2:").grid(row=2, column=0, pady=5, padx=5)
        cw2_entry = Entry(frame_main)
        cw2_entry.grid(row=2, column=1, pady=5, padx=5)

        Label(frame_main, text="CW3:").grid(row=3, column=0, pady=5, padx=5)
        cw3_entry = Entry(frame_main)
        cw3_entry.grid(row=3, column=1, pady=5, padx=5)

        def save_marks():
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE students
                SET cw1 = ?, cw2 = ?, cw3 = ?
                WHERE student_id = ?
            ''', (cw1_entry.get(), cw2_entry.get(), cw3_entry.get(), student_id_entry.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Marks updated successfully!")
            clear_screen()

        Button(frame_main, text="Update Marks", command=save_marks).grid(row=4, columnspan=2, pady=10)

    def delete_student():
        clear_screen()

        Label(frame_main, text="Student ID:").grid(row=0, column=0, pady=5, padx=5)
        student_id_entry = Entry(frame_main)
        student_id_entry.grid(row=0, column=1, pady=5, padx=5)

        def delete():
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM students WHERE student_id = ?
            ''', (student_id_entry.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student deleted successfully!")
            clear_screen()

        Button(frame_main, text="Delete", command=delete).grid(row=1, columnspan=2, pady=10)

    def view_students():
        clear_screen()

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        conn.close()

        text = Text(frame_main)
        for row in rows:
            text.insert(END, f"{row}\n")
        text.pack(fill=BOTH, expand=1)

    root = Tk()
    root.title("Student Management System")
    root.geometry("800x600")

    frame_menu = Frame(root, width=800, height=100)
    frame_menu.pack(side=TOP, fill=X)

    Button(frame_menu, text="Add Student", command=add_student).pack(side=LEFT, padx=10, pady=10)
    Button(frame_menu, text="Update Marks", command=update_marks).pack(side=LEFT, padx=10, pady=10)
    Button(frame_menu, text="Delete Student", command=delete_student).pack(side=LEFT, padx=10, pady=10)
    Button(frame_menu, text="View Students", command=view_students).pack(side=LEFT, padx=10, pady=10)
    Button(frame_menu, text="Visualize Marks", command=visualize_marks).pack(side=LEFT, padx=10, pady=10)

    frame_main = Frame(root, width=800, height=500)
    frame_main.pack(side=TOP, fill=BOTH, expand=1)

    root.mainloop()


# Initialize the database and show login window
setup_database()
login_window()
