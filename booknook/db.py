import psycopg2 as psycopg
import click
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = psycopg.connect(
            current_app.config["DATABASE_URL"]
        )
        g.db.autocommit = True

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        sql = f.read().decode("utf-8")

    with db.cursor() as cur:
        cur.execute(sql)

    db.commit()

    # database seeding
    with db.cursor() as cur:
        cur.execute("""
            INSERT INTO "user" (username, password)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        """, ("test", "test"))

    db.commit()

@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Database initialized.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)