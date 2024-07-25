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

-- R(ead):
-- Used to display all the designs
SELECT d.partNumber, d.tool, d.revision, p.projectId
FROM Designs d
LEFT JOIN DesignProjects dp ON d.partNumber = dp.partNumber
LEFT JOIN Projects p ON dp.projectId = p.projectId;

-- Used to display all the requirements
SELECT * FROM Requirements;

-- Used to display all the users
SELECT * FROM Users;

-- Used to display all the projects and the users assigned to each
SELECT 
    u.userId,
    u.firstName,
    u.lastName,
    p.projectId,
    p.projectStatus
FROM 
    Users u
JOIN 
    UserProjects up ON u.userId = up.userId
JOIN 
    Projects p ON up.projectId = p.projectId
ORDER BY 
    u.userId, p.projectId;

-- Used to display all the requirements and their associated projects
SELECT 
    r.requirementId,
    r.level,
    p.projectId,
    p.projectStatus
FROM 
    Requirements r
LEFT JOIN 
    ProjectRequirements pr ON r.requirementId = pr.requirementId
LEFT JOIN 
    Projects p ON pr.projectId = p.projectId
ORDER BY 
    r.requirementId, p.projectId;

-- U(pdate):
-- Used in the edit_design form to update a design
UPDATE Designs SET tool = %s, revision = %s WHERE partNumber = %s;

-- Used in the edit_requirement form to update a requirement
UPDATE Requirements SET level = %s WHERE requirementId = %s;

-- Used in the edit_project form to update a project
UPDATE Projects SET projectStatus = %s WHERE projectId = %s;

-- Used in the edit_user form to update a user
UPDATE Users SET firstName = %s, lastName = %s, discipline = %s WHERE userId = %s;

-- D(elete):
-- Used to delete a design
DELETE FROM Designs WHERE partNumber = %s;

-- Used to delete a requirement
DELETE FROM Requirements WHERE requirementId = %s;

-- Used to delete a project
DELETE FROM Projects WHERE projectId = %s;

-- Used to delete a user
DELETE FROM Users WHERE userId = %s;