# GUION DE PRESENTACIÓN - EVALUACIÓN SUMATIVA N°3 (10 MINUTOS)
**Asignatura:** Programación Orientada a Objeto Seguro (POOS) - TI3V21  
**Docente:** Michael Arjel | **Sección:** 114-2A-F2 | **Laboratorio:** A407  
**Equipo 12:** Agencia de Viajes RutaSur  
**Expositores:** Cristopher Figueroa & Elías Reyes  
**Tiempo Límite:** 10:00 minutos exactos (+ 5:00 minutos de defensa individual)

---

## REGLAS DE ORO DE LA PRESENTACIÓN
1. **NO SE EJECUTA EL PROGRAMA:** Se evalúa y explica el **código proyectado en el editor** (VS Code / Antigravity).
2. **TIMING PRECISO:** 5 minutos para Cristopher y 5 minutos para Elías. Tengan un cronómetro visible en el teléfono.
3. **ROL ACTIVO CON EL EDITOR:** Mientras uno habla, el compañero navega en el editor hacia el archivo y las líneas correspondientes, resaltando el código relevante.

---

## ESTRUCTURA DEL TIEMPO

| Tiempo | Expositor | Tema / Criterio de la Rúbrica | Archivos a Proyectar |
|---|---|---|---|
| **0:00 - 1:30** | Cristopher | Introducción, Arquitectura en 3 Capas y Requisitos No Funcionales | `conectar.py`, estructura general de carpetas |
| **1:30 - 3:30** | Cristopher | Requisitos Funcionales: Polimorfismo, Validaciones y Excepciones | `paquete.py`, `viajero.py`, `excepciones.py` |
| **3:30 - 5:00** | Cristopher | Recorrido Completo de una Operación (Reserva Transaccional) | `main.py` -> `reserva.py` -> `reserva_dao.py` |
| **5:00 - 7:00** | Elías | Incorporación de la Retroalimentación de la ES2 (Política Fail-Secure) | `mindicador.py`, `main.py` (Opción 6 y 7) |
| **7:00 - 8:30** | Elías | Mecanismos de Seguridad del Código (SQL Injection, Encapsulamiento) | `paquete_dao.py`, `reserva_dao.py`, `persona.py` |
| **8:30 - 10:00** | Elías | Uso Crítico de Inteligencia Artificial y Conclusión | `README.md`, `excepciones.py` |

---

# GUION PASO A PASO

---

### [0:00 - 1:30] PARTE 1: INTRODUCCIÓN Y ARQUITECTURA
**Expositor: Cristopher Figueroa**  
*(Acción en pantalla: Elías muestra el árbol de directorios del proyecto y abre `conectar.py`)*

> **Cristopher:**  
> "Buenas tardes profesor Michael y compañeros. Hoy junto a Elías presentamos la defensa de código de nuestro sistema de gestión y reservas para la **Agencia de Viajes RutaSur**, correspondiente a la Evaluación Sumativa N°3.
> 
> Como se puede observar en la estructura de carpetas, nuestro software implementa una **arquitectura desacoplada en tres capas fundamentales**:
> 1. La capa **`model/`**, que encapsula la lógica de negocio y entidades puras de Programación Orientada a Objetos, sin una sola línea de SQL.
> 2. La capa **`dao/`** (Data Access Object), encargada de la persistencia aislada en SQLite.
> 3. La capa **`servicios/`**, que gestiona la comunicación externa hacia la API de indicadores económicos.
> 4. Y **`main.py`**, que actúa como orquestador y controlador de la interfaz de consola.
> 
> Para cumplir con los **Requisitos No Funcionales** de seguridad e integridad:
> * En `conectar.py` (línea 5), ejecutamos `PRAGMA foreign_keys = ON`, lo que fuerza a SQLite a verificar la integridad referencial de base de datos, impidiendo que existan detalles huérfanos sin una reserva válida.
> * Y en todas las clases implementamos sanitización y validación estricta de entradas para evitar datos corruptos."

---

### [1:30 - 3:30] PARTE 2: UBICACIÓN DE REQUISITOS FUNCIONALES
**Expositor: Cristopher Figueroa**  
*(Acción en pantalla: Elías abre `model/paquete.py`, luego `model/viajero.py` y `model/excepciones.py`)*

