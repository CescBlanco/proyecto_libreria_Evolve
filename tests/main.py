from fbref_scraper_cesc.league_manager import LeagueManager
from fbref_scraper_cesc.player_data import *
from fbref_scraper_cesc.team_data import * 

#Llamada a la clase LeagueManager para generar URLs de jugadores.

manager = LeagueManager()

#Generación de todas las urls posibles para extraer la infomarcion de los jugadores y equipos.

player_urls = manager.generate_player_urls()
teams_urls= manager.generate_team_urls()

#----------------------------------------------------------------------------------------
#Ejemplo de creacíon de un dataframe de una estadisticas unica de la liga seleccionada para todos los jugadores.

#PASOS PARA PODER ELEGIR LA URL DESEADA:

# 1: Elegir liga dispoible en player_urls: ['La Liga', 'Premier League', 'Serie A', 'League 1', 'Bundesliga']
liga_jugadores = 'La Liga'

# 2: Elegir la temporada disponible en player_urls: ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021']
temporada_jugadores = '2024-2025'

# 3: Elegir una estadísticas disponibles: ['Standard Stats', 'Goalkeeping', 'Advanced Goalkeeping', 'Shooting', 'Passing','Pass Types',
# 'Goal and Shot Creation', 'Defensive Actions', 'Possession', 'Playing Time', 'Miscellaneous Stats']
tipo_estadistica_jugadores =  'Standard Stats'

# 4: Creacion de la url para la funcion:
url_player = player_urls[liga_jugadores][temporada_jugadores][tipo_estadistica_jugadores]
print("URL:", url_player)
print('------')

#PRUEBA DE USO:
print("\n🔹 Probando función para crear el dataframe de los jugadores de una liga con un tipo de estadística de la temporada.")
print(' ')
df_estadistica_unica =creacion_df_jugadores_estadistica_unica(url_player, guardar_csv=True, league=liga_jugadores, season=temporada_jugadores)
print(df_estadistica_unica.sample(3))
print('------')
print(' ')

#--------------------------------------------------------------------------------------------------------------- 

#Ejemplo de creación de un dataframe de todas las estadisticas de los jugadores de campo para una liga y una temporada concreta.

#PASOS PARA PODER ELEGIR EL DATAFRAME DESEADO:

# 1: Elegir liga dispoible en player_urls: ['La Liga', 'Premier League', 'Serie A', 'League 1', 'Bundesliga']
liga_todos_jugadores = 'Ligue 1'
# 2: Elegir la temporada disponible en player_urls: ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021']
temporada_todos_jugadores= '2024-2025'

#PRUEBA DE USO
print("\n🔹 Probando función para crear el dataframe completo con todas las estadísticas de los jugadores de campo para una liga y temporada.")
print(' ')
df_ligue1_2024 = creacion_df_players_torneo_fbref( league=liga_todos_jugadores,  season=temporada_todos_jugadores,
      stat_list=["Standard Stats", "Shooting", "Passing", "Pass Types","Goal and Shot Creation", "Defensive Actions", 
                     "Possession", "Miscellaneous Stats"], player_urls=player_urls, guardar_csv=True, guardar_csv_individuales=False)
print(df_ligue1_2024.sample(3))
print('------')
print(' ')

#--------------------------------------------------------------------------------------------------------------- 

#Ejemplo de creación de un dataframe de todas las estadisticas de los porteros para una liga y una temporada concreta.

#PASOS PARA PODER ELEGIR EL DATAFRAME DESEADO:

# 1: Elegir liga dispoible en player_urls: ['La Liga', 'Premier League', 'Serie A', 'League 1', 'Bundesliga']
liga_todos_porteros = 'Ligue 1'
# 2: Elegir la temporada disponible en player_urls: ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021']
temporada_todos_porteros= '2024-2025'

#PRUEBA DE USO
print("\n🔹 Probando función para crear el dataframe completo con todas las estadísticas de los porteros para una liga y temporada.")
print(' ')
df_porteros_premier_2024= creacion_df_porteros_torneo_fbref(league=liga_todos_porteros,  season=temporada_todos_porteros,
      stat_list=['Goalkeeping', 'Advanced Goalkeeping'], player_urls=player_urls, guardar_csv=True, guardar_csv_individuales=False)
print(df_porteros_premier_2024.sample(3))
print('------')
print(' ')

#--------------------------------------------------------------------------------------------------------------- 

#Ejemplo de creación de un dataframe de una estadistica unica de la liga seleccionada para todos los equipos, 
#el primero a favor y el segundo en contra (aplicando el stats_vs)

#PASOS PARA PODER ELEGIR LA URL DESEADA:

# 1: Elegir liga dispoible en player_urls: ['La Liga', 'Premier League', 'Serie A', 'League 1', 'Bundesliga']
liga_equipos = 'La Liga'

# 2: Elegir la temporada disponible en player_urls: ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021']
temporada_equipos= '2024-2025'

# 3: Elegir una estadísticas disponibles:  ['Standard Stats', 'Goalkeeping', 'Advanced Goalkeeping', 'Shooting', 'Passing','Pass Types',
# 'Goal and Shot Creation', 'Defensive Actions', 'Possession', 'Playing Time', 'Miscellaneous Stats']
tipo_estadistica_equipos =  'Miscellaneous Stats'

