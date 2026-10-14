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
8. **Guía Completa Archivo por Archivo y Recorridos del Menú**
9. **Qué Hace el Programa y Qué Todavía No Hace**

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
En `model/persona.py` hay tres usos relacionados de `nombre`, pero no son la misma variable:
```python
class Persona(ABC):
    def __init__(self, nombre: str, rut: str):
        self.nombre = nombre

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        valor = str(valor).strip()
        if len(valor) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres.")
        if not valor.replace(" ", "").isalpha():
            raise ValueError("El nombre solo puede contener letras.")
        self._nombre = valor
```

### Primero: ¿qué es `self` y qué es el parámetro?
Cuando se crea un objeto, por ejemplo `Persona("Juan", "11111111-1")`, Python llama a `__init__`. `self` representa el objeto que se está inicializando. `nombre` y `rut`, dentro de los paréntesis, son parámetros: nombres locales que reciben los valores entregados al constructor. En este ejemplo, el parámetro `nombre` recibe el texto `"Juan"`.

### ¿Qué significa cada aparición?
1. **`nombre` en `def __init__(self, nombre, rut)`:** parámetro local del constructor. No es todavía el lugar permanente donde se guarda el nombre.
2. **`self.nombre = nombre`:** asigna el valor a la propiedad pública llamada `nombre`. Como esta clase define un setter para esa propiedad, Python ejecuta ese setter al hacer la asignación. No se escribe `self.nombre()` porque esta sintaxis es una asignación a una propiedad, no una llamada directa a una función.
3. **`valor` en `def nombre(self, valor)`:** parámetro del setter. Recibe lo que estaba a la derecha de `=`; al inicializar, recibe el valor del parámetro `nombre` del constructor.
4. **`self._nombre = valor`:** atributo interno del objeto donde el setter guarda el texto después de limpiarlo y validarlo.

El recorrido para `Persona(" Juan ", "11111111-1")` es: el constructor recibe `" Juan "`; `self.nombre = nombre` activa el setter; el setter elimina espacios de los extremos, revisa las reglas y guarda `"Juan"` en `self._nombre`. Si el dato no pasa una regla, lanza `ValueError` y no lo guarda.

### ¿Qué es una property, explicado sin darlo por sabido?
Una **property** (propiedad) permite usar una función con la sintaxis de un atributo. En este caso, `nombre` es la forma pública y cómoda de consultar o cambiar el nombre. La función decorada con `@property` es el **getter**: se ejecuta al leer `persona.nombre` y devuelve `self._nombre`. La función decorada con `@nombre.setter` es el **setter**: se ejecuta al asignar `persona.nombre = "Ana"` y puede validar el nuevo valor antes de guardarlo.

Por eso se escribe `persona.nombre`, sin paréntesis: la property está diseñada para usarse como atributo. En cambio, una función o método normal se llama con paréntesis, por ejemplo `persona.validar()`.

### ¿Por qué no guardar directamente en `self.nombre`?
Porque `nombre` es el acceso controlado y `self._nombre` es el almacenamiento interno que usa esta clase. Si el constructor guardara directamente en `self._nombre`, se saltaría el setter y también su limpieza y validación. La misma property deja que el código externo lea y cambie el nombre de forma sencilla, pasando las asignaciones por las reglas de la clase.

El guión bajo inicial de `_nombre` **no vuelve el atributo privado de verdad**. En Python es una convención que indica: “esto es interno; usa `nombre` en vez de acceder directamente a `_nombre`”. Otro código todavía podría escribir `persona._nombre`, pero estaría saltándose el mecanismo previsto. Dos guiones bajos (`__nombre`) activan una transformación del nombre para evitar choques accidentales en subclases; tampoco son una barrera de seguridad.

Importante: el setter guarda en `self._nombre`, no en `self.nombre`. Si asignara `self.nombre = valor` desde dentro del setter, volvería a llamar al mismo setter una y otra vez. El getter también lee `_nombre` directamente para no llamarse a sí mismo en un ciclo.

