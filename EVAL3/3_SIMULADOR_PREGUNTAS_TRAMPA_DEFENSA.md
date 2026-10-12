# SIMULADOR DE PREGUNTAS TRAMPA Y DEFENSA INDIVIDUAL
## EVALUACIÓN SUMATIVA N°3 - POOS TI3V21 (INACAP)
**Docente:** Michael Arjel | **Puntaje en juego:** 21 puntos individuales (50% de la nota final)  
**Modalidad:** Preguntas orales al azar con el código proyectado en el editor.

---

## ESTRUCTURA DE LA DEFENSA INDIVIDUAL (5 MINUTOS)
El profesor elegirá al azar a **Cristopher** o a **Elías**, señalará una línea o bloque de código en el editor y realizará preguntas correspondientes a tres categorías obligatorias de la rúbrica:
1. **Explicación línea a línea y Predicción de cambios** (7 pts): *"¿Qué hace esta línea y qué pasaría si la cambio por X?"*
2. **Justificación de una decisión de seguridad** (7 pts): *"¿Por qué está protegido así y qué riesgo evita?"*
3. **Uso crítico de Inteligencia Artificial** (7 pts): *"¿Qué sugirió la IA aquí y por qué decidieron aceptarlo o modificarlo?"*

A continuación se presentan las **12 preguntas trampa más probables** con su respuesta técnica exacta y fundamentada.

---

# CATEGORÍA 1: PREDICCIÓN DE CAMBIOS ("¿QUÉ PASARÍA SI...?")

---

### PREGUNTA 1: Persistencia e Inyección SQL
> **Profesor:** *"Ábreme `dao/paquete_dao.py` en la línea 17. ¿Por qué usan `(?, ?, ?)`? ¿Qué pasaría si reemplazo esa línea por un f-string como este?:"*  
> ```python
> self.cursor.execute(f"INSERT INTO paquete (nombre, precio_base, tipo) VALUES ('{paquete.nombre}', {paquete.precio_base}, '{tipo}')")
> ```

* **Respuesta de Oro (Cristopher o Elías):**
  > "Profesor, si cambiamos los marcadores `?` por un f-string, introducimos una **vulnerabilidad crítica de Inyección SQL (SQL Injection)**.
  > 
  > Al concatenar texto, el motor de SQLite no puede distinguir entre la sintaxis de la consulta y los datos que ingresa el usuario. Si alguien ingresa en el nombre del paquete algo tan simple como un nombre con comilla simple como `O'Higgins 3 Días`, la consulta se rompería con un `OperationalError`. Pero peor aún: un atacante podría escribir `' OR '1'='1` o inyectar comandos maliciosos para manipular o vaciar la base de datos.
  > 
  > Con las **consultas parametrizadas con `?`**, los valores se envían por separado en una tupla. La librería oficial de SQLite sanitiza y escapa automáticamente cada carácter, tratándolo estrictamente como dato literal y nunca como código ejecutable."

---

### PREGUNTA 2: Integridad Referencial y Foreign Keys
> **Profesor:** *"En `conectar.py`, línea 5 tienen `conexion.execute("PRAGMA foreign_keys = ON")`. ¿Qué pasaría si elimino esa línea?"*

* **Respuesta de Oro:**
  > "Por defecto en SQLite, la verificación de claves foráneas viene **desactivada**. Si quitamos esa instrucción, el motor de base de datos ignoraría la restricción `FOREIGN KEY(reserva_id) REFERENCES reserva(id)` en la tabla `detalle_reserva`.
  > 
  > Esto permitiría insertar líneas de detalle asociadas a un ID de reserva inexistente (por ejemplo, `reserva_id = 9999`), generando **registros huérfanos e inconsistencia en la base de datos**. Al activar `PRAGMA foreign_keys = ON`, SQLite rechaza a nivel de motor cualquier inserción o borrado que viole la integridad referencial."

---

