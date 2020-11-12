import sqlite3

username = input("PLease enter a username: ")

with sqlite3.connect("user.db") as db:
    cursor = db.cursor()


cursor.execute("""
INSERT INTO UserInfo(username, email, password)
VALUES("test_User", "Bob", "Smith")
 """)
db.commit()
cursor.execute("SELECT * FROM UserInfo")
print(cursor.fetchall())
