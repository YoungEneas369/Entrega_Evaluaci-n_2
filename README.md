# Agencia de Viajes RutaSur - Evaluación Sumativa N°3
**Asignatura:** Programación Orientada a Objeto Seguro (TI3V21)  
**Docente:** Michael Arjel | **Sección:** 114-2A-F2  
**Integrantes:** Cristopher Figueroa y Elías Reyes  

Esta rama (`evaluacion-3`) contiene la entrega final organizada en dos carpetas principales:

---

## 1. `codigo_corregido/`
Contiene la solución completa del software con todas las correcciones de arquitectura, seguridad y persistencia:
* `model/`: Clases del dominio con encapsulamiento, polimorfismo, validación de pasaporte y excepciones propias.
* `dao/`: Persistencia segura con consultas parametrizadas (`?`) y transacciones atómicas.
* `servicios/`: Consumo de la API del dólar con tiempo de espera (`timeout=5`) y política *Fail-Secure* (`APITipoCambioError`).
* `main.py`: Menú interactivo y captura controlada de excepciones.
* `conectar.py`: Conexión SQLite con integridad referencial (`PRAGMA foreign_keys = ON`).

### Ejecución del Sistema:
```bash
cd codigo_corregido
pip install -r requirements.txt
python main.py
```

---

## 2. `estudio_y_analisis/`
Contiene el material de preparación, análisis y presentación para la defensa oral:
* `1_GUIA_DE_DIALOGOS_EVAL3.md`: Guion oficial de 10 minutos (Cristopher 5 min / Elías 5 min).
* `2_COMO_SE_LEE_EL_CODIGO.md`: Guía de lectura oral técnica línea por línea.
* `3_COORDINACION_CON_EL_DIAGRAMA_UML.md`: Comparativa y mapeo 100% con `Diagrama_RutaSur.drawio`.
* `4_SIMULADOR_PREGUNTAS_TRAMPA_DEFENSA.md`: 12 preguntas trampa de código y seguridad para la defensa individual.
* `5_ESTRUCTURA_PRESENTACION_DIAPOSITIVAS.md`: Esquema de 9 diapositivas sincronizadas con el guion.
* `6_EXPLICACION_MINUCIOSA_DEL_CODIGO.md`: Manual maestro de arquitectura, métodos y atributos.
* `7_GUIA_EVOLUTIVA_PASO_A_PASO.md`: Explicación paso a paso desde cero (constructores, `@property`, `@setter`).
* `8_GUION_PRESENTACION_10_MINUTOS.md`: Guion complementario.
* `9_CAMBIOS_Y_DEFENSA_DEL_PROFESOR.txt`: Justificación del cambio de la API del dólar.
* `10_MEMORIA_TECNICA_AUDITORIA.md`: Memoria técnica de la auditoría inicial.
