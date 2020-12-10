--1--  View All Movies in our Database
Select *
FROM movie;

--2--  Search for a specific movie title
SELECT movie.m_title, movie.m_genre, movie.m_releasetime, desc_cast.g_cast, desc_cast.g_description
FROM movie
      INNER JOIN desc_cast ON movie.m_moviekey = desc_cast.g_key and m_title LIKE '%The Great Hack%';

--3-- Search for a specific tv show genre
SELECT *
FROM tvshowTable
WHERE t_genre LIKE '%HORROR%';

--4-- Search for a specific actress (BROAD SEARCH)

      SELECT m_title AS movie_TVShow, m_genre AS Genre, desc_cast.g_cast AS Casts, m_releasetime AS releaseTime, m_language AS Languages , desc_cast.g_description AS Descriptions, c_name AS Country
      FROM movie, country, desc_cast
      WHERE desc_cast.g_cast LIKE '%Son Ye-jin%' AND m_countrykey = c_countrykey AND m_moviekey
= g_key
UNION
      SELECT t_showtitle, t_genre, desc_cast.g_cast, t_releasetime, t_language, desc_cast.g_description, c_name
      FROM tvshowTable, country, desc_cast
      WHERE desc_cast.g_cast LIKE '%Son Ye-jin%' AND t_countrykey = c_countrykey AND t_showkey
= g_key;

--5-- Search for movies pf a specific country
SELECT m_title
FROM movie
WHERE EXISTS(SELECT c_name
      FROM country
      WHERE m_countrykey = c_countrykey) AND m_countrykey = 5;

--6-- Search for a specific language and year in movies 
SELECT m_title
FROM movie
WHERE m_language = 'English' AND
      m_releasetime
= 2019;

--7-- Search for a genre in movies and tv shows that appear in both
      SELECT DISTINCT m_genre
      FROM movie
INTERSECT
      SELECT DISTINCT t_genre
      FROM tvshowTable

--8-- Creating an account for user
INSERT INTO UserInfo
      (u_username, u_password, u_email)
VALUES
      ('hannah', 'dots', 'nursewannabe@gmail.com');

