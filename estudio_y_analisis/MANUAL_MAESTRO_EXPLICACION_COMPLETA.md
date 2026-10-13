# MANUAL MAESTRO: EXPLICACIÓN COMPLETA DEL CÓDIGO
## Sistema de Gestión y Reservas - Agencia RutaSur
### Documento Único de Estudio Integral para la Defensa Oral (Evaluación Sumativa N°3)

---

## ÍNDICE DE CONTENIDOS
1. **Arquitectura del Sistema en 3 Capas**
2. **Fundamentos POO: Variables, Constructores y Propiedades (Sin Confusiones)**
3. **Métodos Públicos vs Privados (UML y Python)**
4. **Los 5 Requisitos de la Ficha Explicados a Fondo**
   - *Requisito 1: Subtipos y Polimorfismo (Cálculo exacto de fórmulas)*
   - *Requisito 2: Dato con Validación (Viajero y Pasaporte)*
   - *Requisito 3: Dos Reglas de Negocio con Excepciones Propias*
   - *Requisito 4: Integrador Externo (API del Dólar y Política Segura)*
   - *Requisito 5: Transacción con Líneas de Detalle (La verdad sobre DetalleReserva y TipoItem)*
5. **Cadena de Propagación de Errores (De `raise` en el Modelo a `except` en `main.py`)**
6. **Seguridad y Persistencia (DAO, Inyección SQL y Claves Foráneas)**
7. **Diccionario Técnico: Cómo Leer el Código en Voz Alta**

---

# 1. ARQUITECTURA DEL SISTEMA EN 3 CAPAS

El proyecto está diseñado bajo el principio de **separación de responsabilidades** (SoC), estructurado en 3 capas desacopladas:

```
[ Capa de Presentación e Interacción ] -> main.py (Menú de consola)
                  ↓                                  ↓
[ Capa de Servicios Externos ]          [ Capa de Acceso a Datos ]
servicios/mindicador.py (API Dólar)      dao/paquete_dao.py, reserva_dao.py
                  ↓                                  ↓
      [ Capa de Negocio / Dominio ] -> model/ (Clases puras POO)
```

1. **Capa `model/` (Lógica de Dominio):**  
   Contiene las entidades del negocio (`Paquete`, `Persona`, `Reserva`, `DetalleReserva`, etc.). **Regla de oro:** No contiene ni una sola línea de SQL ni llamadas a APIs. Es POO pura.
2. **Capa `dao/` (Acceso a Datos):**  
   Implementa el patrón *Data Access Object*. Centraliza toda la interacción con la base de datos SQLite (`agencia.db`).
3. **Capa `servicios/` (Servicios Externos):**  
   Aísla la comunicación HTTP con la API de `mindicador.cl`.
4. **Archivo `conectar.py`:**  
   Gestiona la conexión SQLite y activa la integridad referencial con `PRAGMA foreign_keys = ON;`.

---

# 2. FUNDAMENTOS POO: CONSTRUCTORES, ATRIBUTOS Y PROPERTIES

### La gran duda resuelta: ¿Por qué hay tres veces `nombre` en una clase?
En una clase típica como `model/persona.py`, verás esto:
```python
class Persona:
    def __init__(self, nombre: str, rut: str):
        self.nombre = nombre  # ¿Por qué tres veces "nombre"?
```

Para entenderlo paso a paso:
1. **`nombre` (en el paréntesis):** Es el **parámetro**. Es la variable temporal que entra desde afuera cuando alguien crea el objeto: `Persona("Juan", "11111111-1")`.
2. **`self._nombre` (con guión bajo):** Es el **atributo privado/protegido real** que se guarda en la memoria del objeto.
3. **`self.nombre` (sin guión bajo a la izquierda del `=`):** Es la **Property (Setter)**. 

Al escribir `self.nombre = nombre`, Python **NO** guarda el dato directamente en la memoria; lo redirige automáticamente hacia el método `@nombre.setter`. 

