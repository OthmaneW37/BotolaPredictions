"""
╔════════════════════════════════════════════════════════════════╗
║                  🏆 BOTOLA PREDICTION - SYNTHÈSE 🏆           ║
║                     Web Scraper pour Machine Learning          ║
╚════════════════════════════════════════════════════════════════╝

📅 Date: Novembre 2025
📦 Version: 1.0
👤 Créateur: Expert Data Engineering
🎯 Objectif: Dataset pour prédiction des résultats Botola Pro
"""

# ═══════════════════════════════════════════════════════════════
# 📋 RÉSUMÉ DU PROJET
# ═══════════════════════════════════════════════════════════════

Le projet "Botola Prediction" fournit un **scraper complet** pour extraire
les données de matchs de la **Botola Pro** (ligue marocaine) depuis
**FootyStats.org** et les exporter en **CSV** pour des projets de **ML**.

# ═══════════════════════════════════════════════════════════════
# 🗂️ STRUCTURE DES FICHIERS
# ═══════════════════════════════════════════════════════════════

📁 BotolaPrediction/
│
├── 🎯 FICHIERS PRINCIPAUX
│   ├── main.py                 ⭐ Point d'entrée (menu interactif)
│   ├── botola_scraper.py       📥 Scraper principal (classe BotolaScraper)
│   ├── inspect_footystats.py   🔍 Analyse de structure HTML
│   └── test_install.py         ✅ Vérification de l'installation
│
├── 📚 DOCUMENTATION
│   ├── README.md               📖 Guide complet (détaillé)
│   ├── QUICKSTART.md           🚀 Démarrage rapide (5 min)
│   ├── CHEATSHEET.md           📋 Commandes essentielles
│   ├── ADAPTATION.md           🔧 Adapter si site change
│   └── PROJECT_SUMMARY.md      📄 Ce fichier
│
├── ⚙️ CONFIGURATION
│   ├── requirements.txt        📦 Dépendances Python
│   └── config.ini              🔧 Configuration du projet
│
├── 📊 DONNÉES (créées après scraping)
│   ├── botola_matches_*.csv    💾 Fichiers de données
│   └── botola_scraper.log      📝 Logs du scraper
│
└── 🔗 AUTRES FICHIERS
    ├── footystats_structure.html    🌐 HTML inspecté (debug)
    ├── footystats_analysis.json     📊 Métadonnées
    └── footystats_main.py           🏀 Code du repo original (référence)

# ═══════════════════════════════════════════════════════════════
# 🚀 DÉMARRAGE RAPIDE (2 min)
# ═══════════════════════════════════════════════════════════════

1. INSTALLATION
   ─────────────
   $ cd "D:\Projets Dev\BotolaPrediction"
   $ pip install -r requirements.txt

2. VÉRIFICATION
   ─────────────
   $ python test_install.py
   ✅ Tous les checks doivent être verts

3. LANCER LE SCRAPER
   ──────────────────
   $ python main.py
   Puis choisir option [2] pour scraper

4. RÉSULTAT
   ────────
   ✅ botola_matches.csv créé
   ✅ ~200-400 matchs de 3 saisons

→ Plus de détails: Lire QUICKSTART.md

# ═══════════════════════════════════════════════════════════════
# 🎨 FONCTIONNALITÉS PRINCIPALES
# ═══════════════════════════════════════════════════════════════

✅ WEB SCRAPING
   - Selenium (contourne Cloudflare)
   - BeautifulSoup4 (parsing HTML)
   - Gestion des délais et timeouts
   - Logs détaillés

✅ GESTION DES DONNÉES
   - Extraction structurée
   - Parsing de scores et dates
   - Export en CSV
   - Métadonnées de saison

✅ INTERFACE UTILISATEUR
   - Menu interactif (main.py)
   - Mode automatique
   - Mode headless/visible
   - Rapports de progression

✅ ANALYSE
   - Structure HTML inspectable
   - Statistiques des matchs
   - Validation des données
   - Logs d'erreurs

# ═══════════════════════════════════════════════════════════════
# 💡 UTILISATION DES FICHIERS
# ═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│ FICHIER                 │ QUAND L'UTILISER                  │
├─────────────────────────┼──────────────────────────────────┤
│ main.py                 │ Interface principale (recommandé) │
│ botola_scraper.py       │ Scraping direct en Python        │
│ inspect_footystats.py   │ Inspecter structure du site      │
│ test_install.py         │ Vérifier l'installation          │
│ README.md               │ Pour la documentation complète   │
│ QUICKSTART.md           │ Démarrage rapide                 │
│ CHEATSHEET.md           │ Commandes courantes              │
│ ADAPTATION.md           │ Si site change                   │
│ config.ini              │ Modifier la configuration        │
│ requirements.txt        │ Installer dépendances           │
└─────────────────────────┴──────────────────────────────────┘

