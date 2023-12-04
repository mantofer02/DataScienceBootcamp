# Tarea 1 Big Data - Resumen y Guía Rápida

## Estudiante: Marco Ferraro

### Resumen de la Tarea

La tarea consiste en desarrollar un programa de procesamiento de datos relacionados con ciclistas, actividades y rutas. La implementación se divide en varios archivos, donde `main.py` inicia el programa, `controller.py` gestiona el flujo y `functions.py` contiene funciones de procesamiento. Se proporcionan scripts en la carpeta `scripts` para construir la imagen de Docker, ejecutar el programa y realizar pruebas unitarias. Además, la carpeta `assets` contiene documentos relacionados con la tarea.

### Guía Rápida

1. **Configuración del Ambiente:**

   - Ejecute `build_image.sh` para construir la imagen de Docker.
     ```bash
     ./scripts/build_image.sh
     ```

2. **Inicio del Contenedor:**

   - Use `run_image.sh` para iniciar el contenedor.
     ```bash
     ./scripts/run_image.sh
     ```

3. **Ejecución del Programa:**

   - Dentro del contenedor, ejecute `run_program.sh` para ejecutar el programa.
     ```bash
     ./scripts/run_program.sh
     ```

4. **Visualización de Resultados:**

   - Explore la carpeta `results` para acceder a archivos CSV con resultados detallados.
     ```bash
     cd results
     cat nombre_archivo.csv
     ```

5. **Pruebas Unitarias:**
   - Ejecute pruebas unitarias con `pytest`.
     ```bash
     pytest test_functions.py -v
     ```

Para detalles completos y configuración adicional, consulte el documento [Tarea_1_MarcoFerraro](Tarea_1_MarcoFerraro.pdf).
