# Authors: Derek Greene & Nathan Schuler
# Date: 7/2024
# Course: CS340 - Introduction to Databases
# Citation for db_connector.py:
# Adapted to utilize pymysql instead of MySQLdb and removed unnecessary functions/sample query
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/database/db_connector.py

import pymysql
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Get db credentials from environment variables
host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
passwd = os.environ.get("340DBPW")
db = os.environ.get("340DB")

# Function to connect to the database using pymysql
def connect_to_database(host=host, user=user, passwd=passwd, db=db):
    db_connection = pymysql.connect(host=host, user=user, password=passwd, database=db, 
cursorclass=pymysql.cursors.DictCursor)
    return db_connection

# Function to execute a query on the database
def execute_query(db_connection=None, query=None, query_params=()):
    cursor = db_connection.cursor()
    cursor.execute(query, query_params)
    db_connection.commit()
    return cursor