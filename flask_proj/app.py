from flask import Flask, render_template, json, redirect
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
    return render_template('designs.j2', designs=results)

@app.route('/requirements')
def requirements():
    query = "SELECT * FROM Requirements;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('requirements.j2', requirements=results)

@app.route('/projects')
def projects():
    query = "SELECT * FROM Projects;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('projects.j2', projects=results)

@app.route('/users')
def users():
    query = "SELECT * FROM Users;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('users.j2', users=results)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        discipline = request.form['discipline']
        query = "INSERT INTO Users (firstName, lastName, discipline) VALUES (%s, %s, %s);"
        db.execute_query(db_connection=db_connection, query=query, data=(first_name, last_name, discipline))
        return redirect(url_for('users'))
    return render_template('add_user.j2')

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        discipline = request.form['discipline']
        query = "UPDATE Users SET firstName = %s, lastName = %s, discipline = %s WHERE userId = %s;"
        db.execute_query(db_connection=db_connection, query=query, data=(first_name, last_name, discipline, user_id))
        return redirect(url_for('users'))
    else:
        query = "SELECT * FROM Users WHERE userId = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, data=(user_id,))
        user = cursor.fetchone()
        return render_template('edit_user.j2', user=user)

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    query = "DELETE FROM Users WHERE userId = %s;"
    db.execute_query(db_connection=db_connection, query=query, data=(user_id,))
    return redirect(url_for('users'))

# Listener
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=43277, debug=True)