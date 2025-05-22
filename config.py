import os

def get_env_NATS():
    NATS_HOST = os.getenv("NATS_HOST")
    if NATS_HOST is None:
        raise Exception("NATS_HOST no propocionado")
    return NATS_HOST

DB_ORIGEN_HOST = os.getenv("DB_ORIGEN_HOST")
DB_ORIGEN_NAME = os.getenv("DB_ORIGEN_NAME")
DB_ORIGEN_USER = os.getenv("DB_ORIGEN_USER")
DB_ORIGEN_PASSWORD = os.getenv("DB_ORIGEN_PASSWORD")

DB_DESTINO_HOST = os.getenv("DB_DESTINO_HOST")
DB_DESTINO_NAME = os.getenv("DB_DESTINO_NAME")
DB_DESTINO_USER = os.getenv("DB_DESTINO_USER")
DB_DESTINO_PASSWORD = os.getenv("DB_DESTINO_PASSWORD")