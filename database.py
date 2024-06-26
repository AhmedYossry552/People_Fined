from common_imports import *
from flask import g, current_app
config = {
  'host':'azure-finder-database.mysql.database.azure.com',
  'user':'AbdulrahmanSaad',
  'password':'finder66@@',
  'database':'lost_people_finder',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': '/DigiCertGlobalRootG2.crt.pem'
    }

    
def get_connection():
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(**config)
            print("Connection established")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(f"Error: {err}")
                g.db = None
    return g.db

def close_connection(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_connection)