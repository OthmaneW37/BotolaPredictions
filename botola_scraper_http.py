"""
BOTOLA PRO SCRAPER - Méthode HTTP Pure (Sans Navigateur)
========================================
Alternative sans dépendance à Chrome/Firefox
Utilise requests + BeautifulSoup avec stratégies anti-protection
"""

import os
import time
import pandas as pd
import logging
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from typing import List, Dict, Tuple
import json
import random

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('botola_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# User-Agents variés pour contourner les filtres
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
]


class BotolaScraper:
    """Scraper pour FootyStats.org - Botola Pro (HTTP Pure)"""
    
    def __init__(self, headless=False):
        """Initialise le scraper"""
        self.session = requests.Session()
        # --- UPDATE: More comprehensive headers to mimic a real browser ---
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
        })
        
    def warmup_session(self, url: str):
        """Makes an initial request to the base URL to acquire cookies."""
        try:
            logger.info(f"Warming up session by visiting {url}...")
            self.session.get(url, timeout=15)
            logger.info("Session is warm, cookies should be set.")
            time.sleep(2) # Brief pause after warmup
        except requests.exceptions.RequestException as e:
            logger.warning(f"Warm-up request failed: {e}. Continuing anyway.")

    def get_page(self, url: str, max_retries: int = 3) -> Tuple[bool, BeautifulSoup]:
        """Récupère une page avec retry logic"""
        for attempt in range(max_retries):
            try:
                logger.info(f"Tentative {attempt+1}/{max_retries} - Chargement {url}...")
                self.session.headers['User-Agent'] = random.choice(USER_AGENTS)
                response = self.session.get(url, timeout=20)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                logger.info("Succès: Page chargée")
                return True, soup
            except requests.exceptions.RequestException as e:
                logger.warning(f"Erreur tentative {attempt+1}: {e}")
                time.sleep(5 + random.uniform(0, 2)) # Increased delay
                continue
        logger.error("Impossible de charger la page après plusieurs tentatives")
        return False, None
    
    def extract_matches_from_page(self, soup: BeautifulSoup, season_name: str) -> List[Dict]:
        """Extrait les données des matchs depuis la page"""
        matches = []
        match_table = soup.select_one("table.matches-table")
        if not match_table:
            logger.warning("Table des matchs non trouvée sur la page.")
            return []
            
        table_rows = match_table.select("tbody tr")
        logger.info(f"Lignes trouvées: {len(table_rows)}")
        
        for row in table_rows:
            cells = row.find_all('td')
            if len(cells) < 5: continue
            match_data = self._parse_match_row(cells, season_name)
            if match_data: matches.append(match_data)
        
        logger.info(f"Matchs extraits: {len(matches)}")
        return matches
    
    def _parse_match_row(self, cells: List, season_name: str) -> Dict:
        """Parse une ligne de match"""
        try:
            home_team = cells[1].select_one("a.team-name").get_text(strip=True)
            away_team = cells[3].select_one("a.team-name").get_text(strip=True)
            score = cells[2].select_one("a.match-link").get_text(strip=True)
            date = cells[0].get_text(strip=True)
            return {'season': season_name, 'date': date, 'home_team': home_team, 'away_team': away_team, 'score': score}
        except Exception: return None

    def scrape_season(self, season_name: str, url: str) -> pd.DataFrame:
        """Scrape une saison entière à partir d'une URL directe"""
        logger.info(f"\n=== Saison {season_name} ===")
        success, soup = self.get_page(url)
        if not success:
            logger.error(f"Échec: impossible de charger les données pour {season_name}")
            return pd.DataFrame()
        matches = self.extract_matches_from_page(soup, season_name)
        return pd.DataFrame(matches) if matches else pd.DataFrame()
    
    def scrape_multiple_seasons(self, seasons: Dict[str, str]) -> pd.DataFrame:
        """Scrape plusieurs saisons à partir d'un dictionnaire d'URLs"""
        # --- UPDATE: Perform a warm-up request before scraping ---
        self.warmup_session("https://footystats.org/")
        
        all_matches_df = []
        for i, (season_name, season_url) in enumerate(seasons.items()):
            logger.info(f"\n[{i+1}/{len(seasons)}] Scraping saison {season_name}...")
            df = self.scrape_season(season_name, season_url)
            if not df.empty: all_matches_df.append(df)
            if i < len(seasons) - 1:
                delay = 3 + random.uniform(0, 3)
                logger.info(f"Attente {delay:.1f}s avant la saison suivante...")
                time.sleep(delay)
        
        if not all_matches_df:
            logger.warning("Aucune donnée n'a été récupérée.")
            return pd.DataFrame()
        
        return pd.concat(all_matches_df, ignore_index=True)
    
    def save_to_csv(self, df: pd.DataFrame, filename: str):
        """Sauvegarde en CSV"""
        try:
            df.to_csv(filename, index=False, encoding='utf-8')
            logger.info(f"Fichier sauvegardé: {filename}")
        except Exception as e: logger.error(f"Erreur de sauvegarde: {e}")

def main():
    """Fonction principale"""
    logger.info("=" * 60)
    logger.info("BOTOLA PRO SCRAPER - HTTP Method (Pure Python)")
    logger.info("=" * 60)
    
    seasons_urls = {
        "2023/2024": "https://footystats.org/morocco/botola-pro/matches?season_id=9102",
        "2022/2023": "https://footystats.org/morocco/botola-pro/matches?season_id=8223",
        "2021/2022": "https://footystats.org/morocco/botola-pro/matches?season_id=7235"
    }
    
    scraper = BotolaScraper()
    
    try:
        df_botola = scraper.scrape_multiple_seasons(seasons_urls)
        if not df_botola.empty:
            logger.info(f"\nScraping terminé. Total de {len(df_botola)} matchs récupérés.")
            scraper.save_to_csv(df_botola, "botola_matches_all_seasons.csv")
        else:
            logger.error("Aucune donnée n'a été récupérée après le scraping.")
    except Exception as e:
        logger.error(f"Erreur critique dans main: {e}", exc_info=True)

if __name__ == "__main__":
    main()
