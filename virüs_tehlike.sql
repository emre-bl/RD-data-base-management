CREATE TABLE virus_tehlike(
	virus CHAR(6) NOT NULL,
	tehlike INT NOT NULL,
	
	PRIMARY KEY(virus),
	FOREIGN KEY(virus) REFERENCES virus(ad)
);
