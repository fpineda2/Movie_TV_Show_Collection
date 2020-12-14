from prettytable import from_db_cursor
import os
import sqlite3
from sqlite3 import Error
import random
import sys
import time


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


def createv1(_conn):

    try:
        createv1 = """CREATE VIEW V1(v_key, v_title, v_genre, v_releasetime, v_language, v_countrykey) AS SELECT * FROM movie UNION ALL SELECT t_showkey, t_showtitle, t_genre, t_releasetime, t_language, t_countrykey FROM tvshowTable"""
        _conn.execute(createv1)
        _conn.commit()

    except Error as e:
        print(e)
        print("++++++++++++++++++++++++++++++++++")


def changePassword(_conn):
    while True:
        username = input("PLease enter username: ")
        find_user = (
            "SELECT * FROM UserInfo WHERE username = ?")
        cur = _conn.cursor()
        cur.execute(find_user, [(username), ])
        results = cur.fetchall()

        if results:
            for i in results:
                password = input("PLease enter your NEW password: ")
                password1 = input("Please re-enter your NEW password: ")
                updateData = '''UPDATE UserInfo SET password = ? WHERE username = ?'''
                cur.execute(updateData, [(password), (username), ])
                _conn.commit()
                main(username)
        else:
            print("Username not recognized")
            again = input("Do you want to try again?(y/n): ")
            if again.lower() == "n":
                print("Goodbye")
                time.sleep(1)
                break

# def displayfavoriteList(_conn,username):
#     try:
#         print("Would you like to view --or-- edit your favorite list?: ")
#         question = input()

#         if question == 'view':
#             view(_conn,username)

#         if question == 'edit':
#             modify(_conn,username)

#     except Error as e:
#         print(e)
#         print("++++++++++++++++++++++++++++++++++")


def search(_conn, username):

    try:
        print("Would you like to search for a Movie (Enter 1) -or- a TV Show (Enter 2) -or- leave Coral (Enter 0)? :")
        answer = input()

        if answer == '0':
            exit()

        if answer == '1':
            search = input(
                "Would you like to search by Title -or- Genre -or- Cast -or- Keyword?: ")
            if search == 'Title':
                title = input("\nEnter a Movie Title: ")
                moviesearchbyTitle(_conn, title, username)
            if search == 'Genre':
                genre = input("\nEnter the Genre of a Movie: ")
                moviesearchbyGenre(_conn, genre, username)
            if search == 'Cast':
                cast = input("\nEnter the name of Actor/Actresses: ")
                moviesearchbyCast(_conn, cast, username)
            if search == 'Keyword':
                keyword = input("\nEnter a key concept of a Movie: ")
                moviesearchbyKeyword(_conn, keyword, username)

        if answer == '2':
            look = input(
                "Would you like to search by Title, Genre, Cast, or Keyword?: ")
            if look == 'Title':
                title = input("\nEnter the name of a TV Show: ")
                tvsearchbyTitle(_conn, title, username)
            if look == 'Genre':
                genre = input("\nEnter the GENRE of a TV Show: ")
                tvsearchbyGenre(_conn, genre, username)
            if look == 'Cast':
                cast = input("\nEnter the name of Actor/Actresses: ")
                tvsearchbyCast(_conn, cast, username)
            if look == 'Keyword':
                keyword = input("\nEnter a key concept of a TV Show: ")
                tvsearchbyKeyword(_conn, keyword, username)

    except Error as e:
        print(e)
        print("++++++++++++++++++++++++++++++++++")

# def view(_conn, username):
#     try:
#         print("\nViewing Favorite List...")

#         view = """SELECT f_movie_show AS favoriteList
#                   FROM favoriteList, UserInfo
#                   WHERE f_userid = userid AND
#                   username = ?"""
#         #args = [username]

#         cur = _conn.cursor()
#         cur.execute(view,(username,))
#         mytable = from_db_cursor(cur)
#         print(mytable)

#         main(username)

#     except Error as e:
#         print(e)
#         print("++++++++++++++++++++++++++++++++++")


