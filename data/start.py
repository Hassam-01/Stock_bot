import csv
import os

# Get the directory of the current script
current_dir = os.path.dirname(__file__)

# File to store user data
USER_DATA_FILE = os.path.join(current_dir, "user_data.csv")

# Ensure the CSV file exists
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "ID", "InitialDeposit", "StocksOwned"])

def register_user():
    """Registers a new user by taking their details and writing to the CSV."""
    username = input("Enter your username: ")
    user_id = input("Enter your ID: ")
    
    # Check for duplicate ID
    with open(USER_DATA_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["ID"] == user_id:
                print("A user with this ID already exists. Please use a different ID.")
                return
    while True:
        try:
            initial_deposit = float(input("Enter your initial deposit amount: "))
            break
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
    
    with open(USER_DATA_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, user_id, initial_deposit, 0])
    print("Registration successful!")

def login_user():
    """Logs in a user by verifying their username and ID."""
    username = input("Enter your username: ")
    user_id = input("Enter your ID: ")
    with open(USER_DATA_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Username"] == username and row["ID"] == user_id:
                print("Login successful!")
                return {
                    "username": username,
                    "id": user_id,
                    "deposit": float(row["InitialDeposit"]),
                    "stocks_owned": int(row["StocksOwned"])
                }
    print("Login failed! Please check your credentials.")
    return None

def update_user_data(user_data):
    """Updates the CSV file with modified user data."""
    rows = []
    with open(USER_DATA_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Username"] == user_data["username"] and row["ID"] == user_data["id"]:
                row["InitialDeposit"] = str(user_data["deposit"])
                row["StocksOwned"] = str(user_data["stocks_owned"])
            rows.append(row)
    
    with open(USER_DATA_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Username", "ID", "InitialDeposit", "StocksOwned"])
        writer.writeheader()
        writer.writerows(rows)

def validateUser():
    """Main program loop."""
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            register_user()
        elif choice == "2":
            user_data = login_user()
            if user_data:
                return True
        elif choice == "3":
            print("Exiting program.")
            print("Thank you for using the trading bot!")
            exit()
            break
        else:
            print("Invalid choice. Please try again.")