# ═══════════════════════════════════════════════════════════════
# 📊 DONNÉES EN SORTIE
# ═══════════════════════════════════════════════════════════════

Fichier: botola_matches_YYYYMMDD_HHMMSS.csv

Colonnes:
├── date              Date du match (YYYY-MM-DD)
├── time              Heure du match (HH:MM)
├── home_team         Équipe domicile
├── away_team         Équipe extérieur
├── score             Score brut (ex: "2-1")
├── home_goals        Buts domicile (entier)
├── away_goals        Buts extérieur (entier)
├── xg_home           Expected Goals domicile
├── xg_away           Expected Goals extérieur
├── shots_home        Tirs domicile
├── shots_away        Tirs extérieur
├── possession_home   Possession % domicile
├── possession_away   Possession % extérieur
└── season            Saison (2023/2024, 2022/2023, etc.)

Exemple de ligne:
  2024-01-15,15:00,Raja,Wydad,2-1,2,1,1.5,0.8,7,5,55,45,2023/2024

# ═══════════════════════════════════════════════════════════════
# 🔧 ARCHITECTURE TECHNIQUE
# ═══════════════════════════════════════════════════════════════

┌─────────────────┐
│   FootyStats    │
│   (site)        │
└────────┬────────┘
         │
         │ (requests HTTP + Cloudflare bypass)
         ▼
┌─────────────────┐
│   Selenium      │
│ (webdriver)     │
└────────┬────────┘
         │
         │ (HTML brut)
         ▼
┌─────────────────┐
│  BeautifulSoup  │
│  (HTML parsing) │
└────────┬────────┘
         │
         │ (Analyse DOM)
         ▼
┌─────────────────┐
│   BotolaScraper │
│  (extraction)   │
└────────┬────────┘
         │
         │ (Dict de matches)
         ▼
┌─────────────────┐
│   Pandas        │
│  (DataFrame)    │
└────────┬────────┘
         │
         │ (Structuration)
         ▼
┌─────────────────┐
│   CSV Export    │
│   (fichier)     │
└─────────────────┘

# ═══════════════════════════════════════════════════════════════
# 📦 DÉPENDANCES
# ═══════════════════════════════════════════════════════════════

Principales:
  • selenium 4.0+       Web scraping automatisé
  • beautifulsoup4 4.9+ Parsing HTML
  • pandas 1.3+         Manipulation DataFrames
  • requests 2.26+      Requêtes HTTP
  • webdriver-manager   Gestion ChromeDriver
  • lxml 4.6+           Parser HTML rapide

Installation:
  $ pip install -r requirements.txt

# ═══════════════════════════════════════════════════════════════
# ⚙️ CONFIGURATION
# ═══════════════════════════════════════════════════════════════

Fichier: config.ini

