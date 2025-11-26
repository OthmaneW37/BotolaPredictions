"""
INSPECTION FOOTYSTATS - Analyse de la structure HTML
====================================================
Utilisé pour identifier les sélecteurs CSS exacts et la structure des données
"""

import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


def inspect_footystats_structure():
    """Inspecte la structure HTML de FootyStats pour extraire les sélecteurs"""
    
    url = "https://footystats.org/morocco/botola-pro/matches"
    
    logger.info("🔍 Inspection de FootyStats.org...")
    logger.info(f"URL: {url}")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    try:
        logger.info("⏳ Chargement de la page (attente Cloudflare)...")
        driver.get(url)
        
        # Attend que les éléments se chargent
        time.sleep(10)
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
        )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Inspecte la structure
        logger.info("\n" + "="*60)
        logger.info("📋 STRUCTURE DÉTECTÉE")
        logger.info("="*60)
        
        # Cherche les tables
        tables = soup.find_all('table')
        logger.info(f"\n📊 Nombre de tables trouvées: {len(tables)}")
        
        # Analyse la première table de matchs
        if tables:
            main_table = tables[0]
            logger.info("\n🔎 Première table (matchs):")
            
            # En-têtes
            headers = main_table.find_all('th')
            if headers:
                logger.info(f"  En-têtes ({len(headers)}):")
                for i, h in enumerate(headers):
                    logger.info(f"    [{i}] {h.get_text(strip=True)}")
            
            # Premières lignes
            rows = main_table.find_all('tr')[1:4]  # Skip en-têtes
            logger.info(f"\n  Premières lignes ({len(rows)}):")
            
            for row_idx, row in enumerate(rows):
                cells = row.find_all('td')
                logger.info(f"\n  ◆ Ligne {row_idx + 1}:")
                for cell_idx, cell in enumerate(cells[:6]):  # Premiers 6 éléments
                    text = cell.get_text(strip=True)[:50]  # Tronque à 50 chars
                    logger.info(f"      [{cell_idx}] {text}")
        
        # Cherche les divs avec classe contenant 'match'
        logger.info("\n\n🔍 Divs avec 'match' dans la classe:")
        match_divs = soup.find_all(class_=lambda x: x and 'match' in x.lower())
        logger.info(f"   Trouvés: {len(match_divs)}")
        if match_divs[:3]:
            for div in match_divs[:3]:
                logger.info(f"   - {div.get('class', [])} : {div.get_text(strip=True)[:40]}")
        
        # Sauvegarde le HTML pour inspection manuelle
        with open("footystats_structure.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        logger.info("\n✅ HTML sauvegardé dans: footystats_structure.html")
        
        # Export de données brutes
        data_summary = {
            "url": url,
            "tables_found": len(tables),
            "match_divs_found": len(match_divs),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open("footystats_analysis.json", "w", encoding="utf-8") as f:
            json.dump(data_summary, f, indent=2)
        
        logger.info("✅ Analyse sauvegardée dans: footystats_analysis.json")
        
        return soup
        
    except Exception as e:
        logger.error(f"❌ Erreur: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None
    
    finally:
        driver.quit()


def manual_html_inspection():
    """Permet une inspection manuelle du HTML sauvegardé"""
    try:
        with open("footystats_structure.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        logger.info("\n📖 Inspection du fichier HTML sauvegardé")
        
        # Cherche tous les attributs data- qui pourraient être utiles
        all_elements = soup.find_all(attrs={"data-stat": True})
        logger.info(f"\nÉléments avec data-stat: {len(all_elements)}")
        
        # Cherche les classes d'équipes
        team_elements = soup.find_all(class_=lambda x: x and ('team' in x.lower() or 'team-name' in x.lower()))
        logger.info(f"Éléments équipe: {len(team_elements)}")
        
        # Cherche les scores
        score_elements = soup.find_all(class_=lambda x: x and 'score' in x.lower())
        logger.info(f"Éléments score: {len(score_elements)}")
        if score_elements[:3]:
            for elem in score_elements[:3]:
                logger.info(f"  - {elem.get('class', [])} : {elem.get_text(strip=True)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors de la lecture du HTML: {e}")
        return False


if __name__ == "__main__":
    logger.info("🚀 DÉMARRAGE DE L'INSPECTION")
    logger.info("="*60)
    
    # Étape 1: Scrape et analyse
    logger.info("\n📡 Étape 1: Scraping et analyse...")
    soup = inspect_footystats_structure()
    
    # Étape 2: Inspection du fichier sauvegardé
    if soup:
        logger.info("\n🔍 Étape 2: Inspection détaillée...")
        manual_html_inspection()
    
    logger.info("\n" + "="*60)
    logger.info("✅ Inspection terminée!")
    logger.info("📂 Fichiers créés:")
    logger.info("   - footystats_structure.html (HTML complet)")
    logger.info("   - footystats_analysis.json (Métadonnées)")