### PREGUNTA 3: Transacciones Atómicas y `commit()`
> **Profesor:** *"En `dao/reserva_dao.py`, dentro del método `insertar()`, ¿qué pasaría si quito el `self.conexion.commit()` de la línea 49 o si ocurre un error antes de llegar a esa línea?"*

* **Respuesta de Oro:**
  > "El método `insertar()` ejecuta múltiples sentencias SQL: primero inserta la fila cabecera en `reserva` y luego itera para insertar cada ítem en `detalle_reserva`.
  > 
  > Si quitamos el `commit()`, las operaciones quedarían solo en la memoria transaccional y **nunca se guardarían físicamente en el archivo `agencia.db`**; al cerrar el programa, los datos se perderían.
  > 
  > Además, mantener un único `commit()` al final de todas las inserciones garantiza el principio de **Atomicidad en transacciones (ACID)**: se guardan la reserva y todos sus detalles juntos, o no se guarda nada si falla en el camino, evitando guardar una reserva vacía sin sus ítems contratados."

---

### PREGUNTA 4: Encapsulamiento y Setters en el Modelo
> **Profesor:** *"En `model/viajero.py`, ¿por qué crearon una property y un setter para `numero_pasaporte` en vez de dejar simplemente `self.numero_pasaporte = numero_pasaporte` como atributo público normal? ¿Qué pasaría si elimino el setter?"*

* **Respuesta de Oro:**
  > "Si quitamos el `@setter`, rompemos el principio de **encapsulamiento y validación de entradas**.
  > 
  > Si fuera un atributo público sin setter, cualquier parte del programa podría asignarle una cadena vacía, un número negativo o un texto corrupto como `""` o `123`. Al utilizar `@property` y `@numero_pasaporte.setter`, interceptamos cualquier intento de escritura tanto en el constructor como en el resto del ciclo de vida. Si el pasaporte viene vacío o no cumple con el formato alfanumérico de 6 a 12 caracteres, se detiene de inmediato lanzando un `ValueError`.
  > 
  > Esto actúa como una **barrera de contención** en memoria para que jamás llegue basura o información no verificada a la base de datos."

---

### PREGUNTA 5: Excepciones Propias vs Booleanos / Prints
> **Profesor:** *"En `model/reserva.py`, en el método `validar_confirmacion()`, ¿por qué lanzan `SinCuposError` o `AnticipoInsuficienteError` en vez de simplemente hacer un `print("Error")` o retornar `False`?"*

* **Respuesta de Oro:**
  > "Porque retornar `False` o hacer un `print` viola los principios de la Programación Orientada a Objetos y el manejo seguro de errores (Criterio 2.1.4 y Sesión 8 del curso).
  > 
  > Si el método retornara `False`, el código que lo llama podría olvidar verificar ese valor de retorno y continuar erróneamente guardando la reserva sin cupos o sin pago. Además, un `print` acopla la lógica del modelo con la pantalla.
  > 
  > Al lanzar una **excepción propia tipada (`SinCuposError`)**, forzamos una interrupción limpia del flujo normal que obliga a la capa superior a capturarla con `try/except`. El error queda tipado, es rastreable y permite que la interfaz informe exactamente qué regla de negocio falló sin que el sistema colapse."

---

### PREGUNTA 6: Timeout en la API Externa
> **Profesor:** *"En `servicios/mindicador.py`, tienen `timeout=5`. ¿Qué pasaría si quito ese parámetro y dejo simplemente `requests.get("https://mindicador.cl/api/dolar")`?"*

* **Respuesta de Oro:**
  > "Por defecto en la librería `requests`, si no se define un `timeout`, la llamada espera de forma **indefinida** a que el servidor remoto responda.
  > 
  > Si la API de `mindicador.cl` sufriera un ataque de Denegación de Servicio (DoS), una caída de enlaces o un congelamiento del servidor, **nuestro programa quedaría completamente congelado en esa línea para siempre**, bloqueando al usuario. Al definir `timeout=5`, garantizamos que si en 5 segundos no hay respuesta, la librería corta la espera y lanza `requests.exceptions.RequestException`, permitiendo que nuestro sistema atrape la falla y aplique la política de Fallo Seguro sin congelar la aplicación."

