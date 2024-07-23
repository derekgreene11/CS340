SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Requirements;
DROP TABLE IF EXISTS Projects;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Designs;
DROP TABLE IF EXISTS ProjectRequirements;
DROP TABLE IF EXISTS UserProjects;
DROP TABLE IF EXISTS DesignProjects;
DROP TABLE IF EXISTS DesignUsers;
SET FOREIGN_KEY_CHECKS = 1;

-- Requirements table
CREATE TABLE Requirements (
    requirementId int(11) NOT NULL AUTO_INCREMENT,
    level ENUM('low', 'medium', 'high') NOT NULL,
    PRIMARY KEY (requirementId)
);

-- Projects table
CREATE TABLE Projects (
    projectId int(11) NOT NULL AUTO_INCREMENT,
    projectStatus ENUM('Not started', 'In process', 'On hold', 'Completed', 'Canceled') NOT NULL,
    PRIMARY KEY (projectId)
);

-- Users table
CREATE TABLE Users (
    userId int(11) NOT NULL AUTO_INCREMENT,
    firstName varchar(255) NOT NULL,
    lastName varchar(255) NOT NULL,
    discipline ENUM('Mechanical Engineering', 'Architecture', 'Software Engineering', 'Electrical Engineering', 'Other') NOT NULL,
    PRIMARY KEY (userId),
    UNIQUE KEY fullName (firstName, lastName)
);

-- Designs table
CREATE TABLE Designs (
    partNumber int(11) NOT NULL AUTO_INCREMENT,
    revision int(11) DEFAULT NULL,
    tool varchar(255) NOT NULL,
    PRIMARY KEY (partNumber)
);

-- Project-Requirement intersection table
CREATE TABLE ProjectRequirements (
    projectId int(11) NOT NULL,
    requirementId int(11) NOT NULL,
    PRIMARY KEY (projectId, requirementId),
    FOREIGN KEY (projectId) REFERENCES Projects(projectId),
    FOREIGN KEY (requirementId) REFERENCES Requirements(requirementId)
);

-- User-Project intersection table
CREATE TABLE UserProjects (
    userId int(11) NOT NULL,
    projectId int(11) NOT NULL,
    PRIMARY KEY (userId, projectId),
    FOREIGN KEY (userId) REFERENCES Users(userId),
    FOREIGN KEY (projectId) REFERENCES Projects(projectId)
);

-- Design-Project intersection table
CREATE TABLE DesignProjects (
    partNumber int(11) NOT NULL,
    projectId int(11) NOT NULL,
    PRIMARY KEY (partNumber, projectId),
    FOREIGN KEY (partNumber) REFERENCES Designs(partNumber),
    FOREIGN KEY (projectId) REFERENCES Projects(projectId)
);

-- Design-User intersection table
CREATE TABLE DesignUsers (
    partNumber int(11) NOT NULL,
    userId int(11) NOT NULL,
    PRIMARY KEY (partNumber, userId),
    FOREIGN KEY (partNumber) REFERENCES Designs(partNumber),
    FOREIGN KEY (userId) REFERENCES Users(userId)
);

-- Insert sample data into Requirements table
INSERT INTO Requirements (requirementId, level) VALUES
(1, 'low'), (2, 'low'), (3, 'high'), (4, 'medium'), (5, 'medium'),
(6, 'low'), (7, 'high'), (8, 'high'), (9, 'high'), (10, 'medium'), (11, 'low');

-- Insert sample data into Projects table
INSERT INTO Projects (projectId, projectStatus) VALUES
(126, 'Not started'), (152, 'Not started'), (364, 'Completed'), (315, 'On hold'),
(155, 'Canceled'), (332, 'Completed'), (416, 'On hold'), (598, 'Not started'),
(655, 'Canceled'), (285, 'Completed'), (632, 'Completed');

-- Insert sample data into Users table
INSERT INTO Users (userId, firstName, lastName, discipline) VALUES
(24913, 'John', 'Doe', 'Mechanical Engineering'), (35682, 'Jane', 'Smith', 'Software Engineering'),
(27795, 'Bob', 'Johnson', 'Software Engineering'), (24614, 'Alice', 'Williams', 'Electrical Engineering'),
(18502, 'Tom', 'Brown', 'Other'), (30562, 'Emma', 'Jones', 'Software Engineering'),
(18832, 'James', 'Garcia', 'Architecture'), (35562, 'Emily', 'Martinez', 'Other'),
(5526, 'Michael', 'Rodriguez', 'Software Engineering'), (26553, 'Sarah', 'Davis', 'Mechanical Engineering'),
(14732, 'David', 'Lopez', 'Mechanical Engineering');

-- Insert sample data into Designs table
INSERT INTO Designs (partNumber, revision, tool) VALUES
(256413432, NULL, 'CAD'), (544545123, NULL, 'Revit'), (869178821, NULL, 'CAD'),
(238464815, 1, 'CAD'), (535654652, 3, 'CAD'), (498743514, NULL, 'Revit'),
(494651565, 7, 'CAD'), (489655316, 2, 'CAD'), (203248465, NULL, 'CAD'),
(335454554, 1, 'CAD'), (854564553, 4, 'CAD');

-- Insert sample data into ProjectRequirements table
INSERT INTO ProjectRequirements (projectId, requirementId)
SELECT p.projectId, r.requirementId
FROM Projects p, Requirements r;

-- Insert sample data into UserProjects table
INSERT INTO UserProjects (userId, projectId)
SELECT u.userId, p.projectId
FROM Users u, Projects p;

-- Insert sample data into DesignProjects table
INSERT INTO DesignProjects (partNumber, projectId)
SELECT d.partNumber, p.projectId
FROM Designs d, Projects p;

-- Insert sample data into DesignUsers table
INSERT INTO DesignUsers (partNumber, userId)
SELECT d.partNumber, u.userId
FROM Designs d, Users u;