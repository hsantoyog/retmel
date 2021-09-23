import imaplib
import email
import datetime
import hashlib

#####################
# Variables globales
#####################
#// Conexión a Gmail
usuario = 'hsantoyo.retomeli@gmail.com'
contrasena = 'R3t0M3l1@2021'
imap_url = 'imap.gmail.com'

#// Resultados de la búsqueda, en arrays
arr_emailID = []
arr_emailDate = []
arr_emailFrom = []
arr_emailSubject = []

#// Conexión de imaplib
con = imaplib.IMAP4_SSL(imap_url)
con.login(usuario, contrasena)

# print(con.list())

#####################
# Recuperación de correos
#####################
# Selección de la bandeja de entrada
con.select('INBOX')

# Ahora buscaremos DevOps en BODY. Los resultados incluyen correos donde en el asunto venga 
# el término 'devops'
result, data = con.uid('search', None, '(BODY "devops")')
i = len(data[0].split()) # Longitud de los resultados

# Ciclo de lectura de los mensajes
for x in range(i):
    latest_email_uid = data[0].split()[x]
    result, email_data = con.uid('fetch', latest_email_uid, '(RFC822)')

    raw_email = email_data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)

    # Contenido del Header
    date_tuple = email.utils.parsedate_tz(email_message['Date'])
    if date_tuple:
        local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
    email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
    email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
    subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))

    # Es necesario hacer un mapeo del contenido de email_message, ya que el texto del mensaje no es un índice fijo
    # Por ejemplo, un correo no multipart, bastaría únicamente llamar al contenido con email_message.get_payload()
    # Sin embargo, para multipart el contenido estaría en email_message.get_payload()[0].get_payload()
    # Peor aún, si contiene archivos adjuntos, lo encontraremos en email_message.get_payload()[0].get_payload()[0].get_payload()
    # Y así sucesivamente.

    # Primero, revisamos que el tipo de la variable no sea ya 'text/plain' o  'text/html'
    if email_message.get_content_type() == 'text/plain' or email_message.get_content_type() == 'text/html':
        # Caso verdadero, guardamos directamente el valor en body
        body = email_message.get_payload()
    else:
        # Caso contrario dividimos el contenido del mensaje en partes, para ir mapeando a manera de árbol
        for part in email_message.walk():
            # Posteriormente validamos que el contenido sea del tipo 'text/plain', que puede indicarnos el mensaje.
            if part.get_content_type() == 'text/plain' or part.get_content_type() == 'text/html':
                body = part.get_payload() # prints the raw text

    # Imprimiendo en pantalla los datos
    print(email_from)
    print(email_to)
    print(subject)
    print(body)

    if body.lower().rfind("devops") == -1:
        print("No contiene el término en el body.")
    else:
        print("Válido. El término está dentro del body del mensaje.")
        # Hash del mensaje (sha256)
        email_hash_id = hashlib.sha256(raw_email).hexdigest()
        print(email_hash_id)
        arr_emailID.append(email_hash_id)
        arr_emailDate.append(local_message_date)
        arr_emailFrom.append(email_from)
        arr_emailSubject.append(subject)
    print("")


    

con.close()
con.logout()
