-- ":" used to denote variables that will be input by the user

-- ******************** CRUD ***************************
-- C(reate):
-- Used in the add_design form to add a new design
INSERT INTO Designs (partNumber, tool, revision) VALUES (:partNumber_input, :tool_input, :revision_input)
-- Used in the add_requirement form to add a new requirement
INSERT INTO Requirements (level) VALUES (:level_input);
-- Used in the add_project form to add a new project
INSERT INTO Projects (projectStatus) VALUES (:projectStatus_input);
-- Used in the add_user form to add a new user
INSERT INTO Users (firstName, lastName, discipline) VALUES (:firstName_input, :lastName_input, :discipline_input);

-- R(ead):
-- used to display all the designs, projects, users, and requirements
SELECT * FROM Designs; 
SELECT * FROM Projects;
SELECT * FROM Users;
SELECT * FROM Requirements;

-- U(pdate)
-- used in the edit_design form to update a design
UPDATE Designs SET tool = :tool_input, revision = :revision_input WHERE partNumber = :partNumber_input;
-- used in the edit_requirement form to update a requirement
UPDATE Requirements SET level = :level_input WHERE requirementId = :requirementId_input;
-- used in the edit_project form to update a project
UPDATE Projects SET projectStatus = :projectStatus_input WHERE projectId = :projectId_input;
-- used in the edit_user form to update a user
UPDATE Users SET firstName = :firstName_input, lastName = :lastName_input, discipline = :discipline_input WHERE userId = :userId_input;

-- D(elete):
-- used to delete a design, part_number is passed in the URL route
DELETE FROM Designs WHERE partNumber = :partNumber_input
-- used to delete a requirement, requirement_id is passed in the URL route
DELETE FROM Requirements WHERE requirementId = :requirementId_input;
-- used to delete a project, project_id is passed in the URL route
DELETE FROM Projects WHERE projectId = :projectId_input;
-- used to delete a user, user_id is passed in the URL route
DELETE FROM Users WHERE userId = :userId_input;