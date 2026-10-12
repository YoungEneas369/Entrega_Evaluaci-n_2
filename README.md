# Agencia de Viajes RutaSur

## 1. Integrantes y Negocio
* **Negocio**: Sistema de gestión y reserva de paquetes turísticos para la Agencia de Viajes RutaSur.
* **Integrantes**: Cristopher Figueroa y Elías Reyes

## 2. Instalación y Ejecución
1. Clona o descarga el repositorio en tu máquina local.
2. Abre una terminal y navega hasta la carpeta raíz del proyecto (`Entrega_Evaluaci-n_2`).
3. Instala las dependencias necesarias ejecutando:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta el programa iniciando el archivo principal:
   ```bash
   python main.py
   ```

## 3. Decisiones de Seguridad
* **Inyección SQL**: Toda la comunicación con la base de datos SQLite en la capa DAO (Data Access Object) se realiza utilizando consultas parametrizadas (ej. `?` en los `execute()`). Esto previene ataques de inyección SQL, ya que el motor de SQLite sanitiza las variables antes de integrarlas al comando.
* **Validaciones y Encapsulamiento**: Se implementaron decoradores `@property` y `@setter` en las clases del modelo (como `Persona`, `Viajero` y `Reserva`). Esto permite validar la integridad de las entradas (por ejemplo, evitar RUTs vacíos o anticipos negativos) e interrumpe el flujo con excepciones propias antes de que los datos corruptos lleguen a la base de datos.
* **Seguridad en la API (Política Fail-Secure)**: El consumo del indicador del dólar (`mindicador.cl`) se maneja con la librería `requests` estableciendo un `timeout=5`. Inicialmente se contempló un valor por defecto fijo ($950.0) en caso de caída, pero fue descartado por seguridad financiera: si el dólar real fluctúa y el sistema utiliza una tasa fija desactualizada, la agencia absorbe pérdidas económicas directas. Por ende, se implementó el principio de **Fallo Seguro (*Fail-Secure*)**: ante fallas de red, timeout o caída de la API, se lanza la excepción personalizada `APITipoCambioError`, impidiendo cotizar o reservar paquetes en moneda extranjera sin el valor oficial del día, mientras que los paquetes nacionales siguen operando normalmente sin interrupción.

## 4. Uso de Inteligencia Artificial
* **Sugerencia 1 (Adoptada - Arquitectura de Dominio)**: Durante el desarrollo, usamos un asistente de IA para resolver un *bug* lógico en la creación de reservas (Opción 7). La IA nos sugirió instanciar el objeto `Viajero` e integrarlo explícitamente en el constructor de `Reserva (viajero=v)`. 
  * **Razón Técnica**: Adoptamos esta sugerencia porque, de lo contrario, el método `.validar_confirmacion()` arrojaba un `ValidacionError` por considerar que no existía el pasaporte en memoria, ocultando otras validaciones como el cálculo del 50% del anticipo. Al acoplar correctamente el objeto `Viajero`, logramos que las reglas de negocio fluyeran en el orden correcto exigido por la rúbrica.
* **Sugerencia 2 (Adoptada y Refinada - Seguridad Financiera y Excepciones)**: La IA propuso reemplazar el retorno de un dólar fijo ($950.0) por el lanzamiento de `APITipoCambioError` ante caídas de la API externa.
  * **Razón Técnica**: Cumple con el criterio de Fallo Seguro (*Fail-Secure*), protegiendo la rentabilidad de la agencia frente a la volatilidad cambiaria y aprovechando la jerarquía de excepciones personalizadas (`AgenciaError`) para notificar al usuario de forma clara sin provocar una terminación anormal del sistema (cumpliendo con la prueba P17 de la rúbrica).
