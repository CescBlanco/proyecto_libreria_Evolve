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


#-----------------------------------------------------------------------------------------------------------------------------

def obtener_tabla_tiros_partido(url_partido, tiros_por_equipo=False):
    """
    Extrae las tablas de tiros de un partido de fútbol desde la URL de FBref.

    Esta función lee las tablas HTML de la página especificada y devuelve:
    - la tabla principal de tiros combinada (para ambos equipos), y
    - opcionalmente, las tablas de tiros individuales para el equipo local y visitante.

    Args:
        url_partido (str): URL de la página del partido en FBref.
        tiros_por_equipo (bool, optional): 
            Si True, también devuelve las tablas de tiros individuales por equipo (local y visitante).
            Por defecto es False.

    Returns:
        tuple:
            - pd.DataFrame: Tabla de tiros general del partido (ambos equipos).
            - pd.DataFrame or None: Tabla de tiros del equipo local (si se solicita).
            - pd.DataFrame or None: Tabla de tiros del equipo visitante (si se solicita).

    Notes:
        - La tabla general de tiros se asume que está en el índice 17 del listado de tablas HTML.
        - Las tablas individuales (local y visitante) están en los índices 18 y 19, respectivamente.
        - Esta función elimina el nivel superior del índice de columnas para facilitar el análisis posterior.
    """
    # Leer todas las tablas de la URL
    tablas = pd.read_html(url_partido)
    
    # Extraer tabla principal de tiros (ambos equipos)
    tabla_sucia = tablas[17]
    tabla_sucia.columns = tabla_sucia.columns.droplevel(0)
    tabla_tiros_completo = tabla_sucia.copy()

    # Inicializar tablas individuales como None (en caso de no solicitarlas)
    tabla_tiros_local = None
    tabla_tiros_visitante = None

    # Extraer tablas individuales si se solicita
    if tiros_por_equipo:
        tabla_local = tablas[18]
        tabla_local.columns = tabla_local.columns.droplevel(0)
        tabla_tiros_local = tabla_local.copy()

        tabla_visitante = tablas[19]
        tabla_visitante.columns = tabla_visitante.columns.droplevel(0)
        tabla_tiros_visitante = tabla_visitante.copy()
    
    return tabla_tiros_completo, tabla_tiros_local, tabla_tiros_visitante

#-----------------------------------------------------------------------------------------------------------------------
def limpiar_df_estadisticas_partido(df):
    """
    Limpia y normaliza un DataFrame de estadísticas de partido.

    - Busca y normaliza la columna de nacionalidad, extrayendo solo el código de país en mayúsculas si existe.
    - Busca y normaliza la columna de edad, extrayendo solo la parte numérica antes del guion si existe.
    - Devuelve el DataFrame limpio.

    Args:
        df (pd.DataFrame): DataFrame original con estadísticas de partido.

    Returns:
        pd.DataFrame: DataFrame limpio y normalizado.
    """
    # Convertir columnas a minúsculas para búsqueda flexible
    cols_lower = [col.lower() for col in df.columns]
    
    # Buscar columna de nacionalidad (ignorando mayúsculas/minúsculas)
    nationality_col = [df.columns[i] for i, col in enumerate(cols_lower) if 'nation' in col]
    if nationality_col:
        col_name = nationality_col[0]
        df[col_name] = df[col_name].astype(str).str.extract(r'([A-Z]+)$')
    
    # Buscar columna de edad (ignorando mayúsculas/minúsculas)
    edad_col = [df.columns[i] for i, col in enumerate(cols_lower) if 'age' in col]
    if edad_col:
        col_name = edad_col[0]
        df[col_name] = df[col_name].astype(str).str.split('-').str[0]

    return df

def bajada_nivel_porteros(df):
    """
    Normaliza los nombres de las columnas de un DataFrame de porteros, eliminando niveles de MultiIndex.

    - Si las columnas del DataFrame son un MultiIndex, combina los niveles en un solo nombre de columna
      con el formato 'nombre_columna_nivel2_nombre_columna_nivel1', todo en minúsculas y con espacios reemplazados por guiones bajos.
    - Si las columnas no son MultiIndex, simplemente normaliza los nombres a minúsculas y reemplaza espacios por guiones bajos.

    Args:
        df (pd.DataFrame): DataFrame con estadísticas de porteros, posiblemente con columnas MultiIndex.

    Returns:
        pd.DataFrame: DataFrame con nombres de columnas normalizados a un solo nivel.
    """
    if isinstance(df.columns, pd.MultiIndex):
        new_columns = []
        for col in df.columns:
            over_header = str(col[0]).strip().replace(' ', '_').lower()
            data_stat = str(col[1]).strip().replace(' ', '_').lower()
            new_col_name = f"{data_stat}_{over_header}"
            new_columns.append(new_col_name)
        df.columns = new_columns
    else:
        df.columns = [str(col).strip().replace(' ', '_').lower() for col in df.columns]
    return df

def obtener_tabla_estadisticas_principales_partido(url_partido, keepers=False):
    """
    Extrae y limpia las tablas principales de estadísticas de un partido de fútbol desde FBref.

    Args:
        url_partido (str): URL de la página del partido en FBref.
        keepers (bool, opcional): Si es True, también extrae y limpia las tablas de estadísticas de porteros
                                  para ambos equipos. Por defecto es False.

    Returns:
        tuple:
            - estadisticas_local (pd.DataFrame): Estadísticas principales del equipo local.
            - estadisticas_visitante (pd.DataFrame): Estadísticas principales del equipo visitante.
            - keeper_local (pd.DataFrame or None): Estadísticas del portero local (si keepers=True, si no None).
            - kepper_visitante (pd.DataFrame or None): Estadísticas del portero visitante (si keepers=True, si no None).

    Notas:
        - Utiliza índices fijos de las tablas extraídas con pd.read_html, por lo que pueden variar si FBref cambia el orden.
        - Aplica limpieza y normalización a las tablas usando funciones auxiliares.
    """
    keeper_local = None
    kepper_visitante = None

    tablas = pd.read_html(url_partido)

    # Obtener y limpiar estadísticas del equipo local
    estadisticas_local = tablas[3]
    estadisticas_local.columns = estadisticas_local.columns.droplevel(0)
    estadisticas_local = estadisticas_local.iloc[:-1, :]
    estadisticas_local = limpiar_df_estadisticas_partido(estadisticas_local)

    # Obtener y limpiar estadísticas del equipo visitante
    estadisticas_visitante = tablas[10]
    estadisticas_visitante.columns = estadisticas_visitante.columns.droplevel(0)
    estadisticas_visitante = estadisticas_visitante.iloc[:-1, :]
    estadisticas_visitante = limpiar_df_estadisticas_partido(estadisticas_visitante)

    if keepers:
        kepperlocal = tablas[9]
        kepperlocal_bajadanivel = bajada_nivel_porteros(kepperlocal)
        keeper_local = limpiar_df_estadisticas_partido(kepperlocal_bajadanivel)

        keppervisitante = tablas[16]
        kepper_visitante_bajadanivel = bajada_nivel_porteros(keppervisitante)
        kepper_visitante = limpiar_df_estadisticas_partido(kepper_visitante_bajadanivel)

    return estadisticas_local, estadisticas_visitante, keeper_local, kepper_visitante