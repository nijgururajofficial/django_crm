import mysql.connector

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'root'
)

cursorObject = conn.cursor()

cursorObject.execute("CREATE DATABASE cratso")

print("All Done!")