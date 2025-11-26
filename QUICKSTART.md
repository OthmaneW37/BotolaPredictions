# 🚀 GUIDE DE DÉMARRAGE RAPIDE

## ⏱️ 5 minutes pour commencer

### Étape 1: Installation (2 min)

```powershell
# Ouvrir PowerShell dans le dossier du projet
cd "D:\Projets Dev\BotolaPrediction"

# Installer les dépendances
pip install -r requirements.txt
```

### Étape 2: Test (1 min)

```powershell
# Vérifier que tout fonctionne
python test_install.py
```

Vous devriez voir:
```
✅ Python 3.x
✅ pip
✅ Packages
✅ Internet
✅ FootyStats.org
```

### Étape 3: Inspecter (1 min)

```powershell
# Comprendre la structure du site
python inspect_footystats.py
```

Cela va:
- Charger FootyStats.org
- Analyser la structure HTML
- Créer `footystats_structure.html`

### Étape 4: Scraper (1 min)

```powershell
# Lancer le scraping
python botola_scraper.py
```

Résultat:
- 📊 `botola_matches.csv` créé
- Toutes les données de 3 saisons
- ~200-400 matchs

### Ou Mode Interactif (recommandé)

```powershell
python main.py
```

Menu avec options:
```
[1] 🔍 Inspecter la structure
[2] 📥 Scraper les matchs
[3] 📊 Analyser les données
[4] ⚙️  Configuration
[5] 🚀 Mode automatique
[0] 🚪 Quitter
```

---

## 📊 Vérifier les résultats

### Voir le CSV créé

```powershell
# Afficher le contenu
Get-Content botola_matches.csv | Select-Object -First 5
```

### Analyser en Python

```powershell
python -c "
import pandas as pd
df = pd.read_csv('botola_matches.csv')
print(f'Matchs: {len(df)}')
print(f'Colonnes: {list(df.columns)}')
print(df.head())
"
```

---

## 🐛 Troubleshooting rapide

### "No module named 'selenium'"
```powershell
pip install selenium
```

### "ChromeDriver not found"
```powershell
pip install --upgrade webdriver-manager
```

### Le scraper est lent
```powershell
# Mode headless (sans affichage)
# Modifier botola_scraper.py ligne 320:
with BotolaScraper(headless=True) as scraper:
```

### Cloudflare bloque
```powershell
# Augmenter le délai dans botola_scraper.py ligne 115:
wait_time=30  # Au lieu de 15
```

---

## 📂 Fichiers créés après exécution

```
BotolaPrediction/
├── botola_matches.csv           ✨ Les données!
├── botola_scraper.log           📝 Logs détaillés
├── footystats_structure.html    🌐 HTML du site (après inspection)
└── footystats_analysis.json     📊 Métadonnées (après inspection)
```

---

## 🎯 Prochaines étapes

### Pour le Machine Learning

```python
import pandas as pd

# Charger
df = pd.read_csv('botola_matches.csv')

# Nettoyer
df = df.dropna(subset=['home_goals', 'away_goals'])

# Feature engineering
df['total_goals'] = df['home_goals'] + df['away_goals']
df['home_win'] = (df['home_goals'] > df['away_goals']).astype(int)

# Exporter
df.to_csv('botola_clean.csv', index=False)
```

### Pour l'analyse

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('botola_matches.csv')

# Moyenne de buts
print(f"Buts domicile: {df['home_goals'].mean():.2f}")
print(f"Buts extérieur: {df['away_goals'].mean():.2f}")

# Équipes
teams = pd.concat([df['home_team'], df['away_team']]).unique()
print(f"Équipes: {len(teams)}")
```

---

## 💡 Conseils

✅ **Premier run**: Gardez `headless=False` pour voir le processus  
✅ **Production**: Utilisez `headless=True` pour la vitesse  
✅ **Débogage**: Vérifiez `botola_scraper.log`  
✅ **Mise à jour**: Relancez l'inspection si le site change  
✅ **Saisons**: Modifiez la liste dans `botola_scraper.py` ligne 319  

---

## 📞 Besoin d'aide?

1. **Vérifier les logs**: `botola_scraper.log`
2. **Inspecter le site**: `python inspect_footystats.py`
3. **Tester l'installation**: `python test_install.py`
4. **Lire le README**: `README.md`

---

**Vous êtes maintenant prêt! 🎉**

Lancez: `python main.py`
