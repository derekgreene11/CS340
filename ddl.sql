SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Requirments;
DROP TABLE IF EXISTS Projects;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Designs;
SET FOREIGN_KEY_CHECKS = 1;

-- Table structure for table `Requirments`

CREATE TABLE `Requirments` (
`requirmentId` int(11) NOT NULL AUTO_INCREMENT,
`partNumber` int(11) NOT NULL,
`projectId` int(11) DEFAULT NULL,
`level` ENUM('low', 'medium', 'high') NOT NULL,
PRIMARY KEY (`requirmentId`),
KEY `partNumber` (`partNumber`),
KEY `projectId` (`projectId`)
) ENGINE=InnoDB;

-- Dumping sample data for table `Requirments`

INSERT INTO `Requirments` (`requirmentId`, `partNumber`, `projectId`, `level`) VALUES
(001, 256413432, 126, 'low'),
(002, 544545123, 152, 'low'),
(003, 869178821, 364, 'high'),
(004, 238464815, 315, 'medium'),
(005, 535654652, 155, 'medium'),
(006, 498743514, 332, 'low'),
(007, 494651565, 416, 'high'),
(008, 489655316, 598, 'high'),
(009, 203248465, 655, 'high'),
(010, 335454554, 285, 'medium'),
(011, 854564553, 632, 'low');

-- Table structure for table `Projects`

CREATE TABLE `Projects` (
`projectId` int(11) NOT NULL AUTO_INCREMENT,
`partNumber` int(11) NOT NULL,
`requirmentId` int(11) NOT NULL,
`userId` int(11) NOT NULL,
`projectStatus` ENUM('Not started', 'In process', 'On hold', 'Completed', 'Canceled') NOT NULL,
PRIMARY KEY (`projectId`),
KEY `partNumber` (`partNumber`),
KEY `requirmentId` (`requirmentId`),
KEY `userId` (`userId`)
) ENGINE=InnoDB;

-- Dumping sample data for table `Projects`

INSERT INTO `Projects` (`projectId`, `partNumber`, `requirmentId`, `userId`, `projectStatus`) VALUES
(126, 256413432, 001, 24913, 'Not started'),
(152, 544545123, 002, 35682, 'Not started'),
(364, 869178821, 003, 27795, 'Completed'),
(315, 238464815, 004, 24614, 'On hold'),
(155, 535654652, 005, 18502, 'Canceled'),
(332, 498743514, 006, 30562, 'Completed'),
(416, 494651565, 007, 18832, 'On hold'),
(598, 489655316, 008, 35562, 'Not started'),
(655, 203248465, 009, 05526, 'Canceled'),
(285, 335454554, 010, 26553, 'Completed'),
(632, 854564553, 011, 14732, 'Completed');

-- Table structure for table `Users`

CREATE TABLE `Users` (
`userId` int(11) NOT NULL AUTO_INCREMENT,
`projectId` int(11) DEFAULT NULL,
`partNumber` int(11) NOT NULL,
`discipline` ENUM('Mechanical Engineering', 'Architecture', 'Software Engineering', 'Electrical Engineering', 'Other') NOT NULL,
PRIMARY KEY (`userId`),
KEY `projectId` (`projectId`),
KEY `partNumber` (`partNumber`)
) ENGINE=InnoDB;

-- Dumping sample data for table `Users`

INSERT INTO `Users` (`userId`, `projectId`, `partNumber`, `discipline`) VALUES
(24913, 126, 256413432, 'Mechanical Engineering'),
(35682, 152, 544545123, 'Software Engineering'),
(27795, 364, 869178821, 'Software Engineering'),
(24614, 315, 238464815, 'Electrical Engineering'),
(18502, 155, 535654652, 'Other'),
(30562, 332, 498743514, 'Software Engineering'),
(18832, 416, 494651565, 'Architecture'),
(35562, 598, 489655316, 'Other'),
(05526, 655, 203248465, 'Software Engineering'),
(26553, 285, 335454554, 'Mechanical Engineering'),
(14732, 632, 854564553, 'Mechanical Engineering');

-- Table structure for table `Designs`

CREATE TABLE `Designs` (
`partNumber` int(11) NOT NULL AUTO_INCREMENT,
`requirmentId` int(11) NOT NULL,
`projectId` int(11) NOT NULL,
`userId` int(11) DEFAULT NULL, 
`revision` int(11) DEFAULT NULL, 
`discipline` ENUM('Mechanical Engineering', 'Architecture', 'Software Engineering', 'Electrical Engineering', 'Other') NOT NULL,
`tool` varchar(255) NOT NULL,
PRIMARY KEY (`partNumber`),
KEY `requirmentId` (`requirmentId`),
KEY `projectId` (`projectId`)
) ENGINE=InnoDB;

-- Dumping sample data for table `Designs`

INSERT INTO `Designs` (`partNumber`, `requirmentId`, `projectId`, `userId`, `revision`, `discipline`, `tool`) VALUES
(256413432, 001, 126, 24913, NULL, 'Mechanical Engineering', 'CAD'),
(544545123, 002, 152, 35682, NULL, 'Software Engineering', 'Revit'),
(869178821, 003, 364, 27795, NULL, 'Software Engineering', 'CAD'),
(238464815, 004, 315, 24614, 1, 'Electrical Engineering', 'CAD'),
(535654652, 005, 155, 18502, 3, 'Other', 'CAD'),
(498743514, 006, 332, 30562, NULL, 'Software Engineering', 'Revit'),
(494651565, 007, 416, 18832, 7, 'Architecture', 'CAD'),
(489655316, 008, 598, 35562, 2, 'Other', 'CAD'),
(203248465, 009, 655, 05526, NULL, 'Software Engineering', 'CAD'),
(335454554, 010, 285, 26553, 1, 'Mechanical Engineering', 'CAD'),
(854564553, 011, 632, 14732, 4, 'Mechanical Engineering', 'CAD');