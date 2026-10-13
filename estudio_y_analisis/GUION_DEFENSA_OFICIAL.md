# GUION OFICIAL DE DEFENSA (10 MINUTOS)
## Evaluación Sumativa N°3 - POOS TI3V21
**Agencia de Viajes RutaSur**  
**Expositores:** Cristopher Figueroa y Elías Reyes  
**Docente:** Michael Arjel  

---

## ESTRUCTURA DEL TIEMPO

| Tiempo | Expositor | Tema Principal | Archivos de Apoyo |
| :--- | :--- | :--- | :--- |
| **0:00 - 1:30** | Cristopher | Introducción y Arquitectura en 3 Capas | `conectar.py`, estructura de carpetas |
| **1:30 - 3:30** | Cristopher | Los 5 Requisitos de la Ficha en el Modelo POO | `model/` (`paquete.py`, `viajero.py`, `reserva.py`, `excepciones.py`) |
| **3:30 - 5:00** | Cristopher | Flujo de la Transacción con Líneas de Detalle | `main.py` -> `reserva.py` -> `dao/reserva_dao.py` |
| **5:00 - 7:00** | Elías | Modificaciones ES2 vs ES3 (API y Excepciones) | `servicios/mindicador.py`, `main.py` |
| **7:00 - 8:30** | Elías | Seguridad: Inyección SQL y Encapsulamiento | `dao/paquete_dao.py`, `dao/reserva_dao.py`, `model/persona.py` |
| **8:30 - 10:00** | Elías | Conclusión y Coordinación con el Diagrama UML | Diagrama UML vs Código |

---

# DIÁLOGO DE LA PRESENTACIÓN

---

### [0:00 - 1:30] PARTE 1: INTRODUCCIÓN Y ARQUITECTURA
**Expositor: Cristopher Figueroa**  
*(Acción: Elías proyecta el editor mostrando las carpetas y abre `conectar.py`)*

> **Cristopher:**  
> "Buenas tardes profesor Michael y compañeros. Junto a Elías presentamos la defensa de código de nuestro sistema de gestión para la **Agencia de Viajes RutaSur**, correspondiente a la Evaluación Sumativa N°3.
> 
> Nuestro software está organizado en una arquitectura de tres capas limpiamente separadas:
> 1. La capa **`model/`**, donde reside la lógica del negocio pura con clases y objetos, sin ninguna consulta SQL.
> 2. La capa **`dao/`**, que implementa el patrón Data Access Object para centralizar las consultas SQLite.
> 3. La capa **`servicios/`**, encargada de la comunicación externa mediante la API del dólar.
> 
> Además, en `conectar.py` activamos de forma obligatoria la instrucción `PRAGMA foreign_keys = ON;` para garantizar que la base de datos proteja la integridad referencial y las claves foráneas entre reservas y sus detalles."

---

### [1:30 - 3:30] PARTE 2: LOS 5 REQUISITOS DE LA FICHA EN EL MODELO POO
**Expositor: Cristopher Figueroa**  
*(Acción: Elías abre `model/paquete.py`, `model/viajero.py` y `model/reserva.py`)*

> **Cristopher:**  
> "En el modelo damos cumplimiento estricto a los 5 requisitos de la ficha de evaluación:
> 
> **1. Subtipos y Polimorfismo:**  
> En `model/paquete.py` definimos la clase abstracta padre `Paquete(ABC)` con el método abstracto `calcular_precio_final()`. Sus tres subclases hijas sobrescriben este método con su propio cálculo:
> * `PaqueteNacional` devuelve el precio base directo en pesos chilenos sin aplicar tipo de cambio.
> * `PaqueteInternacional` multiplica su precio base en dólares por el valor del dólar obtenido de la API.
> * `PaqueteCrucero` multiplica el precio por el dólar y además por `1.12`, aplicando un recargo del 12% por tasas portuarias.
> 
> **2. Dato con Validación:**  
> En `model/viajero.py`, el atributo `numero_pasaporte` está encapsulado. Su setter valida que no esté vacío, lo convierte a mayúsculas y exige entre 6 y 12 caracteres alfanuméricos mediante `ValueError`. Además, implementamos el método público `validar_pasaporte()`, coordinado exactamente con el método `+ validarPasaporte(): Boolean` de nuestro diagrama UML.
> 
> **3. Reglas de Negocio con Excepciones Propias:**  
> En `model/excepciones.py` creamos excepciones específicas que heredan de una base común:
> * `AnticipoInsuficienteError`: se lanza en `reserva.py` si el cliente abona menos del 50% del total de la reserva.
> * `SinCuposError`: se lanza si la cantidad de pasajeros supera la disponibilidad del proveedor.
> 
> **4. Integrador Externo:**  
> El servicio `servicios/mindicador.py` consulta el tipo de cambio oficial para cotizar los paquetes internacionales."

---

