import requests
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup, Comment



#--------------------------------------------------------------------------------------


def get_players_data(url, metrica_general=None):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 1️⃣ Si no pasas metrica_general, lo extraemos de la URL
    if metrica_general is None:
        stat_match = re.search(r'/(\w+)/La-Liga-Stats', url)
        if stat_match:
            metrica_general = stat_match.group(1).replace('-', ' ').title()
        else:
            metrica_general = 'Standard Stats'  # Valor por defecto

    metrica_general_clean = metrica_general.replace(' ', '_')

    # Buscar tablas ocultas (comentadas)
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    player_table = None

    for comment in comments:
        comment_soup = BeautifulSoup(comment, 'html.parser')
        tables = comment_soup.find_all('table')
        for table in tables:
            if table.find('td', {'data-stat': 'player'}):
                player_table = table
                break
        if player_table:
            break

    if not player_table:
        print("No se encontró la tabla de jugadores.")
        return None, None

    # -----------------------
    # 1️⃣ Procesar el encabezado de la tabla
    # -----------------------
    header_rows = player_table.find('thead').find_all('tr')
    last_header_row = header_rows[-1]

    columns_data = []
    column_names = []

    for th in last_header_row.find_all('th'):
        data_stat = th.get('data-stat')
        data_over_header = th.get('data-over-header') or 'General'
        data_over_header = data_over_header.replace(' ', '_')
        metrica_general_clean = metrica_general.replace(' ', '_')
        column_name = f"{data_stat}_{data_over_header}_{metrica_general_clean}"
        column_names.append(column_name)

        columns_data.append({
            'data-stat': data_stat,
            'data-over-header': data_over_header,
            'metrica-general': metrica_general
        })

    df_columns = pd.DataFrame(columns_data)

    # -----------------------
    # 2️⃣ Extraer las filas de jugadores
    # -----------------------
    data_rows = []
    for row in player_table.find('tbody').find_all('tr'):
        row_data = []
        for cell in row.find_all(['th', 'td']):
            cell_text = cell.get_text(strip=True)
            row_data.append(cell_text)
        if row_data:  # Evitar filas vacías
            data_rows.append(row_data)

    # -----------------------
    # 3️⃣ Crear el DataFrame de jugadores
    # -----------------------
    df_players = pd.DataFrame(data_rows, columns=column_names)

    return  df_players


def limpieza_df_players(df, url):
    """
    Limpia y procesa un DataFrame que contiene datos de jugadores extraídos de FBref.
    Esta función realiza las siguientes operaciones:
    1. Elimina las filas donde la columna de ranking (que contiene 'ranker' en su nombre) tiene el valor 'Rk', y elimina la columna de ranking.
    2. Elimina cualquier columna relacionada con partidos (columnas que contienen 'matches' en su nombre).
    3. Procesa la columna de nacionalidad (si existe) extrayendo el código de país (letras mayúsculas al final de la cadena).
    4. Extrae el nombre de la competición de la URL proporcionada y lo añade como una nueva columna 'competition' si aún no existe.
    5. Reemplaza las celdas vacías por NaN y luego rellena todos los valores NaN con 0.
    Args:
        df (pd.DataFrame): El DataFrame con los datos de jugadores a limpiar.
        url (str): La URL de la que se extrajeron los datos, utilizada para extraer el nombre de la competición.
    Returns:
        pd.DataFrame: El DataFrame limpio y procesado.
    """
    stat_match = re.search(r'/([^/]+)/La-Liga-Stats', url)
    if stat_match:
        metrica_general = stat_match.group(1).replace('-', ' ').title()
    else:
        metrica_general = 'Standard Stats'  # Valor por defecto si no encuentra nada

    metrica_general_clean = metrica_general.replace(' ', '_')

     
    # Filtrar dinámicamente las columnas a eliminar
    columns_to_drop = [
        col for col in df.columns
        if (col.startswith("ranker_") or col.startswith("matches_"))
        and col.endswith(f"_{metrica_general_clean}")
    ]

    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)
    
    # Eliminar filas con encabezados repetidos
    player_cols = [col for col in df.columns if col.lower().startswith('player')]
    if player_cols:
        player_col = player_cols[0]
        # Filtrar filas donde esa columna contenga 'Player', 'Team' o 'Totals'
        df = df[~df[player_col].isin(['Player', 'Team', 'Totals'])]

    # Procesar la columna de nacionalidad si existe
    nationality_col = [col for col in df.columns if 'nationality' in col]
    if nationality_col:
        col_name = nationality_col[0]
        df[col_name] = df[col_name].astype(str).str.extract(r'([A-Z]+)$')

    # Extraer la parte de la competición
    competition_name_match = re.search(r'/([^/]+)-Stats(?:/|$)', url)
    if competition_name_match:
        competition_name = competition_name_match.group(1).replace('-', ' ')
    else:
        competition_name = 'Desconocida'

    competition_col = [col for col in df.columns if 'competition' in col]
    if not competition_col:
        df['competition'] = competition_name
    # Reemplazar celdas vacías por NaN y luego NaN por 0
    df.replace('', np.nan, inplace=True)
    df.fillna(0, inplace=True)
    df.reset_index(drop=True,inplace=True)

    
    return df

