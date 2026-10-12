# GUÍA EVOLUTIVA PASO A PASO: DESDE CERO HASTA EL SISTEMA FINAL
## CÓMO SE CONSTRUYÓ, CÓMO SE CONECTA TODO Y CÓMO FUNCIONA CADA PARTE
**Agencia de Viajes RutaSur** — Evaluación Sumativa N°3  
**Para:** Cristopher Figueroa y Elías Reyes

---

## 0. ACLARACIÓN PREVIA: EL GRAN MISTERIO DE LOS "TRES NOMBRES" (`self.nombre = nombre`)

Antes de ver el paso a paso, resolvamos la duda más común que confunde a cualquiera en Python:
¿Por qué en una sola línea vemos `nombre` repetido tantas veces?

```python
class Persona:
    def __init__(self, nombre: str):
        self.nombre = nombre
```

Parece un trabalenguas:
1. `nombre` en el paréntesis del `__init__(self, nombre)`: Es la **variable temporal que viene desde afuera**. Es el dato crudo que alguien escribió (por ejemplo: `"Cristopher"`).
2. `self.nombre = ...` (a la izquierda del signo `=`): **NO es una variable común**. Debido al decorador `@nombre.setter`, escribir `self.nombre =` en Python significa: *"Ejecuta de inmediato la función validadora `nombre(self, valor)`"*.
3. `= nombre` (a la derecha del signo `=`): Es el dato que venía en el paréntesis de afuera (`"Cristopher"`), que entra como el argumento `valor` del setter.

### ¿Cómo funciona la tríada en la práctica?

```python
class Persona:
    # 1. EL CONSTRUCTOR: Recibe el dato desde el teclado o menú
    def __init__(self, nombre: str):
        self.nombre = nombre  # <-- Dispara al setter automáticamente

    # 2. EL GETTER (Sin llamarse 'get'): 
    # El decorador @property disfraza una función como si fuera una variable.
    # Cuando alguien escribe 'print(p.nombre)', Python ejecuta esto por detrás.
    @property
    def nombre(self) -> str:
        return self._nombre  # <-- Devuelve el dato guardado en la caja real

    # 3. EL SETTER (El guardia de seguridad):
    # Cuando alguien escribe 'p.nombre = "algo"', Python salta aquí.
    # 'valor' es lo que venía a la derecha del signo '='.
    @nombre.setter
    def nombre(self, valor: str) -> None:
        valor = str(valor).strip()
        if len(valor) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres.")
        # Aquí recién se guarda en la variable real privada con guión bajo:
        self._nombre = valor
```

* **`self._nombre` (con guión bajo):** Es el **casillero real y privado** en la memoria del computador. Nadie de afuera debería tocarlo directamente.
* **`nombre` (sin guión bajo):** Es la **puerta de entrada pública**. Siempre que alguien intenta leer o escribir en `nombre`, pasa por el guardia de seguridad (`@property` o `@setter`).

---

# PASO 1: EL INICIO EN MEMORIA (CREAR EL MODELO POO)

En la primera etapa del proyecto, el profesor no pidió base de datos ni internet. Solo pidió representar el negocio en código puro de Python dentro de la carpeta `model/`.

### 1.1 La Clase Raíz: `model/persona.py`
Todo parte con una persona.
* **¿Qué instrucción usamos?** Creamos una clase abstracta `Persona(ABC)` porque en la vida real nadie es "solo una persona"; en nuestro negocio eres un Cliente, un Viajero o un Trabajador.
* **¿Qué recibe?**
  * `nombre`: Texto con el nombre.
  * `rut`: Texto con el RUT (ej: `"11111111-1"`).
* **¿Qué restricciones tiene?**
  * El setter de `nombre` exige mínimo 2 letras y prohíbe números.
  * El setter de `rut` exige que tenga guión `-` y al menos 8 caracteres.

### 1.2 La Diferenciación Clave: `Cliente` vs `Viajero`
* **El problema de negocio:** El profesor preguntó: *"¿Quién compra es siempre quien viaja?"*. La respuesta es **NO**. Un padre puede pagar las vacaciones de su hijo.
* **`model/cliente.py`:**
  * Hereda de `Persona` con `super().__init__(nombre, rut)`.
  * Representa al comprador/pagador. **No tiene pasaporte**.
* **`model/viajero.py`:**
  * Hereda de `Persona`, pero recibe 3 datos: `__init__(self, rut, nombre, numero_pasaporte)`.
  * **¿Qué hace `super().__init__(nombre, rut)`?** Le pasa el nombre y el RUT a la clase padre `Persona` para que ella los valide y guarde, mientras que `Viajero` se encarga de su dato único: el pasaporte.
  * **Validación del Pasaporte:** El setter `@numero_pasaporte.setter` convierte a mayúsculas con `.upper()`, prohíbe que esté vacío y exige que tenga entre 6 y 12 caracteres alfanuméricos.

