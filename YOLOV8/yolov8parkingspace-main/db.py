#pip install mysql-connector-python
import mysql.connector 

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="renato"
)

mycursor = db.cursor()

mycursor.execute("CREATE DATABASE carros")