import mysql.connector

#  Vul hier je eigen Username en Password in van je mysql server
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="mydatabase"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")

mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)
