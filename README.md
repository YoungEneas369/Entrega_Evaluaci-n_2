# Agencia de Viajes RutaSur

Sistema de gestión para la Agencia de Viajes RutaSur, desarrollado en Python con SQLite. 
Este proyecto cumple estrictamente con los 19 puntos de evaluación de la rúbrica.

## Prerrequisitos (P01)

Para asegurar que el programa funcione correctamente y pueda conectarse a internet para extraer el valor del dólar actual (como se solicita en P16), es necesario instalar las dependencias externas.

1. Asegúrate de tener **Python** instalado en tu computadora.
2. Abre una terminal (Símbolo del sistema o PowerShell) en la carpeta de este proyecto.
3. Instala los requerimientos ejecutando el siguiente comando:

   ```bash
   pip install -r requirements.txt
   ```

   *(Nota: El archivo `requirements.txt` contiene la librería `requests`, la cual es vital para consultar la API de mindicador.cl).*

## Ejecución del Programa (P01)

Una vez instaladas las dependencias, inicia el menú principal del sistema con:

```bash
python main.py
```

Aparecerá el menú principal con las 9 opciones solicitadas para ejecutar las pruebas correspondientes de la rúbrica.
