import requests
from model.excepciones import APITipoCambioError

class MiIndicador:
    def obtener_dolar(self):
        try:
            response = requests.get("https://mindicador.cl/api/dolar", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data['serie'][0]['valor']
            else:
                raise APITipoCambioError(f"La API respondió con código de estado HTTP {response.status_code}.")
        except requests.exceptions.RequestException:
            raise APITipoCambioError("No se pudo conectar a la API del dólar (sin internet o servicio caído).")
        except (KeyError, IndexError, ValueError):
            raise APITipoCambioError("La respuesta de la API no contiene el formato esperado del valor del dólar.")
