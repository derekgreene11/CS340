from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL
import database.db_connector as db
import os

app = Flask(__name__)
mysql = MySQL(app)

# Routes
@app.route('/')
def root():
    return render_template('index.html')

@app.route('/designs')
def designs():
    db_connection = db.connect_to_database()
    query = """
        SELECT d.partNumber, d.tool, d.revision, p.projectId
        FROM Designs d
        LEFT JOIN DesignProjects dp ON d.partNumber = dp.partNumber
        LEFT JOIN Projects p ON dp.projectId = p.projectId;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('designs.html', designs=results)

@app.route('/add_design', methods=['GET', 'POST'])
def add_design():
    if request.method == 'POST':
        part_number = request.form['partNumber']
        tool = request.form['tool']
        revision = request.form.get('revision', None)
        query = "INSERT INTO Designs (partNumber, tool, revision) VALUES (%s, %s, %s);"
        db_connection = db.connect_to_database()
        try:
            db.execute_query(db_connection=db_connection, query=query, query_params=(part_number, tool, revision))
            db_connection.commit()
            return redirect(url_for('designs'))
        except Exception as e:
            print(f"Error: {e}")
            return "There was an error adding the design.", 500
    return render_template('add_design.html')

@app.route('/edit_design/<int:part_number>', methods=['GET', 'POST'])
def edit_design(part_number):
    if request.method == 'POST':
        tool = request.form['tool']
        revision = request.form.get('revision', None)
        query = "UPDATE Designs SET tool = %s, revision = %s WHERE partNumber = %s;"
        db_connection = db.connect_to_database()
        try:
            db.execute_query(db_connection=db_connection, query=query, query_params=(tool, revision, part_number))
            db_connection.commit()
            return redirect(url_for('designs'))
        except Exception as e:
            print(f"Error: {e}")
            return "There was an error editing the design.", 500
    else:
        query = "SELECT * FROM Designs WHERE partNumber = %s;"
        db_connection = db.connect_to_database()
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(part_number,))
        design = cursor.fetchone()
        return render_template('edit_design.html', design=design)
    
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

@app.route('/requirements')
def requirements():
    db_connection = db.connect_to_database()
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

@app.route('/add_requirement', methods=['GET', 'POST'])
def add_requirement():
    db_connection = db.connect_to_database()
    if request.method == 'POST':
        try:
            level = request.form['level']
            query = "INSERT INTO Requirements (level) VALUES (%s);"
            db.execute_query(db_connection=db_connection, query=query, query_params=(level,))
            db_connection.commit()
            return redirect(url_for('requirements'))
        except Exception as e:
            print(f"Error: {e}")
            return "There was an error adding the requirement.", 500
    return render_template('add_requirement.html')

@app.route('/edit_requirement/<int:requirement_id>', methods=['GET', 'POST'])
def edit_requirement(requirement_id):
    db_connection = db.connect_to_database()
    if request.method == 'POST':
        try:
            level = request.form['level']
            query = "UPDATE Requirements SET level = %s WHERE requirementId = %s;"
            db.execute_query(db_connection=db_connection, query=query, query_params=(level, requirement_id))
            db_connection.commit()
            return redirect(url_for('requirements'))
        except Exception as e:
            print(f"Error: {e}")
            return "There was an error editing the requirement.", 500
    else:
        query = "SELECT * FROM Requirements WHERE requirementId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(requirement_id,))
        requirement = cursor.fetchone()
        return render_template('edit_requirement.html', requirement=requirement)

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

@app.route('/projects')
def projects():
    db_connection = db.connect_to_database()
    query = """
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
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    grouped_projects = {}
    for row in results:
        user_id = row['userId']
        if user_id not in grouped_projects:
            grouped_projects[user_id] = {
                'name': f"{row['firstName']} {row['lastName']}",
                'projects': []
            }
        grouped_projects[user_id]['projects'].append({
            'projectId': row['projectId'],
            'projectStatus': row['projectStatus']
        })
    return render_template('projects.html', grouped_projects=grouped_projects)

