# CÓMO SE LEE EL CÓDIGO (GUÍA DE LECTURA ORAL TÉCNICA)
## DICCIONARIO DE TRADUCCIÓN: DE SINTAXIS PYTHON A LENGUAJE ORAL PROFESIONAL
**Evaluación Sumativa N°3 - POOS TI3V21**  
**Agencia de Viajes RutaSur** — Cristopher Figueroa y Elías Reyes

---

## INTRODUCCIÓN: EL ERROR MÁS COMÚN EN LA DEFENSA
Cuando el profesor Michael Arjel señala la pantalla y pregunta: *"¿Qué dice y qué hace esta línea?"*, la mayoría de los estudiantes comete el error de "leer caracteres" en vez de "explicar la semántica".

* ❌ **Cómo NO se lee:** *"Self punto nombre igual a nombre, dos puntos, def return self guión bajo nombre"*. (Suena robótico, mecánico y demuestra que no se entiende la lógica).
* ✅ **Cómo SÍ se lee:** *"Aquí definimos el constructor que recibe el parámetro `nombre` y lo asigna a la propiedad pública, lo que dispara automáticamente el setter validador para sanitizar la entrada antes de almacenarla en el atributo protegido `_nombre`"*.

A continuación tienes la guía exacta de **cómo se lee y explica cada línea clave del proyecto**.

---

# 1. CÓMO SE LEEN LAS CLASES, EL CONSTRUCTOR Y LAS PROPERTIES

### Caso A: Clase Abstracta y Herencia Base
```python
# En model/persona.py:
class Persona(ABC):
```
* **Cómo se lee en voz alta:**
  > "Declaramos la clase `Persona`, la cual hereda de `ABC` (Abstract Base Class). Esto la convierte en una **clase abstracta**, lo que significa que no se puede instanciar directamente; sirve como molde base para que hereden `Cliente`, `Viajero` y `Trabajador`."

---

### Caso B: Constructor y Asignación con Setter
```python
def __init__(self, nombre: str, rut: str):
    self.nombre = nombre
    self.rut = rut
```
* **Cómo se lee en voz alta:**
  > "En el constructor `__init__`, recibimos los parámetros tipados `nombre` y `rut` como cadenas de texto. Al escribir `self.nombre = nombre`, **no estamos asignando una variable común**, sino invocando al método `@nombre.setter`, el cual valida y sanitiza el dato antes de asignarlo a la variable interna protegida `_nombre`."

---

### Caso C: El Getter (`@property`)
```python
@property
def nombre(self):
    return self._nombre
```
* **Cómo se lee en voz alta:**
  > "El decorador `@property` define un **getter**. Nos permite consultar el valor del atributo protegido `_nombre` desde afuera usando la sintaxis limpia `persona.nombre`, pero protegiendo la variable interna para que nadie la modifique sin pasar por el setter."

---

### Caso D: El Setter con Validación
```python
@nombre.setter
def nombre(self, valor):
    valor = str(valor).strip()
    if len(valor) < 2:
        raise ValueError("El nombre debe tener al menos 2 caracteres.")
    if not valor.replace(" ", "").isalpha():
        raise ValueError("El nombre solo puede contener letras.")
    self._nombre = valor
```
* **Cómo se lee en voz alta:**
  > "Este es el **setter validador**. Recibe el nuevo dato en el parámetro `valor`, le aplica `.strip()` para limpiar espacios accidentales en los extremos, y evalúa dos reglas de integridad: que tenga al menos dos caracteres y que contenga exclusivamente letras. Si alguna regla falla, interrumpe el flujo lanzando un `ValueError`. Si pasa las validaciones, recién ahí se guarda en la variable real `self._nombre` con guión bajo."

---

### Caso E: Herencia y Constructor Padre (`super()`)
```python
# En model/viajero.py:
class Viajero(Persona):
    def __init__(self, rut, nombre, numero_pasaporte):
        super().__init__(nombre, rut)
        self.numero_pasaporte = numero_pasaporte
```
* **Cómo se lee en voz alta:**
  > "La clase `Viajero` hereda de `Persona`. Su constructor recibe el RUT, el nombre y el número de pasaporte. Con la instrucción `super().__init__(nombre, rut)`, invocamos al constructor de la clase padre `Persona` para que ella se encargue de inicializar y validar el nombre y el RUT. Luego, `Viajero` se encarga de su dato especializado asignando `self.numero_pasaporte = numero_pasaporte`, lo que dispara su propio setter validador de pasaporte."

---

# 2. CÓMO SE LEE EL POLIMORFISMO EN LOS PAQUETES

