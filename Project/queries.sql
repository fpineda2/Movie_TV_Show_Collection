--1--  View All Movies in our Database
Select *
FROM movie;

--2--  View All TV Shows in our Database
SELECT *
FROM tvshowTable;

--3--  Search for a specific movie title
SELECT m_title, m_genre, m_cast, m_releasetime, m_description
FROM movie
WHERE m_title LIKE '%The Great Hack%';

--4-- Search for a specific tv show genre
SELECT *
FROM tvshowTable
WHERE t_genre LIKE '%HORROR%';

--5-- Search for a specific actress (BROAD SEARCH)
      SELECT m_title AS movie_TVShow, m_genre AS Genre, m_cast AS Casts, m_releasetime AS releaseTime, m_language AS Languages , m_description AS Descriptions, c_name AS Country
      FROM movie, country
      WHERE m_cast LIKE '%Son Ye-jin%' AND
            m_countrykey = c_countrykey
UNION
      SELECT t_showtitle, t_genre, t_cast, t_releasetime, t_language, t_description, c_name
      FROM tvshowTable, country
      WHERE t_cast LIKE '%Son Ye-jin%' AND
            t_countrykey = c_countrykey;

--6-- Search for a specific actor in movies
SELECT m_title, m_genre, m_cast, m_releasetime, m_description
FROM movie
WHERE m_cast LIKE '%Robert Downey Jr.%';

--7-- Search for a specific language in movies
SELECT m_title
FROM movie
WHERE m_language = 'English';

--8-- Search for a specific genre and release time in tv shows
SELECT t_showtitle
FROM tvshowTable
WHERE t_genre  LIKE '%Romance%' AND
      t_releasetime = 2019;

--9-- Search for a specific genre in movies and tv shows
      SELECT DISTINCT m_title AS Movie_TVShow, m_genre AS Genre
      FROM movie
      WHERE m_genre LIKE '%Comedy%'
UNION
      SELECT DISTINCT t_showtitle AS TVShow, t_genre AS Genre
      FROM tvshowTable
      WHERE t_genre LIKE '%Comedy%'

--10-- Creating an account for user
INSERT INTO UserInfo
      (u_userid,u_username, u_password, u_email)
VALUES
      ('1', 'bobcat', 'password', 'bobcat@gmail.com');

--11-- Inserting User's chosen movie into their favorite list
INSERT INTO favoriteList
      (f_userid,f_moviekey)
SELECT u_userid, m_moviekey
FROM movie, UserInfo
WHERE u_userid = 1 AND
      m_title = 'The Classic';

--12-- Inserting User's chosen tvshow into their favorite list
INSERT INTO favoriteList
      (f_userid,f_showkey)
SELECT u_userid, t_showkey
FROM tvshowTable, UserInfo
WHERE t_showtitle = 'Summer Scent' AND
      u_userid = 1;

--13--
SELECT m_title, m_genre
FROM movie
WHERE m_title = 'A Moment To Remember';
-- Recommendation Example -- Run these together
      SELECT m_title AS movie_TVShow, m_genre AS Genre
      FROM movie
      WHERE m_genre LIKE '%Romance%'
UNION
      SELECT t_showtitle, t_genre
      FROM tvshowTable
      WHERE t_genre LIKE '%Romance%';

--14-- Viewing how many movies of a specific genre in our database
SELECT COUNT(m_title) AS Documentary_movies
FROM movie
WHERE m_genre LIKE '%Documentary%';

--15-- Viewing how many new movies in our database 
SELECT COUNT(m_title) AS newMovies
FROM movie
WHERE m_releasetime = 2020;

--16-- Viewing how many new tv shows in our database
SELECT COUNT(t_showtitle) AS newTVShow
FROM tvshowTable
WHERE t_releasetime = 2020;

--17-- Viewing all the movies from a specific country
SELECT m_title, m_cast, m_language, c_name
FROM movie, country
WHERE m_countrykey = c_countrykey AND
      c_name = 'South Korea';

--18-- Searching for the cast of a specific show
SELECT t_showtitle, t_cast
FROM tvshowTable
WHERE t_showtitle = 'New Girl';

--19-- Searching for movies with a specific theme
SELECT *
FROM movie
WHERE m_description LIKE '%kidnap%';

--20-- Searching for tv shows with a specific amount of seasons
SELECT *
FROM tvshowTable
WHERE t_seasonkey = 1;