# <span style="color: #007bff;">Engineering Services Database</span>

Final project for Introduction to Databases - CS340 @ <span style="color: #D73F09;">O</span>S<span style="color: #D73F09;">U</span>

Made with :green_heart: by Derek Greene & Nathan Schuler

## <span style="color: #007bff;">Description</span>

Three tier architecutre application built with:

<ul>
<li style="color: limegreen;"><span style="color: limegreen;">Flask/Python</span></li>
<li style="color: lightblue;"><span style="color: lightblue;">MySQL</span></li>
<li style="color: #FF00FF;"><span style="color: #FF00FF;">HTML/CSS</span></li>
<li style="color: #F08080;"><span style="color: #F08080;">Jinja2</span></li>
</ul>

Application showcases web development & database knowledge. Users are able to view, add, edit, and remove records from various tables in the Engineering Services Database. 

## <span style="color: #007bff;">Getting started</span>

Clone the repository

`git clone https://github.com/derekgreene11/CS340.git`

`cd CS340/flask_proj`

Install MySQL and create the database

`CREATE DATABASE cs340_database;`

Load the Engineering Services SQL and sample data into the database

`source database/es_db.sql`

Create a .env file in the CS340/flask_proj directory & paste the credentials for the MySQL database 

```
340DBHOST=localhost
340DBUSER=root
340DBPW="Enter the password you created during setup of MySQL Server"
340DB=cs340_database
340PORT="Enter open port of your choosing e.g. 5000"
```

Setup and Activate Python Virtual Enviornment

`python3 -m venv venv`

`./venv/Scripts/activate`

Install requirements.txt

`pip install -r requirements.txt`

## <span style="color: #007bff;">Usage</span>

Run `python app.py` to start application

Navigate to localhost at the port listed in the .env e.g. http://localhost:5000/