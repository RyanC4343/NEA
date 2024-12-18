import sqlite3
import tkinter as tk
from tkinter import messagebox
import hashlib


# Establish connection to the database
connection = sqlite3.connect('Login.db')

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

def addTestData():
    # Add data to table
    username = 'User2'
    password = 'password2'
    passwordHash = hash(password)

    cursor.execute('''
            INSERT INTO users (username, passHash)
            VALUES (?, ?)
        ''', (username, passwordHash))

# Login system UI

def hash(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def submitAction():
    username = username_entry.get()
    passwordHash = hash(password_entry.get())
    cursor.execute('SELECT passHash FROM Users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if result:
        storedHash = result[0]
        if passwordHash == storedHash:
            messagebox.showinfo('Login success', 'Welcome '+ username)
            login()

        else:
            messagebox.showerror("Login Failed", "Incorrect password.")
    else:
        messagebox.showerror("Login Failed", "Username not found.")


# Create the main window
root = tk.Tk()
root.title("Login Screen")

# Set window size and center it on the screen
window_width, window_height = 300, 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int((screen_height - window_height) / 2)
position_right = int((screen_width - window_width) / 2)
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# Create and place the username label and entry
username_label = tk.Label(root, text = "Username:")
username_label.pack(pady = (20, 5))
username_entry = tk.Entry(root, width = 30)
username_entry.pack(pady=(0, 10))

# Create and place the password label and entry
password_label = tk.Label(root, text="Password:")
password_label.pack(pady=(10, 5))
password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack(pady=(0, 10))

# Create and place the submit button
submit_button = tk.Button(root, text="Submit", command=submitAction)
submit_button.pack(pady=(10, 20))

# Start the Tkinter event loop
root.mainloop()

def addTestData():
    # Add data to table
    username = 'User2'
    password = 'password2'
    passwordHash = hash(password)

    cursor.execute('''
            INSERT INTO users (username, passHash)
            VALUES (?, ?)
        ''', (username, passwordHash))


# Commit changes and close the connection
connection.commit()
connection.close()