from pandas import DataFrame


def transformar(df: DataFrame):
    df['procesado'] = True  # Ejemplo de transformación
    return df
