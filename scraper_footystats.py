"""
BOTOLA PRO SCRAPER - Méthode Selenium Robuste (Finale V2)
=====================================================
Ce script utilise Selenium pour piloter un navigateur Firefox.
Il est conçu pour attendre que l'utilisateur résolve manuellement les
protections anti-bot (CAPTCHA/Cloudflare) avant de procéder au scraping.
"""

import pandas as pd
import time
import logging
from typing import Dict
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# --- Configuration du Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# --- URLs des saisons ---
SEASONS_URLS = {
    "2023/2024": "https://footystats.org/morocco/botola-pro/matches?season_id=9102",
    "2022/2023": "https://footystats.org/morocco/botola-pro/matches?season_id=8223",
    "2021/2022": "https://footystats.org/morocco/botola-pro/matches?season_id=7235"
}

def initialize_driver() -> uc.Chrome:
    """Initialise le WebDriver pour Chrome avec undetected-chromedriver."""
    logger.info("Initialisation du driver Chrome avec undetected-chromedriver...")
    try:
        options = uc.ChromeOptions()
        driver = uc.Chrome(
            browser_executable_path=r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            options=options
        )
        logger.info("Driver Chrome initialisé avec succès.")
        return driver
    except Exception as e:
        logger.error(f"Erreur critique: Impossible de lancer le navigateur. {e}")
        return None

def scrape_all_seasons(driver: uc.Chrome, seasons: Dict[str, str]) -> pd.DataFrame:
    """Scrape toutes les saisons en tentant de contourner les protections anti-bot."""
    all_matches = []
    
    for season_name, url in seasons.items():
        logger.info(f"\n--- Démarrage du scraping pour la saison {season_name} ---")
        driver.get(url)

        # --- ATTENTE DU CHARGEMENT DE LA PAGE ---
        logger.info("Tentative de contournement de la protection anti-bot...")
        logger.info("Attente du chargement de la table des matchs (max 2 minutes)...")
        
        try:
            WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.matches-table tbody tr"))
            )
            logger.info("Table des matchs détectée. Poursuite du scraping.")
        except TimeoutException:
            logger.error(f"Timeout : La table des matchs ne s'est pas chargée après 2 minutes pour la saison {season_name}.")
            logger.error("La protection anti-bot a peut-être bloqué l'accès. Passage à la saison suivante.")
            continue

        # --- Clic sur "Voir plus" ---
        while True:
            try:
                load_more_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.load_more a")))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", load_more_button)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", load_more_button)
                logger.info("Bouton 'Voir plus' cliqué. Attente du chargement...")
                time.sleep(3)
            except TimeoutException:
                logger.info(f"Tous les matchs pour {season_name} sont chargés.")
                break
            except Exception as e:
                logger.error(f"Erreur en cliquant sur 'Voir plus': {e}. Arrêt pour cette saison.")
                break
        
        # --- Extraction des données ---
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        match_rows = soup.select("table.matches-table tbody tr")
        logger.info(f"{len(match_rows)} matchs trouvés pour la saison {season_name}.")

        for row in match_rows:
            cells = row.find_all('td')
            if len(cells) > 3:
                date = cells[0].get_text(strip=True)
                home_team = cells[1].select_one("a.team-name").get_text(strip=True) if cells[1].select_one("a.team-name") else ""
                score = cells[2].select_one("a").get_text(strip=True) if cells[2].select_one("a") else ""
                away_team = cells[3].select_one("a.team-name").get_text(strip=True) if cells[3].select_one("a.team-name") else ""
                
                if home_team and away_team and score:
                    all_matches.append({'season': season_name, 'date': date, 'home_team': home_team, 'away_team': away_team, 'score': score})

    return pd.DataFrame(all_matches)

def main():
    logger.info("="*50)
    logger.info("Lancement du Scraper Botola Pro (Mode Automatisé)")
    logger.info("="*50)

    driver = initialize_driver()
    if driver is None: return

    try:
        final_df = scrape_all_seasons(driver, SEASONS_URLS)
        if not final_df.empty:
            output_file = "botola_matches_all_seasons.csv"
            final_df.to_csv(output_file, index=False, encoding='utf-8')
            logger.info(f"\n✅ Scraping terminé avec succès!")
            logger.info(f"Total de {len(final_df)} matchs sauvegardés dans '{output_file}'.")
            logger.info(final_df.head())
        else:
            logger.warning("Aucun match n'a été scrapé. Le fichier CSV est vide.")
    except Exception as e:
        logger.error(f"Erreur inattendue: {e}", exc_info=True)
    finally:
        if driver:
            logger.info("Fermeture du navigateur.")
            driver.quit()

if __name__ == "__main__":
    main()
