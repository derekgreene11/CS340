import MySQLdb
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from the .env file
load_dotenv(find_dotenv())

# Set the variables in application with environment variables
host = os.environ.get("DBHOST")
user = os.environ.get("DBUSER")
passwd = os.environ.get("DBPW")
db = os.environ.get("ESDB")

def connect_to_database(host=host, user=user, passwd=passwd, db=db):
    db_connection = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    return db_connection

def execute_query(db_connection=None, query=None, query_params=()):
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, query_params)
    db_connection.commit();
    return cursor