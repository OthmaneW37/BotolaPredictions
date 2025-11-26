#!/usr/bin/env python3
"""
EXEMPLE D'UTILISATION - Botola Scraper
=======================================
Exemples pratiques de scraping et d'analyse
"""

import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def example_1_basic_scraping():
    """Exemple 1: Scraping simple"""
    logger.info("\n" + "="*60)
    logger.info("📌 EXEMPLE 1: Scraping Simple")
    logger.info("="*60)
    
    logger.info("""
from botola_scraper import BotolaScraper

# Créer le scraper
with BotolaScraper(headless=False) as scraper:
    # Scraper une saison
    df = scraper.scrape_season("2023/2024")
    
    # Afficher les résultats
    print(f"Matchs: {len(df)}")
    print(df.head())
    
    # Sauvegarder
    scraper.save_to_csv(df, "botola_2023_2024.csv")
    """)


def example_2_multiple_seasons():
    """Exemple 2: Scraping de plusieurs saisons"""
    logger.info("\n" + "="*60)
    logger.info("📌 EXEMPLE 2: Plusieurs Saisons")
    logger.info("="*60)
    
    logger.info("""
from botola_scraper import BotolaScraper

with BotolaScraper(headless=True) as scraper:
    # Scraper 3 saisons
    seasons = ["2023/2024", "2022/2023", "2021/2022"]
    df = scraper.scrape_multiple_seasons(seasons)
    
    # Sauvegarder tout
    scraper.save_to_csv(df, "botola_3_ans.csv")
    """)


def example_3_data_analysis():
    """Exemple 3: Analyse des données"""
    logger.info("\n" + "="*60)
    logger.info("📌 EXEMPLE 3: Analyse des Données")
    logger.info("="*60)
    
    logger.info("""
import pandas as pd

# Charger les données
df = pd.read_csv('botola_matches.csv')

# Statistiques générales
print(f"Total matchs: {len(df)}")
print(f"Saisons: {df['season'].unique()}")
print(f"Équipes: {len(pd.concat([df['home_team'], df['away_team']]).unique())}")

# Moyenne de buts
print(f"\\nMoyenne buts domicile: {df['home_goals'].mean():.2f}")
print(f"Moyenne buts extérieur: {df['away_goals'].mean():.2f}")

# Top scoreurs (équipes)
home_goals = df.groupby('home_team')['home_goals'].sum().sort_values(ascending=False)
print(f"\\nTop 5 équipes (domicile):\\n{home_goals.head()}")
    """)


def example_4_feature_engineering():
    """Exemple 4: Feature engineering pour ML"""
    logger.info("\n" + "="*60)
    logger.info("📌 EXEMPLE 4: Feature Engineering")
    logger.info("="*60)
    
    logger.info("""
import pandas as pd

df = pd.read_csv('botola_matches.csv')

# Créer des features
df['total_goals'] = df['home_goals'] + df['away_goals']
df['goal_diff'] = df['home_goals'] - df['away_goals']
df['home_win'] = (df['home_goals'] > df['away_goals']).astype(int)
df['away_win'] = (df['away_goals'] > df['home_goals']).astype(int)
df['draw'] = (df['home_goals'] == df['away_goals']).astype(int)

# Moyennes mobiles par équipe
home_avg = df.groupby('home_team')['home_goals'].rolling(3).mean()
away_avg = df.groupby('away_team')['away_goals'].rolling(3).mean()

# Exporter
df.to_csv('botola_features.csv', index=False)
print(df.head())
    """)