### [3:30 - 5:00] PARTE 3: TRANSACCIÓN CON LÍNEAS DE DETALLE
**Expositor: Cristopher Figueroa**  
*(Acción: Elías abre `model/reserva.py`, luego `model/detalle_reserva.py` y `dao/reserva_dao.py`)*

> **Cristopher:**  
> "**5. Transacción con Líneas de Detalle:**  
> En `model/reserva.py`, cada objeto `Reserva` se compone de una lista llamada `detalles`.  
> No creamos clases sueltas para cada servicio; utilizamos la clase **`DetalleReserva`**, la cual se asocia con un **`TipoItem`** que define la categoría (como Vuelo, Hotel, Seguro o Excursión) junto con su cantidad y precio unitario.
> 
> El método `reserva.total()` calcula el costo final sumando el precio del paquete principal más el subtotal de cada objeto `DetalleReserva` en la lista.
> 
> Cuando pasamos a la base de datos en `dao/reserva_dao.py`, el método `insertar()` ejecuta una transacción atómica real:
> 1. Inserta primero la cabecera en la tabla `reserva` con `INSERT INTO reserva`.
> 2. Recupera el ID autogenerado mediante `self.cursor.lastrowid`.
> 3. Recorre la lista de detalles insertando cada fila en `detalle_reserva` vinculada a ese ID foráneo.
> 4. Si todo es correcto ejecuta `commit()`. Si algo falla, el motor aborta la operación completa para evitar datos huérfanos.
> 
> Ahora le cedo la palabra a mi compañero Elías para explicar las modificaciones de la evaluación y la seguridad del sistema."

---

### [5:00 - 7:00] PARTE 4: MODIFICACIONES DE LA EVALUACIÓN (ES2 vs ES3)
**Expositor: Elías Reyes**  
*(Acción: Elías abre `servicios/mindicador.py` y luego `main.py` en la Opción 7)*

> **Elías:**  
> "Gracias Cristopher. A partir de la retroalimentación de la Evaluación 2, realizamos dos modificaciones fundamentales en el código:
> 
> **Primero, eliminamos el valor por defecto en la API:**  
> En la entrega anterior, si la API del dólar fallaba por falta de internet, el sistema utilizaba silenciosamente un valor fijo de $950 CLP. Identificamos que esto representaba un grave riesgo financiero para la agencia si el dólar real subía.  
> Ahora, en `servicios/mindicador.py`, ante un corte de red se lanza la excepción `APITipoCambioError`.  
> 
> **Segundo, captura de errores clara en `main.py`:**  
> Reemplazamos la captura genérica `except Exception` por bloques específicos. Si falla la API, el sistema captura `APITipoCambioError` y le avisa directamente al usuario:  
> *'No hay conexión a internet, no se puede cotizar la reserva. Los paquetes nacionales sí se pueden reservar sin internet'*.  
> De este modo, protegemos las finanzas del negocio y a la vez mantenemos el software resiliente y operativo para viajes nacionales."

---

### [7:00 - 8:30] PARTE 5: SEGURIDAD (SQL INJECTION Y ENCAPSULAMIENTO)
**Expositor: Elías Reyes**  
*(Acción: Elías abre `dao/paquete_dao.py` líneas 25-35 y luego `model/persona.py`)*

> **Elías:**  
> "En materia de seguridad del código implementamos dos defensas clave:
> 
> **1. Prevención de Inyección SQL:**  
> En todas las clases DAO (`paquete_dao.py` y `reserva_dao.py`), ninguna consulta concatena texto con variables. Usamos exclusivamente **consultas parametrizadas con signos de interrogación (`?`)**:
> `cursor.execute('SELECT ... WHERE id = ?', (id,))`  
> Esto delega la sanitización al motor de SQLite, neutralizando cualquier intento de inyección maliciosa.
> 
> **2. Encapsulamiento con Properties:**  
> En `model/persona.py` y en las clases del modelo protegemos los atributos internos con guión bajo (por ejemplo `_rut` y `_nombre`). El decorador `@property` actúa como getter y el `@setter` valida los tipos y formatos antes de asignar memoria, impidiendo estados inconsistentes."

---

### [8:30 - 10:00] PARTE 6: COORDINACIÓN CON EL DIAGRAMA UML Y CIERRE
**Expositor: Elías Reyes**  
*(Acción: Elías muestra la coordinación con el diagrama de clases y concluye)*

> **Elías:**  
> "Por último, coordinamos el código con nuestro diagrama de clases UML:
> * La relación de agregación entre `Reserva` y `DetalleReserva` se implementa mediante la lista de objetos `self.detalles`.
> * La composición con `TipoItem` garantiza que cada detalle posea su categoría formal.
> * Y el método público `validar_pasaporte()` en `Viajero` da cumplimiento exacto a la firma `+ validarPasaporte(): Boolean` del modelo.
> 
> En conclusión, el sistema RutaSur no solo satisface los 5 requisitos de la ficha y las reglas de negocio, sino que cuenta con una arquitectura mantenible, segura y resistente a fallos. Quedamos atentos a sus preguntas, profesor."
