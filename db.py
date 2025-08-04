import sqlite3
import click
from flask import current_app, g

def get_db():
    ## Verifica si 'db' no está en 'g'
    if 'db' not in g:
        ## Establece una conexión a la base de datos
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        ## Devuelve filas que se comportan como diccionarios
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    ## Elimina 'db' de 'g' y cierra la conexión si existe
    db = g.pop('db', None)

    if db is not None:
        db.close()
## flaskr/db.py

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    
## flaskr/db.py

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
