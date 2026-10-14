# Auditoría Integral y Memoria Técnica Permanente: Agencia de Viajes RutaSur
**Asignatura:** Programación Orientada a Objetos Seguro (POOS) - TI3V21 (Primavera 2026)  
**Sección:** 114-2A-F2 / 114-2B-F1 | **Sede:** Puente Alto  
**Docente:** Michael Arjel  
**Equipo:** Cristopher Figueroa y Elías Reyes  
**Proyecto:** Agencia de Viajes RutaSur (Evaluación Sumativa N°2)  
**Rama activa:** `master` (commit `52da51d`)

---

## 1. Inventario y Análisis Línea por Línea de Todos los Archivos

### 1.1 Archivos Raíz

* **`conectar.py` (7 líneas):**
  * `crear_conexion()` establece enlace a `agencia.db`.
  * `PRAGMA foreign_keys = ON`: Clave para forzar la integridad referencial de `detalle_reserva` hacia `reserva`.
* **`requirements.txt` (1 línea):**
  * Contiene `requests`.
* **`.gitignore`:**
  * Ignora `__pycache__`, `agencia.db`, y la carpeta `Materia Pasada en el Aula/`.
* **`README.md` (23 líneas):**
  * Negocio, instrucciones de ejecución.
  * Decisiones de seguridad: consultas parametrizadas `?`, validación y encapsulamiento en setters, resiliencia y timeout en consumo de API.
  * Uso de IA documentado con justificación técnica (instanciación de `Viajero` en `Reserva`).

---

### 1.2 Capa de Servicios (`servicios/`)

* **`servicios/mindicador.py` (14 líneas):**
  * Clase `MiIndicador`.
  * Método `obtener_dolar()`: Realiza `requests.get("https://mindicador.cl/api/dolar", timeout=5)`.
  * En caso de timeout, error HTTP o falta de conexión, captura la excepción y retorna `$950.0` como valor fijo de contingencia para continuidad operativa (requisito 3.1.1/3.1.3 y prueba P17).

---

### 1.3 Capa DAO (`dao/`)

* **`dao/dao.py` (5 líneas):**
  * Clase base `DAO(conexion)`. Instancia `self.cursor = conexion.cursor()`.
* **`dao/paquete_dao.py` (61 líneas):**
  * `PaqueteDAO(DAO)`.
  * `crear_tabla()`: Crea tabla `paquete (id, nombre, precio_base, tipo)`.
  * `insertar(paquete, tipo)`: Parametrizado con `?`, hace `commit()` y asigna `paquete.id_paquete = cursor.lastrowid`.
  * `buscar(id)`: Reconstituye la instancia correcta (`PaqueteNacional`, `PaqueteInternacional`, `PaqueteCrucero`) según la columna `tipo`.
  * `listar()`: Retorna lista de tuplas `(objeto_paquete, tipo)`.
  * `actualizar(paquete, tipo)`: Modifica nombre, precio y tipo según `id`.
  * `eliminar(id)`: Borra por `id` y retorna booleano según `cursor.rowcount > 0`.
* **`dao/reserva_dao.py` (62 líneas):**
  * `ReservaDAO(DAO)`.
  * `crear_tabla()`: Crea tabla principal `reserva` y tabla hija `detalle_reserva` (con FK a `reserva(id)`).
  * `insertar(reserva)`: Inserta cabecera en `reserva`, obtiene `reserva_id`, itera los ítems de `reserva.detalles` e inserta cada uno en `detalle_reserva`, cerrando con un único `commit()` transaccional.
  * `buscar_detalles(id_reserva)`: Extrae reserva y sus líneas de detalle asociadas.

---

### 1.4 Capa del Modelo (`model/`)

* **`model/excepciones.py` (27 líneas):**
  * `AgenciaError(Exception)`
  * `AnticipoInsuficienteError(AgenciaError)` (Regla del negocio: anticipo < 50%).
  * `SinCuposError(AgenciaError)` (Regla del negocio: sin cupos de proveedor).
  * `ValidacionError(AgenciaError)` (Validación de pasaporte y datos obligatorios).
  * `RecursoNoEncontradoError`, `APITipoCambioError`, `AutenticacionError`.
* **`model/persona.py` (33 líneas):**
  * Clase abstracta base `Persona(ABC)`.
  * Valida nombre ($\ge 2$ letras, solo texto) y RUT (no vacío, con guión `-`, longitud $\ge 8$) en sus setters.
* **`model/trabajador.py` (7 líneas):**
  * Subclase abstracta de `Persona`. Hereda con `super().__init__(nombre, rut)`.
* **`model/administrador.py` (15 líneas):**
  * Hereda de `Trabajador`. `puede_atender_clientes()` devuelve `False`.
* **`model/agente_viajes.py` (15 líneas):**
  * Hereda de `Trabajador`. `puede_atender_clientes()` devuelve `True`. Métodos de venta y atención.
* **`model/cliente.py` (7 líneas):**
  * Hereda de `Persona`. Representa a la persona que compra/paga la reserva.
* **`model/viajero.py` (21 líneas):**
  * Hereda de `Persona`. Representa a quien viaja.
  * Constructor: `__init__(self, rut, nombre, numero_pasaporte)`.
  * Setter `numero_pasaporte`: No vacío, alfanumérico entre 6 y 12 caracteres.
* **`model/proveedor.py` (23 líneas):**
  * Atributos: `id_proveedor`, `nombre`, `disponibilidades`.
  * Métodos: `agregar_disponibilidad()`, `tiene_cupos(fecha)`, `descontar_cupo(fecha)`.
* **`model/disponibilidad.py` (24 líneas):**
  * Atributos: `fecha`, `cupos_disponibles` ($\ge 0$).
  * Métodos: `tiene_cupos()`, `descontar_cupo()`.
