"""
BOTOLA PRO SCRAPER - Version Démo avec Données Exemple
========================================
Version de démonstration avec données de test
Pour montrer le fonctionnement complet du scraper
"""

import os
import time
import pandas as pd
import logging
from datetime import datetime

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
    """Scraper pour FootyStats.org - Botola Pro (Mode Démo)"""
    
    def __init__(self, headless=False):
        """Initialise le scraper"""
        self.headless = headless
        
    def get_demo_data(self, season: str):
        """Retourne des données de démonstration réalistes"""
        
        demo_matches = {
            "2023/2024": [
                {
                    'date': '2023-08-18', 'time': '15:00',
                    'home_team': 'Raja Casablanca', 'away_team': 'Wydad Casablanca',
                    'score': '2-1', 'home_goals': 2, 'away_goals': 1,
                    'xg_home': 1.8, 'xg_away': 1.2,
                    'shots_home': 8, 'shots_away': 6,
                    'possession_home': 52, 'possession_away': 48,
                    'season': '2023/2024'
                },
                {
                    'date': '2023-08-19', 'time': '18:30',
                    'home_team': 'FUS Rabat', 'away_team': 'AS FAR',
                    'score': '1-1', 'home_goals': 1, 'away_goals': 1,
                    'xg_home': 1.5, 'xg_away': 1.4,
                    'shots_home': 7, 'shots_away': 9,
                    'possession_home': 48, 'possession_away': 52,
                    'season': '2023/2024'
                },
                {
                    'date': '2023-08-20', 'time': '20:00',
                    'home_team': 'Moghreb Fez', 'away_team': 'Raja Casablanca',
                    'score': '0-2', 'home_goals': 0, 'away_goals': 2,
                    'xg_home': 0.9, 'xg_away': 2.1,
                    'shots_home': 5, 'shots_away': 10,
                    'possession_home': 42, 'possession_away': 58,
                    'season': '2023/2024'
                },
                {
                    'date': '2023-08-21', 'time': '16:00',
                    'home_team': 'Difaa Hassani', 'away_team': 'Sporting Casablanca',
                    'score': '1-2', 'home_goals': 1, 'away_goals': 2,
                    'xg_home': 1.2, 'xg_away': 1.9,
                    'shots_home': 6, 'shots_away': 8,
                    'possession_home': 46, 'possession_away': 54,
                    'season': '2023/2024'
                },
            ],
            "2022/2023": [
                {
                    'date': '2022-08-25', 'time': '19:00',
                    'home_team': 'Wydad Casablanca', 'away_team': 'Raja Casablanca',
                    'score': '3-1', 'home_goals': 3, 'away_goals': 1,
                    'xg_home': 2.5, 'xg_away': 0.8,
                    'shots_home': 12, 'shots_away': 7,
                    'possession_home': 60, 'possession_away': 40,
                    'season': '2022/2023'
                },
                {
                    'date': '2022-08-26', 'time': '17:30',
                    'home_team': 'AS FAR', 'away_team': 'FUS Rabat',
                    'score': '2-0', 'home_goals': 2, 'away_goals': 0,
                    'xg_home': 2.2, 'xg_away': 0.6,
                    'shots_home': 9, 'shots_away': 4,
                    'possession_home': 55, 'possession_away': 45,
                    'season': '2022/2023'
                },
                {
                    'date': '2022-08-27', 'time': '20:00',
                    'home_team': 'Moghreb Fez', 'away_team': 'Difaa Hassani',
                    'score': '1-1', 'home_goals': 1, 'away_goals': 1,
                    'xg_home': 1.4, 'xg_away': 1.3,
                    'shots_home': 7, 'shots_away': 6,
                    'possession_home': 51, 'possession_away': 49,
                    'season': '2022/2023'
                },
                {
                    'date': '2022-08-28', 'time': '16:00',
                    'home_team': 'Sporting Casablanca', 'away_team': 'Wydad Casablanca',
                    'score': '0-1', 'home_goals': 0, 'away_goals': 1,
                    'xg_home': 0.7, 'xg_away': 1.6,
                    'shots_home': 5, 'shots_away': 9,
                    'possession_home': 45, 'possession_away': 55,
                    'season': '2022/2023'
                },
            ],
            "2021/2022": [
                {
                    'date': '2021-09-10', 'time': '18:00',
                    'home_team': 'Raja Casablanca', 'away_team': 'AS FAR',
                    'score': '2-2', 'home_goals': 2, 'away_goals': 2,
                    'xg_home': 1.9, 'xg_away': 2.0,
                    'shots_home': 10, 'shots_away': 11,
                    'possession_home': 50, 'possession_away': 50,
                    'season': '2021/2022'
                },
                {
                    'date': '2021-09-11', 'time': '17:00',
                    'home_team': 'Wydad Casablanca', 'away_team': 'Moghreb Fez',
                    'score': '4-0', 'home_goals': 4, 'away_goals': 0,
                    'xg_home': 3.2, 'xg_away': 0.4,
                    'shots_home': 14, 'shots_away': 3,
                    'possession_home': 68, 'possession_away': 32,
                    'season': '2021/2022'
                },
                {
                    'date': '2021-09-12', 'time': '19:30',
                    'home_team': 'FUS Rabat', 'away_team': 'Sporting Casablanca',
                    'score': '1-0', 'home_goals': 1, 'away_goals': 0,
                    'xg_home': 1.3, 'xg_away': 0.5,
                    'shots_home': 8, 'shots_away': 4,
                    'possession_home': 57, 'possession_away': 43,
                    'season': '2021/2022'
                },
                {
                    'date': '2021-09-13', 'time': '15:30',
                    'home_team': 'Difaa Hassani', 'away_team': 'FUS Rabat',
                    'score': '3-1', 'home_goals': 3, 'away_goals': 1,
                    'xg_home': 2.7, 'xg_away': 1.1,
                    'shots_home': 11, 'shots_away': 5,
                    'possession_home': 62, 'possession_away': 38,
                    'season': '2021/2022'
                },
            ]
        }
        
        return demo_matches.get(season, [])
    
    def scrape_season(self, season: str):
        """Scrape une saison (en mode démo)"""
        logger.info(f"\nScraping saison {season}...")
        
        # Simule un délai réseau
        time.sleep(1)
        
        # Récupère les données de démo
        matches = self.get_demo_data(season)
        
        if not matches:
            logger.warning(f"Aucun match trouvé pour {season}")
            return pd.DataFrame()
        
        df = pd.DataFrame(matches)
        logger.info(f"DataFrame créé avec {len(df)} matchs")
        
        return df
    
    def scrape_multiple_seasons(self, seasons):
        """Scrape plusieurs saisons"""
        all_matches = []
        
        for i, season in enumerate(seasons):
            logger.info(f"\n[{i+1}/{len(seasons)}] Traitement {season}...")
            
            df = self.scrape_season(season)
            
            if df is not None and not df.empty:
                all_matches.append(df)
            
            # Petit délai entre les saisons
            if i < len(seasons) - 1:
                time.sleep(1)
        
        if not all_matches:
            logger.warning("Aucune donnée récupérée")
            return pd.DataFrame()
        
        combined_df = pd.concat(all_matches, ignore_index=True)
        logger.info(f"\nTOTAL: {len(combined_df)} matchs sur {len(seasons)} saisons")
        
        return combined_df
    
    def save_to_csv(self, df, filename=None):
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
    logger.info("BOTOLA PRO SCRAPER - Mode Demo (Donnees Exemple)")
    logger.info("=" * 60)
    logger.info("\nNote: Cette version utilise des donnees de demonstration.")
    logger.info("Pour scraper les vraies donnees, installer Firefox ou Chrome.")
    
    seasons = ["2023/2024", "2022/2023", "2021/2022"]
    
    scraper = BotolaScraper()
    
    try:
        logger.info(f"\nScraping de {len(seasons)} saisons...")
        df_botola = scraper.scrape_multiple_seasons(seasons)
        
        if df_botola is not None and not df_botola.empty:
            logger.info("\nAPERCU DES DONNEES:")
            for idx, row in df_botola.head(5).iterrows():
                logger.info(f"  {row['date']} {row['time']} | {row['home_team']} {row['score']} {row['away_team']}")
            
            logger.info(f"\nColonnes: {list(df_botola.columns)}")
            
            csv_file = scraper.save_to_csv(df_botola, "botola_matches.csv")
            
            logger.info("\nSTATISTIQUES:")
            logger.info(f"Total matchs: {len(df_botola)}")
            if 'season' in df_botola.columns:
                logger.info(f"Saisons: {df_botola['season'].unique().tolist()}")
            
            teams = set()
            if 'home_team' in df_botola.columns:
                teams.update(df_botola['home_team'].unique())
            if 'away_team' in df_botola.columns:
                teams.update(df_botola['away_team'].unique())
            logger.info(f"Equipes: {len(teams)} - {', '.join(sorted(teams))}")
            
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
