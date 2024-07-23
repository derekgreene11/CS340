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

    return "<h1>Working</h1>"

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

# Listener
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=43277, debug=True)