import tkinter as tk
from tkinter import messagebox
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Ensure the CSV file exists
file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'student.csv')

if not os.path.exists(file_name):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["studentid", "student name", "module", "module id", "gender", "cw1", "cw2", "cw3"])

# Function to add student details to CSV
def add_student():
    name = name_var.get()
    module = module_var.get()
    module_id = module_id_var.get()
    gender = gender_var.get()
    cw1 = cw1_var.get()
    cw2 = cw2_var.get()
    cw3 = cw3_var.get()

    if all([name, module, module_id, gender, cw1, cw2, cw3]):
        with open(file_name, mode='a+', newline='') as file:
            writer = csv.writer(file)
            with open(file_name, mode='r') as read_file:
                reader = csv.reader(read_file)
                rows = list(reader)
                new_id = len(rows)  # Automatically generate studentid
            writer.writerow([new_id, name, module, module_id, gender, cw1, cw2, cw3])
        display_recent_entries()
        clear_form()
        messagebox.showinfo("Success", "Student added successfully!")
    else:
        messagebox.showerror("Input Error", "All fields are required")

# Function to display the 10 most recent entries
def display_recent_entries():
    for widget in record_frame.winfo_children():
        widget.destroy()

    headers = ["Student ID", "Student Name", "Module", "Module ID", "Gender", "CW1", "CW2", "CW3"]
    for i, header in enumerate(headers):
        tk.Label(record_frame, text=header, font=("Arial", 10, "bold")).grid(row=0, column=i)

    if os.path.exists(file_name):
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)[1:]  # Skip the header
            recent_rows = rows[-10:]
            for i, row in enumerate(recent_rows):
                for j, value in enumerate(row):
                    tk.Label(record_frame, text=value).grid(row=i + 1, column=j)

# Function to delete a student by studentid
def delete_student():
    student_id = delete_id_var.get()

    if not student_id.isdigit():
        messagebox.showerror("Error", "Please enter a valid Student ID.")
        return

    updated_rows = []
    deleted = False

    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)

        for row in rows:
            if row[0] == student_id:
                deleted = True
            else:
                updated_rows.append(row)

    if deleted:
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)
        display_recent_entries()
        messagebox.showinfo("Success", f"Student with ID {student_id} deleted.")
    else:
        messagebox.showerror("Error", f"No student found with ID {student_id}.")

# Function to update a student by studentid
def update_student():
    student_id = update_id_var.get()

    if not student_id.isdigit():
        messagebox.showerror("Error", "Please enter a valid Student ID.")
        return

    updated_rows = []
    updated = False

    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)

        for row in rows:
            if row[0] == student_id:
                updated = True
                row[1] = name_var.get()
                row[2] = module_var.get()
                row[3] = module_id_var.get()
                row[4] = gender_var.get()
                row[5] = cw1_var.get()
                row[6] = cw2_var.get()
                row[7] = cw3_var.get()
            updated_rows.append(row)

    if updated:
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)
        display_recent_entries()
        clear_form()
        messagebox.showinfo("Success", f"Student with ID {student_id} updated.")
    else:
        messagebox.showerror("Error", f"No student found with ID {student_id}.")

# Function to clear form fields
def clear_form():
    name_var.set("")
    module_var.set("")
    module_id_var.set("")
    gender_var.set(None)
    cw1_var.set("")
    cw2_var.set("")
    cw3_var.set("")

# Function to visualize CW1, CW2, CW3 data using a bar chart
def visualize_data():
    if os.path.exists(file_name):
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)[1:]  # Skip header

            cw1_values = [int(row[5]) for row in rows]
            cw2_values = [int(row[6]) for row in rows]
            cw3_values = [int(row[7]) for row in rows]

            # Create a bar chart
            labels = ['CW1', 'CW2', 'CW3']
            cw1_avg = sum(cw1_values) / len(cw1_values) if cw1_values else 0
            cw2_avg = sum(cw2_values) / len(cw2_values) if cw2_values else 0
            cw3_avg = sum(cw3_values) / len(cw3_values) if cw3_values else 0
            averages = [cw1_avg, cw2_avg, cw3_avg]

            fig, ax = plt.subplots()
            ax.bar(labels, averages, color=['blue', 'green', 'red'])
            ax.set_title('Average CW Scores')
            ax.set_ylabel('Average Score')

            # Embed the plot in Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=my_w)
            canvas.draw()
            canvas.get_tk_widget().grid(row=7, column=0, columnspan=6, pady=20)
    else:
        messagebox.showerror("Error", "No student data available to visualize.")