---

# 3. MÉTODOS PÚBLICOS VS PRIVADOS (UML Y PYTHON)

### ¿Cómo se representan en UML y qué significan en Python?
En UML, `+` indica que una operación o atributo es público y `-` indica que se modela como privado. Son símbolos del diagrama; Python no aplica automáticamente esos permisos según UML.

En Python, los nombres sin guión bajo inicial son públicos por convención y están disponibles desde otros objetos. Un guión bajo, como en `_nombre`, comunica que el elemento es de uso interno, pero no impide acceder a él. Dos guiones bajos, como en `__formatear_rut`, hacen que Python transforme el nombre internamente (name mangling), principalmente para evitar choques accidentales con nombres de subclases; no convierten el método en inaccesible ni constituyen seguridad.

Por eso, una explicación precisa es que `Persona` **encapsula por convención** el almacenamiento en `_nombre` y ofrece `nombre` como acceso público con validación. El acceso no se vuelve privado solo por poner guiones bajos.

### ¿Por qué `validar_pasaporte()` es público?
Porque otra clase, `Reserva`, necesita llamarlo desde `model/reserva.py`:
```python
# Dentro de Reserva.validar_confirmacion():
if not self.viajero.validar_pasaporte():
    raise ValidacionError("Un paquete internacional requiere un Viajero con pasaporte válido.")
```
Por eso el método se deja con un nombre público, sin guión bajo inicial: forma parte de la interfaz que `Reserva` necesita usar. Python no aplica permisos privados como otros lenguajes; un nombre que empieza con `_` indica que se considera interno, pero no impide llamarlo desde otra clase.

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
    def calcular_precio_final(self, tipo_cambio=None):
        pass  # Es abstracto: no calcula nada, obliga a las hijas a programarlo sin valores asumidos por defecto.
