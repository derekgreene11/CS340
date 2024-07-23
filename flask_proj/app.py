from flask import Flask, render_template, json, redirect, url_for
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db

app = Flask(__name__)

db_connection = db.connect_to_database()
mysql = MySQL(app)

# Routes
@app.route('/')
def root():

    return "<h1>Engineering Services Database 1.0</h1>"

@app.route('/designs')
def designs():
    query = "SELECT * FROM Designs;"
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
        try:
            tool = request.form['tool']
            revision = request.form.get('revision', None)  # Use `None` if `revision` is optional
            query = "UPDATE Designs SET tool = %s, revision = %s WHERE partNumber = %s;"
            db.execute_query(db_connection=db_connection, query=query, query_params=(tool, revision, part_number))
            db_connection.commit()  # Ensure changes are committed
            return redirect(url_for('designs'))
        except Exception as e:
            print(f"Error: {e}")
            return "There was an error editing the design.", 500
    else:
        query = "SELECT * FROM Designs WHERE partNumber = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(part_number,))
        design = cursor.fetchone()
        return render_template('edit_design.html', design=design)
    
@app.route('/delete_design/<int:part_number>')
def delete_design(part_number):
    try:
        query = "DELETE FROM Designs WHERE partNumber = %s;"
        db.execute_query(db_connection=db_connection, query=query, query_params=(part_number,))
        db_connection.commit()  # Ensure changes are committed
        return redirect(url_for('designs'))
    except Exception as e:
        print(f"Error: {e}")
        return "There was an error deleting the design.", 500

@app.route('/requirements')
def requirements():
    query = "SELECT * FROM Requirements;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('requirements.html', requirements=results)

@app.route('/add_requirement', methods=['GET', 'POST'])
def add_requirement():
    if request.method == 'POST':
        try:
            level = request.form['level']
            query = "INSERT INTO Requirements (level) VALUES (%s);"
            db.execute_query(db_connection=db_connection, query=query, query_params=(level,))
            db_connection.commit()  # Ensure changes are committed
            return redirect(url_for('requirements'))
        except Exception as e:
            print(f"Error: {e}")
            return "There was an error adding the requirement.", 500
    return render_template('add_requirement.html')

@app.route('/edit_requirement/<int:requirement_id>', methods=['GET', 'POST'])
def edit_requirement(requirement_id):
    if request.method == 'POST':
        try:
            level = request.form['level']
            query = "UPDATE Requirements SET level = %s WHERE requirementId = %s;"
            db.execute_query(db_connection=db_connection, query=query, query_params=(level, requirement_id))
            db_connection.commit()  # Ensure changes are committed
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
    try:
        query = "DELETE FROM Requirements WHERE requirementId = %s;"
        db.execute_query(db_connection=db_connection, query=query, query_params=(requirement_id,))
        db_connection.commit()  # Ensure changes are committed
        return redirect(url_for('requirements'))
    except Exception as e:
        print(f"Error: {e}")
        return "There was an error deleting the requirement.", 500

@app.route('/projects')
def projects():
    query = "SELECT * FROM Projects;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('projects.html', projects=results)

@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        project_status = request.form['projectStatus']
        query = "INSERT INTO Projects (projectStatus) VALUES (%s);"
        db.execute_query(db_connection=db_connection, query=query, query_params=(project_status,))
        db_connection.commit()
        return redirect(url_for('projects'))
    return render_template('add_project.html')

@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    if request.method == 'POST':
        project_status = request.form['projectStatus']
        query = "UPDATE Projects SET projectStatus = %s WHERE projectId = %s;"
        db.execute_query(db_connection=db_connection, query=query, query_params=(project_status, project_id))
        db_connection.commit()
        return redirect(url_for('projects'))
    else:
        query = "SELECT * FROM Projects WHERE projectId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(project_id,))
        project = cursor.fetchone()
        return render_template('edit_project.html', project=project)

@app.route('/delete_project/<int:project_id>')
def delete_project(project_id):
    query = "DELETE FROM Projects WHERE projectId = %s;"
    db.execute_query(db_connection=db_connection, query=query, query_params=(project_id,))
    db_connection.commit()
    return redirect(url_for('projects'))

@app.route('/users')
def users():
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
        db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, discipline))
        db_connection.commit()  # Ensure changes are committed
        return redirect(url_for('users'))
    return render_template('add_user.html')

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        discipline = request.form['discipline']
        query = "UPDATE Users SET firstName = %s, lastName = %s, discipline = %s WHERE userId = %s;"
        db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, discipline, user_id))
        db_connection.commit()  # Ensure changes are committed
        return redirect(url_for('users'))
    else:
        query = "SELECT * FROM Users WHERE userId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(user_id,))
        user = cursor.fetchone()
        return render_template('edit_user.html', user=user)
    
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    query = "DELETE FROM Users WHERE userId = %s;"
    db.execute_query(db_connection=db_connection, query=query, query_params=(user_id,))
    db_connection.commit()  # Ensure changes are committed
    return redirect(url_for('users'))

# Listener
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=43277, debug=True)