from fbref_scraper.league_manager import LeagueManager
from fbref_scraper.player_data import *
from fbref_scraper.team_data import * 

#Llamada a la clase LeagueManager para generar URLs de jugadores.
manager = LeagueManager()

#Generación de todas las urls posibles para extraer la infomarcion de los jugadores.

player_urls = manager.generate_player_urls()

# Ver las URL de la estadistica shooting de La Liga 2024-2025.

url=  player_urls['La Liga']['2024-2025']['Shooting']
print("URL:", url)
print('------')

#Ejemplo de creacíon de un dataframe de una estadisticas unica de la liga seleccionada para todos los jugadores.

df_final =creacion_df_jugadores_estadistica_unica(url= url, guardar_csv=True, league='La Liga', season='2024')
print(df_final)
print('------')

#--------------------------------------------------------------------------------------------------------------- 

#Ejemplo de creación de un dataframe de una estadistica unica de la liga seleccionada para todos los equipos, 
#el primero a favor y el segundo en contra (aplicando el stats_vs)

url_stat_equipo = 'https://fbref.com/en/comps/12/stats/La-Liga-Stats'

df_equipo_stat = obtener_tabla_equipos_estadistica_unica(url_stat_equipo, stats_vs=False, guardar_csv= True, league='La Liga', season='2024')
print(df_equipo_stat)
print('------')

df_vs_equipo_stat = obtener_tabla_equipos_estadistica_unica(url_stat_equipo, stats_vs=True, guardar_csv= True, league='La Liga', season='2024')
print(df_vs_equipo_stat)
print('------')

#--------------------------------------------------------------------------------------------------------------- 

#Ejemplo de creacion de la tabla general de la competicion según la liga 
df_tabla_liga= obtener_tabla_liga_principal('https://fbref.com/es/comps/12/Estadisticas-de-La-Liga')
print(df_tabla_liga)
print('------')

#--------------------------------------------------------------------------------------------------------------- 

#Ejemplo de creacion de la tabla de jugadores similares al jugador de la url.

url_jugador_yamal= 'https://fbref.com/es/jugadores/82ec26c1/scout/365_m1/Informe-de-reclutamiento-de-Lamine-Yamal'

#Ejecución de la función para extraer los jugadores más similares al jugador deseable.

jugadores_similares_yamal= obtener_jugadores_similares(url_jugador_yamal)
print(jugadores_similares_yamal)
print('------')

#--------------------------------------------------------------------------------------------------------------- 

#Ejecución de la función para extraer los datos por90 y sus percentiles del jugador deseable.

datos_per90_percentil_yamal= obtener_tabla_datos_jugador_por90_percentiles(url_jugador_yamal)
print(datos_per90_percentil_yamal)
print('------')

#----------------------------------------------------------------------------------------------------------------

#Ejecucion de la funcion para extraer los datos de los tiros de un partido para ambos equipos y individualmente.
url_partido = 'https://fbref.com/en/partidos/20bdd334/Athletic-Club-Barcelona-Mayo-25-2025-La-Liga'
tabla_tiros_completo,tabla_tiros_local, tabla_tiros_visitante= obtener_tabla_tiros_partido(url_partido, tiros_por_equipo= False)
print(tabla_tiros_completo)
print('------')
print(tabla_tiros_local)
print('------')
print(tabla_tiros_visitante)
print('------')

#----------------------------------------------------------------------------------------------------------------

#Ejecucion de la funcion para extraer las estadisticas de un partido para ambos equipos individualmente y tambien de sus respectivos porteros.
estadisticas_local, estadisticas_visitante, keeper_local, kepper_visitante= obtener_tabla_estadisticas_principales_partido(url_partido, keepers= True)
print(estadisticas_local)
print('------')
print(estadisticas_visitante)
print('------')
print(keeper_local)
print('------')
print(estadisticas_local)
print('------')
print(kepper_visitante)
print('------')

#----------------------------------------------------------------------------------------------------------------