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

def obtener_tabla_equipos_estadistica_unica(url_general, stats_vs=False, guardar_csv= False, league='La Liga', season='2024'):
    """
    Descarga y limpia la tabla de estadísticas de equipos desde una URL de FBref.
    Args:
        url_general (str): URL de la tabla de FBref.
        stats_vs (bool): True si la tabla deseada es la segunda (vs) en la página.
        league (str): Nombre de la liga
        season (str): Fecha de la temporada
    Returns:
        pd.DataFrame: Tabla limpia con columnas renombradas.
    """
    tables = pd.read_html(url_general)
    
    if stats_vs:
        df = tables[1]
    else:
        df = tables[0]
    
    # Comprobamos si la cabecera es un MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        # Extraemos la metrica_general desde la URL
        metrica_general = url_general.split('/')[-2]  # Ejemplo: 'shooting', 'passing'
        metrica_general = metrica_general.replace('-', '_').lower()

        # Procesamos las columnas
        columns_data = []
        new_columns = []

        for col in df.columns:
            over_header = col[0].strip().replace(' ', '_').lower()
            data_stat = col[1].strip().replace(' ', '_').lower()

            columns_data.append({
                'data-stat': data_stat,
                'data-over-header': over_header,
                'metrica-general': metrica_general
            })

            new_col_name = f"{data_stat}_{over_header}_{metrica_general}"
            new_columns.append(new_col_name)
        
        df.columns = new_columns

    # Eliminamos filas con nombres de cabecera duplicados o que sean filas vacías
    if any(df.iloc[:,0].str.contains('Squad', case=False, na=False)):
        df = df[~df.iloc[:,0].str.contains('Squad', case=False, na=False)].copy()
    
    # Resetear el índice
    df = df.reset_index(drop=True)

    # Extraer metrica_general de la URL
    metrica_general_match = re.search(r'/(\w+)/La-Liga-Stats', url_general)
    if metrica_general_match:
        metrica_general = metrica_general_match.group(1)
    else:
        metrica_general = 'unknown'

    # Suprimir espacios en el parámetro league
    league_clean = league.lower().replace(' ', '_')

    # Guardar CSV si es necesario
    if guardar_csv:
        df.to_csv(f'./df_equipos_{metrica_general}_{league_clean}_{season}.csv', index=False)

    return df
