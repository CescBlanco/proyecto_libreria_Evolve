from fbref_scraper.league_manager import LeagueManager
from fbref_scraper.player_data import creacion_df_jugadores_estadistica_unica

#Llamada a la clase LeagueManager para generar URLs de jugadores
manager = LeagueManager()
player_urls = manager.generate_player_urls()
# Ver las URLs de La Liga 2024-2025
url=  player_urls['La Liga']['2024-2025']['Shooting']
print("URL:", url)


df_final = creacion_df_jugadores_estadistica_unica(url, guardar_csv=False, stat='Shooting', league='La Liga', season='2024-25')
print(df_final.head())