> **Cristopher:**  
> "Pasando a la ubicación exacta de los **cinco requisitos funcionales** exigidos en la ficha de negocio:
> 
> 1. **Subtipos y Polimorfismo:** En `model/paquete.py`, definimos la clase abstracta `Paquete(ABC)` con el método abstracto `calcular_precio_final()`. Sus tres subtipos en `paquete_nacional.py`, `paquete_internacional.py` y `paquete_crucero.py` sobrescriben este método con `super().__init__()`. El nacional cobra en CLP directo, el internacional multiplica por el tipo de cambio oficial, y el crucero aplica su propia fórmula con un recargo del 12%.
> 
> 2. **Dato con Validación:** En `model/viajero.py` (líneas 12 a 20), el atributo `numero_pasaporte` está protegido y posee un `@setter` que rechaza cadenas vacías y exige un formato alfanumérico estricto de 6 a 12 caracteres mediante `ValueError`.
> 
> 3. **Transacción con Líneas de Detalle:** En `model/reserva.py`, una reserva compone múltiples instancias de `DetalleReserva` (Vuelo, Hotel, Seguro de Viaje, Excursión), catalogadas mediante `TipoItem`.
> 
> 4. **Reglas del Negocio con Excepciones Propias:** En `model/excepciones.py`, creamos `AnticipoInsuficienteError` y `SinCuposError` heredando de `AgenciaError`. En `Reserva.validar_confirmacion()` (líneas 66 a 79), si el anticipo es menor al 50% se lanza `AnticipoInsuficienteError`, y si el proveedor no tiene cupos para la fecha se lanza `SinCuposError`."

---

### [3:30 - 5:00] PARTE 3: EL CAMINO DE UNA OPERACIÓN COMPLETA
**Expositor: Cristopher Figueroa**  
*(Acción en pantalla: Elías muestra el flujo desde `main.py` opción 7, luego `model/reserva.py` y termina en `dao/reserva_dao.py`)*

> **Cristopher:**  
> "Para ilustrar el flujo completo de una operación de punta a punta, sigamos la **creación de una Reserva**:
> 
> 1. **Capa Vista/Controlador (`main.py`):** En la Opción 7 (líneas 181-224), el usuario selecciona el paquete y la cantidad de pasajeros. Se instancian los objetos del modelo `Cliente`, `AgenteViajes`, `Proveedor` y, si es internacional, el `Viajero` con su pasaporte validado.
> 2. **Capa Modelo (`model/reserva.py`):** Se ensambla el objeto `Reserva`, se agregan los cuatro ítems de detalle y se ejecuta `reserva.validar_confirmacion()`. Aquí el modelo valida en memoria que el proveedor tenga cupos y que el anticipo cubra al menos el 50% del total. Si alguna regla falla, la excepción interrumpe el flujo antes de tocar la base de datos.
> 3. **Capa DAO (`dao/reserva_dao.py`):** Una vez validada, `main.py` delega el guardado a `reserva_dao.insertar(reserva)`. En las líneas 34 a 46, el DAO realiza un guardado en dos fases dentro de una **única transacción atómica**:
>    * Primero inserta la cabecera en la tabla `reserva` con `?`.
>    * Recupera el ID autogenerado con `cursor.lastrowid`.
>    * Itera los detalles e inserta cada fila en `detalle_reserva` enlazando la clave foránea `reserva_id`.
>    * Finalmente ejecuta `self.conexion.commit()`.
> 
> Con esto concluyo la primera parte y le doy el pase a mi compañero Elías."

---

### [5:00 - 7:00] PARTE 4: INCORPORACIÓN DE LA RETROALIMENTACIÓN (ES2)
**Expositor: Elías Reyes**  
*(Acción en pantalla: Cristopher abre `servicios/mindicador.py` y luego `main.py` opciones 6 y 7)*

> **Elías:**  
> "Continuando con la presentación, abordaré la **incorporación de la retroalimentación recibida en la Evaluación Sumativa N°2**:
> 
> En la entrega anterior, el profesor nos observó que, ante la caída de la API de tipo de cambio o pérdida de conexión, el sistema utilizaba un valor fijo por defecto de $950.0. Como nos indicó el docente, esto representaba un **riesgo financiero directo**: si el dólar real está en $980 o $1.000 y el sistema vende a $950, la agencia asume pérdidas patrimoniales irreversibles.
> 
> Por este motivo, **reestructuramos la solución aplicando el principio de Fallo Seguro (*Fail-Secure*)**:
> * En `servicios/mindicador.py` (líneas 6 a 15), eliminamos por completo el retorno estático de $950. Si `requests.get` sufre un timeout o no hay internet, lanzamos nuestra excepción propia: `raise APITipoCambioError()`.
> * En `main.py` (líneas 180 a 195 y 240 a 255), capturamos específicamente `APITipoCambioError`:
>   * Si el usuario cotiza o intenta reservar un **Paquete Internacional o Crucero sin conexión**, el sistema informa que la cotización se suspende para proteger las finanzas de la agencia y **bloquea la creación de la reserva**. El programa informa el problema claramente y **no se cae**, cumpliendo con la prueba P17 de la rúbrica.
>   * Pero con un diseño inteligente: si el cliente reserva un **Paquete Nacional**, el sistema reconoce que la tarifa es en CLP y **sí permite reservar**, demostrando que no bloqueamos operaciones que no dependen de divisas.
> * Adicionalmente, en `main.py` corregimos el bloque de captura de excepciones en la reserva, reemplazando el `except Exception` genérico por capturas tipadas de `AnticipoInsuficienteError`, `SinCuposError` y `ValidacionError`."

