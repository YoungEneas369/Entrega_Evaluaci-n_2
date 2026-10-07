# Agencia de Viajes RutaSur

## 1. Integrantes y Negocio
* **Negocio**: Sistema de gestión y reserva de paquetes turísticos para la Agencia de Viajes RutaSur.
* **Integrantes**: [Ingresa los nombres de tu equipo aquí]

## 2. Instalación y Ejecución
1. Clona o descarga el repositorio en tu máquina local.
2. Abre una terminal y navega hasta la carpeta raíz del proyecto (AgenciaViajesEval).
3. Instala las dependencias necesarias ejecutando:
   pip install -r requirements.txt
4. Ejecuta el programa iniciando el archivo principal:
   python main.py

## 3. Decisiones de Seguridad
* **Inyección SQL**: Toda la comunicación con la base de datos SQLite en la capa DAO (Data Access Object) se realiza utilizando consultas parametrizadas (ej. ? en los execute()). Esto previene ataques de inyección SQL, ya que el motor de SQLite sanitiza las variables antes de integrarlas al comando.
* **Validaciones y Encapsulamiento**: Se implementaron decoradores @property y @setter en las clases del modelo (como Persona, Viajero y Reserva). Esto permite validar la integridad de las entradas (por ejemplo, evitar RUTs vacíos o anticipos negativos) e interrumpe el flujo con excepciones propias antes de que los datos corruptos lleguen a la base de datos.
* **Seguridad en la API**: El consumo del indicador del dólar (mindicador.cl) se maneja con la librería equests estableciendo un 	imeout=5. Además, está encapsulado en un bloque 	ry/except que asegura que, si la API sufre un ataque de denegación de servicio o se cae, nuestro sistema atrapa el error e inyecta un valor por defecto (.0), garantizando la continuidad operativa.

## 4. Uso de Inteligencia Artificial
* **Sugerencia adoptada y modificada**: Durante el desarrollo, usamos un asistente de IA para resolver un *bug* lógico en la creación de reservas (Opción 7). La IA nos sugirió instanciar el objeto Viajero e integrarlo explícitamente en el constructor de Reserva (viajero=v). 
* **Razón Técnica**: Adoptamos esta sugerencia porque, de lo contrario, el método .validar_confirmacion() arrojaba un ValidacionError por considerar que no existía el pasaporte en memoria, ocultando otras validaciones como el cálculo del 50% del anticipo. Al acoplar correctamente el objeto Viajero, logramos que las reglas de negocio fluyeran en el orden correcto exigido por la rúbrica.
