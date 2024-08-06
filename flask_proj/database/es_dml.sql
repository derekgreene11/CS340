-- Authors: Derek Greene & Nathan Schuler
-- Date: 7/2024
-- Course: CS340 - Introduction to Databases
-- Description: This file the SQL queries used in the Engineering Services Database Flask App.

-- ******************** CRUD ***************************
-- C(reate):
-- Used in the add_design form to add a new design
INSERT INTO Designs (partNumber, tool, revision) VALUES (%s, %s, %s);

-- Used in the add_requirement form to add a new requirement
INSERT INTO Requirements (level) VALUES (%s);

-- Used in the add_project form to add a new project
INSERT INTO Projects (projectStatus) VALUES (%s);

-- Used in the add_user form to add a new user
INSERT INTO Users (firstName, lastName, discipline) VALUES (%s, %s, %s);

-- Associate a user with a project
INSERT INTO UserProjects (userId, projectId) VALUES (%s, %s);

-- Associate a requirement with a project
INSERT INTO ProjectRequirements (projectId, requirementId) VALUES (%s, %s);

-- Insert partNumber and projectID into DesignProjects
INSERT INTO DesignProjects (partNumber, projectId) VALUES (%s, %s);

-- Insert partNumber and userID into DesignUsers
INSERT INTO DesignUsers (partNumber, userId) VALUES (%s, %s);

-- R(ead):
-- Fetch all designs with associated projects and users
SELECT d.partNumber, d.tool, d.revision, p.projectId, GROUP_CONCAT(du.userId SEPARATOR ', ') AS users
FROM Designs d
LEFT JOIN DesignProjects dp ON d.partNumber = dp.partNumber
LEFT JOIN Projects p ON dp.projectId = p.projectId
LEFT JOIN DesignUsers du ON d.partNumber = du.partNumber
GROUP BY d.partNumber, d.tool, d.revision, p.projectId;

-- Fetch all requirements
SELECT * FROM Requirements;

-- Fetch all users
SELECT * FROM Users;

-- Fetch all projects
SELECT * FROM Projects

-- Fetch all designs
SELECT * FROM Designs

-- Fetch all users with their ID, first name, and last name
SELECT userId, firstName, lastName FROM Users;

-- Fetch all projects with their associated users
SELECT p.projectId, p.projectStatus, u.userId, u.firstName, u.lastName
FROM Projects p
LEFT JOIN UserProjects up ON p.projectId = up.projectId
LEFT JOIN Users u ON up.userId = u.userId
ORDER BY p.projectId, u.userId;

-- Fetch all requirements with their associated projects
SELECT r.requirementId, r.level, p.projectId, p.projectStatus
FROM Requirements r
LEFT JOIN ProjectRequirements pr ON r.requirementId = pr.requirementId
LEFT JOIN Projects p ON pr.projectId = p.projectId
ORDER BY r.requirementId, p.projectId;

-- Fetch all designs by partNumber
SELECT * FROM Designs WHERE partNumber = %s;

-- Fetch all requirements by requirementId
SELECT * FROM Requirements WHERE requirementId = %s;

-- Fetch all projects by projectId
SELECT * FROM Projects WHERE projectId = %s;

-- Fetch all users by userId
SELECT * FROM Users WHERE userId = %s;

-- Fetch all projects and their associated users
SELECT p.projectId, p.projectStatus, u.userId, u.firstName, u.lastName
FROM Projects p
LEFT JOIN UserProjects up ON p.projectId = up.projectId
LEFT JOIN Users u ON up.userId = u.userId
ORDER BY p.projectId, u.userId;

-- Fetch all requirements and their associated projects
SELECT r.requirementId, r.level, p.projectId, p.projectStatus
FROM Requirements r
LEFT JOIN ProjectRequirements pr ON r.requirementId = pr.requirementId
LEFT JOIN Projects p ON pr.projectId = p.projectId
ORDER BY r.requirementId, p.projectId;

-- Fetch all part numbers associated with a project
SELECT partNumber FROM DesignProjects WHERE projectId = %s;

-- Fetch all user IDs associated with a project
SELECT userId FROM UserProjects WHERE projectId = %s;

-- Fetcj all user IDs associated with a design
SELECT userId FROM DesignUsers WHERE partNumber = %s;

-- Fetch all parts associated with a project
SELECT DISTINCT partNumber FROM Designs WHERE partNumber IN (SELECT partNumber FROM DesignProjects WHERE projectId = %s);

-- Fetch all users associated with a project
SELECT u.userId, u.firstName, u.lastName FROM Users u
JOIN UserProjects up ON u.userId = up.userId
WHERE up.projectId = %s;

-- Fetch all project IDs associated with a requirement
SELECT projectId FROM ProjectRequirements WHERE requirementId = %s;

-- Fetch all project IDs from Projects
SELECT projectId FROM Projects;

-- Fetch all user IDs from Users
SELECT userId FROM Users;

-- U(pdate):
-- Update a design
UPDATE Designs SET tool = %s, revision = %s WHERE partNumber = %s;

-- Update a requirement
UPDATE Requirements SET level = %s WHERE requirementId = %s;

-- Update a project
UPDATE Projects SET projectStatus = %s WHERE projectId = %s;

-- Update a user
UPDATE Users SET firstName = %s, lastName = %s, discipline = %s WHERE userId = %s;

-- D(elete):
-- Delete a design
DELETE FROM Designs WHERE partNumber = %s;

-- Delete a design from DesignProjects
DELETE FROM DesignProjects WHERE partNumber = %s;

-- Delete a design from DesignUsers
DELETE FROM DesignUsers WHERE partNumber = %s;

-- Delete a requirement
DELETE FROM Requirements WHERE requirementId = %s;

-- Delete a requirement from ProjectRequirements
DELETE FROM ProjectRequirements WHERE requirementId = %s;

-- Delete a project
DELETE FROM Projects WHERE projectId = %s;

-- Delete a user
DELETE FROM Users WHERE userId = %s;

-- Delete all user projects associated with a project
DELETE FROM UserProjects WHERE projectId = %s;

-- Delete all design projects associated with a project
DELETE FROM DesignProjects WHERE projectId = %s;