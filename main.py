import os
import time
from datetime import datetime as dt

#Initilize the stock dictionary
stock_dic = {}

#HR related dictionaries
employees = {
    1: {"name": "Hamza", "password": "admin", "cnic": 3520234862403, "branch": "HDOF", "des": "HR"}
}
salary_dic = {
    1: {"name": "Hamza", "day": 6, "com": 0}
}
attendance_dic = {
}

#Read the stock file
def read_file_stock():
    with open("stock.txt", "r") as st_fl_dt:
        st_fl_dt_list = st_fl_dt.readlines()
        for st in st_fl_dt_list:
            stock = st.strip().split("|")
            if len(stock) > 0:
                stock_dic[stock[0]] = {'quantity': int(stock[1]), 'price': float(stock[2])}

#Read Salary File
def read_file_salary():
    with open("salary.txt", "r") as rfs:
        rfs_list = rfs.readlines()
        for sl in rfs_list:
            salary = sl.strip().split("|")
            if len(salary) >= 4:
                salary_dic[int(salary[0])] = {'name': (salary[1]), 'day': int(salary[2]), 'com': int(salary[3])}

#Read Attendance File
def read_file_attendance():
    with open("attendance.txt", "r") as rfa:
        rfa_list = rfa.readlines()
        for rfa_line in rfa_list:
            attend = rfa_line.strip().strip("|")
            if len(attend) > 0:
                attendance_dic[attend[0]] = {'date': (attend[1])}

#Update Attendance File
def update_file_attendance():
    with open("attendance.txt", "w") as ufa:
        for att, details in attendance_dic.items():
            ufa.write(f"{att}|{details['date']}")

#Update stock file
def update_file():
    with open("stock.txt", "w") as uf:
        for product, details in stock_dic.items():
            uf.write(f"{product}|{details['quantity']}|{details['price']}\n")

#Update the salary file
def update_file_salary():
    with open("salary.txt", "w") as ufs:
        for emp, details in salary_dic.items():
            ufs.write(f"{emp}|{details['name']}|{details['day']}|{details['com']}\n")


#Funtion to clear terminal and 1 second delay
def clear_terminal():
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')

#Login function
def login():
    while True:
        uilgun = int(input("Enter your username: "))
        uilgpw = input("Enter your password: ")
        if uilgun in employees and uilgpw == employees[uilgun]["password"]:
            clear_terminal()
            salary_dic[uilgun]['day'] += 1
            update_file_salary()
            update_file_attendance()
            main_menu(uilgun)
            return uilgun
        else:
            print("Invalid Credentials")
            clear_terminal()

#Logout function
def logout():
    print("Logged Out")
    print("Login again to continue")
    login()

#POS Terminal function
def pos_terminal(uilgun):
    print(f"Welcome {employees[uilgun]['name']} to POS Terminal")
    popnm = input("Product: ")
    if popnm in stock_dic:
        if stock_dic[popnm]["quantity"] > 0:
            popqu = int(input("Quantity: "))
            print(f"Total is {popqu * stock_dic[popnm]['price']}")
            stock_dic[popnm]["quantity"] -= popqu
            salary_dic[uilgun]['com'] += popqu/10
            update_file_salary()
            update_file()
        else:
            clear_terminal()
            print("Desired product is out of stock")
    else:
        clear_terminal()
        print("Desired product unavailable")
        pos_terminal(uilgun)
    another = input("Would you like to buy anything else(yes/no)? ")
    if another.lower() == "yes":
        pos_terminal(uilgun)
    else:
        clear_terminal()
        main_menu(uilgun)

