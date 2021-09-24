# retmel - Aplicación Reto Meli
retmel es una aplicación diseñada para hacer una revisión automática de la bandeja de entrada de una dirección de correo electrónico, y extraer aquellos correos que tengan dentro de su contenido el término "DevOps", esto sin considerar si está en mayúsculas o minúsculas (case insensitive).

Posteriormente, dichos correos son registrados dentro de una base de datos MySQL, almacenando los siguientes datos:
 - Identificador del correo.
 - Fecha de recepción.
 - Remitente
 - Asunto

 Aquellos correos que ya han sido previamente registrados en la base de datos, no generarán registros duplicados.

 ## Configuración
 Para ejecutar la aplicación, es necesario configurar primero una serie de parámetros:
 
  > readEmail.py - OBSOLETA |
En caso de utilizarla, aquí será necesario editar las variables usuario y contrasena con los datos de acceso a la cuenta de correo. Esta función se considera insegura, ya que expone las credenciales del usuario. Adicionalmente, el usuario debe habilitar la opción de "Permitir aplicaciones inseguras" para que pueda funcionar con este método.

  > emailTokenConnect.py |
Función que sustituye a readEmail. Realiza la conexión a Gmail por medio de un token, que es almacenado en un archivo llamado token.pickle. El usuario no necesita almacenar sus credenciales dentro del código, se restringe a la aplicación a únicamente acceder a la lectura de correos, y adicionalmente puede retirarse el acceso a la aplicación en cualquier momento. No es necesario realizar ninguna configuración adicional dentro de este documento.

  > connectDB.py |
Las variables a configurar aquí son host, user, password y database, con los datos correspondientes para acceder a la base de datos creada para almacenar los registros de correo.

  > main.py |
Documento principal donde inicia la ejecución de la aplicación. Por defecto utiliza emailTokenConnect para acceder a los correos.

## Instalación de componentes
Para poder utilizar la aplicación, es necesario instalar Python 3.x y MySQL, así como configurar dichas herramientas.

### Python
Puede instalarse desde una imagen de Docker y ejecutarse en un contenedor, o utilizar los paquetes de instalación para Windows (tanto x86, x64 y Windows store), MacOS, Linux, etc. El código fue desarrollado en Python 3.9, pero sus funciones son compatibles con versiones anteriores de Python 3. Además de las librerías incluídas, es necesario instalar mysql_connector, numpy y las librerías de acceso a las APIs de Google:

```bash
python -m pip install mysql-connector-python
python -m pip install numpy
python -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### MySQL
De igual manera, la base de datos MySQL puede ejecutarse desde un contenedor Docker, ser instalada directamente en el sistema operativo o, incluso, ejecutarse desde un servidor web o proveedor cloud. Para configurar la base de datos, basta ejecutar el query contenido dentro de /db_dump/retmel.sql

Asimismo, es recomendable crear un usuario específico para esta aplicación, asignándole los privilegios de INSERT y SELECT para ejecutar las acciones contenidas dentro de esta aplicación.

## Uso de la aplicación
Una vez configurada, para usar la aplicación, basta ejecutar main.py en una terminal:

```python
python main.py
```
Posteriormente se preguntará al usuario la cantidad de segundos a esperar antes de cada ejecución. 
La aplicación utiliza por defecto la función la función emailTokenConnect.getEmails() para la recuperación del correo. En la primera ejecución se deberá generar un archivo token.pickles con la autorización del usuario, por lo que se abrirá una ventana del navegador en el cual se deberá iniciar sesión con las credenciales de la cuenta hsantoyo.retomeli@gmail.com. Dicha cuenta es la única autorizada a ejecutar este código. Al no ser una App Verificada por Google, se mostrará una advertencia al usuario, donde deberá seleccionarse la opción de "Continuar". Posteriormente será necesario otorgar el permiso de lectura de correo electrónico. Al concluir la autenticación, se mostrará un aviso al usuario, tras lo cual se podrá cerrar la ventana del navegador.

En las siguiente iteraciones, no será necesario volver a autenticar a la aplicación, salvo que ésta caduque o el usuario retire el acceso de la aplicación desde la configuración de su cuenta.

Finalizada esta configuración, la aplicación estará llevando a cabo revisiones de la bandeja de entrada cada vez que se cumpla el tiempo indicado, recuperando los correos nuevos que cumplan con el criterio establecido.

El usuario puede detener en cualquier momento la ejecución de este script presionando Ctrl+C en su teclado.