* **`model/tipo_item.py` (16 líneas):**
  * Catálogo de servicios (`id_tipo`, `nombre_categoria`).
* **`model/paquete.py` (25 líneas):**
  * Clase abstracta `Paquete(ABC)`.
  * Atributos: `id_paquete`, `nombre`, `precio_base` (> 0), `proveedor_id`.
  * Método abstracto: `calcular_precio_final(self, tipo_cambio=None)`.
* **`model/paquete_nacional.py` (10 líneas):**
  * `calcular_precio_final()`: Retorna `round(self.precio_base)` (sin tipo de cambio).
* **`model/paquete_internacional.py` (11 líneas):**
  * `calcular_precio_final(tipo_cambio)`: Retorna `round(self.precio_base * tipo_cambio)`.
* **`model/paquete_crucero.py` (11 líneas):**
  * `calcular_precio_final(tipo_cambio)`: Retorna `round(self.precio_base * tipo_cambio * 1.12)` (recargo de crucero).
* **`model/detalle_reserva.py` (44 líneas):**
  * Composición de reserva: `tipo_item`, `descripcion`, `cantidad` (> 0), `precio_unitario` ($\ge 0$).
  * Método: `subtotal()`.
* **`model/reserva.py` (80 líneas):**
  * `EstadoReserva(str, Enum)`: `PENDIENTE`, `CONFIRMADA`, `PAGADA`, `CANCELADA`.
  * Atributos: `cliente`, `agente`, `paquete`, `proveedor`, `fecha_viaje`, `precio_paquete_clp`, `anticipo`, `detalles`, `viajero`.
  * Métodos: `agregar_detalle()`, `total()`, `saldo_pendiente()`, `pagar_saldo()`, `validar_confirmacion()`.
  * En `validar_confirmacion()`:
    1. Si es internacional o crucero, exige `viajero` con pasaporte (`ValidacionError`).
    2. Exige cupos en proveedor para la fecha (`SinCuposError`).
    3. Exige anticipo $\ge 50\%$ del total (`AnticipoInsuficienteError`).
    4. Cambia estado a `CONFIRMADA` y retorna `True`.

---

### 1.5 Interfaz Principal (`main.py` - 296 líneas)

* 9 opciones de menú:
  1. Crear Paquete (convierte a USD en memoria si es internacional/crucero).
  2. Listar Paquetes.
  3. Modificar Paquete.
  4. Eliminar Paquete.
  5. Validar Pasaporte Viajero (prueba unitaria interactiva).
  6. Calcular Precio con Dólar (obtiene dólar y ejecuta polimorfismo).
  7. Registrar Reserva (crea reserva, agrega 4 detalles, valida reglas y persiste cabecera + líneas).
  8. Ver detalle de reserva (consulta con FK por ID).
  9. Salir.

---

## 2. Base de Datos (`agencia.db`)

* `paquete`: 3 registros existentes:
  * ID 2: "America", $200.000 (nacional)
  * ID 3: "Europa", $500.000 (internacional)
  * ID 4: "Caribe", $800.000 (crucero)
* `reserva`: Esquema listo para transacciones.
* `detalle_reserva`: Esquema listo con FK a `reserva(id)`.

---

## 3. Matriz de Pruebas (P01 - P19) del Excel

* **P01:** Ejecuta `python main.py` -> Inicia menú correctamente.
* **P02:** Crear paquete nacional "Puerto Varas 4 días", $450.000 -> Confirma guardado.
* **P03:** Listar -> Aparece en pantalla.
* **P04:** Modificar precio -> Se refleja el cambio.
* **P05:** Persistencia -> Al reiniciar, los datos se mantienen en SQLite.
* **P06:** Eliminar paquete -> Se elimina de la base de datos.
* **P07:** Pasaporte válido `F12345678` -> Aceptado.
* **P08:** Pasaporte vacío -> Rechazado con mensaje sin caída del script.
* **P09:** Paquete nacional -> En pesos, sin tipo de cambio.
* **P10:** Paquete internacional -> En USD convertido con dólar del día.
* **P11:** Crucero -> Fórmula propia con recargo del 12%.
* **P12:** Registrar reserva con 4 ítems -> Un solo registro con líneas de detalle.
* **P13:** Ver detalle -> Muestra cabecera y todas las líneas.
* **P14:** Anticipo < 50% -> Se bloquea confirmación con `AnticipoInsuficienteError`.
* **P15:** Proveedor sin cupos -> Se bloquea reserva con `SinCuposError`.
* **P16:** Dólar en línea -> Conexión con `mindicador.cl/api/dolar`.
* **P17:** Sin internet -> Mensaje de aviso y uso de valor de contingencia ($950.0).
* **P18:** Opción inválida (`99`) -> Mensaje de error y vuelve al menú.
* **P19:** Letras por números (`abc`) -> Controlado con mensaje sin error fatal.

---

## 4. Rúbrica y Criterios Docentes (Michael Arjel - 42 Puntos)

* **2.1.2 Modelo OO (7 pts):** Herencia (`super()`), polimorfismo, `@property` y validación en setters.
* **2.1.3 Persistencia DAO (7 pts):** CRUD completo, transacciones con líneas de detalle, consultas parametrizadas `?`.
* **2.1.4 Excepciones propias (7 pts):** `AnticipoInsuficienteError` y `SinCuposError` lanzadas y capturadas específicamente.
* **3.1.2 Validación de entradas (7 pts):** Sanitización y validación de tipos, rangos y formatos.
* **3.1.1 / 3.1.3 Consumo de API (7 pts):** `requests`, `timeout=5`, tolerancia a fallas.
* **3.1.4 Justificación de IA y README (7 pts):** README completo con justificación técnica.
