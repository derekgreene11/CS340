# Authors: Derek Greene & Nathan Schuler
# Date: 7/2024
# Course: CS340 - Introduction to Databases

from flask import Flask, render_template, redirect, url_for, request
import pymysql
import database.db_connector as db
import os

app = Flask(__name__)
pymysql.install_as_MySQLdb()

# Route to display the home page
@app.route('/')
def root():

    return render_template('index.html')

# Route to display all designs and associated projects and associated users
@app.route('/designs')
def designs():
    db_connection = db.connect_to_database()

    # Get all designs and associated projects and users
    query = """
        SELECT d.partNumber, d.tool, d.revision, p.projectId, GROUP_CONCAT(du.userId SEPARATOR ', ') AS users
        FROM Designs d
        LEFT JOIN DesignProjects dp ON d.partNumber = dp.partNumber
        LEFT JOIN Projects p ON dp.projectId = p.projectId
        LEFT JOIN DesignUsers du ON d.partNumber = du.partNumber
        GROUP BY d.partNumber, d.tool, d.revision, p.projectId;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template('designs.html', designs=results)

# Route to add a new design
@app.route('/add_design', methods=['GET', 'POST'])
def add_design():
    db_connection = db.connect_to_database()
    if request.method == 'POST':

        # Get form data
        part_number = request.form['partNumber']
        tool = request.form['tool']
        revision = request.form.get('revision', None)
        project_id = request.form['projectId']
        user_ids = request.form.getlist('userIds')

        # Insert design into the database
        query = "INSERT INTO Designs (partNumber, tool, revision) VALUES (%s, %s, %s);"
        try:
            db.execute_query(db_connection=db_connection, query=query, query_params=(part_number, tool, revision))
            db_connection.commit()

            # Associate design with a project
            query = "INSERT INTO DesignProjects (partNumber, projectId) VALUES (%s, %s);"
            db.execute_query(db_connection=db_connection, query=query, query_params=(part_number, project_id))
            db_connection.commit()

            # Associate users with the design
            for user_id in user_ids:
                query = "INSERT INTO DesignUsers (partNumber, userId) VALUES (%s, %s);"
                db.execute_query(db_connection=db_connection, query=query, query_params=(part_number, user_id))
                db_connection.commit()
            return redirect(url_for('designs'))
        except Exception as e:
            print(f"Error: {e}")

            return "There was an error adding the design.", 500
        
    query = "SELECT projectId FROM Projects;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    projects = cursor.fetchall()
    query = "SELECT userId FROM Users;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    users = cursor.fetchall()

    return render_template('add_design.html', projects=projects, users=users)

# Route to edit a design
@app.route('/edit_design/<int:part_number>', methods=['GET', 'POST'])
def edit_design(part_number):
    db_connection = db.connect_to_database()
    if request.method == 'POST':

        # Get form data
        tool = request.form['tool']
        revision = request.form.get('revision', None)
        project_id = request.form['projectId']
        user_ids = request.form.getlist('userIds')
        query = "UPDATE Designs SET tool = %s, revision = %s WHERE partNumber = %s;"
        try:
            db.execute_query(db_connection=db_connection, query=query, query_params=(tool, revision, part_number))
            db_connection.commit()

            # Update DesignProjects
            query = "DELETE FROM DesignProjects WHERE partNumber = %s;"
            db.execute_query(db_connection=db_connection, query=query, query_params=(part_number,))
            db_connection.commit()
            if project_id:
                query = "INSERT INTO DesignProjects (partNumber, projectId) VALUES (%s, %s);"
                db.execute_query(db_connection=db_connection, query=query, query_params=(part_number, project_id))
                db_connection.commit()

            # Update DesignUsers
            query = "DELETE FROM DesignUsers WHERE partNumber = %s;"
            db.execute_query(db_connection=db_connection, query=query, query_params=(part_number,))
            db_connection.commit()
            if user_ids:
                if "" in user_ids:

                    # Ensure that no users are associated if "None" is selected
                    query = "DELETE FROM DesignUsers WHERE partNumber = %s;"
                    db.execute_query(db_connection=db_connection, query=query, query_params=(part_number,))
                    db_connection.commit()
                else:
                    for user_id in user_ids:
                        query = "INSERT INTO DesignUsers (partNumber, userId) VALUES (%s, %s);"
                        db.execute_query(db_connection=db_connection, query=query, query_params=(part_number, user_id))
                    db_connection.commit()
            return redirect(url_for('designs'))
        except Exception as e:
            print(f"Error: {e}")

            return "There was an error editing the design.", 500
    else:

        # Get design details for the form
        query = "SELECT * FROM Designs WHERE partNumber = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(part_number,))
        design = cursor.fetchone()

        # Get projects and users for the form
        query = "SELECT projectId FROM Projects;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        projects = cursor.fetchall()
        query = "SELECT userId FROM Users;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        users = cursor.fetchall()
        query = "SELECT userId FROM DesignUsers WHERE partNumber = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(part_number,))
        design_users = cursor.fetchall()
        design_user_ids = [user['userId'] for user in design_users]

        return render_template('edit_design.html', design=design, projects=projects, users=users, design_user_ids=design_user_ids)

# Route to delete a design    
@app.route('/delete_design/<int:part_number>')
def delete_design(part_number):
    query = "DELETE FROM Designs WHERE partNumber = %s;"
    db_connection = db.connect_to_database()
    try:
        db.execute_query(db_connection=db_connection, query=query, query_params=(part_number,))
        db_connection.commit()
        return redirect(url_for('designs'))
    except Exception as e:
        print(f"Error: {e}")

        return "There was an error deleting the design.", 500

# Route to display all requirements and associated projects
@app.route('/requirements')
def requirements():
    db_connection = db.connect_to_database()

    # Get all requirements
    query = "SELECT * FROM Requirements;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    requirements = cursor.fetchall()

    for requirement in requirements:
        query = """
        SELECT p.projectId, p.projectStatus
        FROM Projects p
        JOIN ProjectRequirements pr ON p.projectId = pr.projectId
        WHERE pr.requirementId = %s;
        """
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(requirement['requirementId'],))
        requirement['projects'] = cursor.fetchall()

    return render_template('requirements.html', requirements=requirements)

# Route to add a requirement
@app.route('/add_requirement', methods=['GET', 'POST'])
def add_requirement():
    db_connection = db.connect_to_database()
    if request.method == 'POST':
        try:
            level = request.form['level']
            project_id = request.form['projectId']

            # Insert requirement into the database
            query = "INSERT INTO Requirements (level) VALUES (%s);"
            db.execute_query(db_connection=db_connection, query=query, query_params=(level,))
            db_connection.commit()

            # Get ID of the new requirement
            query = "SELECT LAST_INSERT_ID() AS requirementId;"
            cursor = db.execute_query(db_connection=db_connection, query=query)
            result = cursor.fetchone()
            requirement_id = result['requirementId']
            
            # Associate the requirement with a project
            if project_id:
                query = "INSERT INTO ProjectRequirements (projectId, requirementId) VALUES (%s, %s);"
                db.execute_query(db_connection=db_connection, query=query, query_params=(project_id, requirement_id))
                db_connection.commit()

            return redirect(url_for('requirements'))
        except Exception as e:
            print(f"Error: {e}")

            return "There was an error adding the requirement.", 500
        
    query = "SELECT projectId FROM Projects;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    projects = cursor.fetchall()
    levels = ["Low", "Medium", "High"]
    000
    return render_template('add_requirement.html', projects=projects, levels=levels)

# Route to edit a requirement
@app.route('/edit_requirement/<int:requirement_id>', methods=['GET', 'POST'])
def edit_requirement(requirement_id):
    db_connection = db.connect_to_database()
    if request.method == 'POST':
        try:
            level = request.form['level']
            project_id = request.form.get('projectId', None)

            # Update requirement details
            query = "UPDATE Requirements SET level = %s WHERE requirementId = %s;"
            db.execute_query(db_connection=db_connection, query=query, query_params=(level, requirement_id))
            db_connection.commit()

            # Update project associations
            query = "DELETE FROM ProjectRequirements WHERE requirementId = %s;"
            db.execute_query(db_connection=db_connection, query=query, query_params=(requirement_id,))
            db_connection.commit()
            if project_id:
                query = "INSERT INTO ProjectRequirements (projectId, requirementId) VALUES (%s, %s);"
                db.execute_query(db_connection=db_connection, query=query, query_params=(project_id, requirement_id))
                db_connection.commit()
            return redirect(url_for('requirements'))
        except Exception as e:
            print(f"Error: {e}")

            return "There was an error editing the requirement.", 500
    else:
        query = "SELECT * FROM Requirements WHERE requirementId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(requirement_id,))
        requirement = cursor.fetchone()
        query = "SELECT * FROM Projects;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        projects = cursor.fetchall()
        query = "SELECT projectId FROM ProjectRequirements WHERE requirementId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(requirement_id,))
        associated_project = cursor.fetchone()
        associated_project_id = associated_project['projectId'] if associated_project else None
        levels = ["Low", "Medium", "High"]

        return render_template('edit_requirement.html', requirement=requirement, projects=projects, associated_project_id=associated_project_id, levels=levels)

# Route to delete a requirement
@app.route('/delete_requirement/<int:requirement_id>')
def delete_requirement(requirement_id):
    query = "DELETE FROM Requirements WHERE requirementId = %s;"
    db_connection = db.connect_to_database()
    try:
        db.execute_query(db_connection=db_connection, query=query, query_params=(requirement_id,))
        db_connection.commit() 
        return redirect(url_for('requirements'))
    except Exception as e:
        print(f"Error: {e}")

        return "There was an error deleting the requirement.", 500

# Route to display all projects and assocated users and designs
@app.route('/projects')
def projects():
    db_connection = db.connect_to_database()
    try:

        # Get all projects
        query_projects = """
            SELECT p.projectId, p.projectStatus
            FROM Projects p;
        """
        cursor_projects = db.execute_query(db_connection=db_connection, query=query_projects)
        all_projects = cursor_projects.fetchall()

        # Get projects with associated users
        query_user_projects = """
            SELECT p.projectId, p.projectStatus, u.userId, u.firstName, u.lastName
            FROM Projects p
            LEFT JOIN UserProjects up ON p.projectId = up.projectId
            LEFT JOIN Users u ON up.userId = u.userId
            ORDER BY p.projectId, u.userId;
        """
        cursor_user_projects = db.execute_query(db_connection=db_connection, query=query_user_projects)
        user_projects = cursor_user_projects.fetchall()

        # Group projects with associated users
        grouped_projects = {}
        for project in all_projects:
            project_id = project['projectId']
            if project_id not in grouped_projects:
                grouped_projects[project_id] = {
                    'projectStatus': project['projectStatus'],
                    'users': []
                }
        for project in user_projects:
            project_id = project['projectId']
            if project_id in grouped_projects:
                user_id = project['userId']
                if user_id:
                    if not any(user['userId'] == user_id for user in grouped_projects[project_id]['users']):
                        grouped_projects[project_id]['users'].append({
                            'userId': user_id,
                            'name': f"{project['firstName']} {project['lastName']}"
                        })

        return render_template('projects.html', grouped_projects=grouped_projects)
    
    except Exception as e:
        print(f"Error: {e}")

        return "There was an error fetching the projects.", 500

# Route to add a project     
@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    db_connection = db.connect_to_database()
    if request.method == 'POST':

        # Get form data
        project_status = request.form['projectStatus']
        selected_part_numbers = request.form.getlist('partNumbers')
        selected_users = request.form.getlist('users')

        # Insert project into the database
        query = "INSERT INTO Projects (projectStatus) VALUES (%s);"
        db.execute_query(db_connection=db_connection, query=query, query_params=(project_status,))
        db_connection.commit()

        # Get ID of new project
        query = "SELECT LAST_INSERT_ID() AS projectId;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        result = cursor.fetchone()
        project_id = result['projectId']

        # Associate parts with project
        if selected_part_numbers:
            query = "INSERT INTO DesignProjects (partNumber, projectId) VALUES (%s, %s);"
            for part_number in selected_part_numbers:
                db.execute_query(db_connection=db_connection, query=query, query_params=(part_number, project_id))
            db_connection.commit()

        # Associate users with project
        if selected_users:
            query = "INSERT INTO UserProjects (userId, projectId) VALUES (%s, %s);"
            for user_id in selected_users:
                db.execute_query(db_connection=db_connection, query=query, query_params=(user_id, project_id))
            db_connection.commit()

        return redirect(url_for('projects'))
    
    # Get users and parts for the form options
    query_users = "SELECT userId, firstName, lastName FROM Users;"
    cursor_users = db.execute_query(db_connection=db_connection, query=query_users)
    users = cursor_users.fetchall()
    query_parts = "SELECT DISTINCT partNumber FROM Designs;"
    cursor_parts = db.execute_query(db_connection=db_connection, query=query_parts)
    parts = cursor_parts.fetchall()

    return render_template('add_project.html', users=users, parts=parts)

# Route to edit a project
@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    db_connection = db.connect_to_database()
    if request.method == 'POST':

        # Get form data
        project_status = request.form['projectStatus']
        selected_users = request.form.getlist('users')
        selected_part_numbers = request.form.getlist('partNumbers')
        try:

            # Update project details
            query = "UPDATE Projects SET projectStatus = %s WHERE projectId = %s;"
            db.execute_query(db_connection=db_connection, query=query, query_params=(project_status, project_id))
            db_connection.commit()

            # Update user associations
            query = "DELETE FROM UserProjects WHERE projectId = %s;"
            db.execute_query(db_connection=db_connection, query=query, query_params=(project_id,))
            db_connection.commit()
            if selected_users and selected_users[0]:
                query = "INSERT INTO UserProjects (userId, projectId) VALUES (%s, %s);"
                for user_id in selected_users:
                    if user_id: 
                        db.execute_query(db_connection=db_connection, query=query, query_params=(user_id, project_id))
                db_connection.commit()

            # Update part associations
            query = "DELETE FROM DesignProjects WHERE projectId = %s;"
            db.execute_query(db_connection=db_connection, query=query, query_params=(project_id,))
            db_connection.commit()
            if selected_part_numbers:
                query = "INSERT INTO DesignProjects (partNumber, projectId) VALUES (%s, %s);"
                for part_number in selected_part_numbers:
                    db.execute_query(db_connection=db_connection, query=query, query_params=(part_number, project_id))
                db_connection.commit()

            return redirect(url_for('projects'))
        
        except Exception as e:
            print(f"Error: {e}")

            return "There was an error updating the project.", 500
    else:
        # Get project details for the form
        query = "SELECT * FROM Projects WHERE projectId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(project_id,))
        project = cursor.fetchone()

        # Get current part and user associations
        query = "SELECT partNumber FROM DesignProjects WHERE projectId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(project_id,))
        project_parts = [row['partNumber'] for row in cursor.fetchall()]
        query = "SELECT userId, firstName, lastName FROM Users;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        users = cursor.fetchall()
        query = "SELECT userId FROM UserProjects WHERE projectId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(project_id,))
        assigned_users = [row['userId'] for row in cursor.fetchall()]
        query = "SELECT DISTINCT partNumber FROM Designs;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        parts = cursor.fetchall()
        return render_template('edit_project.html', project=project, users=users, assigned_users=assigned_users, parts=parts, project_parts=project_parts)

# Route to delete a project
@app.route('/delete_project/<int:project_id>')
def delete_project(project_id):
    query = "DELETE FROM Projects WHERE projectId = %s;"
    db_connection = db.connect_to_database()
    db.execute_query(db_connection=db_connection, query=query, query_params=(project_id,))
    db_connection.commit()

    return redirect(url_for('projects'))

# Route to display all users
@app.route('/users')
def users():
    db_connection = db.connect_to_database()

    # Get all users
    query = "SELECT * FROM Users;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template('users.html', users=results)

# Route to add a user
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':

        # Get form data
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        discipline = request.form['discipline']

        # Insert user into the database
        query = "INSERT INTO Users (firstName, lastName, discipline) VALUES (%s, %s, %s);"
        db_connection = db.connect_to_database()
        db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, discipline))
        db_connection.commit()

        return redirect(url_for('users'))
    
    return render_template('add_user.html')

# Route to edit a user
@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':

        # Get form data
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        discipline = request.form['discipline']

        # Update user details
        query = "UPDATE Users SET firstName = %s, lastName = %s, discipline = %s WHERE userId = %s;"
        db_connection = db.connect_to_database()
        db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, discipline, user_id))
        db_connection.commit()

        return redirect(url_for('users'))
    else:

        # Get user details for the form
        query = "SELECT * FROM Users WHERE userId = %s;"
        db_connection = db.connect_to_database()
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(user_id,))
        user = cursor.fetchone()

        return render_template('edit_user.html', user=user)

# Route to delete a user    
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    query = "DELETE FROM Users WHERE userId = %s;"
    db_connection = db.connect_to_database()
    db.execute_query(db_connection=db_connection, query=query, query_params=(user_id,))
    db_connection.commit()
    return redirect(url_for('users'))

# Listener
if __name__ == "__main__":
    app.run(host='', port=os.environ.get("340PORT"), debug=False)