# COORDINACIÓN TÉCNICA CON EL DIAGRAMA UML
## COMPARATIVA INTEGRAL: `Diagrama_RutaSur.drawio` vs CÓDIGO FUENTE
**Agencia de Viajes RutaSur** — Evaluación Sumativa N°3 (POOS TI3V21)  
**Estudiantes:** Cristopher Figueroa y Elías Reyes

---

## 1. INTRODUCCIÓN Y CONTEXTO
En la Evaluación Sumativa N°1, el profesor Michael Arjel entregó la retroalimentación sobre nuestro modelo conceptual del negocio. En esta Evaluación Sumativa N°3, el Criterio **2.1.2 / 4.1.1** exige que el código mantenga una **coherencia total con el diagrama UML (`Diagrama_RutaSur.drawio`)**.

A continuación se detalla la correspondencia exacta entre cada elemento del diagrama y su implementación en Python.

---

## 2. TABLA DE CORRESPONDENCIA CLASE POR CLASE

| Clase en Diagrama UML | Tipo en UML | Archivo en Código | Atributos Mapeados | Métodos Mapeados | Relación Representada |
|---|---|---|---|---|---|
| **Persona** | Clase Base | `model/persona.py` | `+ nombre: String`<br>`+ rut: String` | `@property`, `@setter` de validación | Superclase abstracta de todos los actores humanos. |
| **Cliente** | Subclase | `model/cliente.py` | Hereda `nombre`, `rut` | `super().__init__(nombre, rut)` | **Herencia** (Generalización) de `Persona`. Quien contrata y paga la reserva. |
| **Viajero** | Subclase | `model/viajero.py` | `- numeroPasaporte: String` | `+ validarPasaporte(): Boolean`<br>`@numero_pasaporte.setter` | **Herencia** de `Persona`. Quien viaja físicamente. Requiere pasaporte en vuelos internacionales. |
| **Trabajador** | Subclase | `model/trabajador.py` | Hereda `nombre`, `rut` | `super().__init__(nombre, rut)` | **Herencia** de `Persona`. Molde común para empleados de la agencia. |
| **AgenteViajes** | Subclase | `model/agente_viajes.py` | Hereda de `Trabajador` | `+ puedeAtenderClientes(): Boolean` (True)<br>`+ atenderCliente(cli)`<br>`+ venderPaquete(paq)` | **Herencia** de `Trabajador`. Habilitado para venta y atención directa. |
| **Administrador** | Subclase | `model/administrador.py` | Hereda de `Trabajador` | `+ puedeAtenderClientes(): Boolean` (False)<br>`+ gestionarProveedor(prov)`<br>`+ gestionarPagos(res)` | **Herencia** de `Trabajador`. Restringido (Principio de Menor Privilegio). |
| **Paquete** | `<<Abstract>>` | `model/paquete.py` | `+ idPaquete: Integer`<br>`+ nombre: String`<br>`+ precioBase: Float` | `+ calcularPrecioFinal(tipoCambio)*` (Abstracto) | **Clase Abstracta** base de productos turísticos. |
| **PaqueteNacional** | Subclase | `model/paquete_nacional.py` | Hereda de `Paquete` | `+ calcularPrecioFinal(t)` | **Herencia** y polimorfismo: tarifa en CLP directo. |
| **PaqueteInternacional** | Subclase | `model/paquete_internacional.py` | Hereda de `Paquete` | `+ calcularPrecioFinal(t)` | **Herencia** y polimorfismo: precio en USD $\times$ dólar oficial. |
| **PaqueteCrucero** | Subclase | `model/paquete_crucero.py` | Hereda de `Paquete` | `+ calcularPrecioFinal(t)` | **Herencia** y polimorfismo: precio en USD $\times$ dólar $\times 1.12$. |
| **Reserva** | Clase Transaccional | `model/reserva.py` | `+ fechaViaje: Date`<br>`+ precioPaqueteCLP: Float`<br>`+ tipoCambio: Float`<br>`+ anticipo: Float`<br>`+ estado: String` | `+ agregarDetalle(detalle)`<br>`+ total()`<br>`+ saldoPendiente()`<br>`+ cancelar()`<br>`+ pagarSaldo(monto)`<br>`+ validarConfirmacion()` | **Composición** hacia `DetalleReserva`. Asociación con `Cliente`, `Agente`, `Paquete`, `Proveedor`, `Viajero`. |
| **DetalleReserva** | Clase Componente | `model/detalle_reserva.py` | `+ descripcion: String`<br>`+ cantidad: Integer`<br>`+ precioUnitario: Float` | `+ subtotal()` | Parte de la **composición** con `Reserva`. |
| **TipoItem** | `<<Catalogo>>` | `model/tipo_item.py` | `+ idTipo: Integer`<br>`+ nombreCategoria: String` | `@property`, `@setter` | Catálogo compartido (Vuelo, Hotel, Seguro, Excursión). |
| **Proveedor** | Entidad de Servicio | `model/proveedor.py` | `+ idProveedor: Integer`<br>`+ nombre: String` | `+ agregar_disponibilidad()`<br>`+ tiene_cupos(fecha)`<br>`+ descontar_cupo(fecha)` | **Agregación** con `Disponibilidad` ($1 \rightarrow 0..*$). |
| **Disponibilidad** | Entidad de Control | `model/disponibilidad.py` | `+ fecha: Date`<br>`+ cuposDisponibles: Integer` | `+ tieneCupos(): Boolean`<br>`+ descontarCupo()` | Controla stock de pasajeros por fecha. |
| **Excepciones** | `<<Exception>>` | `model/excepciones.py` | Jerarquía `AgenciaError` | `AnticipoInsuficienteError`<br>`SinCuposError`<br>`APITipoCambioError`<br>`ValidacionError` | Excepciones personalizadas para reglas de negocio. |

