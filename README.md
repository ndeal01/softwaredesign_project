# f19-msci3300-g2
Group 2 repository for South Liberty Public Library project

Group Members:
Nicholas Deal, Systems Analyst - nicholas-deal@uiowa.edu
Matt Tolton, Systems Analyst - matthew-tolton@uiowa.edu
Tyler Robertson, Systems Analyst - tyler-robertson@uiowa.edu
Alex Contreras, Systems Analyst - alex-contreras@uiowa.edu



This website will help The South Public Library perform their standard processes more effectively and efficiently.

Using this project:
Librarians will be able to add, update and delete all materials
Librarians will be able to check out books for patrons
Patrons will be able to search all materials and check for availability and other info on their material
Patrons will be able to see a list of current books they have checked out
Patrons will be able to see their current wish list
Guests to the website will be able to search for books
Guests will be able to sign up for an account


SQL Scripts:

CREATE TABLE `g2_circulationtable` (
  `CheckoutID` int(30) NOT NULL AUTO_INCREMENT,
  `MaterialID` int(30) DEFAULT NULL,
  `PeopleID` int(30) DEFAULT NULL,
  `Checkoutdate` date DEFAULT NULL,
  `Datedue` date DEFAULT NULL,
  PRIMARY KEY (`CheckoutID`),
  UNIQUE KEY `MaterialID_UNIQUE` (`MaterialID`),
  KEY `MaterialID_fk` (`MaterialID`),
  KEY `PeopleID_fk` (`PeopleID`),
  CONSTRAINT `Material_fk1` FOREIGN KEY (`MaterialID`) REFERENCES `g2_materialtable` (`MaterialID`),
  CONSTRAINT `People_fk2` FOREIGN KEY (`PeopleID`) REFERENCES `g2_peopletable` (`PeopleID`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;

CREATE TABLE `g2_materialtable` (
  `MaterialID` int(11) NOT NULL AUTO_INCREMENT,
  `Title` varchar(255) DEFAULT NULL,
  `DateAdded` timestamp NULL DEFAULT NULL,
  `LastModified` timestamp NULL DEFAULT NULL,
  `Genre` varchar(255) DEFAULT NULL,
  `Author` varchar(255) DEFAULT NULL,
  `ISBN` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`MaterialID`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=latin1;

CREATE TABLE `g2_peopletable` (
  `PeopleID` int(11) NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(255) DEFAULT NULL,
  `LastName` varchar(255) DEFAULT NULL,
  `Birthdate` datetime DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `City` varchar(255) DEFAULT NULL,
  `State` varchar(255) DEFAULT NULL,
  `Zip` int(11) DEFAULT NULL,
  `PhoneNumber1` int(11) DEFAULT NULL,
  `PhoneNumber2` int(11) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`PeopleID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
