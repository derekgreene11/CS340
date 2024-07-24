import MySQLdb
import os
from dotenv import load_dotenv, find_dotenv
import time

# Load environment variables from the .env file
load_dotenv(find_dotenv())

# Set the variables in our application with those environment variables
host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
passwd = os.environ.get("340DBPW")
db = os.environ.get("340DB")

def connect_to_database(host=host, user=user, passwd=passwd, db=db):
    '''
    Connects to a database and returns a database connection object
    '''
    db_connection = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    return db_connection

def execute_query(db_connection=None, query=None, query_params=()):
    '''
    Executes a given SQL query on the given db connection and returns a Cursor object

    db_connection: a MySQLdb connection object created by connect_to_database()
    query: string containing SQL query

    returns: A Cursor object as specified at https://www.python.org/dev/peps/pep-0249/#cursor-objects.
    You need to run .fetchall() or .fetchone() on that object to actually access the results.
    '''
    if db_connection is None:
        print("No connection to the database found! Have you called connect_to_database() first?")
        return None

    if query is None or len(query.strip()) == 0:
        print("Query is empty! Please pass a SQL query in query.")
        return None
    
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, query_params)
    db_connection.commit();
    return cursor

    