def modify(_conn, username):
    try:
        view = """SELECT f_movie_show FROM favoriteList, UserInfo WHERE username = ? AND userid = f_userid"""
        cur = _conn.cursor()
        cur.execute(view, (username,))
        rows = cur.fetchall()

        print("1. Would you like to add to your favorite list?")
        print("2. Would you like to delete something?")
        answer = input()
        if answer == '1':
            pick = input(
                "\nWhat would you like to add to your favorite list? : ")
            sql = """INSERT INTO favoriteList(f_userid,f_movie_show) VALUES((SELECT userid from UserInfo WHERE username = ?),?)"""
            #args = [username]
            cur = _conn.cursor()
            cur.execute(sql, (username, pick,))
            rows = cur.fetchall()
            _conn.commit()
            print(pick, "has been added to favoriteList")
            main(username)
        if answer == '2':
            delete = input(
                "\nWhat would you like to delete from your list? : ")
            check = """SELECT f_userid, f_movie_show FROM favoriteList, UserInfo WHERE username = ? AND f_movie_show = ? AND userid = f_userid"""
            cur = _conn.cursor()
            cur.execute(check, (username, delete))
            rows = cur.fetchall()
            if len(rows) == 0:
                print("\nThe Movie/Show you have entered is not in your favorite list")
                main(username)
            else:
                take = """ DELETE FROM favoriteList WHERE f_movie_show = ? AND f_userid IN (SELECT userid from UserInfo, favoriteList WHERE username = ? AND userid = f_userid)"""
                cur = _conn.cursor()
                cur.execute(take, (delete, username))
                _conn.commit()
                print(delete, "has been successfully removed")
                main(username)
    except Error as e:
        print(e)
        print("++++++++++++++++++++++++++++++++++")


def moviesearchbyTitle(_conn, movieTitle, username):
    try:
        movieTitle = '%' + movieTitle + '%'
        sql = """SELECT m_title AS Movie, m_genre AS Genre, m_releasetime AS Year, m_language AS Language, c_name AS Country, g_cast AS Cast
                 FROM movie, country, desc_cast
                 WHERE m_moviekey = g_key AND 
                       m_countrykey = c_countrykey AND 
                       m_title LIKE ?"""
        args = [movieTitle]
        cur = _conn.cursor()
        cur.execute(sql, args)

        rows = cur.fetchall()

        if len(rows) == 0:
            print("The movie does not exist in the system")
            exit()
        else:
            cur.execute(sql, args)
            mytable = from_db_cursor(cur)
            print(mytable)

        main(username)

    except Error as e:
        print(e)
        print("++++++++++++++++++++++++++++++++++")


def moviesearchbyGenre(_conn, movieGenre, username):
    try:
        # Search by Genre
        movieGenre = movieGenre + '%'
        find_genre = """SELECT m_title AS Movie, m_genre AS Genre,m_releasetime AS Year,m_language AS Language,c_name AS Country, SUBSTR(g_description, 1,20) AS Description
                        FROM movie, country, desc_cast
                        WHERE m_moviekey = g_key AND m_countrykey = c_countrykey AND m_genre LIKE ?
                        GROUP BY m_title"""
        args = [movieGenre]
        cur = _conn.cursor()
        cur.execute(find_genre, args)

        rows = cur.fetchall()
        if len(rows) == 0:
            print("The movie does not exist in the system")
            exit()
        else:
            cur.execute(find_genre, args)
            mytable = from_db_cursor(cur)
            print(mytable)

        main(username)
    except Error as e:
        print(e)
        print("++++++++++++++++++++++++++++++++++")


def moviesearchbyCast(_conn, movieCast, username):
    # Search by Actor/Actresses
    try:
        movieCast = '%' + movieCast + '%'
        find_cast = """SELECT m_title AS Movie, m_genre AS Genre, m_releasetime AS Year, m_language AS Language, g_cast AS Cast
                            FROM movie, desc_cast
                            WHERE g_key = m_moviekey AND g_cast LIKE ?
                            GROUP BY m_title"""
        args = [movieCast]
        cur = _conn.cursor()
        cur.execute(find_cast, args)

        rows = cur.fetchall()

        if len(rows) == 0:
            print("The cast does not exist in the system")
            exit()
        else:
            cur.execute(find_cast, args)
            mytable = from_db_cursor(cur)
            print(mytable)

        main(username)

    except Error as e:
        print(e)
        print("++++++++++++++++++++++++++++++++++")


def moviesearchbyKeyword(_conn, movieKeywords, username):

    try:
        movieKeywords = '%' + movieKeywords + '%'
        find_keyword = """SELECT m_title, SUBSTR(g_description,1,100) AS Description
                            FROM movie, desc_cast
                            WHERE g_key = m_moviekey AND g_description LIKE ?"""
        args = [movieKeywords]
        cur = _conn.cursor()
        cur.execute(find_keyword, args)

        rows = cur.fetchall()

        if len(rows) == 0:
            print("The movie does not exist in the system")
            exit()
        else:
            cur.execute(find_keyword, args)
            mytable = from_db_cursor(cur)
            print(mytable)

        main(username)

    except Error as e:
        print(e)
        print("++++++++++++++++++++++++++++++++++")