def creacion_df_jugadores_estadistica_unica(url: str, guardar_csv=False, league='La Liga', season='2024',):
    # Obtener datos de la tabla
    df_sucio = get_players_data(url)
    
    # Limpiar los datos
    df_limpio = limpieza_df_players(df_sucio,  url=url)  # Asegúrate de pasar la URL a la función de limpieza

    # Extraer metrica_general de la URL
    metrica_general_match = re.search(r'/(\w+)/La-Liga-Stats', url)
    if metrica_general_match:
        metrica_general = metrica_general_match.group(1)
    else:
        metrica_general = 'unknown'

    # Suprimir espacios en el parámetro league
    league_clean = league.lower().replace(' ', '_')


    # Guardar CSV si es necesario
    if guardar_csv:
        df_limpio.to_csv(f'./df_players_{metrica_general}_{league_clean}_{season}.csv', index=False)
    
    return df_limpio

#------------------------------------------------------------------------------------------------------------

def obtener_jugadores_similares(url_jugador):
    """
    Extrae y limpia la tabla de jugadores similares del informe de reclutamiento de un jugador en FBref.

    Args:
        url_jugador (str): URL del informe de reclutamiento del jugador en FBref.

    Returns:
        pd.DataFrame: DataFrame limpio con los jugadores similares, sin columnas irrelevantes y con la nacionalidad normalizada.
    """
    #Lee todas las tablas HTML de la página del informe de reclutamiento
    tablas = pd.read_html(url_jugador)
    
    #Selecciona la segunda tabla (índice 1), que suele contener los jugadores similares
    tabla_sucia = tablas[1]
    
    #Elimina las columnas 'RL' y 'Comparar', que no aportan información relevante
    tabla_limpia = tabla_sucia.drop(columns=['RL', 'Comparar'])
    
    #Normaliza la columna de nacionalidad: extrae solo el código de país en mayúsculas
    nationality_col = [col for col in tabla_limpia.columns if 'País' in col]
    if nationality_col:
        col_name = nationality_col[0]
        tabla_limpia[col_name] = tabla_limpia[col_name].astype(str).str.extract(r'([A-Z]+)$')
    
    #Devuelve el DataFrame limpio
    return tabla_limpia

#------------------------------------------------------------------------------------------------------------

def obtener_tabla_datos_jugador_por90_percentiles(url_jugador):
    """
    Extrae y limpia la tabla de percentiles 'Por 90' de un informe de reclutamiento de jugador en FBref.

    Args:
        url_jugador (str): URL del informe de reclutamiento del jugador en FBref.

    Returns:
        pd.DataFrame: DataFrame limpio con los datos de percentiles 'Por 90' del jugador.
    """


    #Lee todas las tablas HTML de la página del informe de reclutamiento

    tablas = pd.read_html(url_jugador)

    #Selecciona la tercera tabla (índice 2), que suele contener los percentiles 'Por 90'

    tabla_sucia = tablas[2]

    #Elimina el primer nivel del MultiIndex de columnas si existe

    tabla_sucia.columns = tabla_sucia.columns.droplevel(0)

    #Elimina filas completamente vacías

    tabla_sucia = tabla_sucia.dropna()

    #Filtra filas para quedarse solo con las que tienen valores numéricos en 'Por 90'

    tabla_sucia = tabla_sucia[~tabla_sucia['Por 90'].str.contains(r'[a-zA-Z]', na=False)] 

    #Limpia la columna 'Por 90': elimina el símbolo '%' y convierte a numérico

    tabla_sucia['Por 90'] = tabla_sucia['Por 90'].str.replace('%', '', regex=True)
    tabla_sucia['Por 90'] = pd.to_numeric(tabla_sucia['Por 90'], errors='coerce')

    #Convierte la columna 'Percentil' a tipo numérico

    tabla_sucia['Percentil'] = pd.to_numeric(tabla_sucia['Percentil'], errors='coerce')

    #Reinicia el índice del DataFrame limpio

    tabla_limpia = tabla_sucia.reset_index(drop=True)

    #Devuelve el DataFrame limpio
    
    return tabla_limpia 

#------------------------------------------------------------------------------------------------------------