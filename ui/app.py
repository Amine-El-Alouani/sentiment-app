"""Interface de démonstration du classifieur de sentiment.

Usage : streamlit run ui/app.py
Prérequis : models/sentiment.joblib, produit par python src/train.py (TP2).
"""
from pathlib import Path

import pandas as pd
import streamlit as st

from helpers import charger_predicteur, classer, predire_lot, resumer

RACINE = Path(__file__).resolve().parents[1]

st.set_page_config(page_title="Analyse de sentiment", page_icon="💬", layout="wide")
st.title("Analyse de sentiment des avis clients")
st.caption("Modèle entraîné en TP2 · interface de démonstration · fil rouge du cours")


@st.cache_resource
def predicteur():
    """Chargé une seule fois, pas à chaque interaction."""
    return charger_predicteur()


try:
    predire = predicteur()
except FileNotFoundError as erreur:
    st.error(str(erreur))
    st.info("Dans un terminal, à la racine du dépôt : `python src/train.py --allocine`")
    st.stop()

onglet_avis, onglet_lot, onglet_aide = st.tabs(["Un avis", "Un fichier CSV", "Comment ça marche"])

with onglet_avis:
    texte = st.text_area("Avis à analyser", "Livraison rapide, produit conforme.", height=130)
    if st.button("Analyser", type="primary"):
        if not texte.strip():
            st.warning("Saisissez un avis.")
        else:
            r = classer(texte, predire)
            colonne_verdict, colonne_score = st.columns([2, 1])
            with colonne_verdict:
                if r["incertain"]:
                    st.warning(f"À vérifier par un agent (penche vers « {r['label']} »)")
                elif r["label"] == "negative":
                    st.error("Avis négatif : à traiter en priorité")
                else:
                    st.success("Avis positif")
            with colonne_score:
                st.metric("Confiance", f"{r['score']:.0%}")
            st.progress(float(r["score"]))

with onglet_lot:
    st.write("Fichier CSV contenant une colonne `review`. Exemple fourni : `data/sample_reviews.csv`.")
    fichier = st.file_uploader("Choisir un fichier", type="csv")
    if fichier is not None:
        try:
            df = predire_lot(pd.read_csv(fichier), predire)
        except (KeyError, ValueError) as erreur:
            st.error(str(erreur))
        else:
            r = resumer(df)
            c1, c2, c3 = st.columns(3)
            c1.metric("Avis analysés", r["total"])
            c2.metric("Négatifs détectés", f"{r['negatifs']} ({r['part_negatifs']} %)")
            c3.metric("À vérifier", r["a_verifier"])
            st.bar_chart(df["prediction"].value_counts())
            st.dataframe(
                df.sort_values(["prediction", "confiance"], ascending=[True, False]),
                use_container_width=True,
            )
            st.download_button(
                "Télécharger les résultats",
                df.to_csv(index=False).encode("utf-8"),
                "resultats.csv",
                "text/csv",
            )

with onglet_aide:
    st.markdown(
        """
**Ce que fait cette interface.** Elle charge le modèle produit au TP2 et appelle sa fonction
`predict()`, la même que celle qu'utilisera l'API. Aucune logique de prédiction n'est dupliquée ici.

**Le seuil d'incertitude.** En dessous de 60 % de confiance, la prédiction est affichée comme
« à vérifier » plutôt que tranchée. Un modèle qui hésite doit le dire : c'est ce qui permet à un
agent de reprendre la main, comme prévu dans la fiche de cadrage du cas 3.

**Ce que l'interface n'est pas.** Une démonstration, pas l'application. Elle sert à montrer le
modèle, à récolter des retours et à faire apparaître les cas où il se trompe. L'API, elle, sera
appelée par d'autres programmes.
        """
    )
