#+++++++++++++++++++#
#*******************#
# Archivo: connectDB.py
# Autor: Héctor Santoyo García
# ----------------------------
# connectDB es la encargada de llevar a cabo
# la conexión con la base de datos MySQL, así
# como los Querys necesarios para el funcionamiento
# de esta aplicación.

# Importamos las librerías que utilizaremos
import mysql.connector
import numpy as np

# La siguiente función es la responsable de realizar la conexión a la base
# de datos MySQL. Es importante configurar las variables host, user, password
# y database con los valores correspondientes para efectuar la conexión.
def connectMySQL():
    mydb = mysql.connector.connect(
    host="HOST",
    user="USER",
    password="PASSWORD",
    database="DATABASE_RETMEL"
    )
    return mydb

# existEmailID verifica, dado un EmailID, que no exista un registro previo
# de dicho correo. En caso de existir dicho ID, regresa True
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

# La función insertNewEmailID recibe como parámetros el ID del correo
# la fecha de recepción, el remitente y el asunto, para insertar el
# registro en la base de datos.
def insertNewEmailID(EmailID,Date,From,Subject):
    mydb = connectMySQL()
    mycursor = mydb.cursor()
    SQLQuery = "INSERT INTO Email (Email_ID, Email_Fecha, Email_Remitente, Email_Asunto) VALUES (%s,%s,%s,%s)"
    val = [
        EmailID,
        Date,
        From,
        Subject
    ]
    # Aquí utilizamos la librería numpy para transponer los valores, de manera que podamos
    # hacer inserciones múltiples, en caso de recibir varios correos para registrar.
    val = np.array([EmailID,Date,From,Subject])
    val_transpose = val.transpose()
    val_list = val_transpose.tolist()
    mycursor.executemany(SQLQuery,val_list)
    mydb.commit()
    # Se notificará al usuario cuántos nuevos correos fueron agregados.
    if mycursor.rowcount > 1:
        print("Se agregaron", mycursor.rowcount, "registros nuevos a la base de datos.")
    elif mycursor.rowcount == 1:
        print("Se agregó 1 registro nuevo a la base de datos.")
    else:
        print("No hay nuevos registros que agregar a la base de datos.")