import sqlite3
import tkinter as tk
from tkinter import messagebox
import hashlib


def addTestData():
    # Add data to table
    username = 'User2'
    password = 'password2'
    passwordHash = hash(password)

    cursor.execute('''
            INSERT INTO users (username, passHash)
            VALUES (?, ?)
        ''', (username, passwordHash))
    
def login(id):

    turretLevels = [
        {'name' : 'basicTurret', 'damageLevel': '', 'ROFLevel': '', 'rangeLevel': ''},
		{'name' : 'machineGun',  'damageLevel': '', 'ROFLevel': '', 'rangeLevel': ''},
		{'name': 'bombTower',  'damageLevel': '', 'ROFLevel': '', 'rangeLevel': ''},
		{'name': 'megaShot',  'damageLevel': '', 'ROFLevel': '', 'rangeLevel': ''}
    ]

    for tower in turretLevels:
        # Creates the query
        query = f"SELECT {tower['name']} FROM Users WHERE id = ?"
        # Executes the query
        cursor.execute(query, (id,))
        # Stores the result of the query
        result = cursor.fetchone()

        # Splits the results up to store the individual towers and levels
        if result and result[0]:
            # Split the string by '-'
            levels = result[0].split('-')
            # Ensure it has the expected number of parts
            if len(levels) == 3:
                tower['damageLevel'] = int(levels[0])
                tower['ROFLevel'] = int(levels[1])
                tower['rangeLevel'] = int(levels[2])


    # Creates query to get tokens
    cursor.execute('SELECT tokens FROM Users WHERE id = ?', (id,))
    
    # Executes query and stores result
    tokens = cursor.fetchone()

    
    # Returns the turret levels, tokens and the user id - for further changes to database
    return turretLevels, tokens[0], id


def saveData(id, tokens, turretLevels):
    # Establish connection to the database
    connection = sqlite3.connect('Login.db')

    # Create a cursor object to execute SQL commands
    cursor = connection.cursor()


    # Update tokens
    cursor.execute('UPDATE Users SET tokens = ? WHERE id = ?', (tokens, id))
    
    # Update turret levels
    for tower in turretLevels:
        # Combine levels into a single string (X-X-X as per database format)
        levelsString = f"{tower['damageLevel']}-{tower['ROFLevel']}-{tower['rangeLevel']}"

        # Update the respective tower column in the database
        query = f"UPDATE Users SET {tower['name']} = ? WHERE id = ?"
        cursor.execute(query, (levelsString, id))

    # Commit changes
    connection.commit()
    
    # Close the connection and save the database
    connection.close()



