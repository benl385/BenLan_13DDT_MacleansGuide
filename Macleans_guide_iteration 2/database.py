# database.py

import os #this is used to create the database file in the correct location
import sqlite3 

# Automatically points to MacleansApp/data/app.db
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "app.db") 
#dirname gets folder wher current file is located, joins with app.db to create path to database file

def get_connection(): #get_connection function returns a connection to database, allowing for interaction
    # Returns a connection to the SQLite database. 
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True) #makedirs creates data folder if it doesnt exist, exist_ok prevents error if already existing
    return sqlite3.connect(DB_PATH) 

def init_db():  
    # Creates database tables and inserts default data if missing.
    with get_connection() as conn: #conn = connection object to database. allows interactions
        cur = conn.cursor() #cursor is used to execute sql commands and queries. cur = cursor object
        #Table for user logins
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users (" 
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "username TEXT UNIQUE NOT NULL, "
            "password TEXT NOT NULL)" 
        ) 
        #line 21-24 creates a table in database for users

        #Table for map markers
        cur.execute(
            "CREATE TABLE IF NOT EXISTS markers ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "name TEXT NOT NULL, " 
            "x_coord INTEGER NOT NULL, " 
            "y_coord INTEGER NOT NULL)"
        )
        #line 30-34 creates a table in database for map markers

        # Add multiple default users if user table is empty
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0: #fetchone returns tuple with count of rows in table. if 0, table is empty and registered users are added
            registered_users = [
                ("student1", "password1"),
                ("teacher1", "teacherpassword1"),
                ("admin1", "adminpassword1")
            ]
            cur.executemany(
                "INSERT INTO users (username, password) VALUES (?, ?)", #Inserts registered users into the users table if empty 
                registered_users
            )
            
        #Adds map markers if table is empty 
        cur.execute("SELECT COUNT(*) FROM markers") 
        if cur.fetchone()[0] == 0: #same as above, checks if table is empty and adds default markers if so
            map_markers = [
                ("Batten House", 150, 150), 
                ("Kupe House", 200, 100), 
                ("Library", 100, 200) 
            ]
            cur.executemany(
                "INSERT INTO markers (name, x_coord, y_coord) VALUES (?, ?, ?)", 
                map_markers 
            )

        conn.commit() #conn commit saves changes made to database. required

def check_login(username: str, password: str) -> bool: 
    # Validates user credentials against SQLite database.

    with get_connection() as conn: 
        cur = conn.cursor() #.cursor is used to execute sql commands and queries
        cur.execute(
            "SELECT id FROM users WHERE username=? AND password=?",
            (username, password),
        )
        return cur.fetchone() is not None

def get_all_markers():
    # Retrieves all map markers from the database.
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, x_coord, y_coord FROM markers")
        return cur.fetchall()