# ESTRUCTURA DE DIAPOSITIVAS DE APOYO - PRESENTACIÓN EVALUACIÓN SUMATIVA N°3
## AGENCIA DE VIAJES RUTASUR
**Expositores:** Cristopher Figueroa & Elías Reyes  
**Docente:** Michael Arjel | **Sección:** 114-2A-F2  
**Formato:** Diapositivas limpias de apoyo proyectadas junto con el editor de código.

---

### DIAPOSITIVA 1: PORTADA
* **Título:** Defensa de Código: Sistema Agencia de Viajes RutaSur
* **Subtítulo:** Evaluación Sumativa N°3 — Programación Orientada a Objeto Seguro (TI3V21)
* **Integrantes:** Cristopher Figueroa y Elías Reyes
* **Docente:** Michael Arjel | Sede Puente Alto | Primavera 2026
* **Tiempo:** 0:00 - 0:30
* **Expositor:** Cristopher Figueroa
* **Acción en Editor:** Abrir la raíz del proyecto en VS Code / Antigravity con el explorador de archivos visible.

---

### DIAPOSITIVA 2: ARQUITECTURA EN TRES CAPAS DESACOPLADAS
* **Título:** Arquitectura y Separación de Responsabilidades
* **Contenido Visual:** Diagrama de 3 capas:
  * **Capa 1: `model/` (Dominio Puro POO):** Clases del negocio, herencia, validaciones en setters y excepciones. Cero líneas de SQL.
  * **Capa 2: `dao/` (Persistencia Segura):** Aislamiento de SQLite, consultas parametrizadas `?`, transacciones atómicas.
  * **Capa 3: `servicios/` (Integración Externa):** Consumo de API REST (`mindicador.cl`) con timeout y resiliencia.
  * **Orquestador: `main.py`:** Menú de consola y captura de excepciones.
* **Tiempo:** 0:30 - 1:30
* **Expositor:** Cristopher Figueroa
* **Acción en Editor:** Mostrar `conectar.py` (línea 5: `PRAGMA foreign_keys = ON`).

---

### DIAPOSITIVA 3: REQUISITOS FUNCIONALES EN EL CÓDIGO (PARTE 1)
* **Título:** Polimorfismo y Validación de Entradas
* **Viñetas Clave:**
  * **Jerarquía de Paquetes (`Paquete` ABC):**
    * `PaqueteNacional`: Precio directo en CLP (sin tipo de cambio).
    * `PaqueteInternacional`: Precio base USD * Dólar del día.
    * `PaqueteCrucero`: Precio base USD * Dólar * 1.12 (recargo del 12%).
  * **Validación de Pasaporte (`Viajero`):**
    * `@numero_pasaporte.setter`: Rechaza cadenas vacías y valida formato alfanumérico estricto (6 a 12 caracteres).
* **Tiempo:** 1:30 - 2:30
* **Expositor:** Cristopher Figueroa
* **Acción en Editor:** Proyectar `model/paquete.py` y `model/viajero.py` (líneas 12-20).

---

### DIAPOSITIVA 4: REQUISITOS FUNCIONALES EN EL CÓDIGO (PARTE 2)
* **Título:** Reglas del Negocio y Excepciones Tipadas
* **Viñetas Clave:**
  * **Jerarquía derivada de `AgenciaError`:**
    * `AnticipoInsuficienteError`: Se activa si el anticipo pagado es menor al 50% del total.
    * `SinCuposError`: Se activa si el proveedor no tiene disponibilidad para la fecha de viaje.
    * `ValidacionError`: Se activa si falta pasaporte en paquetes internacionales.
  * **Motor de Validación:** Método centralizado `Reserva.validar_confirmacion()`.
* **Tiempo:** 2:30 - 3:30
* **Expositor:** Cristopher Figueroa
* **Acción en Editor:** Proyectar `model/excepciones.py` y `model/reserva.py` (líneas 66-79).

---