---

## 3. RELACIONES UML Y CÓMO ESTÁN RESUELTAS EN EL CÓDIGO

### 3.1 Herencia (Generalización con Flecha de Triángulo Hueco $\triangle$)
* **En el Diagrama:** 
  * `Cliente` $\rightarrow$ `Persona`
  * `Viajero` $\rightarrow$ `Persona`
  * `Trabajador` $\rightarrow$ `Persona`
  * `AgenteViajes` $\rightarrow$ `Trabajador`
  * `Administrador` $\rightarrow$ `Trabajador`
  * `PaqueteNacional`, `PaqueteInternacional`, `PaqueteCrucero` $\rightarrow$ `Paquete`
* **En el Código:** Se implementa con sintaxis nativa de subclase en Python: `class Subclase(Superclase):` invocando siempre a `super().__init__(...)`.
* **Corrección respecto a la ES1:** En la primera entrega se habían modelado los paquetes con rombo de agregación hacia `Paquete`. El profesor corrigió que un paquete nacional *es un* paquete (herencia), no *parte de* un paquete. El código actual implementa herencia pura y limpia.

### 3.2 Composición (Rombo Relleno $\blacklozenge$)
* **En el Diagrama:** `Reserva` $\blacklozenge\longrightarrow$ `DetalleReserva` (Multiplicidad $1 \rightarrow 1..*$).
* **En el Código:** 
  * `Reserva` inicializa en su constructor `self.detalles = []`.
  * Los objetos `DetalleReserva` existen en función de la reserva.
  * En la persistencia (`reserva_dao.py`), la tabla `detalle_reserva` tiene una clave foránea `FOREIGN KEY(reserva_id) REFERENCES reserva(id)`. Si se elimina la reserva, los detalles no tienen sentido por sí solos.

### 3.3 Agregación (Rombo Hueco $\lozenge$)
* **En el Diagrama:** `Proveedor` $\lozenge\longrightarrow$ `Disponibilidad` (Multiplicidad $1 \rightarrow 0..*$).
* **En el Código:**
  * En `Proveedor`: `self.disponibilidades = []`.
  * Método `agregar_disponibilidad(self, disponibilidad: Disponibilidad)`.
  * La disponibilidad existe como una entidad asociada al proveedor, pero el proveedor no se destruye si no tiene disponibilidades cargadas.

### 3.4 Asociación de Catálogo Compartido
* **En el Diagrama:** `DetalleReserva` $\longrightarrow$ `TipoItem` (Multiplicidad $* \rightarrow 1$).
* **En el Código:**
  * En `DetalleReserva`: `self.tipo_item = tipo_item` (valida que sea una instancia de `TipoItem`).
  * Múltiples detalles pueden apuntar a la misma categoría del catálogo (por ejemplo, Vuelo, Hotel o Excursión).

---

## 4. DEFENDIENDO LA COHERENCIA ANTE EL PROFESOR
Si el profesor pregunta: *"¿Cómo sé que su código respeta el diagrama de la Evaluación 1?"*, la respuesta es:

> "Profesor, cada clase de nuestro diagrama existe como un archivo individual en la carpeta `model/`. 
> 
> Mantuvimos la separación clave entre `Cliente` (quien paga) y `Viajero` (quien viaja con su método `validar_pasaporte()`), modelamos la herencia polimórfica en los tres tipos de `Paquete`, respetamos la restricción de que `Administrador` no puede atender clientes mediante `puede_atender_clientes() == False`, y la composición de `Reserva` con sus líneas de `DetalleReserva` se refleja tanto en la estructura de clases como en la clave foránea de la base de datos SQLite."