# Tkinter window setup
my_w = tk.Tk()
my_w.title("Student Management System")
my_w.geometry("800x600")

# Form variables
name_var = tk.StringVar()
module_var = tk.StringVar()
module_id_var = tk.StringVar()
gender_var = tk.StringVar(value=None)
cw1_var = tk.StringVar()
cw2_var = tk.StringVar()
cw3_var = tk.StringVar()
delete_id_var = tk.StringVar()
update_id_var = tk.StringVar()

# Form layout
tk.Label(my_w, text="Student Name").grid(row=0, column=0, padx=5, pady=10)
tk.Entry(my_w, textvariable=name_var).grid(row=0, column=1, padx=5, pady=10)

tk.Label(my_w, text="Module").grid(row=0, column=2, padx=5, pady=10)
tk.Entry(my_w, textvariable=module_var).grid(row=0, column=3, padx=5, pady=10)

tk.Label(my_w, text="Module ID").grid(row=0, column=4, padx=5, pady=10)
tk.Entry(my_w, textvariable=module_id_var).grid(row=0, column=5, padx=5, pady=10)

tk.Label(my_w, text="Gender").grid(row=1, column=0, padx=5, pady=10)
tk.Radiobutton(my_w, text="Male", variable=gender_var, value="Male").grid(row=1, column=1, padx=5, pady=10)
tk.Radiobutton(my_w, text="Female", variable=gender_var, value="Female").grid(row=1, column=2, padx=5, pady=10)
tk.Radiobutton(my_w, text="Others", variable=gender_var, value="Others").grid(row=1, column=3, padx=5, pady=10)

tk.Label(my_w, text="CW1").grid(row=2, column=0, padx=5, pady=10)
tk.Entry(my_w, textvariable=cw1_var, width=5).grid(row=2, column=1, padx=5, pady=10)

tk.Label(my_w, text="CW2").grid(row=2, column=2, padx=5, pady=10)
tk.Entry(my_w, textvariable=cw2_var, width=5).grid(row=2, column=3, padx=5, pady=10)

tk.Label(my_w, text="CW3").grid(row=2, column=4, padx=5, pady=10)
tk.Entry(my_w, textvariable=cw3_var, width=5).grid(row=2, column=5, padx=5, pady=10)

# Buttons for Add, Delete, Update, and Visualization
tk.Button(my_w, text="Add Student", command=add_student).grid(row=3, column=0, columnspan=6, pady=10)

tk.Label(my_w, text="Delete by ID").grid(row=4, column=0, padx=5, pady=10)
tk.Entry(my_w, textvariable=delete_id_var).grid(row=4, column=1, padx=5, pady=10)
tk.Button(my_w, text="Delete Student", command=delete_student).grid(row=4, column=2, columnspan=2, pady=10)

tk.Label(my_w, text="Update by ID").grid(row=5, column=0, padx=5, pady=10)
tk.Entry(my_w, textvariable=update_id_var).grid(row=5, column=1, padx=5, pady=10)
tk.Button(my_w, text="Update Student", command=update_student).grid(row=5, column=2, columnspan=2, pady=10)

# Add a button for visualization
tk.Button(my_w, text="Visualize Data", command=visualize_data).grid(row=6, column=0, columnspan=6, pady=10)

# Frame to display recent records
record_frame = tk.Frame(my_w)
record_frame.grid(row=7, column=0, columnspan=6, pady=10)

# Initially display recent entries
display_recent_entries()

# Run the main loop
my_w.mainloop()