def hash(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def submitAction():
    global username_entry, password_entry, turretLevels, DBValues
    username = username_entry.get()
    passwordHash = hash(password_entry.get())
    cursor.execute('SELECT passHash, id FROM Users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if result:
        storedHash = result[0]
        if passwordHash == storedHash:
            messagebox.showinfo('Login success', 'Welcome '+ username)
            DBValues = login(result[1])
            root.destroy()
            
            

        else:
            messagebox.showerror("Login Failed", "Incorrect password.")
    else:
        messagebox.showerror("Login Failed", "Username not found.")


def registerWindowProcedure():
    # Create registration window with text boxes and buttons
    global registerWindow, regUsernameEntry, regPasswordEntry

    registerWindow = tk.Toplevel(root)
    registerWindow.title("Register")
    registerWindow.geometry("300x200")

    reg_username_label = tk.Label(registerWindow, text = "Username:")
    reg_username_label.pack(pady = (20, 5))
    regUsernameEntry = tk.Entry(registerWindow, width = 30)
    regUsernameEntry.pack(pady = (0, 10))

    reg_password_label = tk.Label(registerWindow, text = "Password:")
    reg_password_label.pack(pady = (10, 5))
    regPasswordEntry = tk.Entry(registerWindow, show = "*", width = 30)
    regPasswordEntry.pack(pady = (0, 10))

    reg_submit_button = tk.Button(registerWindow, text = "Register", command = registerAction)
    reg_submit_button.pack(pady = (10, 20))

def registerAction():
    global registerWindow, regUsernameEntry, regPasswordEntry, DBValues

    username = regUsernameEntry.get()
    password = regPasswordEntry.get()

    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty.")
        return
    
    if not validUsername(username):
        return

    if not validPassword(password):
        return
        

    # Hash the password
    passwordHash = hash(password)

    # Check if username exists
    cursor.execute('SELECT username FROM Users WHERE username = ?', (username,))
    if cursor.fetchone():
        messagebox.showerror("Error", "Username already exists.")
        return

    # Insert new user into the database with username and password hash
    try:
        cursor.execute('''INSERT INTO Users (username, passHash)
            VALUES (?, ?)''', (username, passwordHash))
        # Save to database
        connection.commit()
        # Display success message
        messagebox.showinfo("Success", "Account registered successfully!")
        # Close registration window
        registerWindow.destroy()
        root.destroy()


    # If inserting fails, display error
    except Exception as e:
        messagebox.showerror("Error", f"Registration failed: {e}")


        cursor.execute('SELECT id FROM Users WHERE username = ?', (username,))
        result = cursor.fetchone()
        
        DBValues = login(result[0])

def validUsername(username):
    # Check username length
    if len(username) < 6:
        return False
    
    # Loops through all characters in username
    for char in username:
        # Check if the character is alphanumeric
        if not (char.isalnum()):
            # Output error
            messagebox.showerror("Error", "Username can only contain letters and numbers")
            return False
        
    return True


def validPassword(password):
    # Checks password length
    if len(password) < 6:
        messagebox.showerror("Error", "Password too short")
        return False

    # Checks password characters
    hasLowercase = False
    hasUppercase = False
    hasNumber = False
    hasSpecial = False
    specialChar = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"

    # Loop through all characters
    for char in password:
        # Check for lowercase
        if char.islower():
            hasLowercase = True
        # Check for uppercase            
        elif char.isupper():
            hasUppercase = True
        # Check for digits
        elif char.isdigit():
            hasNumber = True
        # Check for special characters
        elif char in specialChar:
            hasSpecial = True

        # Early exit if all conditions are met
        if hasLowercase and hasUppercase and hasNumber and hasSpecial:
            return True
    
    # Output suitable message depending on lack of character(s) and return False

    if not hasLowercase:
        messagebox.showerror("Error", "Password must contain lowercase character(s)")
        return False

    if not hasUppercase:
        messagebox.showerror("Error", "Password must contain uppercase character(s)")
        return False


    if not hasNumber:
        messagebox.showerror("Error", "Password must contain number(s)")
        return False


    if not hasSpecial:
        messagebox.showerror("Error", "Password must contain special character(s)\nSuch as: !@#$%")
        return False
        


# Establish connection to the database
connection = sqlite3.connect('Login.db')

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

# Create the main window
root = tk.Tk()
root.title("Login Screen")

# Set window size and center it on the screen
window_width, window_height = 300, 250
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int((screen_height - window_height) / 2)
position_right = int((screen_width - window_width) / 2)
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# Create and place the username label and entry
username_label = tk.Label(root, text = "Username:")
username_label.pack(pady = (20, 5))
username_entry = tk.Entry(root, width = 30)
username_entry.pack(pady = (0, 10))

# Create and place the password label and entry
password_label = tk.Label(root, text = "Password:")
password_label.pack(pady = (10, 5))
password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack(pady = (0, 10))

# Create and place the submit button
submit_button = tk.Button(root, text="Submit", command = submitAction)
submit_button.pack(pady = (10, 20))

# Create and place the register button
register_button = tk.Button(root, text="Register account", command = registerWindowProcedure)
register_button.pack(pady=(5, 10))

# Start the Tkinter event loop
turretLevels = root.mainloop()


# Commit changes and close the connection
connection.commit()
connection.close()