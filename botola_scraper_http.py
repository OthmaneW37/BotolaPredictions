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
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
]


class BotolaScraper:
    """Scraper pour FootyStats.org - Botola Pro (HTTP Pure)"""
    
    def __init__(self, headless=False):
        """Initialise le scraper"""
        self.base_url = "https://footystats.org/morocco/botola-pro"
        self.matches_url = f"{self.base_url}/matches"
        self.headless = headless
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://footystats.org/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
    def get_page(self, url: str, max_retries: int = 3) -> Tuple[bool, BeautifulSoup]:
        """
        Récupère une page avec retry logic
        
        Args:
            url (str): URL à récupérer
            max_retries (int): Nombre de tentatives
            
        Returns:
            Tuple[bool, BeautifulSoup]: (succès, soup)
        """
        for attempt in range(max_retries):
            try:
                logger.info(f"Tentative {attempt+1}/{max_retries} - Chargement {url}...")
                
                # Rotate user agent
                self.session.headers['User-Agent'] = random.choice(USER_AGENTS)
                
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                logger.info("Succes: Page chargee")
                return True, soup
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Erreur tentative {attempt+1}: {e}")
                time.sleep(2 + random.uniform(0, 2))  # Délai avant retry
                continue
        
        logger.error("Impossible de charger la page apres retries")
        return False, None
    
    def extract_matches_from_page(self, soup: BeautifulSoup, season: str = None) -> List[Dict]:
        """Extrait les données des matchs depuis la page"""
        matches = []
        
        # Cherche les lignes de tableau
        table_rows = soup.find_all('tr')
        logger.info(f"Lignes trouvees: {len(table_rows)}")
        
        for row in table_rows:
            try:
                cells = row.find_all('td')
                if len(cells) < 5:
                    continue
                
                match_data = self._parse_match_row(cells, season)
                if match_data:
                    matches.append(match_data)
                    
            except Exception as e:
                logger.debug(f"Ligne ignoree: {e}")
                continue
        
        logger.info(f"Matchs extraits: {len(matches)}")
        return matches
    
    def _parse_match_row(self, cells: List, season: str = None) -> Dict:
        """Parse une ligne de match"""
        try:
            date_str = cells[0].get_text(strip=True) if len(cells) > 0 else None
            time_str = cells[1].get_text(strip=True) if len(cells) > 1 else ""
            home_team = cells[2].get_text(strip=True) if len(cells) > 2 else None
            score_str = cells[3].get_text(strip=True) if len(cells) > 3 else None
            away_team = cells[4].get_text(strip=True) if len(cells) > 4 else None
            
            # Valide les champs critiques
            if not all([date_str, home_team, score_str, away_team]):
                return None
            
            # Parse le score
            home_goals, away_goals = self._parse_score(score_str)
            
            # Extrait les stats
            stats = self._extract_match_stats(cells)
            
            return {
                'date': date_str,
                'time': time_str,
                'home_team': home_team,
                'away_team': away_team,
                'score': score_str,
                'home_goals': home_goals,
                'away_goals': away_goals,
                'xg_home': stats.get('xg_home', ''),
                'xg_away': stats.get('xg_away', ''),
                'shots_home': stats.get('shots_home', ''),
                'shots_away': stats.get('shots_away', ''),
                'possession_home': stats.get('possession_home', ''),
                'possession_away': stats.get('possession_away', ''),
                'season': season or 'Unknown'
            }
        except Exception as e:
            logger.debug(f"Erreur parsing: {e}")
            return None
    
    def _parse_score(self, score_str: str) -> Tuple[int, int]:
        """Parse le score"""
        try:
            if '-' in score_str:
                parts = score_str.split('-')
                return int(parts[0].strip()), int(parts[1].strip())
            return None, None
        except:
            return None, None
    
    def _extract_match_stats(self, cells: List) -> Dict:
        """Extrait les stats du match"""
        stats = {}
        
        # Combine le texte de toutes les cellules
        all_text = ' '.join([cell.get_text() for cell in cells])
        
        # Cherche les patterns
        import re
        xg_pattern = r'(\d+\.?\d*)\s*xG'
        matches = re.findall(xg_pattern, all_text)
        
        if len(matches) >= 2:
            stats['xg_home'] = matches[0]
            stats['xg_away'] = matches[1]
        
        return stats
    
    def scrape_season(self, season: str) -> pd.DataFrame:
        """Scrape une saison entiere"""
        logger.info(f"\n=== Saison {season} ===")
        
        # Construit l'URL avec le paramètre saison
        url = self.matches_url
        if season:
            url += f"?season={season.replace('/', '%2F')}"
        
        success, soup = self.get_page(url)
        if not success:
            logger.error(f"Echec: impossible de charger {season}")
            return pd.DataFrame()
        
        matches = self.extract_matches_from_page(soup, season)
        
        if not matches:
            logger.warning(f"Aucun match trouve pour {season}")
            return pd.DataFrame()
        
        df = pd.DataFrame(matches)
        logger.info(f"DataFrame cree avec {len(df)} matchs")
        
        return df
    
    def scrape_multiple_seasons(self, seasons: List[str]) -> pd.DataFrame:
        """Scrape plusieurs saisons"""
        all_matches = []
        
        for i, season in enumerate(seasons):
            logger.info(f"\n[{i+1}/{len(seasons)}] Scraping saison {season}...")
            
            df = self.scrape_season(season)
            
            if df is not None and not df.empty:
                all_matches.append(df)
            
            # Délai entre les requêtes (respectueux du serveur)
            if i < len(seasons) - 1:
                delay = 2 + random.uniform(0, 3)
                logger.info(f"Attente {delay:.1f}s avant saison suivante...")
                time.sleep(delay)
        
        if not all_matches:
            logger.warning("Aucune donnee recuperee")
            return pd.DataFrame()
        
        combined_df = pd.concat(all_matches, ignore_index=True)
        logger.info(f"\nTOTAL: {len(combined_df)} matchs sur {len(seasons)} saisons")
        
        return combined_df
    
    def save_to_csv(self, df: pd.DataFrame, filename: str = None):
        """Sauvegarde en CSV"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"botola_matches_{timestamp}.csv"
        
        try:
            df.to_csv(filename, index=False, encoding='utf-8')
            logger.info(f"Fichier sauvegarde: {filename}")
            logger.info(f"Taille: {len(df)} lignes, {len(df.columns)} colonnes")
            return filename
        except Exception as e:
            logger.error(f"Erreur sauvegarde: {e}")
            return None


def main():
    """Fonction principale"""
    
    logger.info("=" * 60)
    logger.info("BOTOLA PRO SCRAPER - HTTP Method (Pure Python)")
    logger.info("=" * 60)
    
    seasons = ["2023/2024", "2022/2023", "2021/2022"]
    
    scraper = BotolaScraper()
    
    try:
        logger.info(f"\nScraping de {len(seasons)} saisons...")
        df_botola = scraper.scrape_multiple_seasons(seasons)
        
        if df_botola is not None and not df_botola.empty:
            logger.info("\nAPERÇU DES DONNEES:")
            logger.info(df_botola.head())
            logger.info(f"\nColonnes: {list(df_botola.columns)}")
            
            csv_file = scraper.save_to_csv(df_botola, "botola_matches.csv")
            
            logger.info("\nSTATISTIQUES:")
            logger.info(f"Total matchs: {len(df_botola)}")
            if 'season' in df_botola.columns:
                logger.info(f"Saisons: {df_botola['season'].unique().tolist()}")
            
            return csv_file
        else:
            logger.error("Aucune donnee recuperee")
            return None
            
    except KeyboardInterrupt:
        logger.info("\nScraping interrompu")
        return None
    except Exception as e:
        logger.error(f"Erreur critique: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


if __name__ == "__main__":
    csv_output = main()
    if csv_output:
        logger.info(f"\nSucces! Fichier cree: {csv_output}")
    else:
        logger.info("\nScraping echoue")
