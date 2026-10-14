# MANUAL MAESTRO DE ARQUITECTURA Y CÓDIGO PASO A PASO
## AGENCIA DE VIAJES RUTASUR - EVALUACIÓN SUMATIVA N°3 (POOS TI3V21)
**Docente:** Michael Arjel | **Sección:** 114-2A-F2  
**Estudiantes:** Cristopher Figueroa y Elías Reyes

Este documento contiene la **descomposición minuciosa clase por clase, función por función y línea por línea** de todo el repositorio, explicando qué recibe, qué retorna, cómo valida, qué excepciones lanza, qué relaciones existen y cómo se alinea con la materia vista en el aula e instrucciones con Inteligencia Artificial.

---

# ÍNDICE GENERAL
1. [Arquitectura Global del Sistema y Flujo de Información](#1-arquitectura-global)
2. [Capa de Persistencia e Infraestructura de Datos](#2-persistencia)
   * `conectar.py` y `agencia.db`
   * `dao/dao.py`
   * `dao/paquete_dao.py`
   * `dao/reserva_dao.py`
3. [Capa de Servicios Externos](#3-servicios-externos)
   * `servicios/mindicador.py`
4. [Jerarquía de Excepciones del Dominio](#4-excepciones)
   * `model/excepciones.py`
5. [Modelo de Clases del Dominio (`model/`)](#5-modelo-del-dominio)
   * `persona.py`, `trabajador.py`, `administrador.py`, `agente_viajes.py`
   * `cliente.py`, `viajero.py`
   * `proveedor.py`, `disponibilidad.py`
   * `tipo_item.py`, `detalle_reserva.py`
   * `paquete.py`, `paquete_nacional.py`, `paquete_internacional.py`, `paquete_crucero.py`
   * `reserva.py`
6. [Orquestación y Flujo de Usuario (`main.py`)](#6-orquestacion-main)
7. [Relación con la Materia Vista en Clases e Instrucciones con IA](#7-materia-e-ia)

---

<a name="1-arquitectura-global"></a>
# 1. ARQUITECTURA GLOBAL DEL SISTEMA

El software sigue el patrón arquitectónico en **3 capas desacopladas**:

```
                       +---------------------------------------+
                       |               main.py                 |
                       | (Controlador y Menú Interactivo en UI) |
                       +-------------------+-------------------+
                                           |
                   +-----------------------+-----------------------+
                   |                                               |
                   v                                               v
        +----------------------+                       +-----------------------+
        |       model/         |                       |        dao/           |
        |  Entidades Puras POO |<----------------------| Acceso a Base Datos   |
        | (Lógica de Negocio   | (DAO traduce tuplas   | (SQL Parametrizado,   |
        |  sin nada de SQL)    |  a objetos de modelo) |  Transacciones)       |
        +----------+-----------+                       +-----------+-----------+
                   ^                                               |
                   |                                               v
        +----------+-----------+                       +-----------------------+
        |     servicios/       |                       |      agencia.db       |
        |  (API Externa Dólar  |                       | (SQLite Relacional    |
        |   Requests, Timeout) |                       |  PRAGMA foreign_keys) |
        +----------------------+                       +-----------------------+
```

### Principios Fundamentales Aplicados:
1. **Separación de Responsabilidades (SoC):** Ninguna clase en `model/` ejecuta SQL ni sabe que existe SQLite. La persistencia es responsabilidad exclusiva de la capa `dao/`.
2. **Encapsulamiento Robusto:** Atributos de instancia privados/protegidos (`_nombre`, `_rut`, `_anticipo`, `_numero_pasaporte`) con `@property` y `@setter` que rechazan estados no válidos antes de que los datos corruptos lleguen al DAO.
3. **Polimorfismo Verdadero:** La variación en el cálculo de precios entre paquetes nacionales, internacionales y cruceros se resuelve mediante **herencia y métodos sobrescritos**, sin estructuras `if/elif` sobre el tipo de objeto en la lógica central.
4. **Principio de Fallo Seguro (*Fail-Secure*):** Si la API externa no responde, el sistema no asume supuestos que generen pérdidas financieras; cancela de forma controlada las operaciones dependientes de divisas.

---

<a name="2-persistencia"></a>
# 2. CAPA DE PERSISTENCIA E INFRAESTRUCTURA DE DATOS

---

### `conectar.py`
* **Propósito:** Módulo centralizado para crear y configurar la conexión hacia SQLite.
* **Función:** `crear_conexion() -> sqlite3.Connection`
  * **Líneas 4-6:**
    ```python
    conexion = sqlite3.connect("agencia.db")
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion
    ```
  * **¿Por qué `PRAGMA foreign_keys = ON`?** SQLite por compatibilidad histórica desactiva las restricciones de clave foránea por defecto. Al activar este pragma en cada conexión, la base de datos rechaza cualquier intento de insertar un detalle de reserva con un `reserva_id` que no exista en la tabla padre `reserva`.

---

### `dao/dao.py`
* **Propósito:** Superclase base para todos los Data Access Objects.
* **Clase:** `DAO`
  * **Constructor `__init__(self, conexion)`:**
    * Recibe: Objeto de conexión activo `sqlite3.Connection`.
    * Atributos inicializados:
      * `self.conexion`: Referencia a la conexión para gestionar transacciones (`commit()` / `rollback()`).
      * `self.cursor`: `conexion.cursor()` utilizado para ejecutar sentencias SQL.

---

### `dao/paquete_dao.py`
* **Propósito:** Gestionar el ciclo de vida CRUD completo de la entidad `Paquete` en la tabla `paquete`.
* **Herencia:** `class PaqueteDAO(DAO)`

#### Métodos detallados:

1. **`crear_tabla(self) -> None`**
   * Ejecuta: `CREATE TABLE IF NOT EXISTS paquete (...)`
   * Columnas:
     * `id`: `INTEGER PRIMARY KEY AUTOINCREMENT`.
     * `nombre`: `TEXT NOT NULL`.
     * `precio_base`: `REAL NOT NULL`.
     * `tipo`: `TEXT NOT NULL` (`'nacional'`, `'internacional'`, `'crucero'`).

2. **`insertar(self, paquete: Paquete, tipo: str) -> None`**
   * **Parámetros recibidos:** Objeto `paquete` del modelo y el string `tipo`.
   * **SQL:** `"INSERT INTO paquete (nombre, precio_base, tipo) VALUES (?, ?, ?)"`
   * **Valores pasados:** `(paquete.nombre, paquete.precio_base, tipo)` en tupla.
   * **Línea clave:** `paquete.id_paquete = self.cursor.lastrowid`. El ID generado por la base de datos se inyecta de vuelta en el objeto en memoria (cumpliendo con lo enseñado en la Sesión 10).
   * **Persistencia:** Ejecuta `self.conexion.commit()`.

3. **`buscar(self, id: int) -> Optional[Paquete]`**
   * **Parámetros recibidos:** Entero `id`.
   * **SQL:** `"SELECT id, nombre, precio_base, tipo FROM paquete WHERE id = ?"`
   * **Retorno:** Si la fila existe, reconstruye la instancia polimórfica adecuada:
     * Si `tipo == 'nacional'` $\rightarrow$ Instancia `PaqueteNacional(fila[0], fila[1], fila[2], None)`.
     * Si `tipo == 'internacional'` $\rightarrow$ Instancia `PaqueteInternacional(fila[0], fila[1], fila[2], None)`.
     * En otro caso $\rightarrow$ Instancia `PaqueteCrucero(fila[0], fila[1], fila[2], None)`.
     * Si no existe, retorna `None`.
   * **Regla pedagógica:** El DAO entrega objetos al controlador, jamás tuplas crudas de base de datos.

4. **`listar(self) -> List[Tuple[Paquete, str]]`**
   * **SQL:** `"SELECT id, nombre, precio_base, tipo FROM paquete"`
   * **Retorno:** Lista de tuplas con el objeto instanciado y su tipo como texto.

5. **`actualizar(self, paquete: Paquete, tipo: str) -> None`**
   * **SQL:** `"UPDATE paquete SET nombre = ?, precio_base = ?, tipo = ? WHERE id = ?"`
   * **Parámetros:** `(paquete.nombre, paquete.precio_base, tipo, paquete.id_paquete)`. Ejecuta `commit()`.

6. **`eliminar(self, id: int) -> bool`**
   * **SQL:** `"DELETE FROM paquete WHERE id = ?"` con `(id,)`.
   * **Retorno:** `True` si `self.cursor.rowcount > 0` (es decir, si la fila existía y fue eliminada).

---

### `dao/reserva_dao.py`
* **Propósito:** Persistir transacciones maestras compuestas (`Reserva`) con sus líneas hijas (`DetalleReserva`).
* **Herencia:** `class ReservaDAO(DAO)`

#### Métodos detallados:

1. **`crear_tabla(self) -> None`**
   * Crea dos tablas relacionadas mediante Foreign Key:
     * `reserva`: `id` (PK), `fecha_viaje` (TEXT), `precio_paquete_clp` (REAL), `anticipo` (REAL), `estado` (TEXT).
     * `detalle_reserva`: `id` (PK), `reserva_id` (INTEGER NOT NULL), `tipo_item` (TEXT), `descripcion` (TEXT), `cantidad` (INTEGER), `precio_unitario` (REAL), `FOREIGN KEY(reserva_id) REFERENCES reserva(id)`.

2. **`insertar(self, reserva: Reserva) -> int`**
   * **Transacción Atómica (Todo o Nada):**
     * **Paso 1:** Inserta cabecera en `reserva` con `?` parametrizado.
     * **Paso 2:** Obtiene el identificador con `reserva_id = self.cursor.lastrowid`.
     * **Paso 3:** Itera `for detalle in reserva.detalles:` e inserta cada ítem en `detalle_reserva` referenciando el `reserva_id`.
     * **Paso 4:** Cierra la transacción con un único `self.conexion.commit()`.
   * **Retorno:** El ID de la reserva insertada.

3. **`buscar_detalles(self, id_reserva: int) -> Optional[dict]`**
   * Ejecuta dos SELECT parametrizados: uno a la cabecera y otro a `detalle_reserva WHERE reserva_id = ?`.
   * Retorna un diccionario con `{"reserva": res, "detalles": detalles}` o `None`.

---

<a name="3-servicios-externos"></a>
# 3. CAPA DE SERVICIOS EXTERNOS

---

### `servicios/mindicador.py`
* **Propósito:** Consumir el indicador económico oficial del dólar desde la API pública `https://mindicador.cl/api/dolar`.
* **Clase:** `MiIndicador`
* **Método:** `obtener_dolar(self) -> float`
  * **Comportamiento:**
    * Ejecuta: `response = requests.get("https://mindicador.cl/api/dolar", timeout=5)`
    * **¿Por qué `timeout=5`?** Evita que la aplicación quede bloqueada indefinidamente si el servidor de la API está saturado o la red se congela.
    * Si `response.status_code == 200`: Deserializa el JSON y extrae el valor flotante más reciente: `data['serie'][0]['valor']`.
    * **Manejo de Errores y Política Fail-Secure:**
      * Si ocurre `requests.exceptions.RequestException` (sin internet, timeout, DNS caído): lanza `raise APITipoCambioError("No se pudo conectar a la API del dólar (sin internet o servicio caído).")`.
      * Si ocurre un error en el formato (`KeyError`, `IndexError`): lanza `APITipoCambioError`.
    * **Decisión de seguridad:** No inyecta valores ficticios como $950 para proteger al negocio de pérdidas por descalce cambiario.

---

<a name="4-excepciones"></a>
# 4. JERARQUÍA DE EXCEPCIONES DEL DOMINIO

---

### `model/excepciones.py`
Define excepciones personalizadas que heredan jerárquicamente de la clase base de la aplicación:

```
                      Exception (Estándar de Python)
                                    ^
                                    |
                               AgenciaError
                                    ^
       +----------------------------+----------------------------+
       |                            |                            |
AnticipoInsuficienteError     SinCuposError              APITipoCambioError
 (Regla: Anticipo < 50%)    (Regla: Cupos = 0)        (API caída / Sin red)
       |                            |                            |
ValidacionError             RecursoNoEncontradoError     AutenticacionError
```

* **`AgenciaError(Exception)`:** Raíz común para identificar cualquier excepción originada por las reglas de la agencia.
* **`AnticipoInsuficienteError`:** Se lanza cuando el pago abonado no alcanza el 50% mínimo del monto total de la reserva.
* **`SinCuposError`:** Se lanza cuando un proveedor no posee disponibilidad en la fecha solicitada para el viaje.
* **`APITipoCambioError`:** Se lanza ante la imposibilidad de verificar la tasa de cambio oficial en tiempo real.
* **`ValidacionError`:** Se lanza cuando faltan datos obligatorios o cuando un paquete internacional carece de un viajero con pasaporte válido.

---

<a name="5-modelo-del-dominio"></a>
# 5. MODELO DE CLASES DEL DOMINIO (`model/`)

---

### `model/persona.py`
* **Clase:** `Persona(ABC)` (Clase abstracta base para seres humanos en el sistema).
* **Constructor:** `__init__(self, nombre: str, rut: str)`
* **Atributos protegidos:** `_nombre`, `_rut`.
* **Propiedades y Validaciones:**
  * `@property nombre` / `@nombre.setter`:
    * Quita espacios en blanco con `.strip()`.
    * Exige mínimo 2 caracteres: `len(valor) < 2` $\rightarrow$ `raise ValueError`.
    * Solo letras y espacios: `not valor.replace(" ", "").isalpha()` $\rightarrow$ `raise ValueError`.
  * `@property rut` / `@rut.setter`:
    * No puede ser vacío.
    * Debe contener guión `-` y tener al menos 8 caracteres (ej. `"11111111-1"`): `raise ValueError`.

---

### `model/trabajador.py`
* **Clase:** `Trabajador(Persona, ABC)` (Subclase abstracta de `Persona`).
* **Constructor:** Llama a `super().__init__(nombre, rut)`.
* **Propósito:** Representa a los empleados de la agencia, sirviendo de puente para el principio de menor privilegio entre agentes y administradores.

---

### `model/administrador.py`
* **Clase:** `Administrador(Trabajador)`
* **Métodos:**
  * `puede_atender_clientes(self) -> bool`: Retorna `False`. (Cumple la regla del enunciado: *"el administrador gestiona proveedores y pagos, pero no atiende clientes directamente"*).
  * `gestionar_proveedor(self, proveedor)`, `gestionar_pagos(self, reserva)`.

---

### `model/agente_viajes.py`
* **Clase:** `AgenteViajes(Trabajador)`
* **Métodos:**
  * `puede_atender_clientes(self) -> bool`: Retorna `True`. (El agente sí interactúa y atiende al cliente).
  * `atender_cliente(self, cliente)`, `vender_paquete(self, paquete)`.

---

### `model/cliente.py`
* **Clase:** `Cliente(Persona)`
* **Propósito:** Representa a la persona jurídica o natural que **contrata y paga** la reserva. No tiene pasaporte porque no necesariamente viaja él mismo.

---

### `model/viajero.py`
* **Clase:** `Viajero(Persona)`
* **Propósito:** Representa al pasajero que **físicamente realiza el viaje**.
* **Constructor:** `__init__(self, rut: str, nombre: str, numero_pasaporte: str)`
  * Ejecuta `super().__init__(nombre, rut)`.
  * Asigna `self.numero_pasaporte = numero_pasaporte` activando el setter de validación.
* **Propiedades y Validaciones:**
  * `@property numero_pasaporte` / `@numero_pasaporte.setter`:
    * Si está vacío o None $\rightarrow$ `raise ValueError("El pasaporte no puede estar vacío.")`.
    * Lo sanitiza a mayúsculas: `valor.strip().upper()`.
    * Exige alfanumérico entre 6 y 12 caracteres: `raise ValueError("Pasaporte inválido. Debe tener entre 6 y 12 caracteres.")`.

---

### `model/proveedor.py`
* **Clase:** `Proveedor`
* **Atributos:**
  * `self.id_proveedor`: int
  * `self.nombre`: str
  * `self.disponibilidades`: List[Disponibilidad] (Relación de agregación: 1 proveedor tiene $0..*$ disponibilidades).
* **Métodos:**
  * `agregar_disponibilidad(self, disponibilidad: Disponibilidad)`: Agrega una fecha y cupo a la lista.
  * `tiene_cupos(self, fecha: str) -> bool`: Recorre las disponibilidades y si coincide la fecha, retorna `disp.tiene_cupos()`. Si no existe la fecha, retorna `False`.
  * `descontar_cupo(self, fecha: str) -> bool`: Descuenta 1 cupo para la fecha o lanza `ValueError`.

---

### `model/disponibilidad.py`
* **Clase:** `Disponibilidad`
* **Constructor:** `__init__(self, fecha: str, cupos_disponibles: int)`
* **Propiedades y Validaciones:**
  * `@property cupos_disponibles` / `@cupos_disponibles.setter`:
    * Convierte a int. Si es menor a cero: `raise ValueError("Los cupos no pueden ser negativos.")`.
* **Métodos:**
  * `tiene_cupos(self) -> bool`: Retorna `self.cupos_disponibles > 0`.
  * `descontar_cupo(self) -> None`: Si no tiene cupos lanza `ValueError`; de lo contrario resta 1 a los cupos.

---

### `model/tipo_item.py`
* **Clase:** `TipoItem`
* **Propósito:** Actúa como catálogo maestro compartido para clasificar los componentes de una reserva (ej. Vuelo, Hotel, Seguro de Viaje, Excursión).
* **Atributos:** `id_tipo: int`, `nombre_categoria: str` (valida no vacío en su `@setter`).

---

### `model/detalle_reserva.py`
* **Clase:** `DetalleReserva`
* **Constructor:** `__init__(self, tipo_item: TipoItem, descripcion: str, cantidad: int, precio_unitario: float)`
* **Propiedades y Validaciones:**
  * `@tipo_item.setter`: Verifica que sea instancia válida de `TipoItem`: `raise ValueError`.
  * `@cantidad.setter`: Valida entero $> 0$: `raise ValueError`.
  * `@precio_unitario.setter`: Valida float $\ge 0$: `raise ValueError`.
* **Método:** `subtotal(self) -> float`: Retorna `self.cantidad * self.precio_unitario`.

---

### `model/paquete.py`
* **Clase:** `Paquete(ABC)` (Clase abstracta base de productos turísticos).
* **Constructor:** `__init__(self, id_paquete: Optional[int], nombre: str, precio_base: float, proveedor_id: Optional[int])`
* **Validación:** `@precio_base.setter` exige `valor > 0`: `raise ValueError`.
* **Método Abstracto Polimórfico:**
  ```python
  @abstractmethod
  def calcular_precio_final(self, tipo_cambio: float = None) -> float:
      pass
  ```

---

### `model/paquete_nacional.py`
* **Clase:** `PaqueteNacional(Paquete)`
* **Sobrescritura:**
  ```python
  def calcular_precio_final(self, tipo_cambio: float = None) -> float:
      return round(self.precio_base)
  ```
  * **Regla de negocio:** Se cotiza en moneda local. No utiliza el tipo de cambio.

---

### `model/paquete_internacional.py`
* **Clase:** `PaqueteInternacional(Paquete)`
* **Sobrescritura:**
  ```python
  def calcular_precio_final(self, tipo_cambio: float = None) -> float:
      if tipo_cambio is None: raise ValueError("El tipo de cambio es obligatorio para paquetes internacionales y no se puede asumir un valor por defecto.")
      if tipo_cambio <= 0: raise ValueError("El tipo de cambio debe ser mayor que cero.")
      return round(self.precio_base * tipo_cambio)
  ```
  * **Regla de negocio:** El precio base está en dólares (USD). Se multiplica directamente por el valor oficial del dólar del día. No asume ningún valor por defecto si no hay conexión oficial.

---

### `model/paquete_crucero.py`
* **Clase:** `PaqueteCrucero(Paquete)`
* **Sobrescritura:**
  ```python
  def calcular_precio_final(self, tipo_cambio: float = None) -> float:
      if tipo_cambio is None: raise ValueError("El tipo de cambio es obligatorio para paquetes de crucero y no se puede asumir un valor por defecto.")
      if tipo_cambio <= 0: raise ValueError("El tipo de cambio debe ser mayor que cero.")
      return round(self.precio_base * tipo_cambio * 1.12)
  ```
  * **Regla de negocio:** Posee su propia fórmula de liquidación: convierte la tarifa en dólares y aplica un recargo marítimo y de tasas portuarias del 12% (`* 1.12`). Exige el tipo de cambio oficial del día.

---

### `model/reserva.py`
* **Clases:**
  * `EstadoReserva(str, Enum)`: `PENDIENTE`, `CONFIRMADA`, `PAGADA`, `CANCELADA`.
  * `Reserva`: Entidad transaccional central.
* **Constructor:**
  ```python
  __init__(self, cliente, agente, paquete, proveedor, fecha_viaje, precio_paquete_clp, anticipo=0.0, estado=EstadoReserva.PENDIENTE, viajero=None, tipo_cambio=None)
  ```
* **Atributos clave:**
  * `self.detalles = []`: Lista de objetos `DetalleReserva` (Composición 1 a muchos).
  * `self.anticipo`: Protegido con setter que prohíbe valores negativos.
* **Métodos del ciclo de vida:**
  1. `agregar_detalle(self, detalle: DetalleReserva)`: Incorpora una línea de detalle a la reserva.
  2. `total(self) -> float`: Retorna `self.precio_paquete_clp + sum(d.subtotal() for d in self.detalles)`.
  3. `saldo_pendiente(self) -> float`: Retorna `max(0.0, self.total() - self.anticipo)`.
  4. `pagar_saldo(self, monto: float)`: Abona al anticipo y actualiza el estado a `PAGADA` si se cancela la totalidad.
  5. **`validar_confirmacion(self) -> bool` (Motor de Reglas de Negocio):**
     * **Regla 1 (Validación de Pasaporte):** Si el paquete es internacional o crucero, exige que `self.viajero` no sea None y posea `numero_pasaporte` válido. Si falta, lanza `raise ValidacionError(...)`.
     * **Regla 2 (Cupos del Proveedor):** Ejecuta `if not self.proveedor.tiene_cupos(self.fecha_viaje):` y si no hay disponibilidad lanza `raise SinCuposError(...)`.
     * **Regla 3 (Anticipo Mínimo del 50%):** Calcula `minimo_anticipo = self.total() * 0.50`. Si `self.anticipo < minimo_anticipo`, lanza `raise AnticipoInsuficienteError(...)`.
     * Si supera todas las reglas: Transiciona a `self.estado = EstadoReserva.CONFIRMADA` y retorna `True`.

---

<a name="6-orquestacion-main"></a>
# 6. ORQUESTACIÓN Y FLUJO DE USUARIO (`main.py`)

`main.py` actúa como la capa controladora del sistema. Presenta un menú interactivo con 9 opciones:

1. **Opción 1 (Crear Paquete):** Solicita nombre, precio base y tipo. Si es internacional o crucero, consulta a `MiIndicador` para almacenar el precio base convertido en USD. Si la API falla, captura `APITipoCambioError` y cancela el ingreso seguro. Inserta mediante `paquete_dao.insertar()`.
2. **Opción 2 (Listar Paquetes):** Invoca `paquete_dao.listar()` y formatea en columnas con espaciado tabulado (`ID`, `NOMBRE`, `PRECIO BASE`, `TIPO`).
3. **Opción 3 (Modificar Paquete):** Busca por ID, muestra el valor actual y actualiza el precio mediante `paquete_dao.actualizar()`.
4. **Opción 4 (Eliminar Paquete):** Solicita ID y llama a `paquete_dao.eliminar(id_buscar)`.
5. **Opción 5 (Validar Pasaporte Viajero):** Prueba interactiva del setter de `Viajero` para demostrar ante el docente el rechazo de cadenas vacías o formatos no válidos.
6. **Opción 6 (Calcular Precio con Dólar):**
   * Si el paquete es `PaqueteNacional`, calcula directamente en pesos sin consumir internet.
   * Si es internacional o crucero, consulta `MiIndicador.obtener_dolar()`. Si no hay internet, atrapa `APITipoCambioError`, emite advertencia de fallo seguro y no detiene el programa.
7. **Opción 7 (Registrar Reserva):** Flujo compuesto. Instancia `Cliente`, `AgenteViajes`, `Proveedor` y `Viajero`. Crea 4 ítems de detalle (Vuelo, Hotel, Seguro, Excursión). Valida reglas con `reserva.validar_confirmacion()` y persiste atómicamente con `reserva_dao.insertar(reserva)`.
8. **Opción 8 (Ver detalle de reserva):** Consulta por clave foránea con `reserva_dao.buscar_detalles(id_reserva)` y desglosa cada ítem secundario guardado.
9. **Opción 9 (Salir):** Cierra limpiamente la conexión a SQLite con `conexion.close()`.

---

<a name="7-materia-e-ia"></a>
# 7. RELACIÓN CON LA MATERIA VISTA EN CLASES E INSTRUCCIONES CON IA

El código replica con total fidelidad los patrones abordados por el profesor Michael Arjel en las unidades 2, 3 y 4:

| Sesión / Unidad | Tema de la Clase | Implementación Concreta en RutaSur |
|---|---|---|
| **Sesión 6 y 7** | Del Diagrama al Código y Herencia | Clases en `model/`, herencia con `super().__init__()` y decoradores `@property` / `@setter` en atributos protegidos. |
| **Sesión 8** | Abc de Excepciones | Excepciones personalizadas derivadas de `AgenciaError` (`SinCuposError`, `AnticipoInsuficienteError`) en lugar de usar `print` o retornar booleanos. |
| **Sesión 9** | Conexión a Base de Datos | `conectar.py` con `PRAGMA foreign_keys = ON` y creación de tablas al inicio de la aplicación. |
| **Sesión 10** | CRUD Seguro con DAO | Uso estricto de parámetros posicionales `?` contra Inyección SQL, inyección de `cursor.lastrowid` al objeto en memoria y transacciones atómicas. |
| **Sesión 15** | Consumo de API Externa | `requests.get()` con `timeout=5`, deserialización de JSON e implementación de contingencia y política Fail-Secure. |

### Instrucciones y Prompts Usados con IA (Replicando la Sesión 10):
En la lámina de la Sesión 10, el profesor enseña a dar instrucciones precisas a la IA para encapsular el modelo. En este proyecto aplicamos exactamente ese enfoque:
* **Prompt 1 (Arquitectura de Dominio):** Se le solicitó a la IA integrar al `Viajero` dentro de la `Reserva` en lugar de dejarlo como un dato suelto, permitiendo que la verificación de pasaporte se ejecute de forma ordenada en `validar_confirmacion()`.
* **Prompt 2 (Refinamiento de Ciberseguridad):** Tras la retroalimentación del docente, se rechazó la sugerencia inicial de inyectar $950 fijos y se instruyó a la IA implementar la excepción `APITipoCambioError` para cerrar las operaciones en divisa ante la caída de la API, garantizando el principio de Fallo Seguro.
