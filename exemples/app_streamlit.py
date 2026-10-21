"""Interface de démonstration du classifieur de sentiment.

Usage : streamlit run app_streamlit.py
"""
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"

st.set_page_config(page_title="Analyse de sentiment", page_icon="💬")
st.title("Analyse de sentiment des avis clients")
st.caption("Fil rouge du cours : modèle entraîné en semaine 2, interface en semaine 5.")


@st.cache_resource
def charger_modele():
    """Chargé une seule fois, pas à chaque interaction."""
    if not MODELE.exists():
        return None
    return joblib.load(MODELE)


pipeline = charger_modele()
if pipeline is None:
    st.error("Modèle introuvable. Lancez d'abord : python train_sentiment.py")
    st.stop()

onglet_simple, onglet_lot = st.tabs(["Un avis", "Un fichier CSV"])

with onglet_simple:
    texte = st.text_area("Avis à analyser", "Livraison rapide, produit conforme.", height=120)
    if st.button("Analyser", type="primary"):
        if not texte.strip():
            st.warning("Saisissez un avis.")
        else:
            etiquette = pipeline.predict([texte])[0]
            proba = pipeline.predict_proba([texte]).max()
            if etiquette == "negative":
                st.error(f"Avis négatif (confiance {proba:.0%})")
            else:
                st.success(f"Avis positif (confiance {proba:.0%})")
            st.progress(float(proba))

with onglet_lot:
    fichier = st.file_uploader("Fichier CSV avec une colonne 'review'", type="csv")
    if fichier is not None:
        df = pd.read_csv(fichier)
        if "review" not in df.columns:
            st.error("Le fichier doit contenir une colonne 'review'.")
        else:
            df["prediction"] = pipeline.predict(df["review"])
            df["confiance"] = pipeline.predict_proba(df["review"]).max(axis=1).round(2)
            negatifs = (df.prediction == "negative").sum()
            st.metric("Avis négatifs détectés", f"{negatifs} sur {len(df)}")
            st.dataframe(df.sort_values("prediction"), use_container_width=True)
            st.download_button(
                "Télécharger les résultats",
                df.to_csv(index=False).encode("utf-8"),
                "resultats.csv",
                "text/csv",
            )