### Caso F: Método Abstracto en la Superclase
```python
# En model/paquete.py:
@abstractmethod
def calcular_precio_final(self, tipo_cambio=None):
    pass
```
* **Cómo se lee en voz alta:**
  > "El decorador `@abstractmethod` define un **contrato polimórfico**. Establece que toda subclase que herede de `Paquete` está obligada a implementar el método `calcular_precio_final()`. No usamos ningún valor fijo por defecto (como $950) para no suponer datos ante caídas de red. En la clase base no tiene código (`pass`) porque cada tipo de viaje tiene su propia regla matemática de cobro."

---

### Caso G: Sobrescritura en Subclases
```python
# En model/paquete_nacional.py:
def calcular_precio_final(self, tipo_cambio=None):
    return round(self.precio_base)

# En model/paquete_internacional.py:
def calcular_precio_final(self, tipo_cambio=None):
    if tipo_cambio is None: raise ValueError("El tipo de cambio es obligatorio para paquetes internacionales y no se puede asumir un valor por defecto.")
    if tipo_cambio <= 0: raise ValueError("El tipo de cambio debe ser mayor que cero.")
    return round(self.precio_base * tipo_cambio)

# En model/paquete_crucero.py:
def calcular_precio_final(self, tipo_cambio=None):
    if tipo_cambio is None: raise ValueError("El tipo de cambio es obligatorio para paquetes de crucero y no se puede asumir un valor por defecto.")
    if tipo_cambio <= 0: raise ValueError("El tipo de cambio debe ser mayor que cero.")
    return round(self.precio_base * tipo_cambio * 1.12)
```
* **Cómo se lee en voz alta:**
  > "Aquí vemos el **polimorfismo en acción**. Las tres clases hijas sobrescriben el método con la misma firma, pero con comportamiento distinto:
  > * En el paquete nacional, la tarifa está en moneda local, por lo que retorna directamente el precio base en pesos ignorando el tipo de cambio.
  > * En el paquete internacional, el precio base está en dólares, por lo que valida que el tipo de cambio sea positivo y multiplica el precio base por el valor del dólar.
  > * Y en el crucero, toma el valor convertido a pesos y le aplica un recargo del 12% por tasas portuarias multiplicando por 1.12."

---

# 3. CÓMO SE LEE LA PERSISTENCIA Y EL DAO

### Caso H: Activación de Integridad Referencial
```python
# En conectar.py:
conexion = sqlite3.connect("agencia.db")
conexion.execute("PRAGMA foreign_keys = ON")
return conexion
```
* **Cómo se lee en voz alta:**
  > "Abrimos la conexión al archivo de base de datos SQLite `agencia.db`. De inmediato ejecutamos el comando `PRAGMA foreign_keys = ON` para forzar al motor a verificar las restricciones de clave foránea en cada operación, impidiendo que se guarden detalles de reserva huérfanos sin una reserva válida."

---

### Caso I: Consulta Parametrizada e Inyección de ID
```python
# En dao/paquete_dao.py:
def insertar(self, paquete, tipo):
    self.cursor.execute("INSERT INTO paquete (nombre, precio_base, tipo) VALUES (?, ?, ?)", 
                        (paquete.nombre, paquete.precio_base, tipo))
    self.conexion.commit()
    paquete.id_paquete = self.cursor.lastrowid
```
* **Cómo se lee en voz alta:**
  > "El método `insertar` recibe el objeto `paquete` del modelo y su `tipo`.
  > Ejecuta una inserción SQL utilizando **marcadores de posición `?`**, enviando los atributos del objeto dentro de una tupla. Esto sanitiza los datos contra Inyección SQL.
  > Luego ejecuta `commit()` para persistir los cambios en el disco.
  > Y en la última línea, recupera el identificador autogenerado por SQLite con `cursor.lastrowid` y se lo inyecta de vuelta al objeto en memoria, dejándolo sincronizado con la base de datos."

---

### Caso J: Traducción de Tupla a Objeto en el SELECT
```python
# En dao/paquete_dao.py:
fila = self.cursor.fetchone()
if fila is None:
    return None

tipo = fila[3]
if tipo == 'nacional':
    p = PaqueteNacional(fila[0], fila[1], fila[2], None)
```
* **Cómo se lee en voz alta:**
  > "El cursor ejecuta la búsqueda y recupera una tupla con `fetchone()`. Si no encuentra coincidencias, retorna `None`.
  > Si encuentra la fila, el DAO cumple con su rol de **traductor de capas**: lee la columna de tipo (`fila[3]`) y en lugar de entregarle datos crudos al menú, fabrica e instancia un objeto de la clase correspondiente (`PaqueteNacional`), inyectándole el ID (`fila[0]`), el nombre (`fila[1]`) y el precio base (`fila[2]`)."

---

