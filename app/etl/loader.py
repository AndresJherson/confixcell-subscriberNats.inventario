from pandas import DataFrame


def cargar(df: DataFrame):
    from app.database import engine
    df.to_sql("eventos_procesados", engine, if_exists="append", index=False)