### ¿Cómo funciona el trío `@property` y `@setter`?
```python
    @property
    def nombre(self):
        """GETTER: Se ejecuta cuando alguien lee el dato: print(p.nombre)"""
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        """SETTER: Se ejecuta cuando alguien asigna: p.nombre = 'Juan'"""
        valor = str(valor).strip()
        if len(valor) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres.")
        self._nombre = valor  # ¡Aquí recién se guarda en la variable real!
```
* **¿Qué entra?** Un valor string por el setter.
* **¿Qué sale?** El valor limpio a través del getter.
* **¿Qué se protege?** Que nadie pueda ponerle a una persona un nombre vacío o un número inválido.

---

# 3. MÉTODOS PÚBLICOS VS PRIVADOS (UML Y PYTHON)

### ¿Cómo se representan en el Diagrama UML?
* **Signo `+`:** Es **PÚBLICO** (`+ validarPasaporte(): Boolean`). Significa que cualquier otra clase puede usarlo.
* **Signo `-`:** Es **PRIVADO** (`- calcular_descuento_interno()`). Solo esa misma clase puede usarlo dentro de sus propias funciones.

### ¿Cómo se programan en Python?
* **Público (por defecto):** Cualquier método normal es público:
  ```python
  def validar_pasaporte(self) -> bool:
      return bool(self._numero_pasaporte and len(self._numero_pasaporte) >= 6)
  ```
* **Privado:** Se le colocan **dos guiones bajos (`__`)** al inicio:
  ```python
  def __formatear_rut(self):
      # Solo ejecutable dentro de la propia clase
      pass
  ```

### ¿Por qué `validar_pasaporte()` TIENE QUE SER PÚBLICO?
Porque quien necesita validar el pasaporte es **otra clase diferente**: la clase `Reserva` en `model/reserva.py` (línea 68):
```python
# Dentro de Reserva.validar_confirmacion():
if not self.viajero.validar_pasaporte():
    raise ValidacionError("Un paquete internacional requiere un Viajero con pasaporte válido.")
```
Si `validar_pasaporte()` fuera privado dentro de `Viajero`, `Reserva` no tendría permiso para llamarlo y Python lanzaría un error `AttributeError`.

---

# 4. LOS 5 REQUISITOS DE LA FICHA EXPLICADOS A FONDO

---

### REQUISITO 1: Subtipos y Polimorfismo (Cálculo exacto de fórmulas)
En `model/paquete.py`, definimos la clase base abstracta:
```python
from abc import ABC, abstractmethod

class Paquete(ABC):
    def __init__(self, id_paquete, nombre, precio_base, proveedor_id):
        self.id_paquete = id_paquete
        self.nombre = nombre
        self.precio_base = precio_base
        self.proveedor_id = proveedor_id

    @abstractmethod
    def calcular_precio_final(self, tipo_cambio=950):
        pass  # Es abstracto: no calcula nada, obliga a las hijas a programarlo.
```

Sus tres subclases hijas sobrescriben el método implementando su fórmula comercial:

1. **`PaqueteNacional` (`model/paquete_nacional.py`):**
   * *Regla:* El precio se cobra directo en pesos chilenos (CLP). No depende del dólar ni de divisas.
   * *Código:*
     ```python
     def calcular_precio_final(self, tipo_cambio=950):
         return round(self.precio_base)
     ```
   * *Ejemplo:* Precio base $180.000 -> Devuelve `$180.000 CLP`.

2. **`PaqueteInternacional` (`model/paquete_internacional.py`):**
   * *Regla:* El precio base está fijado en dólares (USD). Se debe multiplicar por el tipo de cambio oficial del día.
   * *Código:*
     ```python
     def calcular_precio_final(self, tipo_cambio=950):
         if tipo_cambio <= 0:
             raise ValueError("El tipo de cambio debe ser mayor que cero.")
         return round(self.precio_base * tipo_cambio)
     ```
   * *Ejemplo:* Precio base $500 USD con dólar a $950 -> `500 * 950 = $475.000 CLP`.

3. **`PaqueteCrucero` (`model/paquete_crucero.py`):**
   * *Regla:* Mismo cálculo en dólares, pero con un recargo adicional del 12% (`* 1.12`) por concepto de tasas portuarias y servicios de abordo.
   * *Código:*
     ```python
     def calcular_precio_final(self, tipo_cambio=950):
         if tipo_cambio <= 0:
             raise ValueError("El tipo de cambio debe ser mayor que cero.")
         return round(self.precio_base * tipo_cambio * 1.12)
     ```
   * *Ejemplo:* Precio base $500 USD con dólar a $950 -> `500 * 950 * 1.12 = $532.000 CLP`.