### Caso K: Transacción Atómica en Reserva
```python
# En dao/reserva_dao.py:
self.cursor.execute('''
    INSERT INTO reserva (fecha_viaje, precio_paquete_clp, anticipo, estado)
    VALUES (?, ?, ?, ?)
''', (reserva.fecha_viaje, reserva.precio_paquete_clp, reserva.anticipo, reserva.estado))

reserva_id = self.cursor.lastrowid

for detalle in reserva.detalles:
    self.cursor.execute('''
        INSERT INTO detalle_reserva (reserva_id, tipo_item, descripcion, cantidad, precio_unitario)
        VALUES (?, ?, ?, ?, ?)
    ''', (reserva_id, detalle.tipo_item.nombre_categoria, detalle.descripcion, detalle.cantidad, detalle.precio_unitario))

self.conexion.commit()
```
* **Cómo se lee en voz alta:**
  > "Esta es una **transacción atómica de dos fases (Maestro-Detalle)**:
  > 1. Primero insertamos la cabecera en la tabla `reserva` y obtenemos su ID único con `lastrowid`.
  > 2. Luego iteramos la lista de detalles de la reserva e insertamos cada línea hija en `detalle_reserva`, enlazándola mediante la clave foránea `reserva_id`.
  > 3. Al final ejecutamos un único `self.conexion.commit()`. Esto garantiza la propiedad de Atomicidad (ACID): se guarda la reserva completa con todos sus ítems, o si ocurre un fallo en el camino, no se guarda nada."

---

# 4. CÓMO SE LEE LA API EXTERNA Y LA SEGURIDAD FAIL-SECURE

### Caso L: Consumo de API y Timeout
```python
# En servicios/mindicador.py:
response = requests.get("https://mindicador.cl/api/dolar", timeout=5)
if response.status_code == 200:
    data = response.json()
    return data['serie'][0]['valor']
else:
    raise APITipoCambioError(f"La API respondió con código de estado HTTP {response.status_code}.")
```
* **Cómo se lee en voz alta:**
  > "Realizamos una petición HTTP GET al endpoint de indicadores económicos con un tiempo de espera máximo de 5 segundos (`timeout=5`) para prevenir bloqueos por indisponibilidad de red.
  > Si el servidor responde exitosamente con código de estado 200, parseamos el JSON y extraemos el valor más reciente del dólar.
  > Si el código es distinto de 200, levantamos nuestra excepción propia `APITipoCambioError`."

---

### Caso M: Política Fail-Secure ante Excepción
```python
except requests.exceptions.RequestException:
    raise APITipoCambioError("No se pudo conectar a la API del dólar (sin internet o servicio caído).")
```
* **Cómo se lee en voz alta:**
  > "Si ocurre cualquier error de red, fallo de DNS o timeout, capturamos `RequestException` y lanzamos `APITipoCambioError`.
  > Aquí aplicamos la política de **Fallo Seguro (*Fail-Secure*)**: no utilizamos valores estáticos por defecto (como $950) porque un desfase con el tipo de cambio real genera pérdidas financieras para la agencia. Si no hay conexión oficial, la operación en moneda extranjera se interrumpe de forma controlada sin tumbar la aplicación."

---

# 5. CÓMO SE LEE EL MOTOR DE REGLAS DE NEGOCIO

### Caso N: Validación de Confirmación
```python
# En model/reserva.py:
def validar_confirmacion(self):
    if isinstance(self.paquete, (PaqueteInternacional, PaqueteCrucero)):
        if not self.viajero or not self.viajero.validar_pasaporte():
            raise ValidacionError("Un paquete internacional o crucero requiere un Viajero con pasaporte válido.")

    if not self.proveedor.tiene_cupos(self.fecha_viaje):
        raise SinCuposError("No se puede confirmar la reserva porque el proveedor no tiene cupos para esa fecha.")

    minimo_anticipo = self.total() * 0.50
    if self.anticipo < minimo_anticipo:
        raise AnticipoInsuficienteError("El anticipo debe ser al menos el 50% del total.")

    self.estado = EstadoReserva.CONFIRMADA
    return True
```
* **Cómo se lee en voz alta:**
  > "El método `validar_confirmacion` evalúa en memoria las tres reglas de negocio obligatorias:
  > 1. Con `isinstance`, verifica si el paquete involucra viaje al extranjero; si es así, comprueba mediante el método `validar_pasaporte()` que el viajero cuente con pasaporte vigente. Si falta, lanza `ValidacionError`.
  > 2. Consulta al objeto `proveedor` si posee disponibilidad en la fecha con `tiene_cupos()`. Si no hay cupos, interrumpe el flujo lanzando `SinCuposError`.
  > 3. Calcula el 50% del costo total acumulado (paquete más detalles); si el anticipo pagado es inferior, lanza `AnticipoInsuficienteError`.
  > Si supera todas las restricciones, actualiza el estado de la reserva a `CONFIRMADA` y retorna `True`."
