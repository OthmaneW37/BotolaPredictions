#!/usr/bin/env python3
"""
BOTOLA PREDICTION - Script Principal
=====================================
Outil complet de scraping et d'analyse de la Botola Pro
"""

import os
import sys
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_banner():
    """Affiche le bannière de bienvenue"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  🏆 BOTOLA PRO PREDICTION - DATA SCRAPER 🏆".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print()


def print_menu():
    """Affiche le menu principal"""
    print("┌" + "─" * 58 + "┐")
    print("│ MENU PRINCIPAL".ljust(59) + "│")
    print("├" + "─" * 58 + "┤")
    print("│ [1] 🔍 Inspecter la structure FootyStats.org        │")
    print("│ [2] 📥 Scraper les matchs de la Botola Pro          │")
    print("│ [3] 📊 Analyser les données sauvegardées            │")
    print("│ [4] ⚙️  Configuration et dépendances                 │")
    print("│ [5] 🚀 Mode automatique (inspection + scraping)     │")
    print("│ [0] 🚪 Quitter                                       │")
    print("└" + "─" * 58 + "┘")
    print()


def check_dependencies():
    """Vérifie les dépendances requises"""
    logger.info("🔍 Vérification des dépendances...")
    
    dependencies = {
        'selenium': 'Web scraping',
        'bs4': 'HTML parsing',
        'pandas': 'Analyse de données',
        'requests': 'Requêtes HTTP'
    }
    
    missing = []
    
    for package, description in dependencies.items():
        try:
            __import__(package)
            logger.info(f"✅ {package:15} - {description}")
        except ImportError:
            logger.warning(f"❌ {package:15} - {description}")
            missing.append(package)
    
    if missing:
        logger.warning(f"\n⚠️  Packages manquants: {', '.join(missing)}")
        logger.info("💡 Installation: pip install -r requirements.txt")
        return False
    
    logger.info("\n✅ Toutes les dépendances sont installées!\n")
    return True


def setup_directories():
    """Crée les répertoires nécessaires"""
    directories = [
        'data',
        'logs',
        'exports',
        'cache'
    ]
    
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        logger.info(f"✅ Répertoire créé/vérifié: {dir_name}/")


def run_inspection():
    """Lance l'inspection de FootyStats"""
    logger.info("\n" + "=" * 60)
    logger.info("🔍 INSPECTION DE FOOTYSTATS.ORG")
    logger.info("=" * 60)
    
    try:
        from inspect_footystats import inspect_footystats_structure
        inspect_footystats_structure()
        logger.info("\n✅ Inspection terminée!")
        logger.info("📂 Fichiers générés:")
        logger.info("   - footystats_structure.html")
        logger.info("   - footystats_analysis.json")
        return True
    except Exception as e:
        logger.error(f"❌ Erreur: {e}")
        return False


