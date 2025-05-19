from ast import Dict
import pandas as pd

def extraer(payload: Dict) -> pd.DataFrame:
    return pd.DataFrame([payload])
