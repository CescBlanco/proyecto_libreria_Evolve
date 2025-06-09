import requests
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup, Comment

def get_players_data(url, metrica_general='Standard Stats'):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

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
        return None

    # 1️⃣ Procesar el encabezado de la tabla
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

    # 2️⃣ Extraer las filas de jugadores
    data_rows = []
    for row in player_table.find('tbody').find_all('tr'):
        row_data = []
        for cell in row.find_all(['th', 'td']):
            cell_text = cell.get_text(strip=True)
            row_data.append(cell_text)
        if row_data:  # Evitar filas vacías
            data_rows.append(row_data)

    # 3️⃣ Crear el DataFrame de jugadores
    df_players = pd.DataFrame(data_rows, columns=column_names)

    return df_players

def limpieza_df_players(df, url):
    # Filtrar filas donde la columna de ranking sea diferente de 'Rk'
    ranker_cols = [col for col in df.columns if 'ranker' in col]
    if ranker_cols:
        ranker_col = ranker_cols[0]
        df = df[df[ranker_col] != 'Rk'].reset_index(drop=True)
        df.drop(columns=[ranker_col], inplace=True, errors='ignore')

    # Eliminar columna de partidos si existe
    matches_cols = [col for col in df.columns if 'matches' in col]
    if matches_cols:
        df.drop(columns=matches_cols, inplace=True, errors='ignore')

    # Procesar la columna de nacionalidad si existe
    nationality_cols = [col for col in df.columns if 'nationality' in col]
    if nationality_cols:
        col_name = nationality_cols[0]
        df[col_name] = df[col_name].astype(str).str.extract(r'([A-Z]+)$')

    # Extraer la parte de la competición desde la URL
    competition_name_match = re.search(r'/([^/]+)-Stats(?:/|$)', url)
    if competition_name_match:
        competition_name = competition_name_match.group(1).replace('-', ' ')
    else:
        competition_name = 'Desconocida'

    # Si la columna competition no existe, crearla
    competition_cols = [col for col in df.columns if 'competition' in col]
    if not competition_cols:
        df['competition'] = competition_name

    # Reemplazar celdas vacías por NaN y luego por 0
    df.replace('', np.nan, inplace=True)
    df.fillna(0, inplace=True)

    return df

def creacion_df_jugadores_estadistica_unica(url: str, guardar_csv=False, stat='Standard Stat', league='La Liga', season='2024'):
    # Obtener datos de la URL
    df_sucio = get_players_data(url)
    if df_sucio is None:
        print("No se pudo obtener la tabla de jugadores.")
        return None

    # Limpiar los datos
    df_limpio = limpieza_df_players(df_sucio, url)

    # Guardar CSV si se solicita
    if guardar_csv:
        filename = f'./df_players_{stat}_{league}_{season}.csv'
        filename_lower=filename.lower()

        df_limpio.to_csv(filename_lower, index=False)
        print(f'Datos guardados en: {filename_lower}')

    return df_limpio
