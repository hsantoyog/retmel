# imaplib: para acceder al correo via protocolo IMAP
# email:
# pprint: para que sea un poco más vistoso.

import imaplib
import email
import pprint

# Primera prueba de conexión. Vamos a hacer una conexión simple y buscar enrobustecer el método de autenticación.
usuario = 'hsantoyo.retomeli@gmail.com'
contrasena = 'R3t0M3l1@2021'
imap_url = 'imap.gmail.com'

con = imaplib.IMAP4_SSL(imap_url)
con.login(usuario, contrasena)

print(con.list())

con.select('INBOX')

tmp, data = con.search(None, '(BODY "DevOps")')
for num in data[0].split():
    tmp, data = con.fetch(num, '(RFC822)')
    print('Message: {0}\n'.format(num))
    pprint.pprint(data[0][1])
    break


con.close()