---

### [7:00 - 8:30] PARTE 5: MECANISMOS DE SEGURIDAD EN EL CÓDIGO
**Expositor: Elías Reyes**  
*(Acción en pantalla: Cristopher proyecta `dao/paquete_dao.py` líneas 17-20 y `dao/reserva_dao.py` líneas 33-46)*

> **Elías:**  
> "En cuanto a cómo protege nuestro código los datos y garantiza la seguridad del sistema:
> 
> 1. **Prevención de Inyección SQL:**
>    En toda la capa DAO (`dao/paquete_dao.py` y `dao/reserva_dao.py`), el 100% de las consultas SQL utilizan **parámetros posicionales `?`**. Jamás concatenamos variables con operadores `+` ni f-strings. Esto garantiza que el motor SQLite trate las entradas del usuario estrictamente como datos binarios y literales, haciendo imposible que caracteres maliciosos como comillas simples o `' OR '1'='1` alteren la estructura del comando SQL.
> 
> 2. **Encapsulamiento y Validación en Setters:**
>    En clases como `Persona`, `Viajero` y `Reserva`, los atributos internos son privados o protegidos (`_nombre`, `_rut`, `_anticipo`, `_numero_pasaporte`). Los decoradores `@property` y `@setter` actúan como una barrera de contención antes de la base de datos, impidiendo estados inválidos como anticipos negativos o RUTs sin formato.
> 
> 3. **Seguridad en Integraciones Externas:**
>    En `MiIndicador.obtener_dolar()`, establecemos `timeout=5`. Esto previene ataques de denegación de servicio por agotamiento de recursos o bloqueos indefinidos del hilo de ejecución en caso de que la API externa sufra una caída prolongada."

---

### [8:30 - 10:00] PARTE 6: USO CRÍTICO DE IA Y CONCLUSIÓN
**Expositor: Elías Reyes**  
*(Acción en pantalla: Cristopher abre `README.md` sección 4)*

> **Elías:**  
> "Para finalizar, de acuerdo con el criterio 4.1.4, documentamos en nuestro `README.md` el **uso crítico y justificado de Inteligencia Artificial**:
> 
> Durante el desarrollo utilizamos un asistente de IA y tomamos decisiones fundamentadas:
> * **Sugerencia 1 (Adoptada):** La IA nos propuso acoplar la instancia del `Viajero` directamente en el constructor de `Reserva(viajero=v)`. La adoptamos porque resolvió un desacoplamiento que impedía que `validar_confirmacion()` verificara la presencia del pasaporte antes de evaluar las reglas de cupos y anticipo.
> * **Sugerencia 2 (Descartada y Re-diseñada):** Inicialmente, la IA sugirió inyectar un valor de contingencia estático de $950 ante errores de la API para mantener la disponibilidad. **Descartamos técnicamente esa recomendación** tras el feedback del docente, porque priorizamos la integridad financiera sobre la disponibilidad ciega, reemplazándola por la política *Fail-Secure* con `APITipoCambioError`.
> 
> En conclusión, nuestro software es robusto, modular, respeta la separación de responsabilidades de la POO segura y protege tanto la base de datos como las finanzas del negocio.
> 
> Quedamos a su disposición para las preguntas individuales. Muchas gracias."

---

## CONSEJOS CLAVE PARA EL CONTROL DEL TIEMPO (10 MIN)
* **Si Cristopher va en el minuto 4:30:** Empieza a cerrar el recorrido de la reserva de inmediato para entregarle la palabra a Elías a los 5:00.
* **Si Elías va en el minuto 9:00:** Pasa directamente a la conclusión del uso de IA en `README.md` para cerrar antes del minuto 10:00.
* Mantengan un tono tranquilo, técnico y seguro. No duden ni pidan disculpas: hablen de objetos, transacciones, encapsulamiento y consultas parametrizadas.
