from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# 1. Configuration (On garde le navigateur visible pour gérer les captchas si besoin)
options = webdriver.ChromeOptions()
# options.add_argument("--headless") # Ne pas activer pour l'instant
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # 2. URL de la Botola sur FootyStats
    # Astuce : Ajoute /matches à la fin pour tomber direct sur la liste
    url = "https://footystats.org/morocco/botola-pro/matches" 
    print(f"Connexion à {url}...")
    driver.get(url)

    # 3. PAUSE CRITIQUE : Contournement Anti-Bot
    print("⏳ Attente de 10 secondes (Si Cloudflare demande une vérification, fais-la manuellement !)...")
    time.sleep(10) 

    # 4. Récupération du HTML
    # On prend tout le code de la page une fois chargée
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    # 5. Extraction des données (Logique FootyStats)
    # FootyStats met souvent les matchs dans une structure de table ou de div spécifique.
    # On va chercher les lignes qui contiennent des infos de match.
    
    matchs_data = []
    
    # Recherche générique des lignes de matchs (à adapter selon l'inspection)
    # Souvent, les lignes ont la classe 'matchRow' ou sont dans une table 'matches-table'
    rows = soup.find_all('tr') # On tente de trouver toutes les lignes de tableau

    print(f"Nombre de lignes trouvées (brut) : {len(rows)}")

    for row in rows:
        try:
            # Ceci est un exemple, il faudra affiner les selecteurs (voir Étape 5 ci-dessous)
            text_row = row.get_text(separator="|", strip=True)
            
            # Filtre simple : on ne garde que les lignes qui ressemblent à un score (ex: contient "FT")
            if "FT" in text_row or "Terminé" in text_row:
                matchs_data.append(text_row)
        except:
            continue

    # 6. Sauvegarde rapide pour analyse
    print("Exemple des 5 premiers matchs trouvés :")
    for m in matchs_data[:5]:
        print(m)

    # Convertir en DataFrame (très brut pour l'instant)
    df = pd.DataFrame(matchs_data, columns=["Raw_Data"])
    df.to_csv("botola_raw.csv", index=False)
    print("✅ Données brutes sauvegardées dans 'botola_raw.csv'")

except Exception as e:
    print(f"❌ Erreur : {e}")

finally:
    # driver.quit() # Laisse ouvert pour vérifier
    pass