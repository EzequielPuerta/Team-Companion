# Team Companion

  * Python 3.8
  * Docker 19.03.12 (todos los contenedores usan Linux)
## Ejecución

1. Entrar al directorio `source`
> `cd source`

2. Crear un archivo `.env` con los parámetros deseados
> ```cp .env.example .env```
> ```nano .env```

3. Ejecutar algún archivo `.yml`, por ejemplo:

    I. el default (recomendado para la primera vez)
    > `docker-compose up --build`
    
    que es igual a:
    > `docker-compose -f docker-compose.yml up --build`

    Notar que el *flag* `--build` nos permite construir la imagen con los últimos cambios realizados.

    II. el de testing
    > `docker-compose -f docker-compose-testing.yml up --build`

    III. el de debug
    > `docker-compose -f docker-compose-debug.yml up --build`

4. Si se desea ejecutar el aplicativo en segundo plano (*background*), se debe agregar el *flag* `-d` a cualquiera de los comandos antes mencionados.

5. La primera vez, será necesario crear la base de datos con todas sus tablas. Para ello hay que ejecutar lo siguiente:

    > `docker exec -it team_companion /bin/bash`
    > `python`
    > `from team_companion.app import create_app`
    > `from team_companion.app.extensions import db`
    > `rootsystem = create_app()`
    > `db.app = rootsystem`
    > `db.create_all()`
    > `exit()`
    > `exit`

6. Acceder (por default) al siguiente [link](http://10.40.17.3:5000/)

7. En el primer ingreso, el usuario (y su contraseña) que se ingrese, se registrará como administrador.

## Notas

1. Para completar el USER_ID y GROUP_ID se puede usar el comando (el primer valor será el ID del usuario actual, el segundo es el ID del grupo al que pertenece)

> `id -u && id -g`

2. Generar Flask `SECRET_KEY` y pegar en la variable `SECRET_KEY` del archivo `.env`

> `python3 -c "import os; print(os.urandom(40).hex())"`

3. Correr scripts de migración para PostgreSQL con la app ejecutando (con `docker-compose up` por ejemplo:)

> `docker cp db-setup.py team_companion_team_companion_1:/opt/tyke/team_companion_kernel/ && docker exec -it team_companion_team_companion_1 bash -c "python -m db-setup"`

> **Importante:** Al correr los tests, la primera vez puede fallar porque el contenedor principal no encuentra la base de datos para test. Intentarlo una segunda vez.

## Documentación

En lo posible, se deberan documentar las decisiones técnicas en formato ADR (Architectural Decision Records) dentro de la carpeta `docs`, con el formato correspondiente y con nombres siguiendo el patron `####-nombre-propiedad-documentada-adr.md`.