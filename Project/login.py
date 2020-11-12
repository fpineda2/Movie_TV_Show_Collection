import sqlite3
import time
import sys


def newUser():
    found = 0
    while found == 0:
        username = input("PLease enter a username: ")
        with sqlite3.connect("user.db") as db:
            cursor = db.cursor()
        findUser = ("SELECT * FROM UserInfo WHERE username = ?")
        cursor.execute(findUser, [(username)])

        if cursor.fetchall():
            print("That username already exists. Please try another one")
        else:
            found = 1

    email = input("Email: ")
    password = input("Enter a password: ")
    password1 = input("Please reenter your password: ")
    while password != password1:
        print("Your password didn't match, please try again")
        password = input("Enter a password: ")
        password1 = input("Please reenter your password: ")
    insertData = '''INSERT INTO UserInfo(username, email, password)
    VALUES(?,?,?)'''
    print("Great your account is created!")
    cursor.execute(insertData, [(username), (email), (password)])
    db.commit()


def login():
    while True:
        username = input("PLease enter username: ")
        password = input("PLease enter your password: ")
        with sqlite3.connect("user.db") as db:
            cursor = db.cursor()
        find_user = (
            "SELECT * FROM UserInfo WHERE username = ? AND password = ?")
        cursor.execute(find_user, [(username), (password)])
        results = cursor.fetchall()

        if results:
            for i in results:
                print("Welcome " + i[1] + "!")
            break
        else:
            print("username and password not recognised")
            again = input("Do you want to try again?(y/n): ")
            if again.lower() == "n":
                print("Goodbye")
                time.sleep(1)
                break


def menu():
    while True:
        print("Welcome to Coral ")
        menu = ('''
        1 - Create Account
        2 -  Sign in 
        3 - Exit Coral\n''')

        userChoice = input(menu)

        if userChoice == "1":
            newUser()

        elif userChoice == "2":
            login()

        elif userChoice == "3":
            print("Goodbye")
            sys.exit()

        else:
            print("Command not recognised ")


menu()
