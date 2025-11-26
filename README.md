# 🏆 Botola Pro Prediction - Data Scraper

Outil complet de **scraping, nettoyage et analyse** de données de la **Botola Pro** (ligue marocaine de football) depuis **FootyStats.org**.

## 📋 Table des matières

- [Vue d'ensemble](#vue-densemble)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Architecture](#architecture)
- [Dépendances](#dépendances)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Vue d'ensemble

Ce projet automatise l'extraction de données de matches de football de la Botola Pro pour créer un dataset de Machine Learning.

### Données extraites

- **Informations du match**: Date, heure, équipes, score
- **Statistiques du match**: Tirs, possession, passes, etc.
- **Statistiques avancées**: xG (expected goals), si disponibles
- **Métadonnées**: Saison, arbitre, public

### Saisons disponibles

- 2021/2022
- 2022/2023
- 2023/2024

---

## 💾 Installation

### 1. Prérequis

- **Python 3.8+** (vérifier: `python --version`)
- **pip** (gestionnaire de paquets Python)
- **Chrome/Chromium** (installé sur le système)

### 2. Cloner/Copier le projet

```bash
cd "D:\Projets Dev\BotolaPrediction"
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

**Note**: Sur Windows PowerShell, utilisez:
```powershell
pip install -r requirements.txt
```

### 4. Vérifier l'installation

```bash
python main.py
```

Vous devriez voir le menu principal.

---

## 🚀 Utilisation

### Mode interactif (recommandé)

```bash
python main.py
```

**Menu disponible:**
1. 🔍 **Inspecter** la structure de FootyStats
2. 📥 **Scraper** les matchs
3. 📊 **Analyser** les données
4. ⚙️ **Configuration**
5. 🚀 **Mode automatique**

### Mode direct - Inspection uniquement

```bash
python inspect_footystats.py
```

Cela va:
- Charger la page FootyStats
- Contourner Cloudflare
- Analyser la structure HTML
- Sauvegarder `footystats_structure.html` et `footystats_analysis.json`

### Mode direct - Scraping uniquement

```bash
python botola_scraper.py
```

Cela va:
- Scraper les 3 dernières saisons
- Créer un fichier CSV: `botola_matches_YYYYMMDD_HHMMSS.csv`
- Afficher les statistiques

### Mode programme (Python)

```python
from botola_scraper import BotolaScraper

with BotolaScraper(headless=True) as scraper:
    df = scraper.scrape_multiple_seasons(["2023/2024", "2022/2023"])
    scraper.save_to_csv(df, "my_botola_data.csv")
```

---

## 📂 Architecture

```
BotolaPrediction/
├── main.py                      # 🎯 Point d'entrée principal
├── botola_scraper.py            # 📥 Scraper principal (classe BotolaScraper)
├── inspect_footystats.py        # 🔍 Inspection de la structure
├── requirements.txt             # 📦 Dépendances
├── README.md                    # 📖 Ce fichier
├── botola_scraper.log          # 📝 Logs des opérations
├── botola_matches_*.csv        # 💾 Données sauvegardées
├── footystats_structure.html   # 🌐 HTML inspectionné
├── footystats_analysis.json    # 📊 Analyse metadata
└── data/                        # 📂 Répertoire des données
    ├── logs/
    ├── exports/
    └── cache/
```

---

## 📦 Dépendances

### Packages principaux

| Package | Version | Utilité |
|---------|---------|---------|
| `selenium` | >=4.0.0 | Automatisation navigateur (gestion Cloudflare) |
| `webdriver-manager` | >=3.8.0 | Gestion automatique du ChromeDriver |
| `beautifulsoup4` | >=4.9.0 | Parsing HTML/XML |
| `pandas` | >=1.3.0 | Manipulation de DataFrames |
| `requests` | >=2.26.0 | Requêtes HTTP |
| `lxml` | >=4.6.0 | Parser HTML rapide |

### Installation manuelle

```bash
pip install selenium>=4.0.0
pip install webdriver-manager>=3.8.0
pip install beautifulsoup4>=4.9.0
pip install pandas>=1.3.0
pip install requests>=2.26.0
pip install lxml>=4.6.0
```

---

## 🔧 Configuration

### Variables environnementales (optionnel)

```bash
# Windows PowerShell
$env:BOTOLA_HEADLESS = $true      # Lancer en mode headless
$env:BOTOLA_TIMEOUT = 30          # Délai max pour charger (secondes)
```

### Paramètres dans le code

Modifier `botola_scraper.py`:

```python
# Ligne ~320 dans main()
seasons = ["2023/2024", "2022/2023", "2021/2022"]  # Ajuster les saisons

# Ligne ~324
with BotolaScraper(headless=False) as scraper:     # headless=True pour mode invisible
```

---

## 📊 Structure des données en sortie

### Fichier CSV généré

```csv
date,time,home_team,away_team,score,home_goals,away_goals,xg_home,xg_away,shots_home,shots_away,possession_home,possession_away,season
2024-01-15,15:00,Raja Casablanca,Wydad,2-1,2,1,1.5,0.8,7,5,55,45,2023/2024
```

### Colonnes disponibles

- `date` - Date du match (YYYY-MM-DD)
- `time` - Heure du match (HH:MM)
- `home_team` - Équipe domicile
- `away_team` - Équipe extérieur
- `score` - Score brut (ex: "2-1")
- `home_goals` - Buts marqués à domicile
- `away_goals` - Buts marqués en extérieur
- `xg_home` - Expected Goals domicile
- `xg_away` - Expected Goals extérieur
- `shots_home` - Tirs en direction domicile
- `shots_away` - Tirs en direction extérieur
- `possession_home` - Possession (%) domicile
- `possession_away` - Possession (%) extérieur
- `season` - Saison (YYYY/YYYY)

---

## 🐛 Troubleshooting

### ❌ Erreur: "No module named 'selenium'"

**Solution:**
```bash
pip install selenium
```

### ❌ Erreur: "ChromeDriver version mismatch"

**Solution:**
```bash
pip install --upgrade webdriver-manager
```

Le paquet va télécharger automatiquement le bon version.

### ❌ Erreur: "Cloudflare challenge failed"

**Solution:**
- Augmenter le délai d'attente dans `botola_scraper.py` ligne 115:
  ```python
  wait_time=30  # Au lieu de 15
  ```
- Utiliser le mode non-headless pour déboguer:
  ```python
  scraper = BotolaScraper(headless=False)
  ```

### ❌ Site BlockListe "Too many requests"

**Solution:**
- Ajouter des délais entre les requêtes dans `scrape_multiple_seasons()`:
  ```python
  time.sleep(5)  # Au lieu de 2
  ```

### ⚠️ Scraper très lent

**Solution:**
- Utiliser le mode headless:
  ```python
  with BotolaScraper(headless=True) as scraper:
  ```
- Réduire le nombre de saisons

### ❌ CSV vide ou colonnes manquantes

**Solution:**
1. Exécuter l'inspection d'abord:
   ```bash
   python inspect_footystats.py
   ```
2. Vérifier `footystats_structure.html`
3. Adapter les sélecteurs CSS dans `botola_scraper.py` si la structure a changé

---

## 💡 Conseils d'utilisation

### Pour le Machine Learning

```python
import pandas as pd

# Charger les données
df = pd.read_csv("botola_matches.csv")

# Nettoyer les données manquantes
df = df.dropna(subset=['home_goals', 'away_goals'])

# Créer des features
df['total_goals'] = df['home_goals'] + df['away_goals']
df['goal_diff'] = df['home_goals'] - df['away_goals']

# Exporter
df.to_csv("botola_clean.csv", index=False)
```

### Performance

- **Mode headless**: ~30s par saison
- **Mode visuel**: ~2min par saison
- **Avec inspection HTML**: +10s supplémentaires

### Limites

- ⚠️ FootyStats peut bloquer après trop de requêtes
- ⚠️ Les données xG peuvent ne pas être disponibles pour tous les matchs
- ⚠️ Certaines équipes peut avoir des noms variables

---

## 📝 Logs

Les logs sont sauvegardés dans `botola_scraper.log`:

```
2024-01-15 10:30:45 - INFO - ✅ Driver Selenium initialisé
2024-01-15 10:30:46 - INFO - 📄 Chargement de https://footystats.org/...
2024-01-15 10:31:15 - INFO - ✅ Page chargée avec succès
```

---

## 📄 Licence

Public (Utilisation pédagogique)

---

## 🤝 Support

Pour des problèmes:

1. Vérifier les logs: `botola_scraper.log`
2. Exécuter l'inspection: `python inspect_footystats.py`
3. Vérifier que Chrome est installé
4. Tester avec une seule saison d'abord

---

## 🎓 Apprentissage

Ce projet démontre:

- ✅ **Web Scraping** avec Selenium
- ✅ **Gestion de Cloudflare** et protections anti-bot
- ✅ **Parsing HTML** avancé (BeautifulSoup)
- ✅ **Automatisation** de tâches
- ✅ **Traitement de données** (Pandas)
- ✅ **Logging** et gestion d'erreurs
- ✅ **Pattern Design** (Context Manager)

---

Dernière mise à jour: **Novembre 2025** 🎉
