# 🔧 GUIDE D'ADAPTATION DU SCRAPER

Si FootyStats.org change sa structure HTML, voici comment adapter le scraper.

## 🔍 Étape 1: Identifier les changements

### 1.1 Inspecter le site

```powershell
python inspect_footystats.py
```

Cela crée `footystats_structure.html` que vous pouvez ouvrir dans un navigateur.

### 1.2 Ouvrir dans un navigateur

```powershell
# Windows
Start "footystats_structure.html"

# Ou manuellement: D:\Projets Dev\BotolaPrediction\footystats_structure.html
```

### 1.3 Inspecter avec DevTools

1. Aller à https://footystats.org/morocco/botola-pro/matches
2. Appuyer sur `F12` (DevTools)
3. Onglet "Elements/Inspector"
4. Chercher:
   - Tableau des matchs
   - Lignes (TR)
   - Cellules (TD)
   - Classes CSS
   - Attributs data-*

## 📋 Étape 2: Examiner les sélecteurs CSS actuels

Dans `botola_scraper.py`, cherchez:

```python
# Ligne ~145
def _parse_match_row(self, row, cells: List) -> Dict:
    """Parse une ligne de match"""
    
    # Actuellement supposé:
    date_str = cells[0].get_text(strip=True)
    time_str = cells[1].get_text(strip=True)
    home_team = cells[2].get_text(strip=True)
    score_str = cells[3].get_text(strip=True)
    away_team = cells[4].get_text(strip=True)
```

## 🛠️ Étape 3: Adapter les sélecteurs

### Cas 1: Structure de tableau changée

Si les colonnes sont dans un ordre différent, adaptez les indices:

```python
# AVANT:
date_str = cells[0].get_text(strip=True)
time_str = cells[1].get_text(strip=True)
home_team = cells[2].get_text(strip=True)

# APRÈS (si l'ordre change):
date_str = cells[1].get_text(strip=True)    # Colonne 1 au lieu de 0
time_str = cells[0].get_text(strip=True)    # Colonne 0 au lieu de 1
home_team = cells[3].get_text(strip=True)   # Colonne 3 au lieu de 2
```

### Cas 2: Nouvelles classes CSS

Si FootyStats ajoute des classes:

```python
# AVANT:
rows = soup.find_all('tr')

# APRÈS (si le site ajoute une classe):
rows = soup.find_all('tr', class_='match-row')  # Nouvelle classe
```

### Cas 3: Structure complètement différente (divs au lieu de tableau)

```python
# Si FootyStats passe de <table> à <div>:

def extract_matches_from_page(self, soup: BeautifulSoup) -> List[Dict]:
    matches = []
    
    # ANCIEN CODE:
    # table_rows = soup.find_all('tr')
    
    # NOUVEAU CODE:
    match_divs = soup.find_all('div', class_='match-container')
    
    for div in match_divs:
        match_data = self._parse_match_div(div)  # Nouvelle méthode
        if match_data:
            matches.append(match_data)
    
    return matches

def _parse_match_div(self, div) -> Dict:
    """Parse une div de match (nouvelle structure)"""
    try:
        date = div.find('span', class_='match-date').get_text(strip=True)
        home = div.find('div', class_='home-team').get_text(strip=True)
        away = div.find('div', class_='away-team').get_text(strip=True)
        score = div.find('span', class_='score').get_text(strip=True)
        
        # ... reste du parsing
        return {...}
    except Exception as e:
        return None
```

## 🧪 Étape 4: Tester vos changements

```python
# Créer un script de test
from botola_scraper import BotolaScraper
from bs4 import BeautifulSoup

scraper = BotolaScraper()

# Tester une seule page
success, soup = scraper.get_page_with_selenium(
    "https://footystats.org/morocco/botola-pro/matches"
)

if success:
    # Tester le parsing
    matches = scraper.extract_matches_from_page(soup)
    
    print(f"Matchs trouvés: {len(matches)}")
    if matches:
        print(f"Premier match: {matches[0]}")
```