### 1.3 Los Empleados: `Trabajador`, `Administrador` y `AgenteViajes`
* El enunciado decía: *"El agente de viajes atiende clientes y vende paquetes. El administrador gestiona proveedores y pagos, pero no atiende clientes"*.
* **`model/trabajador.py`:** Clase abstracta intermedia hija de `Persona`.
* **`model/administrador.py`:**
  * Método `puede_atender_clientes()` $\rightarrow$ retorna `False`.
* **`model/agente_viajes.py`:**
  * Método `puede_atender_clientes()` $\rightarrow$ retorna `True`.

---

# PASO 2: LOS PRODUCTOS Y EL POLIMORFISMO (`Paquete`)

El negocio vende 3 tipos de viaje. Cada uno calcula su precio de forma distinta.

### 2.1 La Clase Abstracta: `model/paquete.py`
* **¿Qué recibe el constructor?** `(id_paquete, nombre, precio_base, proveedor_id)`
  * `id_paquete`: Parte en `None` porque al nacer en memoria aún no tiene ID de base de datos.
  * `precio_base`: Número flotante mayor a cero (validado por su setter).
* **El método abstracto:**
  ```python
  @abstractmethod
  def calcular_precio_final(self, tipo_cambio=950):
      pass
  ```
  Esto obliga a que cualquier paquete hijo tenga obligatoriamente esta función, pero con su propia fórmula.

### 2.2 Los Tres Hijos y sus Fórmulas
1. **`model/paquete_nacional.py`:**
   * **Fórmula:** `return round(self.precio_base)`
   * **Explicación:** Se vende en Chile en Pesos Chilenos (CLP). **No le importa el dólar**.
2. **`model/paquete_internacional.py`:**
   * **Fórmula:** `return round(self.precio_base * tipo_cambio)`
   * **Explicación:** Su precio base está en dólares (USD). Se multiplica por el valor del dólar del día.
3. **`model/paquete_crucero.py`:**
   * **Fórmula:** `return round(self.precio_base * tipo_cambio * 1.12)`
   * **Explicación:** Está en dólares y además tiene un recargo portuario del 12% (`* 1.12`).

---

# PASO 3: LAS REGLAS DEL NEGOCIO Y EXCEPCIONES PROPIAS

El enunciado exigía dos reglas que impidieran confirmar una reserva:
1. No confirmar sin al menos el 50% de anticipo.
2. No reservar si el proveedor no tiene cupos para esa fecha.

### 3.1 Crear las Excepciones: `model/excepciones.py`
En vez de usar `print("Error")` o `return False` (lo cual es una mala práctica), creamos clases de error:
```python
class AgenciaError(Exception): pass
class AnticipoInsuficienteError(AgenciaError): pass
class SinCuposError(AgenciaError): pass
class ValidacionError(AgenciaError): pass
class APITipoCambioError(AgenciaError): pass
```

### 3.2 El Proveedor y sus Cupos: `Proveedor` y `Disponibilidad`
* **`model/disponibilidad.py`:** Guarda una `fecha` (ej: `"2026-12-01"`) y sus `cupos_disponibles` (ej: `5`).
  * `tiene_cupos()`: Retorna `True` si cupos $> 0$.
  * `descontar_cupo()`: Resta 1 al cupo.
* **`model/proveedor.py`:** Tiene una lista de disponibilidades.
  * `tiene_cupos(fecha)`: Busca si para esa fecha hay cupos disponibles.

### 3.3 El Ensamblado Maestro: `model/reserva.py`
Una reserva reúne todo:
* Cliente, Agente, Paquete, Proveedor, Fecha, Anticipo, Viajero y una lista de `DetalleReserva` (Vuelo, Hotel, Seguro, Excursión).
* **El método `validar_confirmacion()`:**
  1. Si el paquete es internacional y no hay viajero con pasaporte $\rightarrow$ `raise ValidacionError(...)`.
  2. Si el proveedor no tiene cupos $\rightarrow$ `raise SinCuposError(...)`.
  3. Si el anticipo es menor al 50% del total $\rightarrow$ `raise AnticipoInsuficienteError(...)`.
  4. Si todo está correcto $\rightarrow$ cambia estado a `CONFIRMADA` y retorna `True`.

---

# PASO 4: LA PERSISTENCIA EN BASE DE DATOS (EL PATRÓN DAO)

Hasta este punto, si apagabas el computador, todos los objetos se borraban de la memoria RAM.
Aquí entra la Unidad 2 del profesor: **Guardar en SQLite de forma segura**.

### 4.1 La Conexión Segura: `conectar.py`
* Abre `agencia.db`.
* Ejecuta `PRAGMA foreign_keys = ON` para que SQLite vigile que ningún detalle quede huérfano sin su reserva padre.

### 4.2 La Clase Base: `dao/dao.py`
```python
class DAO:
    def __init__(self, conexion):
        self.conexion = conexion
        self.cursor = conexion.cursor()
```
Todos los DAO heredan de aquí. Reciben la conexión y crean su cursor.

