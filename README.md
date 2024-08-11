# TO-DO 
$${\color{red}DUE \space\space 8/12}$$
# Project Step 5 (Portfolio Assignment)

## Executive Summary:

- white_check_mark: 1 page (max) summary of feedback and changes made to this Project from initial version until now.
Note that this summary is different from previous steps, which asked for copy/paste of feedback and your response. We do not want to see the feedback and/or your responses from previous steps here. Just a summary.  

-   Executive summary has facts about the database design process and implementation steps. It is a reflection on major changes to this project from your initial proposal to now, and what feedback influenced those changes.  Think of the executive summary as the only thing your manager will read.
The executive summary should be at the beginning of the PDF that you turn in inside the .ZIP file.

- white_check_mark: Project and Database Outlines

-   The updated versions of the Project and Database outline. Reading these should give a layman the complete idea of your Project and its universe, and thus be able to navigate the website.

- white_check_mark: UI Screen Shots with Informative Titles

-   Screen captures of each of the UI pages on your website. Add a title immediately above each Screen capture which explains the CRUD step. E.g. "READ/BROWSE/DISPLAY Customers page" or "CREATE/INSERT/ADD NEW Invoice page." The captures should be clear and easy to read. Clearly highlight where you have implemented a) Delete from a M:N, b) NULLable relationship and c) Update of a M:N. If you do not highlight these and we overlook them when grading you will lose points, even if you have implemented them. 

:white_check_mark: ER Diagram

-   The updated version of your ERD using the notations that we use in the class should represent a logical model of your design and omit some physical level of detail compared to the Schema. The diagram should avoid crossed lines and be clear and easy to read.


:white_check_mark: Schema 

-   The updated version of the schema that should follow the database outline exactly. It will again be graded on the extent to which it matches the outline with an emphasis on if relationships and keys are set up correctly. Again, please stick to the notations that we use in the class. The diagram should avoid crossed lines and be clear and easy to read. 

:white_check_mark: Sample Data

-   3-5 rows of example data from each table in your schema should be pasted into your report. Clearly indicate from which table the data is being displayed. Data should be polite values that reasonably represent how the table works, e.g. foreign keys demonstrate 1:M relationships and intersection tables show M:N relationships in action.  

:white_check_mark: Data Definition Queries

-   The updated version of the SQL file that you provide should be cleanly import-able on the database Server that is used to host your CS340 database. Add comments at the top to describe the DDL file and make clear this file corresponds to the CS340 Portfolio Project deliverables. If the .SQL file cannot be imported or does not create tables as your Schema describes, using the database you have indicated (e.g. Maria DB), you will lose points. Well-structured, commented and hand-authored SQL files are preferrable. MySQL exports, are acceptable with team authored comments added. 

:white_check_mark: Data Manipulation Queries

-   The updated version of the SQL file which provides all your DML queries in the format described in Step 4. These queries should be consistent with those in your server-side code. Include brief comments mentioning what functionality/entity/relationship the query is related to.

:white_check_mark: Website Functionality

-   All the functionalities described in the CS340 Project Guide should be implemented, and will be assessed according to the rubric below.

-   When dealing with relationships, you cannot expect the user to manually type any data. You should allow the user to select things to relate to each other via drop-down menus or some other UI element, where the user picks from existing items to add them to a relationship. When picking items, you should display the name that makes the most sense to the user. This is very likely not the primary key. For example, in context of the BSG database, when adding a row to the relation between bsg_people and bsg_cert, we would expect the bsg_cert.title values to be shown in a dropdown/set of radio button instead of allowing entry of bsg_cert.id

-   The URL of the website should be included in the PDF as well as a comment on the submission.
READ/BROWSE/DISPLAY entities
CREATE/INSERT/ADD NEW entites
DELETE functionality (one M:N) clearly indicate where you have implemented the delete of a M:N
EDIT/UPDATE functionality (one nullable FK, update one M:N relationship) Clearly indicate where you have implemented update of one M:N relationship and NULLable relationship.
DYNAMIC DROPDOWN functionality of Search instead of picking FKs

:white_check_mark: Style

-   Website: Organization of entities and CRUD operations on the site should be logical and usable. We expect data to be displayed in tabular style and form elements should be reasonably grouped. Section headers for parts of your pages/forms would definitely make your site easier to navigate. Any design elements should assist user in understanding and locating any CRUD elements. Site navigation should not confuse. The use of white space, colors, fonts, graphic elements and/or alignment can help organize material and should be consistent and not detract from the content. Avoid errors in grammar, capitalization, punctuation, and spelling. Using html date input for dates, and highlighting required fields are examples of good quality design. 

-   PDF: Your write-up in the documentation should be well formatted and divided into sections for easy navigation and readability.

:white_check_mark: Code

-   Project code should have a sensible organization with self-documenting folders and file names. Server-side code should be divided into manageable blocks/files instead of large monolithic code blocks.  Use meaningful variable names and have brief comments to explain logic.  HTML and JavaScript files should have comments and be structured to support clarity and readability.
Citations: Any code that is not original should have a citation to clearly credit the source. IOW, if you have adapted the CS340 starter app code this should be clearly stated in the readme (e.g. "All code is based on the CS 340 starter code, with the exception of...") and also in the source code to describe the extent to which any non-original sources were used (e.g. "this module adapted from the starter code"). Highlight your original work (e.g. "update M:N entirely our own work"). If you do not cite code, then we are unable to determine the degree of originality, and a MISSING CITATION is interpreted by the instructional team as a claim that you authored the work. However, if in our review the work bears a strong resemblance to the starter code or any other code source not your own, we may likely conclude there has been a misrepresentation of your effort and skills. This means that a citation will save you from most situations that could get you in trouble with plagiarism. But if you do not cite the source of your code, and it bears a strong resemblance to the starter code or any other source, it will be assumed to be plagiarized and may be flagged for plagiarism and referred to the office of student conduct. The College of Engineering Hearing Officer (CHO) who will be in touch soon regarding the incident, and any inquiries should go to them. For more information on the process, please check the Academic Misconduct Student Resource Page. 

## Rubric
[Rubric](https://canvas.oregonstate.edu/courses/1967354/assignments/9690219)