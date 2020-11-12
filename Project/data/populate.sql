CREATE TABLE country
(
    c_countrykey INT PRIMARY KEY,
    c_name CHAR(20)
);

CREATE TABLE favoriteList
(
    f_userid INT REFERENCES UserInfo(u_userid),
    f_moviekey INT REFERENCES movie(m_moviekey),
    f_showkey INT REFERENCES tvshowTable(t_showkey)
);

CREATE TABLE movie
(
    m_moviekey INT PRIMARY KEY,
    m_title CHAR(20),
    m_genre CHAR(20),
    m_cast CHAR(100),
    m_releasetime INT,
    m_language CHAR(20),
    m_description CHAR(150),
    m_countrykey INT REFERENCES country(c_countrykey)
);

CREATE TABLE tvshowTable
(
    t_showkey INT PRIMARY KEY,
    t_showtitle CHAR(20),
    t_genre CHAR(20),
    t_cast CHAR(50),
    t_releasetime INT,
    t_language CHAR(20),
    t_description CHAR(150),
    t_seasonkey INT,
    t_countrykey INT REFERENCES country(c_countrykey)
);

CREATE TABLE UserInfo
(
    userid INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(30),
    password VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL
);


DROP TABLE country;
DROP TABLE favoriteList;
DROP TABLE movie;
DROP TABLE tvshowTable;
DROP TABLE UserInfo;

