# Citation for db_connector.py:
# Date: 6/23//2024
# Adapted from:
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/database/db_connector.py

import MySQLdb
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Set the variables in application with environment variables
host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
passwd = os.environ.get("340DBPW")
db = os.environ.get("340DB")

def connect_to_database(host=host, user=user, passwd=passwd, db=db):
    db_connection = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    return db_connection

def execute_query(db_connection=None, query=None, query_params=()):
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, query_params)
    db_connection.commit();
    return cursor