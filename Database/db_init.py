import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS PharmaDB")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="PharmaDB"
)

mycursor = mydb.cursor()

#mycursor.execute("DROP TABLE Medicine")

mycursor.execute("""CREATE TABLE IF NOT EXISTS Medicine (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  ATCCode CHAR(7)
)""")

mydb.close()