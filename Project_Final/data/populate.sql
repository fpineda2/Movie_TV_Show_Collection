CREATE TABLE country
(
    c_countrykey INT PRIMARY KEY,
    c_name CHAR(20)
);

CREATE TABLE favoriteList
(
    f_userid INT REFERENCES UserInfo(u_userid),
    f_movie_show INT REFERENCES V1(v_key)
);

CREATE TABLE movie
(
    m_moviekey INT PRIMARY KEY,
    m_title CHAR(20),
    m_genre CHAR(20),
    m_releasetime INT,
    m_language CHAR(20),
    m_countrykey INT REFERENCES country(c_countrykey)
);

CREATE TABLE tvshowTable
(
    t_showkey INT PRIMARY KEY,
    t_showtitle CHAR(20),
    t_genre CHAR(20),
    t_releasetime INT,
    t_language CHAR(20),
    t_seasonkey INT,
    t_countrykey INT REFERENCES country(c_countrykey)
);

CREATE TABLE UserInfo
(
    userid INTEGER PRIMARY KEY,
    username CHAR(50),
    password CHAR(50),
    email CHAR(50)
);

CREATE TABLE review
(
    r_moviekey INT REFERENCES movie(m_moviekey),
    r_showkey INT REFERENCES tvshowTable(t_showkey),
    r_review CHAR(200),
    r_rating INT

);

CREATE TABLE desc_cast
(
    g_key INT PRIMARY KEY,
    g_description CHAR(150),
    g_cast CHAR(100)
);

DROP TABLE country;
DROP TABLE favoriteList;
DROP TABLE movie;
DROP TABLE tvshowTable;
DROP TABLE UserInfo;
DROP TABLE review;
DROP TABLE desc_cast;

DROP VIEW V1;