---

### REQUISITO 2: Dato con Validación (Viajero y Pasaporte)
En `model/viajero.py`:
* **Hereda de:** `Persona` (`class Viajero(Persona)`).
* **Atributo encapsulado:** `numero_pasaporte`.
* **Reglas validadas en el `@setter`:**
  1. No puede ser nulo ni estar vacío (`strip() == ""`).
  2. Se sanitiza automáticamente convirtiéndolo a mayúsculas (`upper()`).
  3. Debe ser alfanumérico (`isalnum()`), sin caracteres especiales raros.
  4. Su longitud debe ser de mínimo 6 y máximo 12 caracteres.
  5. Si no cumple, lanza `raise ValueError("Pasaporte inválido...")`.
* **Método de consulta pública:** `validar_pasaporte() -> bool` (retorna `True` si cumple o `False` si no).

---

### REQUISITO 3: Dos Reglas de Negocio con Excepciones Propias
En `model/excepciones.py`, creamos una jerarquía limpia de errores:
```python
class AgenciaError(Exception):
    """Excepción base de la que heredan todas las reglas del sistema."""
    pass

class AnticipoInsuficienteError(AgenciaError):
    pass

class SinCuposError(AgenciaError):
    pass

class APITipoCambioError(AgenciaError):
    pass

class ValidacionError(AgenciaError):
    pass
```

Las dos reglas de negocio se ejecutan en `model/reserva.py` al confirmar una venta:
1. **Regla de Cupos del Proveedor (`SinCuposError`):**  
   Antes de confirmar, se verifica `proveedor.tiene_cupos(fecha)`. Si no hay cupos suficientes para los pasajeros, se lanza `raise SinCuposError("El proveedor no tiene cupos...")`.
2. **Regla del Anticipo del 50% (`AnticipoInsuficienteError`):**  
   El cliente debe abonar al menos la mitad del costo total de la reserva (`self.total() * 0.50`). Si ingresa menos, se lanza `raise AnticipoInsuficienteError("El anticipo debe ser al menos el 50% del total.")`.

---

### REQUISITO 4: Integrador Externo (API del Dólar y Política Segura)
En `servicios/mindicador.py`:
* Hace una petición HTTP `GET` a `https://mindicador.cl/api/dolar` con `timeout=5`.
* **Modificación de la Evaluación 3:**  
  * *Antes:* Si no había internet, usaba un valor fijo de $950.0.  
  * *Peligro detectado:* Si el dólar real estaba a $990, la agencia perdía $40 pesos por dólar en cada venta.  
  * *Ahora:* Si falla la conexión, lanza `APITipoCambioError`. En `main.py` se bloquean los paquetes internacionales por seguridad comercial, pero los paquetes nacionales siguen vendiéndose normalmente sin necesitar internet.

---

### REQUISITO 5: Transacción con Líneas de Detalle
#### ¿Dónde están las clases Vuelo, Hotel y Seguro?
**No existen clases individuales llamadas Vuelo o Hotel.** En su lugar, el sistema utiliza un diseño más escalable y profesional mediante dos clases:
1. **`TipoItem` (`model/tipo_item.py`):** Define la categoría del servicio (`id_tipo`, `nombre_categoria`). Por ejemplo:
   * `TipoItem(1, "Vuelo")`
   * `TipoItem(2, "Hotel")`
   * `TipoItem(3, "Seguro de Viaje")`
   * `TipoItem(4, "Excursión")`
2. **`DetalleReserva` (`model/detalle_reserva.py`):** Representa cada línea de detalle. Recibe:
   * `tipo_item`: El objeto de categoría anterior.
   * `descripcion`: Texto descriptivo (ej: "Hotel Miami 7 noches").
   * `cantidad`: Entero mayor a 0 (validado en su setter).
   * `precio_unitario`: Valor unitario en pesos.
   * Su método `subtotal()` calcula: `cantidad * precio_unitario`.

