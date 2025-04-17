from tkinter import *
import tkinter.messagebox as messagebox

# Create the main window
window = Tk()
window.title("Login")
window.geometry("300x200")  # Set window size

# Create labels and entry fields
username_label = Label(window, text="Username:")
username_label.grid(row=0, column=0)
username_entry = Entry(window)
username_entry.grid(row=0, column=1)

password_label = Label(window, text="Password:")
password_label.grid(row=1, column=0)
password_entry = Entry(window, show="*")
password_entry.grid(row=1, column=1)

# Variable to track login attempts
login_attempts = 0

def check_credentials():
    """Checks if the entered username and password are valid."""
    global login_attempts
    username = username_entry.get()
    password = password_entry.get()

    # Replace with your actual credentials for validation
    if username == "yash" and password == "1234":
        login_attempts = 0  # Reset attempts on successful login
        window.destroy()  # Close the login window
        # Open your main tkinter application here
        main_window = Tk()
        main_window.title("Main Application")
        # ... (Add your main application's GUI elements here) ...
        main_window.mainloop()
    else:
        login_attempts += 1
        if login_attempts >= 3:
            messagebox.showerror("Access Denied", "Too many failed login attempts.")
            window.destroy()  # Close the window after 3 failed attempts
        else:
            messagebox.showerror("Error", "Invalid username or password.")

login_button = Button(window, text="Login", command=check_credentials)
login_button.grid(row=2, columnspan=2)

window.mainloop()