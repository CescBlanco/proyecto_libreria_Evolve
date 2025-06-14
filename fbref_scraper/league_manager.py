import requests
from bs4 import BeautifulSoup
import re
import json
import time
import random
import pandas as pd
import numpy as np

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

class LeagueManager:
    """
    Clase para gestionar ligas de fútbol y generar URLs de estadísticas de jugadores desde FBref.
    """
    def __init__(self):
        """
        Inicializa los atributos necesarios para acceder a las ligas, temporadas y tipos de estadísticas disponibles.
        """
        self.base_url = "https://fbref.com/en/comps/"
        # Diccionario con ligas disponibles, cada una con su ID, slug para la URL y temporadas disponibles
        self.possible_leagues = {
            'Fbref': {
                'Premier League': {
                    'id': 9,
                    'slug': 'Premier-League',
                    'seasons': ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021']
                },
                'La Liga': {
                    'id': 12,
                    'slug': 'La-Liga',
                    'seasons': ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021']
                },
                'Ligue 1': {
                    'id': 13,
                    'slug': 'Ligue-1',
                    'seasons': ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021']    
                },
                'Bundesliga': {
                    'id': 20,
                    'slug': 'Bundesliga',
                    'seasons': ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021']
                },
                'Serie A': {
                    'id': 11,
                    'slug': 'Serie-A',
                    'seasons': ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021']
                },
                'Big 5 European Leagues': {
                    'id': 'Big5',
                    'slug': 'Big-5-European-Leagues',
                    'seasons': ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021']
                },
            }
        }

        # Tipos de estadísticas disponibles para jugadores
        self.player_tables = {
            "Standard Stats": "stats/players",
            "Goalkeeping": "keepers/players",
            "Advanced Goalkeeping": "keepersadv/players",
            "Shooting": "shooting/players",
            "Passing": "passing/players",
            "Pass Types": "passing_types/players",
            "Goal and Shot Creation": "gca/players",
            "Defensive Actions": "defense/players",
            "Possession": "possession/players",
            "Playing Time": "playingtime/players",
            "Miscellaneous Stats": "misc/players",
        }
        self.team_tables = {
            'stats': 'stats',
            'shooting': 'shooting',
            'passing': 'passing',
            'passingtypes': 'passing_types',
            'gca': 'gca',
            'defensive': 'defense',
            'possession': 'possession',
            'playingtime': 'playingtime',
            'misc': 'misc',
            'keepers': 'keepers',
            'keepersadv': 'keepersadv'
        }

        self.headers = {'User-Agent': USER_AGENT}

    def get_available_leagues(self) -> dict:
        """
        Devuelve un diccionario con las ligas disponibles, sus identificadores y temporadas.

        Return:
            dict: Ligas disponibles con su ID y temporadas.
        """
        return {
            league_name: {
                'id': data['id'],
                'seasons': data['seasons']
            }
            for league_name, data in self.possible_leagues['Fbref'].items()
        }

    def get_league_info(self, league_name: str) -> dict | None:
        """
        Devuelve la información de una liga específica.

        Args:
            league_name (str): Nombre de la liga.

        Return:
            dict or None: Información de la liga seleccionada (id, slug, seasons) o None si no existe.
        """
        return self.possible_leagues['Fbref'].get(league_name)

    def get_all_league_names(self) -> list:
        """
        Devuelve la lista de nombres de todas las ligas disponibles.

        Return:
            list: Nombres de las ligas.
        """
        return list(self.possible_leagues['Fbref'].keys())

    def generate_player_urls(self)-> dict:
        """
        Genera URLs completas para acceder a estadísticas de jugadores por liga, temporada y tipo de estadística.

        Return:
            dict: Diccionario anidado con URLs organizadas por liga y temporada.
                  Formato: {liga: {temporada: {tipo_estadistica: url}}}
        """
        urls = {}

        for league_name, league_data in self.possible_leagues['Fbref'].items():
            league_id = league_data['id']
            seasons = league_data['seasons']
            urls[league_name] = {}

            for season in seasons:
                season_urls = {}
                for stat_name, path in self.player_tables.items():
                    url = (
                            f"{self.base_url}{league_id}/{path}/{season}/"
                            f"{league_data['slug']}-Stats"
                        )
                    season_urls[stat_name] = url

                urls[league_name][season] = season_urls

        return urls
    
    def generate_team_urls(self) -> dict:

        """
        Genera URLs completas para acceder a estadísticas de equipos por liga, temporada y tipo de estadística.

        Return:
            dict: Diccionario anidado con URLs organizadas por liga y temporada.
                Formato: {liga: {temporada: {tipo_estadistica: url}}}
        """
        
        urls = {}

        for league_name, league_data in self.possible_leagues['Fbref'].items():
            league_id = league_data['id']
            slug = league_data['slug']
            seasons = league_data['seasons']
            urls[league_name] = {}

            for season in seasons:
                season_urls = {}
                for stat_name, path in self.team_tables.items():
                    url = f"{self.base_url}{league_id}/{path}/{slug}-Stats"
                    season_urls[stat_name] = url
                urls[league_name][season] = season_urls

        return urls
