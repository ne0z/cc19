CREATE database if not exists aart;
USE aart;
DROP TABLE IF EXISTS art;
CREATE TABLE art 
(
	id INT PRIMARY KEY AUTO_INCREMENT,
	title TEXT,
	art TEXT,
	userid INT,
	karma INT DEFAULT 0
);

DROP TABLE IF EXISTS users;
CREATE TABLE users
(
	id INT PRIMARY KEY AUTO_INCREMENT,
	username TEXT,
	password TEXT
);

DROP TABLE IF EXISTS privs;
CREATE TABLE privs
(
	userid INT PRIMARY KEY,
	isRestricted BOOL
);