def run_scraper():
    """Lance le scraper principal (version Selenium)"""
    logger.info("\n" + "=" * 60)
    logger.info("SCRAPING DE LA BOTOLA PRO")
    logger.info("=" * 60)
    
    try:
        from scraper_footystats import run_footystats_scraper
        csv_file = run_footystats_scraper()
        
        if csv_file:
            logger.info(f"\n✅ Fichier de données sauvegardé: {csv_file}")
            return True
        else:
            logger.error("❌ Le scraping a échoué ou n'a retourné aucune donnée.")
            return False
            
    except ImportError:
        logger.error("❌ Erreur: Le module 'scraper_footystats' est introuvable.")
        return False
    except Exception as e:
        logger.error(f"❌ Une erreur inattendue est survenue: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


def analyze_data():
    """Analyse les données sauvegardées"""
    logger.info("\n" + "=" * 60)
    logger.info("📊 ANALYSE DES DONNÉES")
    logger.info("=" * 60)
    
    import pandas as pd
    import glob
    
    # Cherche les fichiers CSV
    csv_files = glob.glob("botola_matches*.csv")
    
    if not csv_files:
        logger.warning("❌ Aucun fichier CSV trouvé")
        return False
    
    # Utilise le plus récent
    latest_file = max(csv_files, key=os.path.getctime)
    logger.info(f"📖 Lecture de: {latest_file}")
    
    try:
        df = pd.read_csv(latest_file)
        
        logger.info(f"\n📈 STATISTIQUES:")
        logger.info(f"   Nombre de lignes: {len(df)}")
        logger.info(f"   Nombre de colonnes: {len(df.columns)}")
        logger.info(f"\n   Colonnes: {list(df.columns)}")
        
        if 'season' in df.columns:
            logger.info(f"\n   Saisons: {df['season'].unique().tolist()}")
        
        if 'home_team' in df.columns and 'away_team' in df.columns:
            all_teams = pd.concat([df['home_team'], df['away_team']]).unique()
            logger.info(f"   Équipes uniques: {len(all_teams)}")
            logger.info(f"   Équipes: {', '.join(sorted(all_teams)[:5])}...")
        
        # Statistiques des scores
        if 'home_goals' in df.columns and 'away_goals' in df.columns:
            logger.info(f"\n   Moyenne de buts domicile: {df['home_goals'].mean():.2f}")
            logger.info(f"   Moyenne de buts extérieur: {df['away_goals'].mean():.2f}")
        
        logger.info(f"\n✅ Aperçu des 5 premiers matchs:")
        print(df.head().to_string())
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'analyse: {e}")
        return False


def show_config():
    """Affiche la configuration du projet"""
    logger.info("\n" + "=" * 60)
    logger.info("⚙️  CONFIGURATION DU PROJET")
    logger.info("=" * 60)
    
    config = {
        "Nom du projet": "Botola Pro Prediction",
        "Source de données": "FootyStats.org",
        "Ligue": "Botola Pro (Maroc)",
        "Saisons cibles": "2021/2022, 2022/2023, 2023/2024",
        "Méthode": "Web Scraping (Selenium + BeautifulSoup)",
        "Protection": "Gestion de Cloudflare",
        "Format de sortie": "CSV + Analysis"
    }
    
    for key, value in config.items():
        logger.info(f"  {key:20} : {value}")
    
    logger.info("\n📂 RÉPERTOIRES:")
    for dir_name in ['data', 'logs', 'exports', 'cache']:
        exists = "✅" if os.path.exists(dir_name) else "❌"
        logger.info(f"  {exists} {dir_name}/")
    
    logger.info("\n📋 DÉPENDANCES:")
    check_dependencies()


def auto_mode():
    """Mode automatique: inspection + scraping"""
    logger.info("\n" + "=" * 60)
    logger.info("🚀 MODE AUTOMATIQUE")
    logger.info("=" * 60)
    
    choice = input("\n1️⃣  Voulez-vous inspecter d'abord? (o/n): ").strip().lower()
    
    if choice in ['o', 'y', 'yes', 'oui']:
        if not run_inspection():
            logger.warning("⚠️  Inspection échouée, continuant quand même...")
        input("\n✅ Appuyez sur Entrée pour continuer au scraping...")
    
    return run_scraper()


def main_menu():
    """Boucle principale du menu"""
    print_banner()
    
    while True:
        print_menu()
        choice = input("Choisissez une option (0-5): ").strip()
        
        print()
        
        if choice == '0':
            logger.info("👋 Au revoir!")
            break
        elif choice == '1':
            run_inspection()
        elif choice == '2':
            run_scraper()
        elif choice == '3':
            analyze_data()
        elif choice == '4':
            show_config()
        elif choice == '5':
            auto_mode()
        else:
            logger.warning("❌ Option invalide!")
        
        input("\n🔄 Appuyez sur Entrée pour retourner au menu...")


def main():
    """Point d'entrée principal"""
    print_banner()
    
    # Vérifications initiales
    logger.info("⚙️  INITIALISATION DU PROJET")
    logger.info("=" * 60)
    
    setup_directories()
    
    has_deps = check_dependencies()
    
    if not has_deps:
        logger.error("\n❌ Merci d'installer les dépendances avant de continuer")
        logger.info("💡 Exécutez: pip install -r requirements.txt")
        sys.exit(1)
    
    logger.info("✅ Projet prêt!")
    
    # Lance le menu
    main_menu()


if __name__ == "__main__":
    main()
