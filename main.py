import os
import mysql.connector
from dotenv import load_dotenv
load_dotenv('password.env')
from cryptography.fernet import Fernet
import sys

db=mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv('SQLPass'),
    database="password"
)
choice = sys.argv[1]
cursor = db.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ServicePass (
        ServiceName varchar (100) PRIMARY KEY,
        Password LONGBLOB
    )
    """)
servicePass= []
key = os.getenv('MASTER_KEY').encode()
if(choice =="store"):
    service_name = input("Enter the Service Name: ")
    service_password = input("Enter the Service password:")
    try:
        f = Fernet(key)
        token = f.encrypt(service_password.encode())
        query = "INSERT INTO ServicePass VALUES (%s, %s)"
        cursor.execute(query, (service_name, token))
        db.commit()
        print("Password Stored Successfully!!")
    except mysql.connector.Error as err:
        print("Error:", err)
elif (choice =="call"):
    service_name = input("Enter the Service Name: ")
    query = "SELECT * FROM ServicePass WHERE ServiceName = %s"
    cursor.execute(query,[service_name])
    user_details = cursor.fetchone()
    if user_details == None:
        print("Service Not Found!!")
    else: 
        
        f = Fernet(key)
        Pass = f.decrypt(user_details[1])
        userPass = Pass.decode()
        print(f"ServiceName: {user_details[0]} \nPassword: {userPass}")
else:
    print("Wrong Input!!")
db.close()