def example_5_visualization():
    """Exemple 5: Visualisation"""
    logger.info("\n" + "="*60)
    logger.info("📌 EXEMPLE 5: Visualisation")
    logger.info("="*60)
    
    logger.info("""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('botola_matches.csv')

# Distribution des scores
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
df['total_goals'].hist(bins=20)
plt.title('Distribution des Buts Totaux')
plt.xlabel('Buts')

plt.subplot(1, 3, 2)
pd.concat([df['home_goals'], df['away_goals']]).value_counts().sort_index().plot(kind='bar')
plt.title('Distribution des Buts par Match')
plt.xlabel('Nombre de Buts')

plt.subplot(1, 3, 3)
data = [df[df['home_goals'] > df['away_goals']].shape[0],
        df[df['home_goals'] < df['away_goals']].shape[0],
        df[df['home_goals'] == df['away_goals']].shape[0]]
plt.pie(data, labels=['Domicile', 'Extérieur', 'Nul'], autopct='%1.1f%%')
plt.title('Résultats Globaux')

plt.tight_layout()
plt.savefig('botola_analysis.png')
plt.show()
    """)


def example_6_predictive_model():
    """Exemple 6: Modèle prédictif simple"""
    logger.info("\n" + "="*60)
    logger.info("📌 EXEMPLE 6: Modèle Prédictif")
    logger.info("="*60)
    
    logger.info("""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('botola_matches.csv')

# Préparer les données
le_home = LabelEncoder()
le_away = LabelEncoder()

X = pd.DataFrame({
    'home_team_encoded': le_home.fit_transform(df['home_team']),
    'away_team_encoded': le_away.fit_transform(df['away_team']),
})

y = (df['home_goals'] > df['away_goals']).astype(int)

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Évaluer
accuracy = model.score(X_test, y_test)
print(f"Précision: {accuracy:.2%}")

# Prédire
print(f"\\nPrédictions (premiers résultats): {model.predict(X_test[:5])}")
    """)


def example_7_export_formats():
    """Exemple 7: Exporter en différents formats"""
    logger.info("\n" + "="*60)
    logger.info("📌 EXEMPLE 7: Export Formats Multiples")
    logger.info("="*60)
    
    logger.info("""
import pandas as pd

df = pd.read_csv('botola_matches.csv')

# CSV (déjà fait)
# df.to_csv('botola.csv')

# JSON
df.to_json('botola.json', orient='records', indent=2)

# Excel (nécessite openpyxl)
# pip install openpyxl
df.to_excel('botola.xlsx', index=False)

# Parquet (plus compact, nécessite pyarrow)
# pip install pyarrow
df.to_parquet('botola.parquet')

# HTML (pour partager)
df.to_html('botola.html')

# SQL (pour base de données)
import sqlite3
conn = sqlite3.connect('botola.db')
df.to_sql('matches', conn, index=False, if_exists='replace')
    """)


def example_8_filtering_analysis():
    """Exemple 8: Filtrage et analyse avancée"""
    logger.info("\n" + "="*60)
    logger.info("📌 EXEMPLE 8: Filtrage Avancé")
    logger.info("="*60)
    
    logger.info("""
import pandas as pd

df = pd.read_csv('botola_matches.csv')

# Matches avec beaucoup de buts
high_scoring = df[df['home_goals'] + df['away_goals'] >= 4]
print(f"Matches à haut score: {len(high_scoring)}")

# Saison spécifique
season_2023 = df[df['season'] == '2023/2024']
print(f"Matchs 2023/2024: {len(season_2023)}")

# Équipe spécifique
raja_home = df[df['home_team'] == 'Raja Casablanca']
print(f"Raja à domicile: {len(raja_home)} matches")
print(f"Victoires: {(raja_home['home_goals'] > raja_home['away_goals']).sum()}")

# Nuls
draws = df[df['home_goals'] == df['away_goals']]
print(f"Nuls: {len(draws)} ({len(draws)/len(df)*100:.1f}%)")

# Résumé par équipe
for team in df['home_team'].unique()[:3]:
    matches = len(df[(df['home_team'] == team) | (df['away_team'] == team)])
    print(f"{team}: {matches} matches")
    """)


