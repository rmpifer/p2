
DROP TABLE if exists Contain, Photo, Album, User;


CREATE TABLE User (
	username VARCHAR(20),
	password VARCHAR(20),
	firstName VARCHAR(20),
	lastName VARCHAR(20),
	email VARCHAR(40),
	PRIMARY KEY (username)
);

CREATE TABLE Album (
	albumID INTEGER AUTO_INCREMENT,
	title VARCHAR(50),
	created DATETIME DEFAULT CURRENT_TIMESTAMP(),
	lastUpdate DATETIME DEFAULT CURRENT_TIMESTAMP(),
	username VARCHAR(20),
	PRIMARY KEY (albumID),
	FOREIGN KEY (username) REFERENCES User (username)
);

CREATE TABLE Photo (
	picID VARCHAR(40),
	format VARCHAR(3), 
	posted DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (picID)
);

CREATE TABLE Contain (
	sequenceNum INTEGER,
	albumID INTEGER,
	picID VARCHAR(40),
	caption VARCHAR(255),
	PRIMARY KEY (sequenceNum),
	FOREIGN KEY (albumID) REFERENCES Album (albumID),
	FOREIGN KEY (picID) REFERENCES Photo (picID)
);

