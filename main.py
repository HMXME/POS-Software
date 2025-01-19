import os
import time
from datetime import datetime as dt
today = dt.today().date()
formated_today = str(today.strftime("%y%m%d"))

#Admin related dictionaries
stock_dic = {}
employees = {}
salary_dic = {}
attendance_dic = {}

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
            username, date = rfa_line.strip().split("|")
            attendance_dic[int(username)] = {'date': date}

#Read Employees File
def read_file_employees():
    with open("employees.txt", "r") as rfe:
        rfe_list = rfe.readlines()
        for rfe_line in rfe_list:
            employee = rfe_line.strip().split("|")
            if len(employee) >= 5:
                employees[int(employee[0])] = {'name': employee[1], 'password': employee[2], 'cnic': int(employee[3]), 'branch': employee[4], 'des': employee[5]}

#Update Attendance File
def update_file_attendance():
    with open("attendance.txt", "w") as ufa:
        for username, details in attendance_dic.items():
            ufa.write(f"{username}|{details['date']}\n")

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

#Update the Employees file
def update_file_employees():
    with open("employees.txt", "w") as ufe:
        for emp, details in employees.items():
            ufe.write(f"{emp}|{details['name']}|{details['password']}|{details['cnic']}|{details['branch']}|{details['des']}\n")


#Funtion to clear terminal and 1 second delay
def clear_terminal():
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')

#Login function
def login():
    while True:
        read_file_salary()
        read_file_attendance()
        read_file_stock()
        read_file_employees()
        uilgun = int(input("Enter your username: "))
        uilgpw = input("Enter your password: ")
        if uilgun in employees and uilgpw == employees[uilgun]["password"]:
            clear_terminal()
            if attendance_dic[uilgun]['date'] == formated_today:
                main_menu(uilgun)
                return(uilgun)
            else:
                attendance_dic[uilgun]['date'] = formated_today
                salary_dic[uilgun]['day'] += 1
                update_file_salary()
                update_file_employees()
                update_file()
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
    if employees[uilgun]["des"] in ["admin", "hr", "st_manager"]:
        print(f"Welcome {employees[uilgun]["name"]} to Stock Management")
        print("1. View Products")
        print("2. Add New Product")
        print("3. Delect a Product")
        print("4. Edit Product Name")
        print("5. Edit Product Price")
        print("6. Edit Product Quantity")
        print("7. Exit")
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
                print("You selected to delete a product.")
                uistgmmdp = input("Enter product name to delete: ")
                if uistgmmdp in stock_dic:
                    stock_dic.pop(uistgmmdp)
                    print(f"{uistgmmdp.capitalize()} deleted")
                    update_file()
                    clear_terminal()
                    st_mg(uilgun)
                else:
                    print("Product not found")
                    clear_terminal()
                    st_mg(uilgun)
            elif uistgmm == 4:
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
            elif uistgmm == 5:
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
            elif uistgmm == 6:
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
            elif uistgmm == 7:
                clear_terminal()
                main_menu(uilgun)
            else:
                print("Invalid option selected.")
    else:
        print("You dont have access to Stock Management")
        print("Exiting to main menu...")
        clear_terminal()
        main_menu(uilgun)

