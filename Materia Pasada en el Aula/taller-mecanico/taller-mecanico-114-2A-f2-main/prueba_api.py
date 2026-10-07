import requests

respuesta=requests.get("https://mindicador.cl/api/dolar",timeout=5)

print(respuesta.status_code)

datos = respuesta.json()

print(datos)