def tvsearchbyTitle(_conn, tvTitle, username):
    try:
        tvTitle = '%' + tvTitle + '%'
        sql = """SELECT t_showtitle AS TV_Show, t_genre AS Genre, t_releasetime AS Year, t_language AS language, SUBSTR(g_description,1,20) AS Description, g_cast AS Cast
                FROM tvshowTable, desc_cast
                WHERE g_key = t_showkey AND t_showtitle LIKE ?"""
        args = [tvTitle]
        cur = _conn.cursor()
        cur.execute(sql, args)

        rows = cur.fetchall()

        if len(rows) == 0:
            print("The TV Show  does not exist in the system")
            exit()
        else:
            cur.execute(sql, args)
            mytable = from_db_cursor(cur)
            print(mytable)

        main(username)

    except Error as e:
        print(e)
        print("++++++++++++++++++++++++++++++++++")


def tvsearchbyGenre(_conn, tvGenre, username):
    try:
        tvGenre = '%' + tvGenre + '%'
        find_genre = """SELECT t_showtitle AS TV_Show, t_genre AS Genre, t_releasetime AS Year, t_language AS Language, SUBSTR(g_description, 1, 25) AS Description
                        FROM tvshowTable, desc_cast
                        WHERE g_key = t_showkey AND t_genre LIKE ?"""
        args = [tvGenre]
        cur = _conn.cursor()
        cur.execute(find_genre, args)

        rows = cur.fetchall()

        if len(rows) == 0:
            print("The TV Show  does not exist in the system")
            exit()
        else:
            cur.execute(find_genre, args)
            mytable = from_db_cursor(cur)
            print(mytable)

        main(username)

    except Error as e:
        print(e)
        print("++++++++++++++++++++++++++++++++++")


def tvsearchbyCast(_conn, tvCast, username):
    try:
        tvCast = '%' + tvCast + '%'
        find_cast = """SELECT t_showtitle AS TV_Show, t_genre AS Genre, t_releasetime AS Year, t_language AS Language, g_cast AS Cast
                        FROM tvshowTable, desc_cast
                        WHERE g_key = t_showkey AND g_cast LIKE ?"""
        args = [tvCast]
        cur = _conn.cursor()
        cur.execute(find_cast, args)

        rows = cur.fetchall()

        if len(rows) == 0:
            print("The TV Show does not exist in the system")
            exit()
        else:
            cur.execute(find_cast, args)
            mytable = from_db_cursor(cur)
            print(mytable)

        main(username)

    except Error as e:
        print(e)
        print("++++++++++++++++++++++++++++++++++")


def tvsearchbyKeyword(_conn, tvKeyword, username):
    try:
        tvKeyword = '%' + tvKeyword + '%'
        find_keyword = """SELECT t_showtitle, SUBSTR(g_description,1,100)
                        FROM tvshowTable, desc_cast
                        WHERE g_key = t_showkey AND g_description LIKE ?"""
        args = [tvKeyword]
        cur = _conn.cursor()
        cur.execute(find_keyword, args)

        rows = cur.fetchall()

        if len(rows) == 0:
            print("The TV Show does not exist in the system")
            exit()
        else:
            cur.execute(find_keyword, args)
            mytable = from_db_cursor(cur)
            print(mytable)

            main(username)

    except Error as e:
        print(e)
        print("++++++++++++++++++++++++++++++++++")


def recommend(_conn, username):

    try:
        print("\nHere Are Your Recommendations Based On Your Favorite List!")
        sql = """SELECT v_title AS Movie_TVShow, v_genre AS Genre
                FROM V1
                WHERE v_genre IN (SELECT v_genre
                                  FROM (SELECT v_genre, COUNT(v_genre) AS num
                                        FROM favoriteList, V1, UserInfo
                                        WHERE v_title = f_movie_show AND
                                              f_userid = userid AND
                                              username = ?
                                        GROUP BY v_genre
                                        ORDER BY num DESC))
                EXCEPT
                SELECT v_title, v_genre
                FROM V1,favoriteList, UserInfo
                WHERE v_title = f_movie_show AND
                    f_userid = userid AND
                    username = ?"""

        cur = _conn.cursor()
        cur.execute(sql, (username, username,))

        # print out table
        mytable = from_db_cursor(cur)
        print(mytable)

        main(username)

    except Error as e:
        print(e)
        print("++++++++++++++++++++++++++++++++++")


def review(_conn, username):

    try:
        title = input("PLease enter a movie/ TV show title: ")
        findshow = """SELECT v_key FROM V1 WHERE v_title = ?"""
        cur = _conn.cursor()
        cur.execute(findshow, (title,))
        root = cur.fetchall()
        if len(root) != 0:
            find_review = """SELECT r_review AS Review FROM review INNER JOIN V1 ON r_moviekey = v_key WHERE v_title = ? UNION SELECT r_review FROM review
            INNER JOIN V1 ON r_showkey = v_key WHERE v_title = ?"""
            cur = _conn.cursor()
            cur.execute(find_review, (title, title))
            rows = cur.fetchall()

            if len(rows) == 0:
                print(title, "doesn't have any reviews yet")
                choice = input("\nDo you want to make your own review?(y/n):")
                if choice.lower() == "n":
                    main(username)
                else:
                    makerev(_conn, username)
                    # break
            else:
                cur.execute(find_review, (title, title))
                mytable = from_db_cursor(cur)
                print(mytable)
                main(username)
        else:
            print(title, "isn't part of the current collection")
            main(username)

    except Error as e:
        print(e)
        print("++++++++++++++++++++++++++++++++++")


