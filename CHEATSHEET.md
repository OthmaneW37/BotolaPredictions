# 📋 CHEATSHEET - Commandes essentielles

## Installation

```powershell
# Aller au répertoire du projet
cd "D:\Projets Dev\BotolaPrediction"

# Installer toutes les dépendances
pip install -r requirements.txt
```

## Vérification

```powershell
# Test complet
python test_install.py

# Afficher la configuration
python main.py  # Puis sélectionner [4]
```

## Inspection (Étape 1 - Optionnel mais recommandé)

```powershell
# Analyser la structure HTML de FootyStats
python inspect_footystats.py

# Cela va créer:
# - footystats_structure.html (pour debug)
# - footystats_analysis.json (métadonnées)
```

## Scraping (Étape 2 - Principal)

### Option A: Mode interactif (recommandé)

```powershell
python main.py
# Puis sélectionner [2] pour scraper
```

### Option B: Lancer directement

```powershell
python botola_scraper.py
```

### Option C: Mode automatique (inspection + scraping)

```powershell
python main.py
# Puis sélectionner [5]
```

## Analyse des données (Étape 3)

### Option A: Via le menu

```powershell
python main.py
# Puis sélectionner [3]
```

### Option B: En Python

```powershell
python -c "
import pandas as pd
df = pd.read_csv('botola_matches.csv')
print(df.info())
print(df.head(10))
print(f'Nombre de matchs: {len(df)}')
print(f'Saisons: {df[\"season\"].unique()}')
"
```

## Personnalisation

### Modifier les saisons à scraper

Éditer `botola_scraper.py` ligne ~319:

```python
seasons = ["2023/2024", "2022/2023"]  # Ajouter/supprimer les saisons
```

### Mode headless (sans interface)

Éditer `botola_scraper.py` ligne ~320:

```python
with BotolaScraper(headless=True) as scraper:  # Mettre à True
```

### Augmenter le timeout (pour Cloudflare)

Éditer `botola_scraper.py` ligne ~115:

```python
wait_time=30  # Au lieu de 15 (en secondes)
```

## Visualiser les résultats

```powershell
# Lister les fichiers CSV créés
Get-ChildItem -Filter "botola_*.csv"

# Voir les 5 premières lignes
Get-Content botola_matches.csv -Head 5

# Statistiques rapides
python -c "import pandas as pd; print(pd.read_csv('botola_matches.csv').describe())"
```

## Nettoyer

```powershell
# Supprimer les anciens fichiers
Remove-Item botola_matches*.csv

# Supprimer les fichiers d'inspection
Remove-Item footystats_structure.html, footystats_analysis.json

# Nettoyer les logs
Clear-Content botola_scraper.log
```

## Troubleshooting - Commandes rapides

```powershell
# Si erreur "module not found"
pip install --upgrade -r requirements.txt

# Si ChromeDriver n'est pas trouvé
pip install --upgrade webdriver-manager

# Si timeout Cloudflare
# → Augmenter wait_time dans botola_scraper.py (voir ci-dessus)

# Si trop de requêtes bloquées
# → Augmenter delay_between_requests dans botola_scraper.py

# Voir les logs détaillés
Get-Content botola_scraper.log -Tail 50  # Dernières 50 lignes
```

## Flux de travail complet

```powershell
# 1. Installation
pip install -r requirements.txt

# 2. Vérification
python test_install.py

# 3. Inspection (optionnel)
python inspect_footystats.py

# 4. Scraping
python botola_scraper.py

# 5. Vérifier le résultat
python -c "import pandas as pd; print(pd.read_csv('botola_matches.csv').shape)"

# 6. Analyser
python main.py  # Sélectionner [3]
```

## Export pour ML/Analyse

```powershell
# Convertir en JSON
python -c "
import pandas as pd
df = pd.read_csv('botola_matches.csv')
df.to_json('botola_matches.json', orient='records', indent=2)
"

# Convertir en Excel
python -c "
import pandas as pd
df = pd.read_csv('botola_matches.csv')
df.to_excel('botola_matches.xlsx', index=False)
"
# (Nécessite: pip install openpyxl)

# Convertir en Parquet (plus compact)
python -c "
import pandas as pd
df = pd.read_csv('botola_matches.csv')
df.to_parquet('botola_matches.parquet')
"
# (Nécessite: pip install pyarrow)
```

## Monitoring / Logs

```powershell
# Afficher les logs en temps réel
Get-Content -Path botola_scraper.log -Wait

# Filtrer les erreurs
Select-String -Path botola_scraper.log -Pattern "ERROR|❌"

# Compter les matchs scrapés
(Select-String -Path botola_scraper.log -Pattern "Match extrait").Count
```

## Ressources

- 📖 Lire le README complet: `README.md`
- 🚀 Guide rapide (5 min): `QUICKSTART.md`
- 🔧 Configuration: `config.ini`
- 📊 Données: `botola_matches.csv`
- 📝 Logs: `botola_scraper.log`

## Contact / Help

```powershell
# Afficher l'aide du scraper
python botola_scraper.py --help  # Si implémenté

# Executer en debug
python -m pdb botola_scraper.py

# Exécuter avec verbose
python botola_scraper.py 2>&1 | Tee-Object -FilePath debug.log
```

---

**💡 Conseil**: Gardez ce document à proximité pendant votre travail avec le scraper!
