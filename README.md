# 📊 fbref_scraper_cesc

**fbref_scraper_cesc** es una librería en Python que permite extraer de forma automática estadísticas de fútbol desde la página [FBref.com](https://fbref.com/), incluyendo información detallada sobre jugadores, equipos, partidos y comparativas avanzadas. Facilita el trabajo posterior en la creación de informes, análisis avanzados y visualización de datos.

## 📌 Características principales:

- **Gestión de ligas y temporadas:** Selecciona fácilmente la liga y temporada de interés.
- **Extracción de estadísticas de jugadores:** Obtén tablas limpias y combinadas de métricas estándar, avanzadas, porteros, etc.
- **Extracción de estadísticas de equipos:** Descarga estadísticas de equipos por diferentes categorías (posesión, defensa, ataque, porteros...).
- **Datos de partidos:** Accede a tablas de tiros, estadísticas principales y datos de porteros de partidos individuales.
- **Informes de reclutamiento:** Extrae tablas de jugadores similares y percentiles avanzados de informes individuales.
- **Automatización y primera limpieza:** Funciones robustas para hacer la primera limpieza, normalizar y guardar los datos en CSV listos para análisis.

---

## 📁 Estructura del proyecto

```plaintext
fbref_scraper_cesc/
│
├── __init__.py
│   ├── league_manager.py      # Gestión de ligas y generación de URLs
│   ├── player_data.py         # Extracción y limpieza de datos de jugadores
│   └── team_data.py           # Extracción y limpieza de datos de equipos
│
├── tests/
│   └── main.py                # Archivo de ejemplo de uso 
│
├── setup.py                   # Archivo de configuración para empaquetar
├── requirements.txt           # Dependencias del proyecto
└── README.md
```
---
## 🚀 Comandos de Instalación e actualización:

· Instala desde PyPI:

```bash
pip install fbref_scraper_cesc
```

O directamente desde GitHub:

```bash
 git clone https://github.com/CescBlanco/proyecto_libreria_Evolve
```

· Puedes crear un entorno virtual (windows):
```bash
python -m venv libreria_venv
libreria_venv/scripts/activate
```


· En caso que se quiera actualizar la libreria hacer:

```bash
pip install --upgrade fbref_scraper_cesc
```

· Instalar el paquete en modo desarrollo:
```bash
pip install -e .
```
---
## 🛠 Requisitos de instalación:
```plaintext
requests
beautifulsoup4
pandas
numpy
lxml
```


Instalar dependencias necesarias: 
```bash
pip install -r requirements.txt
```
---
## Ejecucion de las pruebas:
Para ejecutar las pruebas y verificar que todo funciona, utiliza: 
```bash
python .\tests\main.py
```

##  🧠 Como se usa?

· Importar la clase:

```python
from fbref_scraper_cesc.league_manager import LeagueManager

manager= LeagueManager()
```

· Importar modulos para poder utilizar todas las funciones de extracción:
```python
from fbref_scraper_cesc.player_data import *
from fbref_scraper_cesc.team_data import * 
```

· Crear URLs para scraping:
```python
player_urls = manager.generate_player_urls()
teams_urls = manager.generate_team_urls()
```

---

##  🔍 Demostraciones rápidas: 


· Obtener dataframe de los jugadores de una liga con un tipo de estadística de la temporada:
```python
#PASOS PARA PODER ELEGIR LA URL DESEADA:

# 1: Elegir liga dispoible en player_urls: ['La Liga', 'Premier League', 'Serie A', 'League 1', 'Bundesliga']
liga= 'La Liga'

# 2: Elegir la temporada disponible en player_urls: ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021']
temporada = '2024-2025'

# 3: Elegir una estadísticas disponibles: ['Standard Stats', 'Goalkeeping', 'Advanced Goalkeeping', 'Shooting', 'Passing','Pass Types','Goal and Shot Creation', 'Defensive Actions', 'Possession', 'Playing Time', 'Miscellaneous Stats']
tipo_estadistica=  'Standard Stats'

# 4: Creacion de la url para la funcion:
url_player = player_urls[liga][temporada][tipo_estadistica]
print("URL:", url_player)
print('------')

#EJEMPLO DE USO:
creacion_df_jugadores_estadistica_unica(url_player,guardar_csv=True, league=liga, season=temporada)
```



· Obtener dataframe de todas las estadisticas de los jugadores de campo para una liga y una temporada concreta:
```python
#PASOS PARA PODER ELEGIR EL DATAFRAME DESEADO:

# 1: Elegir liga dispoible en player_urls: ['La Liga', 'Premier League', 'Serie A', 'League 1', 'Bundesliga']
liga = 'Ligue 1'
# 2: Elegir la temporada disponible en player_urls: ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021']
temporada= '2024-2025'

#EJEMPLO DE USO:
creacion_df_players_torneo_fbref(league=liga, season=temporada,
 stat_list=["Standard Stats", "Shooting", "Passing", "Pass Types","Goal and Shot Creation", "Defensive Actions", "Possession", "Miscellaneous Stats"], player_urls=player_urls, guardar_csv=True, guardar_csv_individuales=False)
```




· Obtener dataframe de todas las estadisticas de los porteros para una liga y una temporada concreta:
```python
#PASOS PARA PODER ELEGIR EL DATAFRAME DESEADO:

# 1: Elegir liga dispoible en player_urls: ['La Liga', 'Premier League', 'Serie A', 'League 1', 'Bundesliga']
liga = 'Premier League'
# 2: Elegir la temporada disponible en player_urls: ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021']
temporada= '2024-2025'

#EJEMPLO DE USO:
creacion_df_porteros_torneo_fbref(league=liga,  season=temporada,
      stat_list=['Goalkeeping', 'Advanced Goalkeeping'], player_urls=player_urls, guardar_csv=True, guardar_csv_individuales=False)
```



· Obtener el dataframe de los equipos y equipos_vs de una liga con un tipo de estadística de la temporada:
```python
#PASOS PARA PODER ELEGIR LA URL DESEADA:

# 1: Elegir liga dispoible en player_urls: ['La Liga', 'Premier League', 'Serie A', 'League 1', 'Bundesliga']
liga_equipos = 'La Liga'

# 2: Elegir la temporada disponible en player_urls: ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021']
temporada_equipos= '2024-2025'

# 3: Elegir una estadísticas disponibles:  ['Standard Stats', 'Goalkeeping', 'Advanced Goalkeeping', 'Shooting', 'Passing','Pass Types', 'Goal and Shot Creation', 'Defensive Actions', 'Possession', 'Playing Time', 'Miscellaneous Stats']
tipo_estadistica_equipos =  'Miscellaneous Stats'

# 4: Creacion de la url para la funcion:
url_stat_equipo = player_urls[liga_equipos][temporada_equipos][tipo_estadistica_equipos]
print("URL:", url_stat_equipo)
print('------')


#EJEMPLO DE USO PARA EQUIPO:
obtener_tabla_equipos_estadistica_unica(url_stat_equipo, stats_vs=False, guardar_csv= True, league='La Liga', season='2024')

#EJEMPLO DE USO PARA EQUIPO_VS:
obtener_tabla_equipos_estadistica_unica(url_stat_equipo, stats_vs=True, guardar_csv= True, league='La Liga', season='2024')
```



· Obtener el dataframe de la tabla principal de la liga de interés a partir de una URL:
```python
obtener_tabla_liga_principal('https://fbref.com/en/comps/12/Estadisticas-de-La-Liga')
```



· Obtener el dataframe de los jugadores más similares al jugador deseable:
```python
#El usuario escoje la url del jugador deseable y lo guarda en una variable para ser usada posteriormente.
url_jugador_yamal= 'https://fbref.com/en/players/82ec26c1/scout/365_m1/Lamine-Yamal-Scouting-Report'

#EJEMPLO DE USO: 
obtener_jugadores_similares(url_jugador_yamal)
```


· Obtener el dataframe de los datos por90 y sus percentiles del jugador deseable:
```python
#Se usa la misma url del jugador desable del caso anterior.
url_jugador_yamal= 'https://fbref.com/en/players/82ec26c1/scout/365_m1/Lamine-Yamal-Scouting-Report'

#EJEMPLO DE USO: 
obtener_tabla_datos_jugador_por90_percentiles(url_jugador_yamal)
```




· Obtener dataframe de los datos de los tiros de un partido para ambos equipos y individualmente:
```python
#El usuario escoje la url del partido deseable y lo guarda en una variable para ser usada posteriormente.
url_partido = 'https://fbref.com/en/partidos/20bdd334/Athletic-Club-Barcelona-Mayo-25-2025-La-Liga'
s
#EJEMPLO DE USO:
tabla_tiros_completo,tabla_tiros_local, tabla_tiros_visitante= obtener_tabla_tiros_partido(url_partido, tiros_por_equipo= True)
```



· Obtener el dataframe de las estadísticas básicas de los jugadores e porteros de un partido para ambos equipos y individualmente:
```python
#Guardar la url del partido elegido:
url_partido = 'https://fbref.com/en/partidos/20bdd334/Athletic-Club-Barcelona-Mayo-25-2025-La-Liga'

#EJEMPLO DE USO:
estadisticas_local, estadisticas_visitante, keeper_local, kepper_visitante= obtener_tabla_estadisticas_principales_partido(url_partido, keepers= True)
```

----
## Licencia 
Este proyecto está licenciado bajo la Licencia MIT.

----
## Autor



Desarrollado por Cesc Blanco Arnau. 

👤 [LinkedIn](www.linkedin.com/in/cescblanco)
📧 [Correo](cesc.blanco98@gmail.com)
🔗 [GitHub](https://github.com/CescBlanco)