# 4: Creacion de la url para la funcion:
url_stat_equipo = player_urls[liga_equipos][temporada_equipos][tipo_estadistica_equipos]
print("URL:", url_stat_equipo)
print('------')


#PRUEBAS DE USOS
print("\n🔹 Probando función para crear el dataframe de los equipos de una liga con un tipo de estadística de la temporada.")
print(' ')
df_equipo_stat = obtener_tabla_equipos_estadistica_unica(url_stat_equipo, stats_vs=False, guardar_csv= True, league='La Liga', season='2024')
print(df_equipo_stat.sample(3))
print('------')
print(' ')

print("\n🔹 Probando función para crear el dataframe de los equipos_vs de una liga con un tipo de estadística de la temporada.")
print(' ')
df_vs_equipo_stat = obtener_tabla_equipos_estadistica_unica(url_stat_equipo, stats_vs=True, guardar_csv= True, league='La Liga', season='2024')
print(df_vs_equipo_stat.sample(3))
print('------')
print(' ')

#--------------------------------------------------------------------------------------------------------------- 

#Ejemplo de creacion de la tabla general de la competicion según la liga 

#PRUEBA DE USO
print("\n🔹 Probando función para crear el dataframe de la tabla principal de la liga de interés a partir de una URL.")
print(' ')
df_tabla_liga= obtener_tabla_liga_principal('https://fbref.com/en/comps/12/Estadisticas-de-La-Liga')
print(df_tabla_liga.sample(3))
print('------')
print(' ')

#--------------------------------------------------------------------------------------------------------------- 

#Ejemplo de creacion de la tabla de jugadores similares al jugador deseable.

#El usuario escoje la url del jugador deseable y lo guarda en una variable para ser usada posteriormente.
url_jugador_yamal= 'https://fbref.com/en/players/82ec26c1/scout/365_m1/Lamine-Yamal-Scouting-Report'

#PRUEBA DE USO: 
print("\n🔹 Probando función para para extraer el dataframe de los jugadores más similares al jugador deseable.")
print(' ')
jugadores_similares_yamal= obtener_jugadores_similares(url_jugador_yamal)
print(jugadores_similares_yamal.sample(3))
print('------')
print(' ')

#--------------------------------------------------------------------------------------------------------------- 
#Ejemplo de creacion de la tabla de las estadísticas por 90 y percentiles del jugador deseable.

#Se usa la misma url del jugador desable del caso anterior.
url_jugador_yamal

#PRUEBA DE USO: 
print("\n🔹 Probando función para para extraer el dataframe de los datos por90 y sus percentiles del jugador deseable")
print(' ')
datos_per90_percentil_yamal= obtener_tabla_datos_jugador_por90_percentiles(url_jugador_yamal)
print(datos_per90_percentil_yamal.sample(3))
print('------')
print(' ')

#----------------------------------------------------------------------------------------------------------------

#Ejecucion de la funcion para extraer los datos de los tiros de un partido para ambos equipos y individualmente.

#El usuario escoje la url del partido deseable y lo guarda en una variable para ser usada posteriormente.
url_partido = 'https://fbref.com/en/partidos/20bdd334/Athletic-Club-Barcelona-Mayo-25-2025-La-Liga'


#PRUEBA DE USO:
print("\n🔹 Probando función para para extraer el dataframe de los datos de los tiros de un partido para ambos equipos y individualmente.")
print(' ')
tabla_tiros_completo,tabla_tiros_local, tabla_tiros_visitante= obtener_tabla_tiros_partido(url_partido, tiros_por_equipo= True)
print('Tabla de todos los tiros del partido:')
print(' ')
print(tabla_tiros_completo.sample(3))
print('------')
print('Tabla de los tiros del local del partido:')
print(' ')
print(tabla_tiros_local.sample(3))
print('------')
print('Tabla de los tiros del visitante del partido:')
print(' ')
print(tabla_tiros_visitante.sample(3))
print('------')

#----------------------------------------------------------------------------------------------------------------

#Ejecucion de la funcion para extraer las estadisticas de un partido para ambos equipos individualmente y tambien de sus respectivos porteros.

#Guardar la url del partido elegido:
url_partido = 'https://fbref.com/en/partidos/20bdd334/Athletic-Club-Barcelona-Mayo-25-2025-La-Liga'


#PRUEBA DE USO:
print("\n🔹 Probando función para para extraer el dataframe dec las estadísticas básicas de los jugadores e porteros de un partido para ambos equipos y individualmente.")
print(' ')

estadisticas_local, estadisticas_visitante, keeper_local, kepper_visitante= obtener_tabla_estadisticas_principales_partido(url_partido, keepers= True)
print('Tabla de las estadísticas del equipo local en el partido:')
print(' ')
print(estadisticas_local.sample(3))
print('------')
print('Tabla de las estadísticas del equipo visitante en el partido:')
print(' ')
print(estadisticas_visitante.sample(3))
print('------')
print('Tabla de las estadísticas del portero local en el partido:')
print(' ')
print(keeper_local)
print('------')
print('Tabla de las estadísticas del portero visitante en el partido:')
print(' ')
print(kepper_visitante)
print('------')

#----------------------------------------------------------------------------------------------------------------

print('LA LIBRERIA REALIZA SU FUNCIÓN CORRECTAMENTE. ¡TODO EL SCRAPEO CON ÉXITO!')