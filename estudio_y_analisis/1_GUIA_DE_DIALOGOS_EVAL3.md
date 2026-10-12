# GUÍA DE DIÁLOGOS OFICIAL: EVALUACIÓN SUMATIVA N°3 (10 MINUTOS)
## PRESENTACIÓN ORAL DEL CÓDIGO - AGENCIA DE VIAJES RUTASUR
**Asignatura:** Programación Orientada a Objeto Seguro (POOS TI3V21)  
**Docente:** Michael Arjel | **Sección:** 114-2A-F2 | **Laboratorio:** A407  
**Equipo 12:** Cristopher Figueroa y Elías Reyes  
**Regla de Oro:** El programa **NO se ejecuta**; se expone y explica el **código proyectado en el editor**.

---

## CRONOGRAMA DE DIÁLOGOS (EXACTAMENTE 10 MINUTOS)

```
[0:00 - 1:30] Cristopher: Introducción, Arquitectura y Coordinación con Diagrama UML
[1:30 - 3:30] Cristopher: Los 5 Requisitos Funcionales y 2 No Funcionales en el Código
[3:30 - 5:00] Cristopher: El Camino Completo de una Operación (Reserva Transaccional)
------------------ CAMBIO DE PALABRA (MINUTO 5:00) ------------------
[5:00 - 7:00] Elías:      Retroalimentación ES2 Corregida (Política Fail-Secure en API)
[7:00 - 8:30] Elías:      Seguridad en Persistencia (Prevención de Inyección SQL y Setters)
[8:30 - 10:00] Elías:     Uso Crítico de Inteligencia Artificial y Cierre
```

---

# GUION DE DIÁLOGOS COMPLETO

---

### [0:00 - 1:30] BLOQUE 1: INTRODUCCIÓN Y ARQUITECTURA
**Habla:** Cristopher Figueroa  
**Acción en pantalla (Elías):** Proyecta la raíz del proyecto con el árbol de carpetas abierto y luego abre el archivo `conectar.py`.

> **Cristopher:**  
> "Buenas tardes profesor Michael y compañeros. Junto a Elías presentamos la defensa de código de nuestro sistema para la **Agencia de Viajes RutaSur**, correspondiente a la Evaluación Sumativa N°3.
> 
> Nuestro software refleja fielmente el diagrama UML que diseñamos en la Unidad 1 (`Diagrama_RutaSur.drawio`), implementando una **arquitectura desacoplada en tres capas principales**:
> 
> 1. La capa **`model/`**, donde viven las entidades del dominio en Programación Orientada a Objetos pura: herencia, validaciones y reglas del negocio, sin escribir una sola línea de SQL.
> 2. La capa **`dao/`** (Data Access Object), responsable exclusiva de la persistencia segura hacia SQLite.
> 3. La capa **`servicios/`**, que gestiona el consumo de la API externa del dólar mediante la librería `requests`.
> 4. Y **`main.py`**, que actúa como orquestador del menú de usuario.
> 
> Como primer **Requisito No Funcional de integridad referencial**, como se observa en `conectar.py`, línea 5, ejecutamos `PRAGMA foreign_keys = ON` al iniciar cada conexión. Esto obliga a SQLite a forzar la integridad entre tablas, impidiendo la existencia de detalles huérfanos sin una reserva asociada."

---

### [1:30 - 3:30] BLOQUE 2: UBICACIÓN DE REQUISITOS EN EL CÓDIGO
**Habla:** Cristopher Figueroa  
**Acción en pantalla (Elías):** Abre secuencialmente `model/paquete.py`, `model/viajero.py` y `model/excepciones.py`.

