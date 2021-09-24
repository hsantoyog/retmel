#+++++++++++++++++++#
#*******************#
# Archivo: readEmail.py
# Autor: Héctor Santoyo García
# ----------------------------
# Este archivo es el principal ejectuable.
# Utiliza readEmail y connectDB para efectuar
# el acceso al correo, la revisión del contenido
# y las consultas necesarias a la base de datos.
#
# Para la automatización se requiere que el usuario
# especifique la cantidad de segundos de espera entre
# cada iteración de la aplicación para revisar su
# bandeja de entrada y registrar en la base de datos
# los correos en cuyo contenido se encuentr el término
# "DEVOPS", sin importar mayúsculas ni minúsculas. 
# Únicamente se registrarán los correos que no se hayan
# registrado antes en la base de datos.

# Importamos las librerías que utilizaremos
import connectDB
import readEmail
import time
import emailTokenConnect

# Introducción y bienvenida
print("¡Hola! Bienvenido a RetMel. Vamos a leer tu bandeja de entrada.")

# Solicitamos un input al usuario, para determinar el tiempo de espera entre cada iteración
while True:
    try:
        checkAfter = int(input("Por favor indica cada cuántos segundos deseas revisar tu correo: "))
        break
    except ValueError:
        print("Error: Por favor escribe con números la cantidad de segundos para revisar tu correo.")

# Mandaremos alguna información relevante sobre el proceso que se está llevando a cabo para mantener
# notificado al usuario.
print("Se revisará automáticamente por nuevos correos con DevOps en el contenido cada ", checkAfter, "segundo(s).")
print("Inicia primera revisión de la bandeja de entrada...")

# La primera iteración la haremos fuera del loop tempora.
# Obtenemos los resultados de la llamada a la función readEmail(), responsable de
# recuperar la información de los correos no registrados.
try:
    # La siguiente función es parte de la primera versión del código, utiliza directamente las
    # credenciales del usuario para obtener los correos. Se aconseja utilizar en su lugar la
    # función emailTokenConnect.getEmails(), el cual utiliza en su lugar un token y la autorización
    # del usuario a través de permisos para que la aplicación lea sus correos
    # Nota: el emailID obtenido es diferente al de emailTokenConnect.getEmails(), por los que ambas
    # funciones no son compatibles entre sí.
    # arr_emailID, arr_emailDate, arr_emailFrom, arr_emailSubject = readEmail.readEmail()

    # La siguiente línea es el approach más reciente para obtener los correos del usuario sin
    # exponer sus credenciales dentro del código.
    arr_emailID, arr_emailDate, arr_emailFrom, arr_emailSubject = emailTokenConnect.getEmails()

except ValueError:
    print("Error al intentar acceder a los correos.")    
# Insertamos dentro de la base de datos MySQL aquellos correos nuevos.
try:
    connectDB.insertNewEmailID(arr_emailID, arr_emailDate, arr_emailFrom, arr_emailSubject)
except ValueError:
    print("Error al intentar guardar la información. Se reintenará posteriormente.")

print("")
print("Próxima revisión en ", checkAfter, "segundo(s)... (Presiona Ctrl + C si deseas detener la operación)")
print("")

# Esta variable nos permitirá hacer un loop virtualmente infinito.
# Es posible mejorar el funcionamiento agregando algún listener para detener el ciclo,
# evitando así que el usuario tenga que ejecutar el comando Ctrl + C para terminar el
# proceso de ejecución.
TimeLoop = True
# Inicia el bucle
while TimeLoop:
    start_time = time.time()
    # El siguiente bucle es el que permitirá medir el tiempo entre cada ejecución.
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > checkAfter:
            print("Revisando la bandeja de entrada...")
            # Llamada a la función de revisión del correo.
            try:
                # arr_emailID, arr_emailDate, arr_emailFrom, arr_emailSubject = readEmail.readEmail() # OBSOLETO
                connectDB.insertNewEmailID(arr_emailID, arr_emailDate, arr_emailFrom, arr_emailSubject)
            except ValueError:
                print("Error al intentar acceder a los correos.")    
            # Insertamos dentro de la base de datos MySQL aquellos correos nuevos.
            try:
                connectDB.insertNewEmailID(arr_emailID, arr_emailDate, arr_emailFrom, arr_emailSubject)
            except ValueError:
                print("Error al intentar guardar la información. Se reintenará posteriormente.")
            print("Próxima revisión en ", checkAfter, "segundo(s)... (Presiona Ctrl + C si deseas detener la operación)")
            print("")
            break