import requests
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup, Comment


def obtener_tabla_liga_principal(url_general):
    """
    Extrae y limpia la tabla clasificatoria de una liga desde FBref.

    Args:
        url_general (str): URL de la página de clasificación de la liga en FBref.

    Returns:
        pd.DataFrame: DataFrame limpio con la tabla clasificatoria, 
                      renombrando la columna 'RL' a 'Posicion' y eliminando la columna 'Notas'.
    """
    tabla = pd.read_html(url_general)
    tabla_sucia = tabla[0]
    tabla_sucia = tabla_sucia.rename(columns={'RL': 'Posicion'})
    tabla_limpia = tabla_sucia.drop(columns=['Notas'])
    return tabla_limpia

#-------------------------------------------------------------------------------------------------------------