CREATE TABLE virus_tehlike(
	virus CHAR(6) NOT NULL,
	tehlike INT NOT NULL,
	
	PRIMARY KEY(virus),
	FOREIGN KEY(virus) REFERENCES virus(ad) ON DELETE restrict ON UPDATE CASCADE
);

INSERT INTO virus_tehlike VALUES('4YE-7D', 10);
INSERT INTO virus_tehlike VALUES('0IW-7O', 5);
INSERT INTO virus_tehlike VALUES('5TU-2V', 8);
INSERT INTO virus_tehlike VALUES('0PR-9F', 7);
INSERT INTO virus_tehlike VALUES('1KA-7Z', 9);
INSERT INTO virus_tehlike VALUES('8ZG-9L', 6);
INSERT INTO virus_tehlike VALUES('3ZB-3C', 8);