Exécuter:
```powershell
python -c "
from botola_scraper import BotolaScraper
scraper = BotolaScraper()
scraper.init_driver()
success, soup = scraper.get_page_with_selenium('https://footystats.org/morocco/botola-pro/matches')
if success:
    matches = scraper.extract_matches_from_page(soup)
    print(f'Matchs: {len(matches)}')
    if matches:
        print(matches[0])
scraper.close()
"
```

## 📐 Cas d'usage courants

### Les cellules ne contiennent que des espacements

Utiliser `.get_text()` sans arguments:

```python
# AVANT:
text = cells[0].get_text(strip=True)

# APRÈS:
text = cells[0].get_text().strip()
# Ou:
text = cells[0].text.strip()
```

### Les données sont dans des attributs (data-*)

```python
# Si le score est dans: <td data-score="2-1">
score = cells[3].get('data-score', '')

# Ou dans un titre:
score = cells[3].get('title', '')
```

### Les équipes sont dans des liens

```python
# Si home_team est: <td><a href="...">Raja</a></td>
home_team = cells[2].find('a').get_text(strip=True)
```

### Les dates sont mal formatées

```python
from datetime import datetime

# Avant de sauvegarder:
date_str = cells[0].get_text(strip=True)

# Parser au format corrèct
try:
    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
    date_str = date_obj.strftime('%Y-%m-%d')
except:
    pass  # Garder le format original
```

## 🔄 Workflow d'adaptation

1. **Inspectez** : `python inspect_footystats.py`
2. **Analysez** : Ouvrez `footystats_structure.html`
3. **Identifiez** : Les nouveaux sélecteurs CSS
4. **Modifiez** : Le code dans `botola_scraper.py`
5. **Testez** : Exécutez le script de test
6. **Validez** : Vérifiez quelques matchs dans le CSV
7. **Lancez** : `python botola_scraper.py` en production

## 🚨 Signaux d'alerte

Si vous voyez ceci dans `botola_scraper.log`:

```
❌ Ligne ignorée: ...
```

→ C'est que le parsing échoue pour certaines lignes

```
⚠️ Aucun match trouvé
```

→ Les sélecteurs CSS ont changé ou la page n'a pas chargé

```
❌ Échec du chargement de la page
```

→ Problème de Cloudflare ou le timeout est trop court

## 📞 Déboguer en détail

```python
from botola_scraper import BotolaScraper
from bs4 import BeautifulSoup

scraper = BotolaScraper()
scraper.init_driver()

success, soup = scraper.get_page_with_selenium(
    "https://footystats.org/morocco/botola-pro/matches",
    wait_time=20
)

if success:
    # Afficher la structure
    print("=== TABLES TROUVÉES ===")
    tables = soup.find_all('table')
    print(f"Nombre: {len(tables)}")
    
    if tables:
        print("\n=== PREMIÈRE TABLE ===")
        rows = tables[0].find_all('tr')
        print(f"Lignes: {len(rows)}")
        
        # Première ligne de données
        if len(rows) > 1:
            row = rows[1]
            cells = row.find_all('td')
            print(f"Cellules: {len(cells)}")
            
            for i, cell in enumerate(cells[:6]):
                print(f"[{i}] {cell.get_text(strip=True)[:50]}")

scraper.close()
```

## 📝 Committing les changements

Après adaptation réussie:

```powershell
# Créer un backup
Copy-Item botola_scraper.py botola_scraper.backup.py

# Documenter les changements
# (Éditer le début du fichier)

# Tester complètement
python botola_scraper.py

# Valider les résultats
python -c "import pandas as pd; print(pd.read_csv('botola_matches.csv').shape)"
```

## 💾 Versions précédentes

Gardez toujours un backup:

```powershell
# Avant de modifier
Copy-Item botola_scraper.py "botola_scraper_v1.0.py"

# Après modification réussie
Copy-Item botola_scraper.py "botola_scraper_v2.0.py"
```

---

**💡 Pro Tip**: Les changements de site sont généralement prévisibles. Relancez l'inspection périodiquement pour détecter les modifications avant qu'elles ne cassent le scraper!
