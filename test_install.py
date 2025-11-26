#!/usr/bin/env python3
"""
TEST RAPIDE - Vérification de l'installation
=============================================
Script pour vérifier que tout est bien configuré avant le scraping
"""

import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def check_python_version():
    """Vérifie la version de Python"""
    logger.info("\n📌 Vérification Python")
    logger.info("-" * 50)
    
    if sys.version_info >= (3, 8):
        logger.info(f"✅ Python {sys.version.split()[0]} (OK)")
        return True
    else:
        logger.error(f"❌ Python {sys.version.split()[0]} (Minimum: 3.8)")
        return False


def check_pip():
    """Vérifie pip"""
    logger.info("\n📌 Vérification pip")
    logger.info("-" * 50)
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            logger.info(f"✅ {result.stdout.strip()}")
            return True
    except:
        pass
    
    logger.error("❌ pip non accessible")
    return False


def check_packages():
    """Vérifie les packages Python"""
    logger.info("\n📌 Vérification des packages Python")
    logger.info("-" * 50)
    
    packages = {
        'selenium': 'Web scraping',
        'bs4': 'HTML parsing',
        'pandas': 'Analyse de données',
        'requests': 'Requêtes HTTP',
        'webdriver_manager': 'Gestion du driver',
        'lxml': 'Parser HTML'
    }
    
    all_installed = True
    
    for package, description in packages.items():
        try:
            __import__(package)
            logger.info(f"✅ {package:20} - {description}")
        except ImportError:
            logger.error(f"❌ {package:20} - {description}")
            all_installed = False
    
    return all_installed


def check_chrome():
    """Vérifie si Chrome est installé"""
    logger.info("\n📌 Vérification de Chrome")
    logger.info("-" * 50)
    
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Chromium\Application\chrome.exe",
    ]
    
    import os
    for path in chrome_paths:
        if os.path.exists(path):
            logger.info(f"✅ Chrome trouvé: {path}")
            return True
    
    logger.warning("⚠️  Chrome non trouvé dans les chemins standards")
    logger.info("   Les webdrivers peuvent le télécharger automatiquement")
    return None  # Warning, pas blocker


def check_internet():
    """Vérifie la connexion Internet"""
    logger.info("\n📌 Vérification Internet")
    logger.info("-" * 50)
    
    try:
        import requests
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            logger.info("✅ Connexion Internet OK")
            return True
    except:
        pass
    
    logger.error("❌ Pas de connexion Internet")
    return False


def check_footystats():
    """Vérifie que FootyStats est accessible"""
    logger.info("\n📌 Vérification de FootyStats.org")
    logger.info("-" * 50)
    
    try:
        import requests
        response = requests.get(
            "https://footystats.org/morocco/botola-pro/matches",
            timeout=10
        )
        if response.status_code == 200:
            logger.info("✅ FootyStats.org accessible")
            return True
        else:
            logger.warning(f"⚠️  Status code: {response.status_code}")
            logger.info("   (Peut être bloqué, Selenium le gère)")
            return None
    except Exception as e:
        logger.warning(f"⚠️  Erreur: {str(e)[:50]}")
        logger.info("   (Selenium peut contourner cela)")
        return None


def check_disk_space():
    """Vérifie l'espace disque"""
    logger.info("\n📌 Vérification de l'espace disque")
    logger.info("-" * 50)
    
    try:
        import shutil
        total, used, free = shutil.disk_usage("/")
        free_gb = free // (1024**3)
        
        if free_gb > 1:
            logger.info(f"✅ Espace libre: {free_gb} GB")
            return True
        else:
            logger.warning(f"⚠️  Espace libre: {free_gb} GB (limite)")
            return None
    except:
        logger.info("⚠️  Impossible de vérifier l'espace disque")
        return None


def main():
    """Exécute tous les tests"""
    logger.info("\n" + "╔" + "═" * 48 + "╗")
    logger.info("║" + "  🔧 TEST RAPIDE DE L'INSTALLATION  ".center(48) + "║")
    logger.info("╚" + "═" * 48 + "╝")
    
    results = {
        "Python": check_python_version(),
        "pip": check_pip(),
        "Packages": check_packages(),
        "Chrome": check_chrome(),
        "Internet": check_internet(),
        "FootyStats": check_footystats(),
        "Disque": check_disk_space(),
    }
    
    # Résumé
    logger.info("\n" + "=" * 50)
    logger.info("📊 RÉSUMÉ")
    logger.info("=" * 50)
    
    critical_ok = all(v is not False for v in [
        results["Python"],
        results["pip"],
        results["Packages"],
        results["Internet"]
    ])
    
    for test, result in results.items():
        if result is True:
            status = "✅"
        elif result is None:
            status = "⚠️"
        else:
            status = "❌"
        logger.info(f"{status} {test}")
    
    logger.info("=" * 50)
    
    if critical_ok:
        logger.info("\n✅ PRÊT POUR LE SCRAPING!\n")
        logger.info("Exécutez: python main.py\n")
        return 0
    else:
        logger.error("\n❌ PROBLÈMES DÉTECTÉS\n")
        logger.error("Merci de corriger les erreurs critiques avant de continuer.\n")
        logger.error("Installez les packages: pip install -r requirements.txt\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