@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        project_status = request.form['projectStatus']
        selected_users = request.form.getlist('users')
        db_connection = db.connect_to_database()
        try:
            query = "INSERT INTO Projects (projectStatus) VALUES (%s);"
            db.execute_query(db_connection=db_connection, query=query, query_params=(project_status,))
            db_connection.commit()
            query = "SELECT LAST_INSERT_ID() AS projectId;"
            cursor = db.execute_query(db_connection=db_connection, query=query)
            result = cursor.fetchone()
            project_id = result['projectId']
            if selected_users:
                query = "INSERT INTO UserProjects (userId, projectId) VALUES (%s, %s);"
                for user_id in selected_users:
                    db.execute_query(db_connection=db_connection, query=query, query_params=(user_id, project_id))
                db_connection.commit()

            return redirect(url_for('projects'))
        except Exception as e:
            print(f"Error: {e}")
            return "There was an error adding the project.", 500

    else:
        db_connection = db.connect_to_database()
        query = "SELECT userId, firstName, lastName FROM Users;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        users = cursor.fetchall()
        return render_template('add_project.html', users=users)

@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    db_connection = db.connect_to_database()
    if request.method == 'POST':
        project_status = request.form['projectStatus']
        selected_users = request.form.getlist('users')
        try:
            query = "UPDATE Projects SET projectStatus = %s WHERE projectId = %s;"
            db.execute_query(db_connection=db_connection, query=query, query_params=(project_status, project_id))
            db_connection.commit()
            query = "DELETE FROM UserProjects WHERE projectId = %s;"
            db.execute_query(db_connection=db_connection, query=query, query_params=(project_id,))
            db_connection.commit()
            if selected_users:
                query = "INSERT INTO UserProjects (userId, projectId) VALUES (%s, %s);"
                for user_id in selected_users:
                    db.execute_query(db_connection=db_connection, query=query, query_params=(user_id, project_id))
                db_connection.commit()
            return redirect(url_for('projects'))
        except Exception as e:
            print(f"Error: {e}")
            return "There was an error updating the project.", 500
    else:
        query = "SELECT * FROM Projects WHERE projectId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(project_id,))
        project = cursor.fetchone()
        query = "SELECT userId, firstName, lastName FROM Users;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        users = cursor.fetchall()
        query = "SELECT userId FROM UserProjects WHERE projectId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(project_id,))
        assigned_users = [row['userId'] for row in cursor.fetchall()]
        return render_template('edit_project.html', project=project, users=users, assigned_users=assigned_users)

@app.route('/delete_project/<int:project_id>')
def delete_project(project_id):
    query = "DELETE FROM Projects WHERE projectId = %s;"
    db_connection = db.connect_to_database()
    db.execute_query(db_connection=db_connection, query=query, query_params=(project_id,))
    db_connection.commit()
    return redirect(url_for('projects'))

@app.route('/users')
def users():
    db_connection = db.connect_to_database()
    query = "SELECT * FROM Users;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('users.html', users=results)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        discipline = request.form['discipline']
        query = "INSERT INTO Users (firstName, lastName, discipline) VALUES (%s, %s, %s);"
        db_connection = db.connect_to_database()
        db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, discipline))
        db_connection.commit()
        return redirect(url_for('users'))
    return render_template('add_user.html')

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        discipline = request.form['discipline']
        query = "UPDATE Users SET firstName = %s, lastName = %s, discipline = %s WHERE userId = %s;"
        db_connection = db.connect_to_database()
        db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, discipline, user_id))
        db_connection.commit()
        return redirect(url_for('users'))
    else:
        query = "SELECT * FROM Users WHERE userId = %s;"
        db_connection = db.connect_to_database()
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(user_id,))
        user = cursor.fetchone()
        return render_template('edit_user.html', user=user)
    
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    query = "DELETE FROM Users WHERE userId = %s;"
    db_connection = db.connect_to_database()
    db.execute_query(db_connection=db_connection, query=query, query_params=(user_id,))
    db_connection.commit()
    return redirect(url_for('users'))

# Listener
if __name__ == "__main__":
    app.run(host='', port=os.environ.get("340PORT"), debug=True)