--9-- comparing values of m_title
SELECT *
FROM movie
WHERE m_title IN ('Be
With You', 'Automata', 'Shutter')

--10--
SELECT m_title, m_genre, t_showtitle, t_genre
FROM movie
      JOIN tvshowTable ON t_genre = m_genre
WHERE m_genre LIKE '%Comedy%';

--11-- Viewing how many movies of a specific genre in our database
SELECT COUNT(m_title) AS Documentary_movies
FROM movie
WHERE m_genre LIKE '%Documentary%';

--12-- What year did countries release more movies
SELECT m_releasetime, m_countrykey
FROM movie, country
WHERE m_countrykey = c_countrykey
GROUP BY m_countrykey;

--13-- Viewing how many new tv shows in our database
SELECT COUNT(t_showtitle) AS newTVShow
FROM tvshowTable
WHERE t_releasetime = 2020;

--14-- Viewing all the movies from a specific country
SELECT m_title, g_cast, m_language, c_name
FROM movie, country, desc_cast
WHERE m_countrykey = c_countrykey AND
      c_name = 'South Korea' AND m_moviekey = g_key;

--15-- Searching for movies with a specific theme
SELECT m_title, g_description
FROM desc_cast, movie
WHERE g_description LIKE '%kidnap%' AND m_moviekey = g_key;

--16-- Searching for tv shows with a specific amount of seasons in order of newest to oldest
SELECT *
FROM tvshowTable
WHERE t_seasonkey = 1
ORDER BY t_releasetime DESC;

--17-- Adding a review and rating
INSERT INTO review
      (r_moviekey)
SELECT m_moviekey
FROM movie
WHERE m_title = 'Sunny';

INSERT INTO review
      (r_review,r_rating,r_moviekey)
VALUES('Such a nostalgic movie! It made me cry! Will Recommend!', 5, 60000724);

INSERT INTO review
      (r_moviekey,r_review,r_rating)
VALUES(80000003, 'Such a nostalgic movie! It made me cry! Will Recommend!', 5);

--18-- Deleting a user
DELETE
FROM UserInfo
WHERE u_username = 'hannah';

--19-- Delete a review
DELETE
FROM makeReview
WHERE make_reviewid = 1;

--20-- User change their password
UPDATE UserInfo
SET u_password = 'blackpinkinyourarea'
WHERE u_username = 'jennie';





Drop Table favoriteList;

INSERT INTO favoriteList
      (f_userid,f_collection,f_type)
SELECT u_userid,
      m_moviekey AS g_type
FROM UserInfo , movie
WHERE m_title= 'Forrest Gump';


SELECT r_review
FROM review, movie, tvshowTable
WHERE m_title = 'Forrest Gump' AND r_showkey = t_showkey OR r_moviekey = m_moviekey
GROUP BY m_title;
---------------------------
SELECT v_title, v_genre
FROM (SELECT v_genre, COUNT(v_genre) AS num
      FROM V1, favoriteList
      WHERE v_title= f_movie_show AND
            v_genre IN (SELECT v_genre
            FROM V1 , favoriteList
            WHERE v_title = f_movie_show)
      GROUP BY v_genre
      ORDER BY num DESC
LIMIT 1


ORDER BY COUNT
(v_genre);


SELECT v_genre, COUNT(v_genre) AS num
FROM favoriteList, V1
WHERE v_title = f_movie_show
GROUP BY v_genre
ORDER BY num DESC
LIMIT 1




      SELECT v_genre
, COUNT
(v_genre) AS num
      FROM V1
      WHERE v_genre IN
(SELECT v_genre
FROM V1, favoriteList
WHERE v_title=f_movie_show)
GROUP BY v_genre
EXCEPT
SELECT v_title, v_genre
FROM favoriteList, V1
WHERE v_title=f_movie_show



INSERT INTO favoriteList
VALUES('2323432', 'A Moment To Remember')


SELECT v_genre, COUNT(v_genre) AS num
FROM V1, favoriteList
WHERE v_title = f_movie_show AND
      v_genre IN (SELECT v_genre
      FROM V1 , favoriteList
      WHERE v_title = f_movie_show)

GROUP BY v_genre
ORDER BY num DESC
LIMIT 1






WHERE v_title
= f_movie_show AND
      v_genre IN
(SELECT v_genre
FROM V1 , favoriteList
WHERE v_title = f_movie_show)


SELECT V1.v_genre, COUNT(V1.v_genre) AS num
FROM V1
      INNER JOIN favoriteList ON V1.v_title = favoriteList.f_movie_show


INSERT INTO review
      (r_moviekey,r_review,r_rating)
SELECT m_moviekey, r_review, r_rating
FROM movie, review
WHERE m_moviekey = 80000003 AND r_review = 'it was interesting' AND r_rating = '4' AND r_moviekey = m_moviekey

SELECT m_moviekey
FROM movie
WHERE m_title= 'EXIT'


INSERT INTO review
      (r_moviekey,r_review,r_rating)
SELECT m_moviekey, r_review, r_rating
FROM movie, review
WHERE m_title = ? AND r_review = ? AND r_rating = ?

SELECT r_review, r_moviekey
FROM review, V1
WHERE v_title = 'Babies' AND r_moviekey
= v_key OR r_showkey = v_key

      SELECT r_review
      FROM review
            INNER JOIN V1 ON r_moviekey = v_key
      WHERE v_title = 'Forrest Gump'
UNION
      SELECT r_review
      FROM review
            INNER JOIN V1 ON r_showkey = v_key
      WHERE v_title = 'Forrest Gump'


INSERT INTO review
      (r_moviekey,r_review,r_rating)
VALUES((SELECT m_moviekey
            FROM movie
            WHERE m_title = 'A Moment To Remember'), 'it was really sad but good', 4)

SELECT userid
from UserInfo
WHERE username = 'bob'

SELECT t_showtitle
FROM tvshowTable
WHERE t_showkey = '81159258'

SELECT m_title
FROM movie
WHERE m_moviekey = '80000003'

SELECT r_review 
FROM review 
INNER JOIN V1 ON r_moviekey = v_key 
WHERE v_title =  
UNION 
SELECT r_review 
FROM review
INNER JOIN V1 ON r_showkey = v_key 
WHERE v_title = ;


SELECT f_movie_show 
FROM favoriteList, UserInfo 
WHERE f_userid = userid AND 
username = 'Annisa';
             
SELECT v_title, v_genre
FROM V1
WHERE v_genre IN (SELECT v_genre
                  FROM (SELECT v_genre, COUNT(v_genre) AS num
                  FROM favoriteList, V1, UserInfo
                  WHERE v_title = f_movie_show AND
                        f_userid = userid AND
                        username = 'Annisa'
                  GROUP BY v_genre
                  ORDER BY num DESC
                  LIMIT 1))
EXCEPT
SELECT v_title, v_genre
FROM V1,favoriteList, UserInfo
WHERE v_title = f_movie_show AND
      f_userid = userid AND
      username = 'Annisa';

INSERT INTO favoriteList(f_userid,f_movie_show) 
VALUES((SELECT userid from UserInfo WHERE username = 'annisa'),'The Classic');

def view(_conn, username):
    try:
        print("\nViewing Favorite List...")

        view = """SELECT f_movie_show AS favoriteList
                  FROM favoriteList, UserInfo 
                  WHERE f_userid = userid AND 
                  username = ?"""
        #args = [username]

        cur = _conn.cursor()
        cur.execute(view,(username,))
        mytable = from_db_cursor(cur)
        print(mytable)

        add = input("Would You Like to EDIT Your Favorite List? (y/n)")
        if add == 'y':
            modify(_conn,username)
        if add == 'n':
            main(username)

    except Error as e:
        print(e)
        print("++++++++++++++++++++++++++++++++++")

DELETE FROM favoriteList WHERE f_userid = 1;
DELETE FROM UserInfo WHERE userid = 2;

INSERT INTO favoriteList(f_userid,f_movie_show) VALUES ((SELECT userid FROM UserInfo WHERE username LIKE 'annisa'),'The Classic')
