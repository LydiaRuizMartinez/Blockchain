"""
PROYECTO FINAL DE FUNDAMENTOS DE LOS SISTEMAS OPERATIVOS
Realizado por:
    - María González Gómez
    - Lydia Ruiz Martínez
"""

import requests
import json

# Cabecera JSON (común a todas)
cabecera = {"Content-type": "application/json", "Accept": "text/plain"}

# Comprobamos la cadena en el puerto 5000 del host local
r = requests.get("http://127.0.0.1:5000/chain")
print(r.text)

# Comprobamos la cadena en el puerto 5001 del host local
r = requests.get("http://127.0.0.1:5001/chain")
print(r.text)

# Comprobamos la cadena en el puerto 5002 del host local
r = requests.get("http://127.0.0.1:5002/chain")
print(r.text)

# Mostramos la información del sistema
r = requests.get("http://127.0.0.1:5000/system")
print(r.text)

# Mostramos la información del sistema
r = requests.get("http://127.0.0.1:5001/system")
print(r.text)

# Mostramos la información del sistema
r = requests.get("http://127.0.0.1:5002/system")
print(r.text)

# Registramos dos nuevos nodos
nodos_nuevos = {"direccion_nodos": ["http://127.0.0.1:5001", "http://127.0.0.1:5002"]}
r = requests.post(
    "http://127.0.0.1:5000/nodos/registrar",
    data=json.dumps(nodos_nuevos),
    headers=cabecera,
)
print(r.text)

# Comprobamos la cadena en el puerto 5000 del host local y se observa que es la misma en el 5001 y en el 5002 al registrar los puertos
r = requests.get("http://127.0.0.1:5000/chain")
print(r.text)

r = requests.get("http://127.0.0.1:5001/chain")
print(r.text)

r = requests.get("http://127.0.0.1:5002/chain")
print(r.text)

# Añadimos una nueva transaccións
transaccion_nueva = {"origen": "nodoA", "destino": "nodoB", "cantidad": 10}
r = requests.post(
    "http://127.0.0.1:5000/transacciones/nueva",
    data=json.dumps(transaccion_nueva),
    headers=cabecera,
)
print(r.text)

# Minamos la transacción
r = requests.get("http://127.0.0.1:5000/minar")
print(r.text)

transaccion_nueva = {"origen": "nodoA", "destino": "nodoB", "cantidad": 10}
r = requests.post(
    "http://127.0.0.1:5001/transacciones/nueva",
    data=json.dumps(transaccion_nueva),
    headers=cabecera,
)
print(r.text)

# Minamos la transacción en el puerto 5001 y ha habido un conflicto
r = requests.get("http://127.0.0.1:5001/minar")
print(r.text)

# Volvemos a registrar los nodos de tal forma que tenemos el mismo blockchain en todos los nodos
nodos_nuevos = {"direccion_nodos": ["http://127.0.0.1:5001", "http://127.0.0.1:5002"]}
r = requests.post(
    "http://127.0.0.1:5000/nodos/registrar",
    data=json.dumps(nodos_nuevos),
    headers=cabecera,
)
print(r.text)

# Creamos una nueva transacción en el puerto 5001
transaccion_nueva = {"origen": "nodoA", "destino": "nodoB", "cantidad": 10}
r = requests.post(
    "http://127.0.0.1:5001/transacciones/nueva",
    data=json.dumps(transaccion_nueva),
    headers=cabecera,
)
print(r.text)

# Minamos la transacción en el puerto 5001
r = requests.get("http://127.0.0.1:5001/minar")
print(r.text)

# Comprobamos la cadena en todos los puertos y vemos que en el nodo 5001 hay un bloque nuevo
r = requests.get("http://127.0.0.1:5000/chain")
print(r.text)

r = requests.get("http://127.0.0.1:5001/chain")
print(r.text)

r = requests.get("http://127.0.0.1:5002/chain")
print(r.text)

# Se realiza el PING del puerto 5000 al 5001 y al 5002 y vemos el retardo en cada puerto
r = requests.get("http://127.0.0.1:5000/ping")
print(r.text)

# Se realiza el PING del puerto 5001 al 5000 y al 5002 y vemos el retardo en cada puerto
r = requests.get("http://127.0.0.1:5001/ping")
print(r.text)

# Se realiza el PING del puerto 5002 al 5000 y al 5001 y vemos el retardo en cada puerto
r = requests.get("http://127.0.0.1:5002/ping")
print(r.text)
