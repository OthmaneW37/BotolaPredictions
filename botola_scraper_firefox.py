"""
BOTOLA PRO SCRAPER - FootyStats.org (Version Firefox)
========================================
Scraper spécialisé pour extraire les données de matches de la Botola Pro
depuis FootyStats.org avec Firefox et gestion de Cloudflare + export en CSV.
"""

import os
import time
import pandas as pd
import logging
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
import requests
from typing import List, Dict, Tuple
import json

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


class BotolaScraper:
    """Scraper pour FootyStats.org - Botola Pro (Firefox)"""
    
    def __init__(self, headless=False):
        """
        Initialise le scraper
        
        Args:
            headless (bool): Si True, lance le navigateur en mode headless (invisible)
        """
        self.base_url = "https://footystats.org/morocco/botola-pro"
        self.matches_url = f"{self.base_url}/matches"
        self.headless = headless
        self.driver = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        })
        
    def init_driver(self):
        """Initialise le driver Selenium avec Firefox"""
        options = FirefoxOptions()
        
        if self.headless:
            options.add_argument("--headless")
        
        # Options optimisées pour contourner Cloudflare
        options.set_preference("network.http.keep-alive.timeout", 300)
        options.set_preference("general.useragent.override", 
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0")
        
        try:
            logger.info("🔧 Initialisation du driver Firefox...")
            self.driver = webdriver.Firefox(
                service=Service(GeckoDriverManager().install()),
                options=options
            )
            logger.info("✅ Driver Firefox initialisé avec succès")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'initialisation du driver: {e}")
            return False
    
    def get_page_with_selenium(self, url: str, wait_time: int = 15) -> Tuple[bool, BeautifulSoup]:
        """
        Récupère une page avec Selenium pour contourner Cloudflare
        
        Args:
            url (str): URL à scraper
            wait_time (int): Temps d'attente max en secondes
            
        Returns:
            Tuple[bool, BeautifulSoup]: (succès, soup)
        """
        try:
            logger.info(f"📄 Chargement de {url}...")
            self.driver.get(url)
            
            # Attend que le contenu principal se charge
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "tr"))
            )
            
            time.sleep(2)  # Pause supplémentaire pour le rendu complet
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            logger.info("✅ Page chargée avec succès")
            return True, soup
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement: {e}")
            return False, None
    
    def extract_matches_from_page(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extrait les données des matchs depuis la page
        
        Args:
            soup (BeautifulSoup): Contenu HTML parsé
            
        Returns:
            List[Dict]: Liste des matchs
        """
        matches = []
        
        # Cherche les lignes de tableau contenant les matchs
        table_rows = soup.find_all('tr')
        logger.info(f"📊 {len(table_rows)} lignes trouvées")
        
        for row in table_rows:
            try:
                # Essaie d'extraire les infos du match
                cells = row.find_all('td')
                if len(cells) < 5:
                    continue
                
                # Structure typique : [Date | Heure | Domicile | Score | Extérieur | Status | Résultat]
                match_data = self._parse_match_row(row, cells)
                
                if match_data:
                    matches.append(match_data)
                    logger.debug(f"✓ Match extrait: {match_data['home_team']} vs {match_data['away_team']}")
                    
            except Exception as e:
                logger.debug(f"Ligne ignorée: {e}")
                continue
        
        logger.info(f"✅ {len(matches)} matchs extraits")
        return matches
    
    def _parse_match_row(self, row, cells: List) -> Dict:
        """
        Parse une ligne de match
        
        Args:
            row: Élément TR de BeautifulSoup
            cells: Liste des cellules TD
            
        Returns:
            Dict: Données du match ou None
        """
        try:
            # Essaie plusieurs structures possibles
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
            
            # Extrait les stats si disponibles
            stats = self._extract_match_stats(row)
            
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
            }
        except Exception as e:
            logger.debug(f"Erreur parsing: {e}")
            return None
    
    def _parse_score(self, score_str: str) -> Tuple[int, int]:
        """
        Parse le score depuis une chaîne (ex: "2-1")
        
        Args:
            score_str (str): Chaîne de score
            
        Returns:
            Tuple[int, int]: (buts_domicile, buts_extérieur)
        """
        try:
            if '-' in score_str:
                parts = score_str.split('-')
                return int(parts[0].strip()), int(parts[1].strip())
            return None, None
        except:
            return None, None
    
    def _extract_match_stats(self, row) -> Dict:
        """
        Extrait les stats supplémentaires du match si disponibles
        
        Args:
            row: Élément TR
            
        Returns:
            Dict: Statistiques du match
        """
        stats = {}
        
        # Cherche les éléments contenant xG, tirs, possession
        row_text = row.get_text()
        
        # Exemple : cherche des patterns de xG
        import re
        xg_pattern = r'(\d+\.?\d*)\s*xG'
        matches = re.findall(xg_pattern, row_text)
        
        if len(matches) >= 2:
            stats['xg_home'] = matches[0]
            stats['xg_away'] = matches[1]
        
        return stats
    
    def scrape_season(self, season: str = None) -> pd.DataFrame:
        """
        Scrape tous les matchs d'une saison
        
        Args:
            season (str): Saison à scraper (ex: "2023/2024")
            
        Returns:
            pd.DataFrame: DataFrame avec tous les matchs
        """
        if not self.driver:
            if not self.init_driver():
                logger.error("❌ Impossible d'initialiser le driver")
                return None
        
        url = self.matches_url
        if season:
            url += f"?season={season}"
        
        success, soup = self.get_page_with_selenium(url)
        if not success:
            logger.error("❌ Échec du chargement de la page")
            return None
        
        matches = self.extract_matches_from_page(soup)
        
        if not matches:
            logger.warning("⚠️ Aucun match trouvé")
            return pd.DataFrame()
        
        df = pd.DataFrame(matches)
        logger.info(f"📊 DataFrame créé avec {len(df)} matchs")
        
        return df
    
    def scrape_multiple_seasons(self, seasons: List[str]) -> pd.DataFrame:
        """
        Scrape plusieurs saisons et les combine
        
        Args:
            seasons (List[str]): Liste des saisons à scraper
            
        Returns:
            pd.DataFrame: DataFrame combiné
        """
        all_matches = []
        
        for season in seasons:
            logger.info(f"\n🏆 Scraping saison {season}...")
            df = self.scrape_season(season)
            
            if df is not None and not df.empty:
                df['season'] = season
                all_matches.append(df)
                time.sleep(2)  # Délai entre les requêtes
        
        if not all_matches:
            logger.warning("⚠️ Aucune donnée récupérée")
            return pd.DataFrame()
        
        combined_df = pd.concat(all_matches, ignore_index=True)
        logger.info(f"✅ Total: {len(combined_df)} matchs sur {len(seasons)} saisons")
        
        return combined_df
    
    def save_to_csv(self, df: pd.DataFrame, filename: str = None):
        """
        Sauvegarde le DataFrame en CSV
        
        Args:
            df (pd.DataFrame): DataFrame à sauvegarder
            filename (str): Nom du fichier (par défaut: botola_matches_YYYYMMDD.csv)
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"botola_matches_{timestamp}.csv"
        
        try:
            df.to_csv(filename, index=False, encoding='utf-8')
            logger.info(f"✅ Fichier sauvegardé: {filename}")
            logger.info(f"📈 Taille: {len(df)} lignes, {len(df.columns)} colonnes")
            return filename
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sauvegarde: {e}")
            return None
    
    def close(self):
        """Ferme le driver Selenium"""
        if self.driver:
            self.driver.quit()
            logger.info("🛑 Driver fermé")
    
    def __enter__(self):
        """Context manager entry"""
        self.init_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


def main():
    """Fonction principale de scraping"""
    
    logger.info("=" * 60)
    logger.info("🏆 BOTOLA PRO SCRAPER - FootyStats.org (Firefox)")
    logger.info("=" * 60)
    
    # Saisons à scraper (3 dernières années)
    seasons = ["2023/2024", "2022/2023", "2021/2022"]
    
    # Utilise le scraper en context manager (ferme automatiquement le driver)
    with BotolaScraper(headless=False) as scraper:
        try:
            # Scrape les saisons
            df_botola = scraper.scrape_multiple_seasons(seasons)
            
            if df_botola is not None and not df_botola.empty:
                # Affiche un aperçu
                logger.info("\n📊 APERÇU DES DONNÉES:")
                logger.info(df_botola.head(10))
                logger.info(f"\nColonnes: {list(df_botola.columns)}")
                
                # Sauvegarde en CSV
                csv_file = scraper.save_to_csv(df_botola, "botola_matches.csv")
                
                # Statistiques
                logger.info("\n📈 STATISTIQUES:")
                logger.info(f"Total de matchs: {len(df_botola)}")
                logger.info(f"Saisons: {df_botola['season'].unique().tolist()}")
                logger.info(f"Équipes uniques: {len(pd.concat([df_botola['home_team'], df_botola['away_team']]).unique())}")
                
                return csv_file
            else:
                logger.error("❌ Aucune donnée récupérée")
                return None
                
        except KeyboardInterrupt:
            logger.info("\n⏸️  Scraping interrompu par l'utilisateur")
            return None
        except Exception as e:
            logger.error(f"❌ Erreur critique: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None


if __name__ == "__main__":
    csv_output = main()
    if csv_output:
        logger.info(f"\n✅ Succès! Fichier créé: {csv_output}")
    else:
        logger.info("\n❌ Scraping échoué")