> **Cristopher:**  
> "A continuación, identificamos en el código los **cinco requisitos funcionales** exigidos en la ficha de nuestro negocio:
> 
> 1. **Subtipos y Polimorfismo:** En `model/paquete.py`, definimos la clase abstracta `Paquete(ABC)` con el método abstracto `calcular_precio_final()`. Sus tres subclases en `paquete_nacional.py`, `paquete_internacional.py` y `paquete_crucero.py` sobrescriben este método:
>    * El paquete nacional devuelve el precio base directo en Pesos Chilenos (CLP) sin considerar divisas.
>    * El paquete internacional multiplica su precio base en USD por el tipo de cambio oficial del día.
>    * Y el paquete crucero aplica la fórmula de cotización en dólares agregando un recargo del 12% por tasas portuarias (`* 1.12`).
> 
> 2. **Dato con Validación:** En `model/viajero.py`, líneas 12 a 23, el atributo `numero_pasaporte` está encapsulado. Su setter `@numero_pasaporte.setter` valida que no esté vacío, lo sanitiza a mayúsculas y exige entre 6 y 12 caracteres alfanuméricos mediante `ValueError`. Además, implementamos el método público `validar_pasaporte()`, coordinando exactamente con el método `+ validarPasaporte(): Boolean` de nuestro diagrama UML.
> 
> 3. **Transacción con Líneas de Detalle:** En `model/reserva.py`, una reserva compone una lista de objetos `DetalleReserva` (Vuelo, Hotel, Seguro, Excursión), clasificados mediante la clase de catálogo `TipoItem`.
> 
> 4. **Dos Reglas de Negocio con Excepciones Propias:** En `model/excepciones.py`, creamos `AnticipoInsuficienteError` y `SinCuposError` heredando de `AgenciaError`. En `Reserva.validar_confirmacion()` (líneas 66 a 79), si el anticipo pagado es menor al 50% del total se lanza `AnticipoInsuficienteError`, y si el proveedor no tiene disponibilidad para la fecha de viaje se lanza `SinCuposError`."

---

### [3:30 - 5:00] BLOQUE 3: EL CAMINO DE UNA OPERACIÓN COMPLETA
**Habla:** Cristopher Figueroa  
**Acción en pantalla (Elías):** Sigue el flujo abriendo `main.py` (líneas 180 a 245), luego `model/reserva.py` (líneas 66 a 80) y finalmente `dao/reserva_dao.py` (líneas 30 a 50).

> **Cristopher:**  
> "Para demostrar la interacción entre capas, recorreremos el flujo completo de la **creación de una Reserva**:
> 
> 1. **Capa Interfaz (`main.py` - Opción 7):** El usuario ingresa los datos por consola. Se instancian los objetos del modelo: `Cliente`, `AgenteViajes`, `Proveedor` y, si el paquete es internacional, el `Viajero` con su pasaporte validado.
> 2. **Capa Modelo (`model/reserva.py`):** Se crea la instancia de `Reserva` y se le añaden cuatro líneas de `DetalleReserva`. Antes de tocar la base de datos, se ejecuta `reserva.validar_confirmacion()`. El modelo valida en memoria que el proveedor tenga cupos y que el anticipo cubra al menos el 50% del total. Si una regla se viola, se lanza la excepción propia y se frena el flujo.
> 3. **Capa DAO (`dao/reserva_dao.py`):** Superada la validación, `main.py` delega a `reserva_dao.insertar(reserva)`. En las líneas 34 a 49 se ejecuta una **transacción atómica**:
>    * Se inserta la cabecera en la tabla `reserva` con parámetros `?`.
>    * Se recupera el ID autogenerado mediante `self.cursor.lastrowid`.
>    * Se itera cada detalle insertándolo en la tabla `detalle_reserva` con la clave foránea `reserva_id`.
>    * Y se confirma todo con un único `self.conexion.commit()`.
> 
> Con esto concluyo la primera parte del recorrido y le doy el pase a mi compañero Elías."

---

### [5:00 - 7:00] BLOQUE 4: RETROALIMENTACIÓN DE LA ES2 CORREGIDA
**Habla:** Elías Reyes  
**Acción en pantalla (Cristopher):** Abre `servicios/mindicador.py` (líneas 6 a 18) y luego `main.py` (líneas 175 a 190 y 240 a 255).