### DIAPOSITIVA 5: RECORRIDO DE UNA OPERACIÓN COMPLETA
* **Título:** Flujo de una Transacción: Crear y Confirmar Reserva
* **Flujo Paso a Paso:**
  1. `main.py` (Opción 7): Entrada de datos y selección de ítems.
  2. `model/reserva.py`: Ensamblado de `DetalleReserva` (Vuelo, Hotel, Seguro, Excursión) y ejecución de `validar_confirmacion()`.
  3. `dao/reserva_dao.py`: Inserción en tabla `reserva`, obtención de `lastrowid`, inserción de ítems hijos en `detalle_reserva` con clave foránea y `commit()` final.
* **Tiempo:** 3:30 - 5:00
* **Expositor:** Cristopher Figueroa *(Entrega de palabra a Elías al minuto 5:00)*
* **Acción en Editor:** Seguir el flujo abriendo `main.py` (líneas 200-245) y `dao/reserva_dao.py` (líneas 34-49).

---

### DIAPOSITIVA 6: RETROALIMENTACIÓN ES2: POLÍTICA FAIL-SECURE
* **Título:** Corrección de la Entrega Anterior: Manejo de la API
* **El Problema Previo:** Retorno fijo de $950 ante fallos de conexión (riesgo de pérdida financiera por descalce cambiario).
* **La Solución Implementada (Fallo Seguro / Fail-Secure):**
  * Lanzamiento de `APITipoCambioError` en `servicios/mindicador.py`.
  * Bloqueo preventivo de cotizaciones y reservas en moneda extranjera si no hay conexión oficial.
  * El programa **no se cae**: emite mensaje claro y vuelve al menú (Prueba P17).
  * **Comportamiento inteligente:** Paquetes Nacionales sí pueden reservarse sin internet (cotizan en CLP).
* **Tiempo:** 5:00 - 7:00
* **Expositor:** Elías Reyes
* **Acción en Editor:** Proyectar `servicios/mindicador.py` y `main.py` (captura de `APITipoCambioError`).

---

### DIAPOSITIVA 7: MECANISMOS DE SEGURIDAD EN PERSISTENCIA
* **Título:** Seguridad de Datos: Prevención de Inyección SQL
* **Comparativa Visual:**
  * ❌ **Vulnerable (Concatenación / f-strings):**
    `execute(f"... WHERE id = '{id}'")` $\rightarrow$ Riesgo de ruptura por comillas o ataque con `' OR '1'='1`.
  * ✅ **Seguro (Parámetros posicionales `?`):**
    `execute("... WHERE id = ?", (id,))` $\rightarrow$ SQLite sanitiza los valores como datos literales.
* **Integridad Referencial:** Forzada con `PRAGMA foreign_keys = ON` para evitar huérfanos.
* **Tiempo:** 7:00 - 8:30
* **Expositor:** Elías Reyes
* **Acción en Editor:** Proyectar `dao/paquete_dao.py` (líneas 17-20 y 53-55).

---

### DIAPOSITIVA 8: USO CRÍTICO DE INTELIGENCIA ARTIFICIAL
* **Título:** Inteligencia Artificial con Criterio Técnico
* **Sugerencia Adoptada:**
  * Acoplamiento del objeto `Viajero` en `Reserva(viajero=v)` para permitir la validación de pasaporte antes de evaluar cupos y anticipos.
* **Sugerencia Descartada y Modificada:**
  * La IA sugirió inyectar un dólar estático de $950 para mantener disponibilidad. Se descartó por el riesgo de pérdida económica, reemplazándola por la excepción personalizada `APITipoCambioError` (*Fail-Secure*).
* **Tiempo:** 8:30 - 9:30
* **Expositor:** Elías Reyes
* **Acción en Editor:** Proyectar `README.md` (Sección 4).

---

### DIAPOSITIVA 9: CONCLUSIONES Y PREGUNTAS
* **Título:** Conclusiones y Defensa Oral
* **Puntos Fuertes de RutaSur:**
  * Arquitectura desacoplada en 3 capas.
  * Modelo robusto con herencia, polimorfismo y encapsulamiento.
  * Persistencia 100% parametrizada y transacciones atómicas.
  * Resiliencia y Fallo Seguro frente a fallos externos.
* **Tiempo:** 9:30 - 10:00
* **Expositor:** Elías Reyes
* **Acción en Pantalla:** Dejar abierto el editor listo para las preguntas individuales del docente.