```

Sus tres subclases hijas sobrescriben el método implementando su fórmula comercial:

1. **`PaqueteNacional` (`model/paquete_nacional.py`):**
   * *Regla:* El precio se cobra directo en pesos chilenos (CLP). No depende del dólar ni de divisas.
   * *Código:*
     ```python
     def calcular_precio_final(self, tipo_cambio=None):
         return round(self.precio_base)
     ```
   * *Ejemplo:* Precio base $180.000 -> Devuelve `$180.000 CLP`.

2. **`PaqueteInternacional` (`model/paquete_internacional.py`):**
   * *Regla:* El precio base está fijado en dólares (USD). Se debe multiplicar por el tipo de cambio oficial del día (no asume 950 ni ningún valor si no hay red).
   * *Código:*
     ```python
     def calcular_precio_final(self, tipo_cambio=None):
         if tipo_cambio is None:
             raise ValueError("El tipo de cambio es obligatorio para paquetes internacionales y no se puede asumir un valor por defecto.")
         if tipo_cambio <= 0:
             raise ValueError("El tipo de cambio debe ser mayor que cero.")
         return round(self.precio_base * tipo_cambio)
     ```
   * *Ejemplo:* Precio base $500 USD con dólar oficial del día obtenido desde API -> `500 * dolar`.

3. **`PaqueteCrucero` (`model/paquete_crucero.py`):**
   * *Regla:* Mismo cálculo en dólares, pero con un recargo adicional del 12% (`* 1.12`) por concepto de tasas portuarias y servicios de abordo.
   * *Código:*
     ```python
     def calcular_precio_final(self, tipo_cambio=None):
         if tipo_cambio is None:
             raise ValueError("El tipo de cambio es obligatorio para paquetes de crucero y no se puede asumir un valor por defecto.")
         if tipo_cambio <= 0:
             raise ValueError("El tipo de cambio debe ser mayor que cero.")
         return round(self.precio_base * tipo_cambio * 1.12)
     ```
   * *Ejemplo:* Precio base $500 USD con dólar oficial del día -> `500 * dolar * 1.12`.

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
    `Reserva.validar_confirmacion()` pregunta si hay al menos un cupo para la fecha mediante `proveedor.tiene_cupos(fecha)`. La comparación entre el número de pasajeros y el número de cupos ingresado se hace antes, en la opción 7 de `main.py`; `Proveedor.tiene_cupos()` por sí solo no compara cantidades. Si la disponibilidad no existe o es cero, se lanza `SinCuposError`.
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

#### ¿Cómo se guardan la reserva y sus detalles en la Base de Datos?
En `reserva_dao.insertar(reserva)`:
1. Se guarda la cabecera con `INSERT INTO reserva (...) VALUES (...)`.
2. Se rescata el ID asignado por SQLite con `reserva_id = self.cursor.lastrowid`.
3. Se recorre la lista `for d in reserva.detalles:` y se inserta cada uno en la tabla hija `detalle_reserva` usando `reserva_id` como clave foránea (`FOREIGN KEY`).
4. Al terminar el recorrido se ejecuta `self.conexion.commit()` para confirmar los cambios pendientes.

**Límite de la implementación actual:** el método no tiene un bloque `try/except` que ejecute `rollback()` si una inserción falla. Por eso no se debe afirmar que cualquier error deja automáticamente la operación revertida: la transacción puede quedar pendiente en esa conexión hasta que se revierta o se cierre. La atomicidad completa debería protegerse explícitamente con `rollback()` ante errores.

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
    Para los valores se utiliza la sintaxis con tupla de parámetros:
    `cursor.execute("SELECT * FROM paquete WHERE id = ?", (id,))`. Esto evita que el valor del usuario se interprete como parte de la instrucción SQL. Es una protección importante para estas consultas, no una garantía de que todo el programa sea "100% seguro" frente a cualquier tipo de problema.

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

---

# 8. GUÍA COMPLETA ARCHIVO POR ARCHIVO Y RECORRIDOS DEL MENÚ

Esta sección se refiere a la versión de trabajo que está en `codigo_corregido/`. La carpeta antigua del taller mecánico es material de referencia distinto. En cada punto separaremos lo que el código **hace ahora** de lo que sería razonable esperar de una aplicación terminada.

## 8.1 Conceptos de Python que aparecen en este proyecto

* **Módulo:** un archivo `.py`. Por ejemplo, `model/persona.py` es el módulo `model.persona`.
* **`import`:** hace disponible en el archivo actual una clase o función definida en otro módulo. No copia ni pega su código.
* **Clase y objeto:** una clase define datos y operaciones; un objeto es una instancia concreta creada al llamar la clase, como `Cliente("Juan", "11111111-1")`.
* **`self`:** dentro de un método de instancia, se refiere al objeto que está usando ese método. `self.nombre` significa “el atributo o propiedad `nombre` de este objeto”. Python entrega el objeto como primer argumento automáticamente.
* **Parámetro y argumento:** el parámetro es el nombre en la definición (`def buscar(id)`); el argumento es el valor enviado al llamar (`buscar(4)`).
* **Anotación de tipo:** `nombre: str` o `-> bool` documenta el tipo esperado o devuelto y ayuda a las herramientas. Por sí sola no obliga a Python a comprobarlo al ejecutar.
* **`None`:** representa la ausencia de un objeto o valor. Aquí se usa, por ejemplo, como ID antes de que SQLite asigne uno, y cuando una búsqueda no encuentra un paquete.
* **`return`:** termina la función y entrega un resultado. Una función sin `return` devuelve `None` implícitamente.
* **`if`, `for` y `while`:** permiten elegir una rama, recorrer elementos y repetir el menú, respectivamente. `for _ in range(pasajeros)` repite una acción esa cantidad de veces; `_` indica que no interesa el número de la repetición.
* **`isinstance(objeto, Clase)`:** pregunta si un objeto es de esa clase o de una subclase. Se usa para distinguir paquetes nacionales de los que requieren dólar.
* **`try`, `except`, `raise`:** `try` ejecuta una operación que puede fallar; `raise` lanza una excepción; `except` la captura para responder sin terminar todo el programa.
* **`pass`:** no ejecuta ninguna acción. En este proyecto aparece en métodos de agente y administrador que son marcadores, no funciones terminadas.
* **Atributo frente a método:** `reserva.estado` consulta un dato; `reserva.total()` llama una operación. Los paréntesis son necesarios al llamar métodos, no al leer propiedades.

## 8.2 Archivos de entrada y configuración

### `main.py`: el coordinador y la interfaz de consola
Este es el punto de entrada de la aplicación. Importa las clases que necesita; define `menu()` para mostrar opciones y recoger una respuesta; y `main()` para conectar las capas. Al final, `if __name__ == "__main__": main()` significa que el menú se inicia cuando ejecutamos este archivo directamente, pero no cuando otro módulo solo lo importa.

Al iniciar, `main()` crea la conexión, instancia `PaqueteDAO` y `ReservaDAO`, pide crear las tablas si aún no existen y confirma esos cambios con `commit()`. Si falla esa preparación, muestra un mensaje y termina mediante `sys.exit(1)`. Después entra en `while True`, que repite el menú hasta seleccionar salir.

Las opciones hacen lo siguiente:

1. **Crear paquete:** lee nombre, precio y tipo. Convierte el precio ingresado a `float`; rechaza valores no positivos. Para internacional y crucero consulta el dólar y convierte el precio ingresado en CLP a USD (`precio_clp / dolar`) antes de crear el objeto y guardarlo. Para nacional conserva CLP. El ID y el proveedor se pasan como `None`; SQLite genera el ID y el sistema no asigna un proveedor real en esta operación.
2. **Listar paquetes:** obtiene objetos desde el DAO y muestra su ID, nombre, precio base y tipo. El precio mostrado es el precio base almacenado: nacional en CLP, internacional/crucero en USD. La pantalla no agrega una etiqueta de moneda en cada fila, así que no hay que interpretar todos los valores como CLP.
3. **Modificar paquete:** busca por ID y cambia solo el precio, no el nombre. Para paquetes extranjeros vuelve a consultar el dólar y convierte el nuevo precio ingresado en CLP a USD. `isinstance` identifica qué tipo concreto se recuperó antes de guardar.
4. **Eliminar paquete:** pide un ID y muestra si el DAO encontró y eliminó una fila.
5. **Validar pasaporte:** crea un `Viajero` de prueba con RUT y nombre fijos, y el pasaporte ingresado. La creación llama al setter; si una regla falla se captura `ValueError` y se informa.
6. **Calcular precio:** busca el paquete. El nacional calcula sin API. Los demás consultan el dólar actual y llaman el método concreto del paquete: internacional multiplica USD por tipo de cambio; crucero agrega el factor `1.12`.
7. **Registrar reserva:** es el recorrido más largo y se detalla en 8.8. Usa proveedor, cliente, agente, fecha y conceptos de detalle de prueba; no es todavía un flujo de venta conectado a registros reales de todos esos actores.
8. **Ver detalle:** busca la cabecera y los detalles guardados por ID, calcula sus subtotales y muestra total y saldo pendiente.
9. **Salir:** cierra la conexión y rompe el ciclo con `break`. Después de otras opciones, `input("Presione Enter...")` pausa antes de mostrar nuevamente el menú.

Las conversiones `int(...)` y `float(...)` pueden lanzar `ValueError`; varios `except ValueError` capturan ese problema. En algunas opciones también capturan errores de validación del modelo, errores de API y, al final, un `Exception` general. El `continue` salta el resto de la opción actual y vuelve al principio del ciclo del menú.

### `conectar.py`: abrir SQLite
`crear_conexion()` llama a `sqlite3.connect("agencia.db")`, activa las claves foráneas para **esa conexión** y devuelve el objeto conexión. Como la ruta es relativa, el archivo de base de datos se crea en el directorio desde el que se ejecuta el programa. El módulo no crea tablas ni cierra la conexión: eso lo hace `main.py`.

### `requirements.txt` y `README.md`
`requirements.txt` declara `requests`, la biblioteca externa que usa la consulta HTTP. `README.md` indica cómo instalar dependencias y ejecutar el programa. SQLite forma parte de la biblioteca estándar de Python, por eso no aparece en `requirements.txt`.

## 8.3 Modelos de personas y roles

### `model/persona.py`
`Persona` centraliza `nombre` y `rut` para que las subclases no repitan sus validaciones. Hereda de `ABC`, pero **no declara ningún método con `@abstractmethod`**, así que en el código actual esa herencia por sí sola no impide crear instancias de `Persona`. La intención de usar una base abstracta y el comportamiento efectivo no son exactamente lo mismo.

El constructor asigna ambos valores a propiedades. El setter de `nombre` convierte a texto, quita espacios de los extremos, exige al menos dos caracteres y permite solo letras y espacios internos. El setter de `rut` también convierte a texto y elimina espacios externos; exige que no esté vacío, que contenga `-` y que mida al menos ocho caracteres. Esto es una comprobación básica de formato, no una verificación matemática del dígito verificador chileno.

### `model/cliente.py`, `model/trabajador.py`, `model/agente_viajes.py` y `model/administrador.py`
`Cliente` hereda de `Persona` y llama `super().__init__(nombre, rut)`; por ahora no añade atributos.

`Trabajador` también hereda de `Persona` y de `ABC`, pero tampoco tiene métodos abstractos decorados. Por tanto, el código no impide instanciarlo solo por heredar de `ABC`.

`AgenteViajes` hereda de `Trabajador`; `puede_atender_clientes()` devuelve `True`. Sus métodos `atender_cliente()` y `vender_paquete()` contienen `pass`, así que no atienden ni venden todavía y devuelven `None`.

`Administrador` hereda de `Trabajador`; su método `puede_atender_clientes()` devuelve `False`. `gestionar_proveedor()` y `gestionar_pagos()` también son marcadores vacíos. Estas clases describen roles, pero el menú actual crea un agente de prueba y no implementa autorización o gestión real.

### `model/viajero.py`
`Viajero` hereda de `Persona`. Su constructor recibe los argumentos en el orden **RUT, nombre, pasaporte**, y luego llama al padre en el orden nombre, RUT: `super().__init__(nombre, rut)`. Este cambio de orden es intencional en el código y conviene respetarlo al crear un viajero.

La property `numero_pasaporte` rechaza vacío, quita espacios externos, convierte a mayúsculas y exige entre 6 y 12 caracteres alfanuméricos. `validar_pasaporte()` devuelve un booleano repitiendo la comprobación sobre el valor ya almacenado. Como el setter ya impide guardar uno inválido, el método es una comprobación adicional útil para la regla de reserva.

## 8.4 Paquetes: herencia, abstracción y cálculo

### `model/paquete.py`
`Paquete` concentra los datos comunes: `id_paquete`, `nombre`, `precio_base` y `proveedor_id`. Solo `precio_base` tiene property: se convierte a `float` y debe ser mayor que cero. Los otros tres son atributos públicos normales. El código no valida el nombre aquí; la opción 1 del menú hace una comprobación básica antes de construir el paquete.

`Paquete` hereda de `ABC` y sí tiene `calcular_precio_final()` decorado con `@abstractmethod`. Eso sí impide instanciar directamente la clase base y obliga a una subclase concreta a proporcionar ese método. El `pass` del método abstracto no es un cálculo: señala que la base define el contrato, no una implementación.

### `model/paquete_nacional.py`, `model/paquete_internacional.py` y `model/paquete_crucero.py`
Las tres clases llaman `super().__init__(...)` para reutilizar la inicialización y validación del precio base.

* `PaqueteNacional.calcular_precio_final()` devuelve `round(precio_base)` y no usa el tipo de cambio.
* `PaqueteInternacional.calcular_precio_final(tipo_cambio)` exige un tipo de cambio positivo y devuelve `round(precio_base * tipo_cambio)`.
* `PaqueteCrucero.calcular_precio_final(tipo_cambio)` hace la misma validación y multiplica además por `1.12`, que representa el recargo del 12% definido por el proyecto.

Esto es **polimorfismo**: el menú puede llamar `p.calcular_precio_final(...)`, y la clase real de `p` determina cuál fórmula se ejecuta. `round()` devuelve un entero cuando se usa sin cantidad de decimales; para montos exactamente a mitad entre enteros, Python redondea al entero par más cercano.

## 8.5 Proveedor y disponibilidad

### `model/disponibilidad.py`
Guarda una fecha y `cupos_disponibles`. La property convierte el valor a entero y no permite negativos. `tiene_cupos()` solo pregunta si el número es mayor que cero. `descontar_cupo()` primero revisa esa condición y luego resta exactamente uno mediante `self.cupos_disponibles -= 1`; esa asignación vuelve a pasar por el setter.

### `model/proveedor.py`
Un proveedor tiene ID, nombre y una lista llamada `disponibilidades`. `agregar_disponibilidad()` añade un objeto a la lista. `tiene_cupos(fecha)` busca la primera disponibilidad con esa fecha y devuelve su respuesta; si no encuentra fecha devuelve `False`. `descontar_cupo(fecha)` busca igual, descuenta uno y devuelve `True`; si no hay una fecha registrada lanza `ValueError`.

En la opción 7 se crea un proveedor temporal con ID y nombre fijos y una sola disponibilidad. No se carga ni se guarda ese proveedor en SQLite. La cantidad de pasajeros se compara con los cupos ingresados en el menú; la regla de `Reserva` solo comprueba que haya al menos un cupo. Después de confirmar, `main.py` descuenta un cupo por pasajero.

## 8.6 Reserva, estados, items y excepciones

### `model/tipo_item.py`
Representa una categoría de línea de reserva, por ejemplo Vuelo, Hotel, Seguro o Excursión. `id_tipo` es un atributo normal con anotación `int`, pero no tiene conversión ni validación. `nombre_categoria` sí es property: convierte a texto, quita espacios exteriores y rechaza una cadena vacía.

### `model/detalle_reserva.py`
Representa una línea concreta de la reserva. Comprueba que `tipo_item` sea una instancia de `TipoItem`; convierte `cantidad` a entero y exige que sea positiva; convierte el precio unitario a `float` y permite cero, pero no valores negativos. `subtotal()` multiplica cantidad por precio unitario. `descripcion` se guarda directamente, sin una validación propia.

### `model/reserva.py`
`EstadoReserva` es un `Enum` cuyos valores posibles son `PENDIENTE`, `CONFIRMADA`, `PAGADA` y `CANCELADA`. Usar nombres fijos reduce errores de escritura frente a guardar estados arbitrarios.

El constructor recibe referencias a cliente, agente, paquete y proveedor, además de fecha y precio del paquete en CLP; convierte precio y tipo de cambio a `float`, crea una lista vacía de detalles y asigna anticipo, estado y viajero. Esas referencias viven en memoria: no significa que los objetos relacionados queden guardados en la base de datos.

`anticipo` es una property que convierte a `float` y prohíbe montos negativos. `agregar_detalle()` añade un elemento a la lista, pero no comprueba su tipo. `total()` suma el precio del paquete más todos los `subtotal()` de los detalles; `sum(...)` recorre el generador de subtotales. `saldo_pendiente()` resta el anticipo al total y usa `max(0, ...)` para que no entregue un saldo negativo.

`cancelar()` solo cambia el estado en memoria: no devuelve cupos ni actualiza la base de datos. `pagar_saldo(monto)` exige un pago positivo, rechaza que la suma de pagos supere el total, actualiza el anticipo y marca la reserva como `PAGADA` cuando el saldo llega a cero. Este método no se llama desde el menú actual y no guarda cambios por sí mismo.

`validar_confirmacion()` aplica las condiciones en este orden: si el paquete es internacional o crucero, debe existir un viajero con pasaporte válido; debe haber cupos para la fecha; y el anticipo debe alcanzar el 50% de `total()`. Cada falla lanza su excepción específica. Si todo pasa, cambia el estado a `CONFIRMADA` y devuelve `True`. La clase no recibe la cantidad de pasajeros, por lo que la comparación pasajeros/cupos queda fuera de este método.

### `model/excepciones.py`
`AgenciaError` es una excepción propia que hereda de `Exception`. Las otras clases heredan de ella para nombrar casos distintos: anticipo insuficiente, falta de cupos, recurso inexistente, problema de API, validación y autenticación. Sus `pass` significan que no agregan lógica ni campos: su utilidad es que `except` pueda capturar un tipo preciso. En la versión actual, `RecursoNoEncontradoError` y `AutenticacionError` están declaradas, pero no las usa el flujo del menú.

## 8.7 Persistencia: cómo se conectan los DAO

### `dao/dao.py`
Es una clase base pequeña: recibe la conexión SQLite y crea un cursor. Un cursor ejecuta instrucciones SQL y permite leer filas devueltas. Los DAO específicos heredan `conexion` y `cursor`.

### `dao/paquete_dao.py`
`crear_tabla()` define una tabla con ID autoincremental, nombre, precio base y tipo. `insertar()` usa marcadores `?` y una tupla de valores, confirma el `INSERT` con `commit()` y coloca en el objeto el ID generado (`lastrowid`).

`buscar()` devuelve `None` si no existe el ID; si existe, crea un objeto de la subclase adecuada a partir de la columna `tipo`. `listar()` hace lo mismo para todas las filas y devuelve pares `(objeto_paquete, tipo)`. En ambos métodos, cualquier tipo que no sea `nacional` o `internacional` termina interpretándose como crucero; el DAO confía en que el dato guardado sea válido.

`actualizar()` cambia nombre, precio y tipo de la fila identificada y hace `commit()`. `eliminar()` borra por ID, hace `commit()` y devuelve si SQLite afectó alguna fila (`rowcount > 0`). Las consultas parametrizadas protegen los valores de la consulta; `?` es un marcador de parámetro, no una cadena que se concatena manualmente.

### `dao/reserva_dao.py`
`crear_tabla()` define la cabecera `reserva` y la tabla `detalle_reserva`. Cada fila hija contiene `reserva_id`, categoría, descripción, cantidad y precio unitario; la clave foránea relaciona el detalle con su reserva. No hay en el esquema actual claves foráneas para cliente, agente, paquete ni proveedor.

`insertar()` inserta primero la cabecera, obtiene su ID, recorre los detalles y los inserta con ese ID, y finalmente hace `commit()`. Devuelve el ID de la reserva. No guarda viajero, tipo de cambio, IDs de cliente/agente/paquete/proveedor, ni el objeto `EstadoReserva` completo: guarda solo las columnas definidas en el esquema. Si falla una inserción antes del `commit()`, el método no ejecuta `rollback()` explícito.

`buscar_detalles(id)` consulta primero la reserva; si no existe devuelve `None`. Si existe, busca detalles asociados y devuelve un diccionario con dos claves: `"reserva"` contiene una tupla de fila y `"detalles"` una lista de tuplas. Por eso `main.py` accede por posición (`r[0]`, `d[2]`), no mediante atributos de objetos.

## 8.8 El flujo completo de registrar una reserva (opción 7)

1. El menú convierte a entero el ID ingresado y `PaqueteDAO.buscar()` reconstruye el paquete desde SQLite. Si no existe, se informa y `continue` vuelve al menú.
2. Para internacional o crucero, pide pasaporte y construye un viajero de prueba. Si falla el setter, muestra el error y abandona esta operación.
3. Pide los cupos y pasajeros. Crea una disponibilidad local con fecha fija `2026-12-01`; si pasajeros supera los cupos escritos por el usuario, lanza `SinCuposError`.
4. Para paquete extranjero, consulta el dólar y calcula el precio final por pasajero; para nacional usa el cálculo sin API. Multiplica el precio final por pasajeros para construir el precio del paquete de la reserva.
5. Construye un cliente y agente con datos fijos, instancia `Reserva` y le agrega cuatro detalles también fijos. Esos detalles se agregan una sola vez aunque haya varios pasajeros.
6. Imprime cada línea y calcula el total. `suma_detalles` se actualiza durante la impresión, pero ese acumulador no se usa después; el total verdadero se obtiene llamando `reserva.total()`.
7. Lee el anticipo, lo asigna a la property y llama `validar_confirmacion()`. La property rechaza negativos; el método verifica viajero si corresponde, disponibilidad positiva y mínimo 50%.
8. Si se confirma, descuenta un cupo por pasajero en el proveedor temporal y llama `ReservaDAO.insertar()`. Se muestra el saldo y el ID generado.

Las excepciones específicas se capturan para mostrar mensajes adecuados. `ValueError` cubre conversiones numéricas y validaciones de propiedades; el último `except Exception` es una red amplia para errores no previstos. La conexión a la API solo es necesaria para paquetes internacionales/crucero; una reserva nacional sigue la rama que no llama a `MiIndicador`.

## 8.9 Cómo funciona el dato del dólar

### `servicios/mindicador.py`
`MiIndicador.obtener_dolar()` solicita con `requests.get()` el endpoint del dólar y establece `timeout=5`, para no esperar indefinidamente. Si el código HTTP es 200, lee JSON y toma `data['serie'][0]['valor']`: `data` es el objeto decodificado, `serie` una lista y `[0]` el primer registro. Si el HTTP no es 200, lanza `APITipoCambioError`. También convierte errores de conexión, claves ausentes, lista vacía y ciertos errores de formato en esa excepción propia. No usa un valor alternativo fijo.

## 8.10 `model/__init__.py`
Este archivo está vacío. Su presencia marca la carpeta `model` como paquete Python en la organización tradicional. No contiene clases ni comportamiento adicional.

# 9. QUÉ HACE EL PROGRAMA Y QUÉ TODAVÍA NO HACE

Esta distinción ayuda a defender el trabajo sin atribuirle capacidades que aún no están programadas:

* **Sí ejecuta:** menú de consola; alta, listado, edición y eliminación de paquetes; cálculo de precios; consulta del dólar para moneda extranjera; creación de reservas de demostración; validación de pasaporte, cupos y anticipo; guardado y consulta de cabecera y detalles de reserva.
* **No mantiene un sistema real de clientes, trabajadores ni proveedores:** la opción de reserva crea objetos con datos fijos en memoria. No hay DAO para esas entidades.
* **No enlaza la reserva al paquete ni a las personas en SQLite:** aunque esos objetos se pasan al constructor, el esquema de `reserva` no tiene columnas para sus IDs. Al consultar después, se recuperan fecha, precio, anticipo, estado y líneas, pero no se reconstruyen los objetos relacionados.
* **No guarda la disponibilidad:** el proveedor y su lista de cupos se crean durante la opción 7 y desaparecen de memoria al terminar. El descuento no cambia una tabla en la base de datos.
* **No implementa las acciones de agente y administrador:** los métodos que tienen `pass` son espacios pendientes, no operaciones ocultas.
* **No ofrece un formulario completo de detalles:** las cuatro líneas de la reserva se crean con valores fijos en el código.
* **No maneja reversión explícita en `ReservaDAO.insertar()`:** existe un único `commit()` al final del flujo, pero falta un `rollback()` para el camino de error.

Nombrar estas limitaciones no quita valor a los conceptos demostrados; distingue correctamente el modelo diseñado del alcance que el programa realmente ejecuta.