def example_9_time_series():
    """Exemple 9: Analyse en série temporelle"""
    logger.info("\n" + "="*60)
    logger.info("📌 EXEMPLE 9: Analyse Temporelle")
    logger.info("="*60)
    
    logger.info("""
import pandas as pd

df = pd.read_csv('botola_matches.csv')

# Parser les dates
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# Buts par mois
goals_per_month = df.groupby('month')[['home_goals', 'away_goals']].mean()
print("Buts moyen par mois:")
print(goals_per_month)

# Tendance temporelle
df_sorted = df.sort_values('date')
df_sorted['rolling_avg_goals'] = df_sorted['home_goals'].rolling(10).mean()

# Progression saison
season_stats = df.groupby('season').agg({
    'home_goals': 'mean',
    'away_goals': 'mean',
    'date': 'count'
})
season_stats.columns = ['Buts Domicile', 'Buts Extérieur', 'Matchs']
print("\\nStatistiques par saison:")
print(season_stats)
    """)


def example_10_complete_workflow():
    """Exemple 10: Workflow complet"""
    logger.info("\n" + "="*60)
    logger.info("📌 EXEMPLE 10: Workflow Complet")
    logger.info("="*60)
    
    logger.info("""
# ÉTAPE 1: Scraper
from botola_scraper import BotolaScraper
with BotolaScraper(headless=True) as scraper:
    df = scraper.scrape_multiple_seasons(["2023/2024", "2022/2023"])
    scraper.save_to_csv(df)

# ÉTAPE 2: Charger
import pandas as pd
df = pd.read_csv('botola_matches_20250126_103045.csv')

# ÉTAPE 3: Nettoyer
df = df.dropna(subset=['home_goals', 'away_goals'])
df['date'] = pd.to_datetime(df['date'])

# ÉTAPE 4: Features
df['total_goals'] = df['home_goals'] + df['away_goals']
df['result'] = df.apply(
    lambda x: 'Home' if x['home_goals'] > x['away_goals']
    else 'Away' if x['away_goals'] > x['home_goals']
    else 'Draw',
    axis=1
)

# ÉTAPE 5: Analyser
print(f"Matchs: {len(df)}")
print(f"Résultats:\\n{df['result'].value_counts()}")

# ÉTAPE 6: Visualiser
import matplotlib.pyplot as plt
df['total_goals'].hist(bins=20)
plt.title('Distribution des Buts')
plt.xlabel('Total de Buts')
plt.ylabel('Fréquence')
plt.show()

# ÉTAPE 7: Exporter
df.to_csv('botola_clean.csv', index=False)
print("✅ Analyse terminée!")
    """)


def main():
    """Affiche tous les exemples"""
    logger.info("\n")
    logger.info("╔" + "═"*58 + "╗")
    logger.info("║" + "  EXEMPLES D'UTILISATION - BOTOLA SCRAPER  ".center(58) + "║")
    logger.info("╚" + "═"*58 + "╝")
    
    examples = [
        ("Basic Scraping", example_1_basic_scraping),
        ("Multiple Seasons", example_2_multiple_seasons),
        ("Data Analysis", example_3_data_analysis),
        ("Feature Engineering", example_4_feature_engineering),
        ("Visualization", example_5_visualization),
        ("Predictive Model", example_6_predictive_model),
        ("Export Formats", example_7_export_formats),
        ("Filtering", example_8_filtering_analysis),
        ("Time Series", example_9_time_series),
        ("Complete Workflow", example_10_complete_workflow),
    ]
    
    logger.info("\n📚 Exemples disponibles:\n")
    for i, (name, _) in enumerate(examples, 1):
        logger.info(f"   [{i}] {name}")
    logger.info(f"   [0] Afficher tous")
    logger.info(f"   [q] Quitter\n")
    
    choice = input("Choisissez (0-10, q): ").strip().lower()
    
    if choice == 'q':
        return
    
    if choice == '0':
        for _, func in examples:
            func()
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(examples):
                examples[idx][1]()
            else:
                logger.error("❌ Option invalide")
        except:
            logger.error("❌ Entrée invalide")
    
    logger.info("\n" + "="*60)
    logger.info("💡 Pour utiliser ces exemples:")
    logger.info("   1. Copier le code de l'exemple")
    logger.info("   2. Créer un fichier .py avec le code")
    logger.info("   3. Exécuter: python nom_fichier.py")
    logger.info("="*60 + "\n")


if __name__ == "__main__":
    main()