#### ¿Cómo se arma la reserva en memoria?
La clase `Reserva` inicializa una lista vacía: `self.detalles = []`.
Luego se agregan los detalles mediante `reserva.agregar_detalle(item)`:
```python
reserva = Reserva(cliente, agente, paquete, prov, "2026-12-01", precio_paquete_clp)
reserva.agregar_detalle(DetalleReserva(TipoItem(1, "Vuelo"), "Santiago-Miami", 1, 150000))
reserva.agregar_detalle(DetalleReserva(TipoItem(2, "Hotel"), "Hotel Miami", 7, 50000))
```
El cálculo total de la reserva se obtiene con:
```python
def total(self):
    total_detalles = sum(d.subtotal() for d in self.detalles)
    return self.precio_paquete_clp + total_detalles
```

#### ¿Cómo se guarda en la Base de Datos? (Transacción Atómica en `dao/reserva_dao.py`)
En `reserva_dao.insertar(reserva)`:
1. Se guarda la cabecera con `INSERT INTO reserva (...) VALUES (...)`.
2. Se rescata el ID asignado por SQLite con `reserva_id = self.cursor.lastrowid`.
3. Se recorre la lista `for d in reserva.detalles:` y se inserta cada uno en la tabla hija `detalle_reserva` usando `reserva_id` como clave foránea (`FOREIGN KEY`).
4. Se ejecuta `self.conexion.commit()`. Si algo falla en el camino, no se guardan datos corruptos.

---

# 5. CADENA DE PROPAGACIÓN DE ERRORES

¿Cómo viaja un error desde el modelo hasta la pantalla del usuario?

```
1. El usuario ingresa un dato en el menú de consola (main.py).
   ↓
2. Se intenta crear la entidad o validar la regla en la capa model/.
   ↓
3. Si el dato no cumple la regla, el modelo ejecuta:
   raise AnticipoInsuficienteError("El anticipo debe ser al menos el 50%.")
   ↓
4. El raise "salta" fuera de la función interrumpiendo el flujo normal.
   ↓
5. En main.py, esa llamada está envuelta en un bloque try:
   try:
       reserva.validar_confirmacion()
       reserva_dao.insertar(reserva)
   except AnticipoInsuficienteError as e:
       print(f"Operación denegada (Anticipo): {e}")
   ↓
6. El bloque except atrapa el error, muestra el mensaje amigable y vuelve al menú.
   ¡El programa NO se cae ni muestra errores de consola feos!
```

---

# 6. SEGURIDAD Y PERSISTENCIA

1. **Prevención de Inyección SQL:**  
   En `dao/paquete_dao.py` y `dao/reserva_dao.py`, nunca se hace:
   `f"SELECT * FROM paquete WHERE id = {id}"` ❌ (Vulnerable a inyecciones).  
   Siempre se utiliza la sintaxis con tupla de parámetros:
   `cursor.execute("SELECT * FROM paquete WHERE id = ?", (id,))` ✔️ (100% seguro).

2. **Integridad Referencial en SQLite:**  
   SQLite por defecto tiene las claves foráneas desactivadas. En `conectar.py`, ejecutamos:
   ```python
   conexion.execute("PRAGMA foreign_keys = ON;")
   ```
   Esto asegura que la base de datos rechace automáticamente cualquier detalle de reserva que no tenga una reserva padre válida.

---

# 7. DICCIONARIO TÉCNICO: CÓMO LEER EL CÓDIGO EN VOZ ALTA

| Sintaxis en el Editor | Cómo se lee profesionalmente en la defensa |
| :--- | :--- |
| `class Paquete(ABC):` | "Definimos la clase base `Paquete`, que hereda de `ABC` convirtiéndose en una clase abstracta." |
| `@abstractmethod` | "Decorador de método abstracto: obliga a cada subclase hija a implementar su propio cálculo." |
| `super().__init__(nombre, rut)` | "Invocamos al constructor de la clase padre mediante `super()` para inicializar los atributos heredados." |
| `@property` y `@setter` | "Implementamos el encapsulamiento: `@property` funciona como getter y el `@setter` valida el dato antes de asignarlo." |
| `self.cursor.lastrowid` | "Recuperamos el identificador autogenerado por la base de datos para enlazar las claves foráneas." |
| `except APITipoCambioError:` | "Capturamos específicamente la excepción de tipo de cambio para avisar al operador sin botar el sistema." |
| `PRAGMA foreign_keys = ON;` | "Instrucción enviada al motor SQLite para activar la verificación estricta de integridad referencial." |