[SCRAPER]
  SEASONS = 2023/2024,2022/2023,2021/2022
  HEADLESS = false (true pour mode invisible)
  TIMEOUT = 15 (secondes d'attente Cloudflare)

[DATA]
  OUTPUT_DIR = data
  EXPORT_DIR = exports
  OUTPUT_FORMAT = csv

[LOGGING]
  LEVEL = INFO
  FILE = botola_scraper.log

Modifier config.ini ou directement dans le code Python.

# ═══════════════════════════════════════════════════════════════
# 🎯 CAS D'USAGE
# ═══════════════════════════════════════════════════════════════

1. MACHINE LEARNING
   ─────────────────
   • Prédire le résultat des matchs
   • Analyser les statistiques par équipe
   • Estimer les xG
   → botola_scraper.py + ML framework

2. ANALYSE STATISTIQUE
   ────────────────────
   • Distribution des scores
   • Tendances par saison
   • Performance des équipes
   → botola_scraper.py + pandas + matplotlib

3. VISUALISATION
   ──────────────
   • Dashboard des matchs
   • Heatmaps de possession
   • Graphiques de performance
   → botola_scraper.py + plotly/seaborn

4. RECHERCHE
   ──────────
   • Étude du football marocain
   • Comparaison Botola vs autres ligues
   • Prédiction sur données enrichies
   → botola_scraper.py + datasets externes

# ═══════════════════════════════════════════════════════════════
# 🐛 TROUBLESHOOTING
# ═══════════════════════════════════════════════════════════════

PROBLÈME                  → SOLUTION
────────────────────────────────────
Module manquant           → pip install -r requirements.txt
ChromeDriver error        → pip install --upgrade webdriver-manager
Cloudflare timeout        → Augmenter wait_time dans botola_scraper.py
Site bloque requêtes      → Augmenter délais (delay_between_requests)
CSV vide                  → Exécuter inspect_footystats.py
Page ne charge pas        → Vérifier connexion Internet
Espace disque insuffisant → Supprimer anciens fichiers CSV

Plus: Voir README.md section "Troubleshooting"

# ═══════════════════════════════════════════════════════════════
# 📈 PERFORMANCE
# ═══════════════════════════════════════════════════════════════

Temps d'exécution:
  • Inspect structure     ~20 sec
  • 1 saison (headless)   ~30 sec
  • 3 saisons (headless)  ~2 min
  • Avec mode visuel      ~5-10 min

Taille fichier:
  • ~400 matchs           ~100 KB
  • ~1200 matchs (3 ans)  ~300 KB

Ressources:
  • RAM: ~200-300 MB
  • Disque: ~1 MB minimum

# ═══════════════════════════════════════════════════════════════
# 🔐 NOTES DE SÉCURITÉ
# ═══════════════════════════════════════════════════════════════

✅ Ce scraper:
   • Respecte le robots.txt de FootyStats
   • Inclut des délais entre requêtes
   • Ne stocke PAS les données personnelles
   • Utilise User-Agent standard

⚠️ À faire:
   • Ne pas relancer trop souvent (risk de ban)
   • Respecter les ToS du site
   • Utiliser à des fins légitimes uniquement
   • Ne pas redistribuer sans permission

# ═══════════════════════════════════════════════════════════════
# 📚 RESSOURCES SUPPLÉMENTAIRES
# ═══════════════════════════════════════════════════════════════

Documentation Interne:
  • README.md              (Complet)
  • QUICKSTART.md          (5 min)
  • CHEATSHEET.md          (Commandes)
  • ADAPTATION.md          (Adapt si site change)

Ressources Externes:
  • Selenium: https://www.selenium.dev/
  • BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/
  • Pandas: https://pandas.pydata.org/
  • FootyStats: https://footystats.org/

# ═══════════════════════════════════════════════════════════════
# 🎓 COMPÉTENCES DÉMONTRÉES
# ═══════════════════════════════════════════════════════════════

Python:
  ✅ Classes et OOP
  ✅ Context managers
  ✅ Logging avancé
  ✅ Exception handling
  ✅ Type hints

Web Scraping:
  ✅ Selenium + WebDriver
  ✅ Gestion Cloudflare
  ✅ BeautifulSoup parsing
  ✅ Requêtes HTTP

Data Processing:
  ✅ Pandas DataFrames
  ✅ Parsing de données
  ✅ Export formats multiples
  ✅ Validation de données

Software Engineering:
  ✅ Architecture propre
  ✅ Gestion d'erreurs robuste
  ✅ Documentation complète
  ✅ Configuration externalisée
  ✅ Logging structuré
  ✅ Tests et vérification

# ═══════════════════════════════════════════════════════════════
# 🚀 PROCHAINES ÉTAPES
# ═══════════════════════════════════════════════════════════════

1. Installer et tester
   → python test_install.py

2. Inspecter la structure
   → python inspect_footystats.py

3. Lancer le scraping
   → python main.py (option 2)

4. Analyser les données
   → python main.py (option 3)

5. Utiliser pour ML
   → Charger botola_matches.csv
   → Feature engineering
   → Entraînement modèle

# ═══════════════════════════════════════════════════════════════
# ✅ CHECKLIST FINALE
# ═══════════════════════════════════════════════════════════════

Avant de commencer:
  □ Python 3.8+ installé
  □ pip fonctionnel
  □ Chrome/Chromium installé
  □ Connexion Internet active
  □ ~1 GB espace disque libre

Installation:
  □ requirements.txt installé
  □ test_install.py validé ✅
  □ Tous les packages importables
  □ Vérification Chrome OK

Scraping:
  □ inspect_footystats.py exécuté
  □ footystats_structure.html généré
  □ botola_scraper.py prêt
  □ main.py fonctionnel

Production:
  □ Premiers CSV générés
  □ Données validées
  □ Logs consultés
  □ Prêt pour ML!

# ═══════════════════════════════════════════════════════════════

💡 Question fréquente:
   "Puis-je utiliser cela pour du scraping d'autres sites?"
   Oui! Le code est modulaire et adaptable. Voir ADAPTATION.md

📞 Support:
   • Lire README.md (guide complet)
   • Lire QUICKSTART.md (5 min)
   • Consulter botola_scraper.log (logs)
   • Exécuter test_install.py (diagnostic)

═════════════════════════════════════════════════════════════════

🎉 PRÊT À DÉMARRER? Exécutez:

   python main.py

═════════════════════════════════════════════════════════════════
"""

# Ce fichier est une documentation de synthèse
# Pour démarrer réellement, exécutez: python main.py