def makerev(_conn, username):
    try:
        about = input("What Movie --or-- TV Show would you like to review? ")
        desc = input("What are your thoughts on it: ")
        rate = input("Rate 1-5 on how good it was: ")
        findmovie = ("SELECT * FROM tvshowTable WHERE t_showtitle = ?")
        cur = _conn.cursor()
        cur.execute(findmovie, [(about)])
        rows = cur.fetchall()
        if len(rows) == 0:
            # if cur.fetchall():
            #key1 = """SELECT t_showkey FROM tvshowTable WHERE t_showtitle = ?"""
            #cur = _conn.cursor()
            #cur.execute(key1, (about,))
            #data = cur.fetchone()
            tv_rev = """INSERT INTO review (r_moviekey,r_review,r_rating) VALUES((SELECT m_moviekey FROM movie WHERE m_title = ?), ?, ?)"""
            cur = _conn.cursor()
            cur.execute(tv_rev, (about, desc, rate,))
            _conn.commit()
            print("\nGreat your review has now been added!")

        else:
            #key = """SELECT m_moviekey FROM movie WHERE m_title = ?"""
            #cur = _conn.cursor()
            #cur.execute(key, (about,))
            #place = cur.fetchone()
            movie_rev = """INSERT INTO review (r_showkey,r_review,r_rating) VALUES((SELECT t_showkey FROM tvshowTable WHERE t_showtitle = ?), ?, ?)"""
            cur = _conn.cursor()
            cur.execute(movie_rev, (about, desc, rate,))
            _conn.commit()
            print("\nGreat your review has now been added!")

        main(username)

    except Error as e:
        print(e)
        print("++++++++++++++++++++++++++++++++++")


def displayallMovie(_conn, username):
    try:
        display = """SELECT m_title AS Movie, m_genre AS Genre, m_releasetime AS Year, m_language AS Language, SUBSTR(g_description, 1, 25) AS Description
                     FROM Movie, desc_cast
                     WHERE m_moviekey = g_key"""
        cur = _conn.cursor()
        cur.execute(display)
        _conn.commit()

        mytable = from_db_cursor(cur)
        print(mytable)
        main(username)

    except Error as e:
        print(e)
        print("++++++++++++++++++++++++++++++++++")


def displayallTvshow(_conn, username):
    try:
        display = """SELECT t_showtitle AS Movie, t_genre AS Genre, t_releasetime AS Year, t_language AS Language, SUBSTR(g_description, 1, 50) AS Description
                     FROM tvshowTable, desc_cast
                     WHERE t_showkey = g_key"""
        cur = _conn.cursor()
        cur.execute(display)
        _conn.commit()

        mytable = from_db_cursor(cur)
        print(mytable)
        main(username)

    except Error as e:
        print(e)
        print("++++++++++++++++++++++++++++++++++")


def displayfavoriteList(_conn, username):
    try:
        display = """SELECT f_movie_show AS favoriteList
                  FROM favoriteList, UserInfo 
                  WHERE f_userid = userid AND 
                  username = ?"""
        #args = [username]

        cur = _conn.cursor()
        cur.execute(display, (username,))
        mytable = from_db_cursor(cur)
        print(mytable)
        main(username)

    except Error as e:
        print(e)
        print("++++++++++++++++++++++++++++++++++")


def main(username):
    database = r"user.db"
    conn = openConnection(database)

    print("\nWhat would you like to do?")
    print("1. Search through collection")
    print("2. Receive a recommendation based on your interests")
    print("3. Look up or make a Review")
    print("4. Edit Your Favorite List")
    print("5. View Favorite List")
    print("6. View ALL Movies")
    print("7. View ALL TV Shows")
    print("8. Leave")
    print("\nEnter the number of what you would like to do: ")

    answer = input()
    with conn:
        if answer == '1':
            search(conn, username)
        if answer == '2':
            recommend(conn, username)
        if answer == '3':
            createv1(conn)
            review(conn, username)
        if answer == '4':
            modify(conn, username)
        if answer == '5':
            displayfavoriteList(conn, username)
        if answer == '6':
            displayallMovie(conn, username)
        if answer == '7':
            displayallTvshow(conn, username)
        if answer == '8':
            exit()
    # create a database connection

    closeConnection(conn, database)


if __name__ == '__main__':
    main()