### 4.3 `dao/paquete_dao.py`: El Ciclo de Vida CRUD
* **Guardar (`insertar`):**
  * El DAO toma el objeto `paquete`.
  * Lee sus propiedades: `paquete.nombre`, `paquete.precio_base`.
  * Ejecuta: `INSERT INTO paquete (nombre, precio_base, tipo) VALUES (?, ?, ?)`
  * **¿De dónde sale el ID?** SQLite le inventa un número único autoincremental. El DAO lo rescata con `self.cursor.lastrowid` y se lo inyecta al objeto:
    ```python
    paquete.id_paquete = self.cursor.lastrowid
    ```
* **Recuperar (`buscar`):**
  * Lee la fila de SQLite: `(1, "Puerto Varas", 450000.0, "nacional")`.
  * **El DAO traduce:** No le entrega una tupla a `main.py`. El DAO lee la columna `tipo` y fabrica un objeto nuevo: `PaqueteNacional(1, "Puerto Varas", 450000.0, None)`.

### 4.4 `dao/reserva_dao.py`: Transacción Atómica Maestro-Detalle
Una reserva son dos tablas: `reserva` (cabecera) y `detalle_reserva` (hijos).
* **El camino en el código:**
  1. Inserta en `reserva`.
  2. Obtiene `reserva_id = self.cursor.lastrowid`.
  3. Recorre `for detalle in reserva.detalles:` e inserta cada ítem en `detalle_reserva` usando ese `reserva_id`.
  4. Hace `self.conexion.commit()` al final. Si algo falla entre medio, no se guarda nada (Atomicidad).

---

# PASO 5: LA CONEXIÓN AL MUNDO EXTERIOR (`servicios/mindicador.py`)

Para saber a cuánto está el dólar hoy, no podemos inventar un número.

### 5.1 Cómo Funciona `obtener_dolar()`
1. Usa la librería `requests` para llamar a `https://mindicador.cl/api/dolar`.
2. Le pusimos `timeout=5` para que si internet se cae o la API se congela, no espere más de 5 segundos.
3. Si responde código 200, lee el JSON y saca el valor actual (ej: `$945.50`).

### 5.2 La Evolución del Error (Feedback del Profesor y Fail-Secure)
* **Versión antigua:** Si fallaba la conexión, el código hacía `return 950.0`.
* **El problema descubierto:** Si el dólar real está a $980 y el sistema vende a $950, **la agencia pierde $30 pesos por cada dólar**.
* **Versión actual corregida:**
  * Eliminamos los $950 fijos.
  * Si la API falla, lanzamos: `raise APITipoCambioError("No se pudo conectar a la API del dólar...")`.
  * En `main.py`, si alguien quiere reservar un paquete internacional sin internet, la operación **se bloquea de inmediato**.
  * Si alguien reserva un paquete nacional, **se permite reservar** porque el nacional no usa dólares.

---

# PASO 6: EL CONTROLADOR FINAL (`main.py`)

`main.py` no tiene lógica de negocio ni sentencias SQL. Solo es el director de orquesta que atiende al usuario por consola:

```
Usuario elige opción en Menú
         │
         ▼
main.py pide datos con input()
         │
         ▼
Se instancia la clase del modelo (ej: Viajero("11111111-1", "Juan", "F12345678"))
         │  ↳ Si el dato está malo, el @setter lanza ValueError
         ▼
Se realizan validaciones de negocio (reserva.validar_confirmacion())
         │  ↳ Si falta anticipo o cupos, lanza AnticipoInsuficienteError o SinCuposError
         ▼
main.py le pasa el objeto al DAO (reserva_dao.insertar(reserva))
         │  ↳ El DAO arma el SQL con (?) y hace commit() en agencia.db
         ▼
main.py muestra mensaje de éxito al usuario
```

---

# RESUMEN DE MAPEO RÁPIDO: DE DÓNDE VIENE Y ADÓNDE VA

| Operación | Dónde nace el dato | Por dónde pasa | Dónde se valida | Dónde termina guardado |
|---|---|---|---|---|
| **Crear Paquete** | `main.py` (Opción 1) | Objeto `Paquete` hijo | Setter `precio_base > 0` | Tabla `paquete` vía `paquete_dao.insertar()` |
| **Pasaporte Viajero** | `main.py` (Opción 5 u 7) | Objeto `Viajero` | Setter `numero_pasaporte` (6-12 chars) | En memoria del objeto `Viajero` |
| **Anticipo 50%** | `main.py` (Opción 7) | Objeto `Reserva` | `reserva.validar_confirmacion()` | Columna `anticipo` en tabla `reserva` |
| **Cupos Proveedor** | `main.py` (Opción 7) | `Proveedor.tiene_cupos()` | `reserva.validar_confirmacion()` | Se descuenta en memoria y base de datos |
| **Valor Dólar** | API `mindicador.cl` | `servicios/mindicador.py` | `timeout=5` y `APITipoCambioError` | Se multiplica en `paquete.calcular_precio_final()` |
