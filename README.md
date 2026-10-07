# Agencia de Viajes RutaSur

## 1. Integrantes y Negocio
* **Negocio**: Sistema de gestión y reserva de paquetes turísticos para la Agencia de Viajes RutaSur.
* **Integrantes**: Cristopher Figueria y Elias Reyes

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
* **Seguridad en la API**: El consumo del indicador del dólar (mindicador.cl) se maneja con la librería equests estableciendo un 	imeout=5. Además, está encapsulado en un bloque 	ry/except que asegura que, si la API sufre un ataque de denegación de servicio o se cae, nuestro sistema atrapa el error e inyecta un valor por defecto (.0), garantizando la continuidad operativa.

## 4. Uso de Inteligencia Artificial
* **Estructuración de la Base de Datos (Patrón DAO y CRUD)**: Utilizamos la IA como guía para estructurar la capa de acceso a datos (DAO). Nos apoyó en la conexión a la base de datos (SQLite), la declaración de las tablas y la sintaxis SQL para las operaciones (insertar, modificar, consultar y eliminar registros). Adoptamos esta ayuda porque nos facilitó organizar correctamente la arquitectura del proyecto y asegurar que las sentencias a la base de datos funcionaran de manera óptima.
* **Apoyo en Seguridad (Inyección SQL)**: La IA nos asistió con la sintaxis exacta para implementar consultas parametrizadas (el uso de `?` en los métodos `execute()`). Adoptamos esta sugerencia técnica porque garantiza la prevención de ataques de Inyección SQL, delegando la sanitización de los datos al motor de la base de datos.
* **Apoyo en Validaciones y Encapsulamiento**: Si bien los conceptos base los vimos en clases, utilizamos la IA como herramienta de apoyo para estructurar correctamente las validaciones de seguridad dentro de los decoradores `@property` y `@setter`. Adoptamos esta forma de estructurarlo porque nos permitió bloquear datos corruptos y levantar excepciones precisas antes de que afecten la base de datos.
