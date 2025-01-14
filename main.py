import os
import time

#Initilize the stock dictionary
stock_dic = {}

#HR related dictionaries
logins = {
    "hamza": {"password": "hamza123", "des": "admin"}
}
salary_dic = {
    "hamza": {"day": 6, "com": 0}
}

#Read the stock file
def read_file_stock():
    st_fl_dt = open("stock.txt", "r+")
    st_fl_dt_list = st_fl_dt.readlines()
    for st in st_fl_dt_list:
        stock = st.strip().split("|")
        if len(stock) > 0:
            stock_dic[stock[0]] = {'quantity': int(stock[1]), 'price': float(stock[2])}
    st_fl_dt.close()

#Update stock file
def update_file():
    with open("stock.txt", "w+") as uf:
        for product, details in stock_dic.items():
            uf.write(f"{product}|{details['quantity']}|{details['price']}\n")

#Read the salary file
def update_file_salary():
    with open("salary.txt", "w+") as ufs:
        for emp, details in salary_dic.items():
            ufs.write(f"{emp}|{details['day']}|{details['com']}\n")

#Funtion to clear terminal and 1 second delay
def clear_terminal():
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')

#Login function
def login():
    while True:
        uilgun = input("Enter your username: ")
        uilgpw = input("Enter your password: ")
        if uilgun in logins and uilgpw == logins[uilgun]["password"]:
            clear_terminal()
            salary_dic[uilgun]['day'] += 1
            update_file_salary()
            read_file_stock()
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
    print(f"Welcome {uilgun} to POS Terminal")
    popnm = input("Product: ")
    if popnm in stock_dic:
        if stock_dic[popnm]["quantity"] > 0:
            popqu = int(input("Quantity: "))
            print(f"Total is {popqu * stock_dic[popnm]['price']}")
            stock_dic[popnm]["quantity"] -= popqu
            salary_dic[uilgun]['com'] += popqu/100
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
    if another == "yes":
        pos_terminal(uilgun)
    else:
        clear_terminal()
        main_menu(uilgun)

#Stock Management function
def st_mg(uilgun):
    print(f"Welcome {uilgun} to Stock Management")
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
    if logins[uilgun]["des"] == "admin":
        print(f"Welcome {uilgun} to HR")
        print("1. View All Branches")
        print("2. View All Staff")
        print("3. Check Salaries")
        print("4. Manage Staff")
        print("5. Manage Branches")
        print("6. Exit HR")
    else:
        print("You dont have acces to HR Menu")
        print("Exiting to main menu...")
        clear_terminal()
        main_menu(uilgun)

#Main Menu function
def main_menu(uilgun):
    print(f"Welcome {uilgun} have a great day!")
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
