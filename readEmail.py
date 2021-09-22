# imaplib: para acceder al correo via protocolo IMAP
# email:
# pprint: para que sea un poco más vistoso.

import imaplib
import email
import datetime
import mailbox
import hashlib

# Primera prueba de conexión. Vamos a hacer una conexión simple y buscar enrobustecer el método de autenticación.
usuario = 'hsantoyo.retomeli@gmail.com'
contrasena = 'R3t0M3l1@2021'
imap_url = 'imap.gmail.com'

con = imaplib.IMAP4_SSL(imap_url)
con.login(usuario, contrasena)

print(con.list())

con.select('INBOX')

# Aquí probaré un search básico, BODY busca en el cuerpo, SUBJECT en el asunto

#tmp, data = con.search(None, '(BODY "DevOps")')
#for num in data[0].split():
#    tmp, data = con.fetch(num, '(RFC822)')
#    print('Message: {0}\n'.format(num))
#    pprint.pprint(data[0][1])
#    break

# Prueba ahora de imprimir los valores FROM, SUBJECT y DATE

# Out: list of "folders" aka labels in gmail.

# Ahora buscaremos DevOps en asunto y contenido
result, data = con.search(None, '(BODY "devops")' )

ids = data[0] # data is a list.
id_list = ids.split() # ids is a space separated string
latest_email_id = id_list[-1] # get the latest

result, data = con.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822)             for the given ID

raw_email = data[0][1] # here's the body, which is raw text of the whole email
# including headers and alternate payloads








result, data = con.uid('search', None, '(BODY "devops")') # BODY devuelve también aquellos con el término en el subject
i = len(data[0].split())

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

    # Imprimiendo en pantalla los datos
    print(email_from + ' ' + email_to + ' ' + subject)

    # Hash del mensaje (sha256)


con.close()
con.logout()
