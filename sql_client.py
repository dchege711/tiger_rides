import pyodbc
import os

"""
Server=tcp:orf401.database.windows.net,1433;
Initial Catalog=orf401;
Persist Security Info=False;
User ID={your_username};
Password={your_password};
MultipleActiveResultSets=False;
Encrypt=True;
TrustServerCertificate=False;
Connection Timeout=30;

Show database connection strings

"""

server = "orf401.database.windows.net"
database = "dgitau_orf401lab"
username = os.environ["TIGER_RIDES_DB_AZURE_USERNAME"]
password = os.environ["TIGER_RIDES_DB_AZURE_PASSWORD"]
driver= "{ODBC Driver 17 for SQL Server}"
connection = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = connection.cursor()

def set_up_tables():
    query="""
        CREATE TABLE ridersdb (
        fName varchar(15),
        lName varchar(15),
        Origin varchar(15),
        Destination varchar(15),
        dDate date,
        dTime time,
        Hascar varchar(5),
        Seats int,
        Pass varchar(15),
        Email varchar(30),
        PRIMARY KEY(email))
    """
    print(cursor.execute(query))
    
if __name__ == "__main__":
    set_up_tables()
