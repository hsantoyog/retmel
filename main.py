import imaplib, email

# Introducción y bienvenida
print("¡Hola! Bienvenido a retmel. Vamos a leer tu bandeja de entrada.")

# Primero hagamos unas pruebas para comprender cómo funciona Python
cars = ["Ford", "Volvo", "BMW"]

# Primer detalle interesante: Python no usa corchetes. La tabulación es sumamente importante.
# Este código:
for c in cars:
    print(c)
print("Fin del ciclo")

# No es lo mismo que este código:
for c in cars:
    print(c)
    print("Fin del ciclo")

# Manejo de excepciones
while True:
    try:
        x = int(input("Please enter a number: "))
        break
    except ValueError:
        print("No es un número correcto, por favor intenta nuevamente")

print(x)