#Stock Management function
def st_mg(uilgun):
    print(f"Welcome {employees[uilgun]["name"]} to Stock Management")
    print("1. View Products")
    print("2. Add New Product")
    print("3. Edit Product Name")
    print("4. Edit Product Price")
    print("5. Edit Product Quantity")
    print("6. Exit")
    try:
        uistgmm = int(input("Select your desired operation: "))
    except ValueError:
        print("You selected wrong")
        uistgmm = None
    finally:
        if uistgmm == 1:
            clear_terminal()
            print("Available Products:")
            for index, product_name in enumerate(stock_dic.keys(), start=1):
                print(f"{index}. {product_name}")
            go_back = int(input("Press 1 to go back: "))
            if go_back == 1:
                st_mg(uilgun)
            else:
                ("Wrong Decision")
        elif uistgmm == 2:
            clear_terminal()
            print("You selected Add new Product.")
            uistgmmna = input("Enter Product name you want to add: ")
            uistgmmnqa = int(input("Enter quantity: "))
            uistgmmnpa = float(input("Enter its price: "))
            if uistgmmna not in stock_dic:
                stock_dic[uistgmmna] = {"quantity": uistgmmnqa, "price": uistgmmnpa}
                update_file()
                st_mg(uilgun)
            else:
                print("Product already exist!")
                st_mg(uilgun)
        elif uistgmm == 3:
            clear_terminal()
            print("You selected Edit Product Name.")
            uistgmmnm = input("Enter Product name you want to edit: ")
            if uistgmmnm in stock_dic:
                uistgmmnmcd = input("Enter New Name: ")
                stock_dic[uistgmmnmcd] = stock_dic.pop(uistgmmnm)
                print(f"{uistgmmnm} changed to {uistgmmnmcd}")
                update_file()
                st_mg(uilgun)
            else:
                print("Entered product not found")
                st_mg(uilgun)
        elif uistgmm == 4:
            clear_terminal()
            print("You selected Edit Product Price.")
            uistgmmnm = input("Enter Product name you want to edit: ")
            if uistgmmnm in stock_dic:
                uistgmmnmcd = float(input("Enter New Price: "))
                stock_dic[uistgmmnm]["price"] = uistgmmnmcd
                print(f"{uistgmmnm} price changed to {uistgmmnmcd}")
                update_file()
                st_mg(uilgun)
            else:
                print("You entered wrong product")
                st_mg(uilgun)
        elif uistgmm == 5:
            clear_terminal()
            print("You selected Edit Product Quantity.")
            uistgmmnm = input("Enter Product name you want to edit: ")
            if uistgmmnm in stock_dic:
                uistgmmnmcd = int(input("Enter Quantity: "))
                stock_dic[uistgmmnm]["quantity"] = uistgmmnmcd
                print(f"{uistgmmnm} quantity changed to {uistgmmnmcd}")
                update_file()
                st_mg(uilgun)
            else:
                print("Product not found")
                st_mg(uilgun)
        elif uistgmm == 6:
            clear_terminal()
            main_menu(uilgun)
        else:
            print("Invalid option selected.")

#HR Salary function
def hr_salary(uilgun):
    if employees[uilgun]["des"] in ["admin", "HR"]:
        print(f"Welcome {employees[uilgun]["name"]} to HR")
        print("1. View All Branches")
        print("2. View All Staff")
        print("3. Check Salaries")
        print("4. Manage Staff")
        print("5. Manage Branches")
        print("6. Exit HR")
        try:
            uihr = int(input("Select your operation: "))
        except ValueError:
            print("Please select bt 1-6")
        finally:
            if uihr == 1:
                print("Available Branches")
            elif uihr == 2:
                print("Available Staff")
            elif uihr == 3:
                print("Check salary")
                uihrsc = int(input("Enter staff id to check their salary: "))
                if uihrsc in salary_dic:
                    clear_terminal()
                    print(f"{salary_dic[uihrsc]['name']} salary of this month is {salary_dic[uihrsc]['day'] + salary_dic[uihrsc]['com']}rs")
            elif uihr == 4:
                print("Manage Staff")
            elif uihr == 5:
                print("Manage Branch")
            elif uihr == 6:
                main_menu(uilgun)
    else:
        print("You dont have acces to HR Menu")
        print("Exiting to main menu...")
        clear_terminal()
        main_menu(uilgun)

#Main Menu function
def main_menu(uilgun):
    print(f"Welcome {employees[uilgun]["name"]} have a great day!")
    print("1. POS Terminal")
    print("2. Stock Management")
    print("3. HR Salary")
    print("4. Logout")
    try:
        uimm = int(input("Select your operation: "))
    except ValueError:
        print("Please Select bt 1-4")
        uimm = None
    finally:
        if uimm == 1:
            clear_terminal()
            pos_terminal(uilgun)
        elif uimm == 2:
            clear_terminal()
            st_mg(uilgun)
        elif uimm == 3:
            clear_terminal()
            hr_salary(uilgun)
        elif uimm == 4:
            clear_terminal()
            logout()
        else:
            print("Invalid selection, please choose a number between 1 and 4.")
            main_menu(uilgun)
login()
