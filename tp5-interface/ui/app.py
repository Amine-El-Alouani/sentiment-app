"""Interface Streamlit (TP5) : elle appelle l'API, jamais le modèle.

Lancer, API déjà démarrée dans un autre terminal : streamlit run ui/app.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # pour importer ui.client

import pandas as pd
import streamlit as st

from ui import client

st.set_page_config(page_title="Analyse de sentiment")
st.title("Analyse de sentiment des avis")

session = client.creer_session()
etat = client.sante(session)
if etat.ok:
    st.caption(f"API prête : {etat.message}")
else:
    st.error(etat.message)

onglet_avis, onglet_lot = st.tabs(["Un avis", "Un fichier d'avis"])

with onglet_avis:
    texte = st.text_area("Avis client")
    if st.button("Analyser"):
        reponse = client.predire(session, texte)
        if reponse.ok and reponse.label is not None and reponse.score is not None:
            st.metric(client.VERDICTS[reponse.label], f"{reponse.score:.0%}")
            if reponse.label == "INDETERMINE":
                st.info("La confiance est sous le seuil d'abstention : un humain doit trancher.")
        elif reponse.message == client.REFUS:
            st.warning(reponse.message)
        else:
            st.error(reponse.message)

with onglet_lot:
    fichier = st.file_uploader("Fichier CSV avec une colonne text", type="csv")
    if fichier is not None:
        avis = pd.read_csv(fichier)
        if "text" not in avis.columns:
            st.error("Colonne text absente du fichier.")
        else:
            reponses = client.predire_lot(session, avis["text"].astype(str).tolist())
            avis["verdict"] = [client.VERDICTS[r.label] if r.ok and r.label else r.message for r in reponses]
            avis["confiance"] = [r.score for r in reponses]
            st.dataframe(avis, use_container_width=True)
            st.write(client.resumer(reponses))
            st.download_button("Télécharger les résultats", avis.to_csv(index=False),
                               file_name="resultats.csv", mime="text/csv")
