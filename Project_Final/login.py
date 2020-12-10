import sqlite3
import time
import sys
import os
from sqlite3 import Error
import random
import functions


def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn


def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")


def newUser(_conn):
    found = 0
    while found == 0:
        username = input("PLease enter a username: ")

        findUser = ("SELECT * FROM UserInfo WHERE username = ?")
        cur = _conn.cursor()
        cur.execute(findUser, [(username)])

        if cur.fetchall():
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
    print("\nGreat your account is created!")
    cur.execute(insertData, [(username), (email), (password)])
    _conn.commit()


def login(_conn):
    while True:
        username = input("PLease enter username: ")
        password = input("PLease enter your password: ")
        find_user = (
            "SELECT * FROM UserInfo WHERE username = ? AND password = ?")
        cur = _conn.cursor()
        cur.execute(find_user, [(username), (password)])
        results = cur.fetchall()

        if results:
            for i in results:
                print("Welcome " + i[1] + "!")
                functions.main(username)
            break
        else:
            print("username and password not recognised")
            again = input("Do you want to try again?(y/n): ")
            if again.lower() == "n":
                print("Goodbye")
                time.sleep(1)
                break


def main():
    database = r"user.db"
    conn = openConnection(database)

    while True:
        print("Welcome to Coral -- Movie/TV Show Collection ")
        menu = ('''
        1 - Create Account
        2 - Sign in 
        3 - Change Password
        4 - Exit Coral\n''')

        userChoice = input(menu)
        with conn:
            if userChoice == "1":
                newUser(conn)

            elif userChoice == "2":
                login(conn)

            elif userChoice == "3":
                functions.changePassword(conn)

            elif userChoice == "4":
                print("Goodbye")
                sys.exit(conn)

            else:
                print("Command not recognized ")

    closeConnection(conn, database)


if __name__ == '__main__':
    main()