---

# CATEGORÍA 2: JUSTIFICACIÓN DE DECISIONES DE SEGURIDAD

---

### PREGUNTA 7: La Retroalimentación de la ES2 y la Política Fail-Secure
> **Profesor:** *"En la entrega anterior su sistema ponía $950 cuando la API se caía. ¿Por qué cambiaron eso y qué decisión de seguridad tomaron?"*

* **Respuesta de Oro:**
  > "Profesor, en la entrega anterior usamos $950 pensando en garantizar la disponibilidad del servicio. Sin embargo, tras su retroalimentación y analizando la ciberseguridad aplicada al negocio, entendimos que esa decisión violaba el principio de integridad financiera.
  > 
  > Si el dólar real está en $980 o $1.000 y el sistema utiliza un valor fijo de $950, **la agencia asume pérdidas económicas directas y acumulativas por cada reserva vendida**.
  > 
  > Por ello, implementamos el principio de **Fallo Seguro (*Fail-Secure / Fail-Closed*)**:
  > 1. Eliminamos el valor de contingencia estático de $950 en `servicios/mindicador.py`.
  > 2. Si no hay conexión o la API falla, lanzamos `APITipoCambioError`.
  > 3. En `main.py`, capturamos la excepción y **bloqueamos la confirmación de reservas en moneda extranjera**, informando al usuario que la operación se suspende por seguridad financiera.
  > 4. Y con diseño inteligente: los paquetes nacionales siguen reservándose normalmente sin internet porque están tasados en pesos chilenos."

---

### PREGUNTA 8: Inyección del ID Autogenerado (`lastrowid`)
> **Profesor:** *"En `dao/paquete_dao.py`, línea 20, tienen `paquete.id_paquete = self.cursor.lastrowid`. ¿Por qué hacen eso?"*

* **Respuesta de Oro:**
  > "Cuando instanciamos un `Paquete` antes de insertarlo en la base de datos, su atributo `id_paquete` parte en `None` porque aún no existe en el almacenamiento persistente.
  > 
  > Al ejecutar el `INSERT`, el motor SQLite le asigna automáticamente un identificador único mediante `AUTOINCREMENT`. Con `self.cursor.lastrowid`, recuperamos ese valor recién asignado y se lo inyectamos de vuelta al objeto en memoria. De esta manera, el objeto queda completamente sincronizado con su registro en la base de datos para operaciones posteriores (como listarlo, modificarlo o asociarlo a reservas)."

---

### PREGUNTA 9: Captura Específica vs `except Exception`
> **Profesor:** *"En `main.py`, ¿por qué tienen múltiples bloques `except` con nombres como `AnticipoInsuficienteError` y `SinCuposError`, en vez de poner un solo `except Exception as e:`?"*

* **Respuesta de Oro:**
  > "Usar un `except Exception` genérico es una mala práctica conocida como **ocultamiento de errores (Exception Swallowing)**, penalizada expresamente en el criterio 2.1.4 de la rúbrica del curso.
  > 
  > Si usamos un `except` genérico, una falla sintáctica, un error de tipos o un fallo de memoria se mezclaría con una regla de negocio. Al capturar de forma específica y tipada:
  > * `except AnticipoInsuficienteError:` sabemos con certeza que el cliente no pagó el 50%.
  > * `except SinCuposError:` sabemos que el proveedor se quedó sin disponibilidad.
  > * `except APITipoCambioError:` sabemos que falló el servicio externo.
  > 
  > Esto permite entregar mensajes contextualizados y precisos al usuario, manteniendo la robustez del sistema."

---

