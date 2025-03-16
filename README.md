# Chatbot con IA Integrada

Este proyecto es un **chatbot impulsado por IA** desarrollado con **Django**, **PostgreSQL** y **WebSockets**. En el frontend, utiliza **HTML, CSS y JavaScript** para la interfaz de usuario.

## Características
- **Arquitectura limpia (Clean Architecture)** aplicada en el backend.
- **Base de datos PostgreSQL** con migraciones gestionadas por Django ORM.
- **Gráficos de ventas** generados dinámicamente.
- **Listado de productos** desde la base de datos.
- **Recomendaciones basadas en IA** según los productos más vendidos.
- **IA integrada con DeepSeek** para mejorar las respuestas y sugerencias.

## Requisitos de instalación

Para correr el backend, instala las siguientes dependencias:

```sh
pip install psycopg2-binary
pip install psycopg
pip install channels
pip install daphne
pip install python-dotenv
pip install matplotlib
pip3 install openai
```

## Configuración de la base de datos

Se debe montar la base de datos utilizando el archivo de configuración correspondiente y aplicar las migraciones de Django:

```sh
python manage.py makemigrations
python manage.py migrate
```

## Ejecución del Servidor

Para correr el servidor, usa el siguiente comando:

```sh
python manage.py runserver
```

## Contacto
Si tienes dudas o sugerencias, no dudes en contribuir o reportar issues en el repositorio.

