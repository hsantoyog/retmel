#+++++++++++++++++++#
#*******************#
# Archivo: emailTokenConnect.py
# Autor: Héctor Santoyo García
# ----------------------------
# Esta función es la responsable de ejecutar el escaneo
# y recuperación de los correos que tengan dentro de
# su contenido la palabra 'devops', sin importar
# mayúsculas ni minúsculas. Se descartarán aquellos
# que únicamente lo contengan en el asunto, así como
# aquellos que ya se encuentren dentro de una base de
# datos determinada.
#
# A diferencia de su predecesora, readEmail, esta
# función utiliza un token generado cuando el usuario
# proporciona privilegios a la aplicación desde su cuenta
# de Gmail, evitando así revelar las credenciales de
# acceso del usuario.

# Importamos las librerías que utilizaremos
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import base64
import hashlib
import connectDB

# Se definen los SCOPES para la autenticación del usuario.
# De esta manera se determinan los permisos que se requieren
# por parte de la aplicación, en este caso, la lectura de correos
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def getEmails():
    #####################
    # Variables globales
    #####################
    #// Resultados de la búsqueda, en arrays
    arr_emailID = []
    arr_emailDate = []
    arr_emailFrom = []
    arr_emailSubject = []

	# La variable cred contendrá el token de acceso del usuario
	# En caso de no existir alguno, se creará.
    creds = None

	# El archivo token.pickle contiene el token de acceso, por lo
    # que primero verificaremos si existe. En caso de existir, pero
    # ser rechazado porque el usuario haya retirado los privilegios
    # a la aplicación, debemos volver a solicitar dichas autorizaciones,
    # eliminando el token anterior. Para tal fin, utilizaremos un ciclo
    # que hará hasta dos intentos de autenticación, antes de terminar la
    # ejecución de la aplicación.
    tokenLoop = 0
    # Variable que indicará si hemos realizado la eliminación de un token
    # inválido.
    tokenDeleted = False
    # Iniciamos el ciclo
    while tokenLoop < 2:
        if os.path.exists('token.pickle'):
		    # Lectura del archivo del token y almacenamiento en la variable creds.
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

	    # Si las credenciales no están disponibles, son inválidas o el usuario ha
        # retirado los privilegios, requeriremos al usuario hacer login nuevamente.
        if not creds or not creds.valid or tokenDeleted:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

		    # Almacenamos el nuevo token en el archivo token.pickle, para evitar
            # requerir la autorización en cada ejecución
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

	    # Conexión al API de Gmail
        service = build('gmail', 'v1', credentials=creds)

	    # Obtención de la lista de mensajes. Si el usuario retiró su autorización, generará
        # una excepción, que capturaremos para eliminar el archivo "token.pickle" y volver a
        # autenticar al usuario para obtener los permisos de lectura de correos.
        try:
            result = service.users().messages().list(userId='me').execute()
            tokenLoop = tokenLoop + 2
        except:
            os.remove('token.pickle')
            tokenDeleted = True
            tokenLoop = tokenLoop + 1

	# Obtenemos la lista de mensajes e iteramos por cada uno para determinar si cumple con los criterios
    messages = result.get('messages')
    for msg in messages:
		# Obtención del mensaje individual
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()

		# En caso de algún error, pasaremos al mensaje siguiente
        try:
			# Obtención del cuerpo y encabezados
            payload = txt['payload']
            headers = payload['headers']

			# Ahora extraemos la información que requerimos de los encabezados
            for d in headers:
                if d['name'] == 'Date':
                    emailDate = d['value']
                if d['name'] == 'Subject':
                    emailSubject = d['value']
                if d['name'] == 'From':
                    emailFrom = d['value']

			# El cuerpo del mensaje está codificado en base 64, por lo que debemos
            # decodificarlo para hacerlo comprensible
            # Generalmente el mensaje viene dividido en partes, pero en caso contrario,
            # accederemos directamente al contenido desde el payload
            try:
                parts = payload.get('parts')[0]
                data = parts['body']['data']
            except:
                data = payload['body']['data']
            
            # Procedemos a la decodificación de base 64
            data = data.replace("-","+").replace("_","/")
            decoded_data = base64.b64decode(data)

            # A continuación volvemos a decodificar el mensaje pero en UTF-8, para
            # generar un string en el cual podremos buscar el término de nuestro
            # interés: DevOps
            emailBody = decoded_data.decode("utf-8")
            if emailBody.lower().rfind("devops") > -1:
                # A partir de la información del mensaje, generamos un ID
                # por medio del hash para evitar registrar mensajes duplicados.
                emailElements = emailDate + emailSubject + emailFrom
                encodedEmailElements = emailElements.encode("utf-8")
                emailHashID = hashlib.sha256(encodedEmailElements).hexdigest()
                # Ahora validamos que el email no esté ya registrado en la base de datos
                BDcon = connectDB
                if not BDcon.existsEmailID(emailHashID):
                    # En caso de no estar registrado, almacenamos el mensaje dentro
                    # de arrays con la información que registraremos en la base de
                    # datos.
                    arr_emailID.append(emailHashID)
                    arr_emailDate.append(emailDate)
                    arr_emailFrom.append(emailFrom)
                    arr_emailSubject.append(emailSubject)
        except:
            pass
        
    return arr_emailID, arr_emailDate, arr_emailFrom, arr_emailSubject