# CATEGORÍA 3: USO CRÍTICO DE INTELIGENCIA ARTIFICIAL

---

### PREGUNTA 10: Justificación del Aporte de la IA
> **Profesor:** *"¿Qué parte de este código la sugirió la Inteligencia Artificial? Denme un ejemplo concreto de algo que le hayan aceptado y algo que hayan descartado o modificado."*

* **Respuesta de Oro:**
  > "Profesor, documentamos dos casos concretos en el `README.md`:
  > 
  > 1. **Sugerencia que ACEPTAMOS (Arquitectura de Objetos):**
  >    Al diseñar la creación de reservas en `main.py`, la IA nos sugirió instanciar el objeto `Viajero` e integrarlo explícitamente en el constructor de `Reserva (viajero=v)`. Aceptamos esta recomendación porque resolvió un problema de desacoplamiento: de lo contrario, el método `validar_confirmacion()` no tenía acceso al pasaporte en memoria y arrojaba error antes de evaluar las reglas de cupos y anticipo.
  > 
  > 2. **Sugerencia que DESCARTAMOS y RE-DISEÑAMOS (Seguridad en la API):**
  >    Al consultar a la IA sobre cómo manejar la caída de `mindicador.cl`, inicialmente nos sugirió inyectar un valor por defecto fijo de $950 para mantener la disponibilidad. **Descartamos técnicamente esa sugerencia de la IA** tras su retroalimentación en la Evaluación 2, porque comprendimos que priorizar la disponibilidad a ciegas genera pérdidas financieras por descalce de tipo de cambio. En su lugar, decidimos implementar la excepción `APITipoCambioError` bajo el principio de Fallo Seguro (*Fail-Secure*)."

---

### PREGUNTA 11: ¿Por qué separaron Cliente de Viajero?
> **Profesor:** *"En el diagrama y en el código tienen `Cliente` y `Viajero` como clases separadas que heredan de `Persona`. ¿Por qué no dejaron todo en una sola clase?"*

* **Respuesta de Oro:**
  > "Porque en el modelo de negocio de una agencia de viajes, **quien compra y paga no siempre es quien viaja**.
  > 
  > Por ejemplo, un padre puede pagar las vacaciones de su hijo, o una empresa puede comprar pasajes corporativos para sus empleados. Si juntáramos todo en una sola clase, le exigiríamos número de pasaporte a quien paga (el Cliente), lo cual no tiene sentido si él no viajará.
  > 
  > Al separarlos, `Cliente` representa la entidad contractual y financiera, mientras que `Viajero` representa la entidad física que abordará el vuelo, la cual requiere pasaporte vigente para paquetes internacionales."

---

### PREGUNTA 12: Jerarquía de Trabajadores y Menor Privilegio
> **Profesor:** *"¿Por qué `Administrador` y `AgenteViajes` heredan de `Trabajador` y tienen el método `puede_atender_clientes()`?"*

* **Respuesta de Oro:**
  > "Porque el enunciado del negocio establecía explícitamente: *'el agente de viajes atiende clientes y vende paquetes, mientras que el administrador gestiona proveedores y pagos, pero no atiende clientes directamente'*.
  > 
  > Aplicamos el principio de **Menor Privilegio**: en `Administrador`, `puede_atender_clientes()` retorna `False`, mientras que en `AgenteViajes` retorna `True`. Ambos heredan sus atributos comunes (`nombre` y `rut`) desde `Trabajador` y `Persona`, pero cada uno restringe o habilita sus métodos según su rol dentro de la empresa."

---

## CONSEJO FINAL PARA LA DEFENSA
* Cuando el profesor pregunte, **tómense 2 segundos para respirar**, miren la línea de código proyectada y respondan con los términos clave que el profesor quiere escuchar: **Inyección SQL, Encapsulamiento, Fallo Seguro (Fail-Secure), Consultas Parametrizadas, Transacciones Atómicas y Atomicidad**.