#HR Salary function
def hr_salary(uilgun):
    if employees[uilgun]["des"] in ["admin", "hr"]:
        print(f"Welcome {employees[uilgun]["name"]} to HR")
        print("1. View All Staff")
        print("2. Check Salaries")
        print("3. Manage Staff")
        print("4. Exit HR")
        try:
            uihr = int(input("Select your operation: "))
        except ValueError:
            print("Please select bt 1-6")
        finally:
            if uihr == 1:
                print("Available Staff")
                for index, staff in enumerate(employees, start=1):
                    print(f"{index}. {employees[staff]['name']}")
            elif uihr == 2:
                print("Check salary")
                uihrsc = int(input("Enter staff id to check their salary: "))
                if uihrsc in salary_dic:
                    clear_terminal()
                    print(f"{salary_dic[uihrsc]['name']} salary of this month is {salary_dic[uihrsc]['day'] + salary_dic[uihrsc]['com']}rs")
            elif uihr == 3:
                clear_terminal()
                print("Manage Staff.")
                try:
                    print("1. Add an Employee")
                    print("2. Delete an Employee")
                    print("3. Change CNIC")
                    print("4. Change Employee Branch")
                    print("5. Change Designation")
                    uihrms = int(input("Select your operation: "))
                except ValueError:
                    print("Invalid Selection")
                finally:
                    if uihrms == 1:
                        clear_terminal()
                        print("Add an Employee.")
                        last_emp_id = list(employees.keys())[-1]
                        uihrmsaeid = last_emp_id + 1
                        uihrmsaenm = input("Enter Employee Name: ").capitalize()
                        uihrmsaeps = input("Enter Employee Login Password: ")
                        uihrmsaecn = int(input("Enter CNIC number: "))
                        uihrmsaebr = input("Enter Employee Branch: ").upper()
                        uihrmsaeds = input("Enter Employee's Designation: ").lower()
                        print(f'{uihrmsaenm} having {uihrmsaecn} Added')
                        employees[int(uihrmsaeid)] = {'name': uihrmsaenm, 'password': uihrmsaeps, 'cnic': uihrmsaecn, 'branch': uihrmsaebr, 'des': uihrmsaeds}
                        attendance_dic[uihrmsaeid] = {'date': formated_today}
                        salary_dic[uihrmsaeid] = {'name': uihrmsaenm, 'day': 0, 'com': 0}
                        update_file_employees()
                        update_file_attendance()
                        update_file_salary()
                        clear_terminal()
                        hr_salary(uilgun)
                    elif uihrms == 2:
                        clear_terminal()
                        print("Delete an Employee")
                        uihrmsdenm = int(input("Enter Employee ID to delete: "))
                        if uihrmsdenm in employees:
                            print(f"{employees[uihrmsdenm]['name']} Deleted")
                            employees.pop(uihrmsdenm)
                            update_file_employees()
                            clear_terminal()
                            hr_salary(uilgun)
                        else:
                            print("Employee not found")
                            clear_terminal()
                            hr_salary(uilgun)
                    elif uihrms == 3:
                        clear_terminal()
                        print("Change CNIC of an Employee")
                        uihrmsccn = int(input("Enter Employee ID to change CNIC: "))
                        if uihrmsccn in employees:
                            uihrmscnc = int(input("Enter New CNIC: "))
                            employees[uihrmsccn]['cnic'] = uihrmscnc
                            print(f"{employees[uihrmsccn]['name']} CNIC changed to {uihrmscnc}")
                            update_file_employees()
                            clear_terminal()
                            hr_salary(uilgun)
                        else:
                            print("Employee not found")
                            clear_terminal()
                            hr_salary(uilgun)
                    elif uihrms == 4:
                        clear_terminal()
                        print("Change Employee Branch")
                        uihrmscebn = int(input("Enter Employee ID to change Branch: "))
                        if uihrmscebn in employees:
                            uihrmscebb = input("Enter New Branch: ")
                            employees[uihrmscebn]['branch'] = uihrmscebb
                            print(f"{employees[uihrmscebn]['name']} Branch changed to {uihrmscebb}")
                            update_file_employees()
                            clear_terminal()
                            hr_salary(uilgun)
                    elif uihrms == 5:
                        clear_terminal()
                        print("Change Desgination")
                        uihrmscd = int(input("Enter Employee ID to change Designation: "))
                        if uihrmscd in employees:
                            uihrmscdd = input("Enter New Designation: ")
                            employees[uihrmscd]['des'] = uihrmscdd
                            print(f"{employees[uihrmscd]['name']} Designation changed to {uihrmscdd}")
                            update_file_employees()
                            clear_terminal()
                            hr_salary(uilgun)
                    else:
                        print("Exiting to HR Menu...")
                        clear_terminal()
                        hr_salary(uilgun)
            elif uihr == 4:
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
