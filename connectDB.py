#+++++++++++++++++++#
#*******************#
# Archivo: connectDB.py
# Autor: Héctor Santoyo García
# ----------------------------
# Esta clase es la encargada de llevar a cabo
# la conexión con la base de datos MySQL.
import mysql.connector

def connectMySQL():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Graz13M1ll3",
    database="retmel"
    )
    return mydb

def existsEmailID(EmailID):
    mydb = connectMySQL()
    mycursor = mydb.cursor()
    SQLQuery = "SELECT Email_ID FROM Email WHERE Email_ID = %s"
    Params = (EmailID,)
    mycursor.execute(SQLQuery,Params)
    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        return True
    else:
        return False