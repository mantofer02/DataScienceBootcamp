# Tarea 3 Big Data

Este proyecto fue desarrollado por los estudiantes Marco Ferraro y Ricardo Blanco como parte de la Tarea 3 de Big Data.

## Requisitos Previos

- Docker Desktop debe estar instalado en su sistema. Puede descargarlo desde [Docker Hub](https://hub.docker.com/).
- Asegúrese de tener los permisos necesarios para ejecutar Docker.

## Pasos para Configurar y Ejecutar el Proyecto

1. **Ejecutar Docker Desktop:**

   - Inicie Docker Desktop para asegurarse de que el entorno Docker esté listo para su uso.

2. **Configurar PostgreSQL:**

   - Vaya a la carpeta "posgresql" y ejecute el script "run_image" para montar la imagen de PostgreSQL.

3. **Construir el Contenedor Principal:**

   - Ejecute el script "build_image.sh" para construir el contenedor principal del proyecto.

4. **Iniciar el Contenedor Principal:**

   - Ejecute el script "run_image" para iniciar el contenedor principal.

5. **Ejecutar Jupyter Notebook:**

   - Dentro de la terminal bash del contenedor principal, ejecute el script "load_jupyter_notebook" para iniciar el Jupyter Notebook.

6. **Acceder al Jupyter Notebook:**
   - Abra su navegador web y vaya a la dirección [http://localhost:8888](http://localhost:8888).
   - Se le pedirá una contraseña; utilice la que se generó durante la ejecución del script "load_jupyter_notebook".

## Estructura del Proyecto

- **posgresql/:** Contiene scripts relacionados con la configuración de PostgreSQL.
- **build_image.sh:** Script para construir el contenedor principal.
- **run_image:** Script para iniciar el contenedor principal.
- **load_jupyter_notebook:** Script para cargar y ejecutar el Jupyter Notebook.

## Notas Importantes

- Asegúrese de seguir los pasos en el orden correcto para evitar problemas de configuración.
- El Jupyter Notebook estará disponible en el puerto 8888.

---

Este es solo un ejemplo básico. Asegúrate de personalizarlo según las necesidades específicas de tu proyecto y de proporcionar detalles adicionales según sea necesario. ¡Espero que te sea de ayuda!
