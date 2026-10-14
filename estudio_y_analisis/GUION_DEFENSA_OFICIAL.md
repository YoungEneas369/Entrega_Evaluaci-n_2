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
| **0:00 - 1:30** | Cristopher | Introducción y Arquitectura por Responsabilidades | `main.py`, `conectar.py`, estructura de carpetas |
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
> Nuestro programa separa las responsabilidades. `main.py` presenta el menú y coordina el flujo; `model/` contiene las entidades y reglas del negocio; `dao/` concentra el acceso a SQLite; y `servicios/` aísla la consulta externa del dólar.
>
> En `conectar.py` activamos `PRAGMA foreign_keys = ON` para que SQLite aplique la clave foránea definida entre una reserva y sus líneas de detalle. Esa relación sí está protegida; no todas las entidades del modelo tienen tablas o relaciones en la base de datos."

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
> * `SinCuposError`: en la opción 7 de `main.py` se lanza si los pasajeros superan los cupos ingresados. Además, `Reserva.validar_confirmacion()` comprueba que exista al menos un cupo para la fecha; ese método no recibe la cantidad de pasajeros.
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
> 4. Si las inserciones terminan correctamente, ejecuta `commit()` para confirmarlas.
>
> Es importante describir el límite actual con precisión: `insertar()` no ejecuta `rollback()` si una inserción falla. Por eso no afirmamos que cualquier error revierta automáticamente toda la operación; una mejora sería añadir una reversión explícita ante errores.
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
> Añadimos capturas específicas antes del bloque general. Si falla la API, el sistema captura `APITipoCambioError` y le avisa directamente al usuario:  
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
> En los DAO, los valores variables de las consultas se envían mediante parámetros con signos de interrogación (`?`), en vez de concatenarlos dentro del SQL:
> `cursor.execute('SELECT ... WHERE id = ?', (id,))`  
> Así SQLite trata ese dato como un valor y no como parte de la instrucción SQL. Es una defensa importante contra inyección en esos valores, no una garantía general de seguridad frente a cualquier problema.
> 
> **2. Encapsulamiento con Properties:**  
> Algunas clases, como `Persona`, `Viajero`, `Reserva` y `DetalleReserva`, usan properties para controlar lecturas o asignaciones concretas. `@property` define la lectura; su `@setter` puede limpiar o validar el valor antes de guardarlo. El guión bajo inicial, como en `_nombre`, indica que el atributo es interno por convención, pero no lo vuelve privado de verdad ni todos los atributos del modelo usan properties."

---

### [8:30 - 10:00] PARTE 6: COORDINACIÓN CON EL DIAGRAMA UML Y CIERRE
**Expositor: Elías Reyes**  
*(Acción: Elías muestra la coordinación con el diagrama de clases y concluye)*

> **Elías:**  
> "Por último, coordinamos el código con nuestro diagrama de clases UML:
> * La relación de agregación entre `Reserva` y `DetalleReserva` se implementa mediante la lista de objetos `self.detalles`.
> * Cada `DetalleReserva` guarda una referencia a un `TipoItem`, y su setter comprueba que el valor sea una instancia de esa clase.
> * El método público `validar_pasaporte()` en `Viajero` cumple la misma intención que `+ validarPasaporte(): Boolean` del diagrama; en el código Python usamos el nombre `validar_pasaporte`.
> 
> En conclusión, el sistema RutaSur aplica los conceptos de orientación a objetos, validaciones, excepciones propias, consulta de un servicio externo y persistencia de reservas con sus detalles. También identificamos aspectos que se pueden fortalecer, como añadir `rollback()` ante errores en el guardado. Quedamos atentos a sus preguntas, profesor."
