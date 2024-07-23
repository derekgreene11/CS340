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

    return render_template("designs.j2")

@app.route('/designs')
def users():

    query = "SELECT * FROM Designs;"

    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = json.dumps(cursor.fetchall())
    
    return results

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 43278))
    app.run(port=port, debug=True)