> **Elías:**  
> "Continuando con la exposición, presento la **incorporación de la retroalimentación que recibimos en la Evaluación Sumativa N°2**:
> 
> En la entrega anterior, cuando la API de tipo de cambio no respondía o se cortaba internet, el sistema capturaba el error e inyectaba un valor fijo de contingencia de $950.0. El profesor nos hizo notar que esto representaba un **riesgo financiero directo**: si el dólar real está en $980 o $1.000 y el sistema vende a $950, la agencia absorbe una pérdida económica en cada reserva.
> 
> Atendiendo esta observación, **reestructuramos la solución bajo el principio de Fallo Seguro (*Fail-Secure*)**:
> * En `servicios/mindicador.py`, eliminamos el valor fijo de $950. Si `requests.get` sufre un timeout o no hay conexión, lanzamos nuestra excepción propia: `raise APITipoCambioError()`.
> * En `main.py`, capturamos específicamente esta excepción:
>   * Si el usuario cotiza o intenta reservar un paquete internacional o crucero sin internet, el sistema notifica que la operación se suspende por seguridad financiera y **bloquea la creación de la reserva**, protegiendo el patrimonio de la empresa sin que el programa colapse, cumpliendo la prueba P17.
>   * Y como muestra de diseño inteligente: si el cliente reserva un **Paquete Nacional**, el sistema reconoce que la tarifa es en moneda local y **sí permite reservar**, demostrando que no bloqueamos operaciones que no dependen del dólar.
> * Adicionalmente, en la captura de excepciones de la reserva en `main.py`, eliminamos el bloque genérico `except Exception` y lo reemplazamos por capturas tipadas e individuales de `AnticipoInsuficienteError`, `SinCuposError` y `ValidacionError`."

---

### [7:00 - 8:30] BLOQUE 5: SEGURIDAD DEL CÓDIGO
**Habla:** Elías Reyes  
**Acción en pantalla (Cristopher):** Proyecta `dao/paquete_dao.py` (líneas 17-20) y `model/persona.py` (líneas 9-33).

> **Elías:**  
> "Respecto a cómo protege nuestro código los datos:
> 
> 1. **Prevención de Inyección SQL:**
>    En toda la capa DAO (`paquete_dao.py` y `reserva_dao.py`), el 100% de las consultas SQL utilizan **consultas parametrizadas con marcadores `?`**, enviando los datos por separado en tuplas. Jamás usamos concatenación de texto con `+` ni f-strings. Esto garantiza que el motor SQLite trate los valores como datos literales, haciendo imposible que caracteres maliciosos como comillas simples o la inyección `' OR '1'='1` alteren los comandos de la base de datos.
> 
> 2. **Encapsulamiento y Sanitización en Setters:**
>    En clases como `Persona`, `Viajero` y `Reserva`, los atributos están protegidos con guión bajo (`_nombre`, `_rut`, `_anticipo`, `_numero_pasaporte`). Los decoradores `@property` y `@setter` actúan como una barrera de contención previa a la base de datos, impidiendo estados corruptos como anticipos negativos o RUTs vacíos.
> 
> 3. **Seguridad en Integraciones Externas:**
>    En `MiIndicador.obtener_dolar()`, establecemos `timeout=5`. Esto evita ataques de denegación de servicio por agotamiento de recursos o bloqueos indefinidos del sistema si el servidor remoto de la API no responde."

---

### [8:30 - 10:00] BLOQUE 6: USO CRÍTICO DE IA Y CIERRE
**Habla:** Elías Reyes  
**Acción en pantalla (Cristopher):** Abre `README.md` (Sección 4).

> **Elías:**  
> "Para finalizar, de acuerdo con el criterio 4.1.4, documentamos en nuestro `README.md` el **uso crítico y justificado de Inteligencia Artificial**:
> 
> Durante el desarrollo utilizamos un asistente de IA aplicando criterio técnico a sus propuestas:
> * **Sugerencia 1 (Adoptada):** La IA nos propuso acoplar la instancia del `Viajero` directamente en el constructor de `Reserva (viajero=v)`. Adoptamos esta sugerencia porque resolvió un desacoplamiento que impedía que `validar_confirmacion()` verificara el pasaporte antes de evaluar las reglas de cupos y anticipo.
> * **Sugerencia 2 (Descartada y Re-diseñada):** Inicialmente, la IA sugirió usar un valor de contingencia estático de $950 ante caídas de la API. **Descartamos técnicamente esa sugerencia** tras el feedback del docente, ya que priorizaba la disponibilidad a costa de pérdidas económicas, reemplazándola por la excepción personalizada `APITipoCambioError` bajo el principio de Fallo Seguro.
> 
> En conclusión, nuestro software es seguro, respeta los patrones de diseño orientados a objetos y protege tanto los datos como la rentabilidad de la agencia.
> 
> Quedamos a su disposición para las preguntas individuales. Muchas gracias."
