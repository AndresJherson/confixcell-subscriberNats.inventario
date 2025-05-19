from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlmodel import Session
from config import DB_DESTINO_HOST, DB_DESTINO_NAME, DB_DESTINO_PASSWORD, DB_DESTINO_USER, DB_ORIGEN_HOST, DB_ORIGEN_NAME, DB_ORIGEN_PASSWORD, DB_ORIGEN_USER

_connection_origen = "mysql+pyodbc:///?odbc_connect=%s" % quote_plus(
    "DRIVER=MySQL ODBC 9.1 Unicode Driver;"
    f"SERVER={DB_ORIGEN_HOST};"
    f"DATABASE={DB_ORIGEN_NAME};"
    f"UID={DB_ORIGEN_USER};"
    f"PWD={DB_ORIGEN_PASSWORD};"
)

engine_origen = create_engine(_connection_origen)

_connection_destino = "mysql+pyodbc:///?odbc_connect=%s" % quote_plus(
    "DRIVER=MySQL ODBC 9.1 Unicode Driver;"
    f"SERVER={DB_DESTINO_HOST};"
    f"DATABASE={DB_DESTINO_NAME};"
    f"UID={DB_DESTINO_USER};"
    f"PWD={DB_DESTINO_PASSWORD};"
)

engine_destino = create_engine(_connection_destino)

def get_session_destino():
    with Session(engine_destino) as session:
        yield session