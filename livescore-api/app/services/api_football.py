import requests
from app.config import get_settings

settings = get_settings()

class APIFootballService:
    # NOUVEAU DOMAINE CORRECT
    BASE_URL = "https://v3.football.api-sports.io"
    API_KEY = settings.API_FOOTBALL_KEY
    
    @staticmethod
    def get_headers():
        return {
            "x-apisports-key": APIFootballService.API_KEY
        }
    
    @staticmethod
    def get_fixtures(league: int, season: int, status: str = None):
        """Get fixtures/matches"""
        url = f"{APIFootballService.BASE_URL}/fixtures"
        params = {
            "league": league,
            "season": season
        }
        if status:
            params["status"] = status
        
        response = requests.get(url, params=params, headers=APIFootballService.get_headers())
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def get_teams(league: int, season: int):
        """Get teams"""
        url = f"{APIFootballService.BASE_URL}/teams"
        params = {
            "league": league,
            "season": season
        }
        response = requests.get(url, params=params, headers=APIFootballService.get_headers())
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def get_players(team_id: int, season: int):
        """Get players by team"""
        url = f"{APIFootballService.BASE_URL}/players"
        params = {
            "team": team_id,
            "season": season
        }
        response = requests.get(url, params=params, headers=APIFootballService.get_headers())
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def get_standings(league: int, season: int):
        """Get standings"""
        url = f"{APIFootballService.BASE_URL}/standings"
        params = {
            "league": league,
            "season": season
        }
        response = requests.get(url, params=params, headers=APIFootballService.get_headers())
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def get_leagues():
        """Get all leagues"""
        url = f"{APIFootballService.BASE_URL}/leagues"
        response = requests.get(url, headers=APIFootballService.get_headers())
        response.raise_for_status()
        return response.json()