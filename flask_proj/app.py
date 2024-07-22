from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_greenede'
app.config['MYSQL_PASSWORD'] = 'rMWUvskFlErM'
app.config['MYSQL_DB'] = 'cs340_greenede'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


# Routes
@app.route('/')
def root():
    return render_template("main.j2")


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 43278))
    app.run(port=port)