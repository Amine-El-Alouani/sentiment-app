"""Entraîne un classifieur de sentiment sur des avis de films en français.

Jeu de données : Allociné (tblard/allocine), 20 000 avis du split de validation,
téléchargés directement depuis leur URL publique. Rien à installer ni à copier.

Usage : python exemples/train_sentiment.py
Produit : models/sentiment.joblib
"""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

RACINE = Path(__file__).resolve().parents[1]
URL = (
    "https://huggingface.co/datasets/tblard/allocine/resolve/main/"
    "allocine/validation-00000-of-00001.parquet"
)
SECOURS = RACINE / "data" / "sample_reviews.csv"   # si le réseau est coupé
MODELE = RACINE / "models" / "sentiment.joblib"
SEUIL_RAPPEL = 0.90


def charger_donnees() -> pd.DataFrame:
    """Avis publics Allociné, avec repli sur le petit jeu du kit."""
    try:
        df = pd.read_parquet(URL)                      # 7,6 Mo, quelques secondes
        df["label"] = df["label"].map({0: "negative", 1: "positive"})
        print(f"Source : Allociné (URL publique), {len(df)} avis")
    except Exception as erreur:                        # proxy, coupure, pare-feu
        print(f"Téléchargement impossible ({type(erreur).__name__}), repli sur le jeu local")
        df = pd.read_csv(SECOURS)
        print(f"Source : {SECOURS.name}, {len(df)} avis")
    return df[["review", "label"]].dropna()


# 1. Charger les données
df = charger_donnees()
print(f"  dont {(df.label == 'negative').sum()} négatifs")

# 2. Découper AVANT toute transformation (sinon fuite de données)
X_train, X_test, y_train, y_test = train_test_split(
    df["review"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)
print(f"{len(X_train)} avis d'entraînement, {len(X_test)} de test")

# 3. Pipeline : vectorisation + modèle, dans un seul objet
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)),
    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
])

# 4. Entraîner
print("Entraînement en cours...")
pipeline.fit(X_train, y_train)
print(f"  {len(pipeline.named_steps['tfidf'].vocabulary_)} termes dans le vocabulaire")

# 5. Évaluer sur le jeu de test, jamais vu pendant l'entraînement
y_pred = pipeline.predict(X_test)
print("\n" + classification_report(y_test, y_pred, digits=3))
print("Matrice de confusion (lignes = vérité, colonnes = prédiction) :")
print(confusion_matrix(y_test, y_pred, labels=["negative", "positive"]))

rapport = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
rappel = rapport["negative"]["recall"]
verdict = "ACCEPTÉ" if rappel >= SEUIL_RAPPEL else "REFUSÉ"
print(f"\nRappel sur la classe négative : {rappel:.3f} (seuil {SEUIL_RAPPEL}) -> {verdict}")

# 6. Sauvegarder le pipeline entier, pas seulement le modèle
MODELE.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(pipeline, MODELE)
print(f"Modèle enregistré : {MODELE.relative_to(RACINE)}")

# 7. Essai rapide
for phrase in [
    "Un film magnifique, je le reverrai avec plaisir.",
    "Scénario creux et acteurs sans conviction, j'ai perdu deux heures.",
]:
    print(f"  {pipeline.predict([phrase])[0]:9s} <- {phrase}")
