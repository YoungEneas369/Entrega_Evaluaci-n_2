import requests

class MiIndicador:
    def obtener_dolar(self):
        try:
            response = requests.get("https://mindicador.cl/api/dolar", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data['serie'][0]['valor']
        except Exception:
            print("[ALERTA] Aviso: No se pudo conectar a la API. Usando valor fijo ($950.0).")
            return 950.0
        return 950.0
