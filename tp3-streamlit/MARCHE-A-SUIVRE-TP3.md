# TP3 : marche à suivre, étape par étape et test par test

Quatre étapes, quatre contrôles numérotés S1 à S4.

## Étape A. Installer le kit et lancer l'interface (15 min)

Décompressez le kit **à côté** de votre dépôt, puis :

```bash
cd tp3-streamlit
python appliquer_tp3.py ../sentiment-app --simulation
python appliquer_tp3.py ../sentiment-app
cd ../sentiment-app
source .venv/bin/activate          # Windows : .venv\Scripts\Activate.ps1
streamlit run ui/app.py
```

### Contrôle S1 : la page s'ouvre

Le navigateur s'ouvre sur `http://localhost:8501` et affiche trois onglets. Si le modèle manque, la page affiche un message d'erreur explicite et s'arrête : lancez `python src/train.py --allocine`, puis rechargez.

Pour arrêter l'interface : `Ctrl+C` dans le terminal. Tant qu'elle tourne, ce terminal est occupé ; ouvrez-en un second pour les autres commandes.

## Étape B. L'onglet « un avis » (30 min)

Saisissez trois avis et observez : un avis clairement positif, un clairement négatif, puis un avis mitigé du type « service impeccable au début, mais finalement produit cassé ».

### Contrôle S2 : le modèle dit quand il hésite

L'avis mitigé doit afficher **« à vérifier »** plutôt qu'un verdict tranché, dès que la confiance tombe sous 60 %.

Ce seuil est dans `ui/helpers.py`, constante `SEUIL_INCERTITUDE`. Faites-le varier à 0,50 puis 0,75 et notez ce qui change : plus le seuil est haut, plus le modèle renvoie de cas à l'agent, et moins il se trompe tout seul. C'est un arbitrage, pas un réglage technique.

## Étape C. L'onglet « un fichier CSV » (40 min)

Téléversez `data/sample_reviews.csv`, puis `data/demo_reviews.csv` produit au TP2.

### Contrôle S3 : le résumé et le tableau

Trois métriques en haut (avis analysés, négatifs détectés avec leur pourcentage, cas à vérifier), un graphique de répartition, un tableau trié avec les négatifs en premier, et un bouton de téléchargement.

Sur `demo_reviews.csv`, comparez la part de négatifs annoncée par l'interface avec le vrai étiquetage du fichier : l'écart correspond aux erreurs mesurées au TP2, celles sur les avis mitigés.

## Étape D. Tests, documentation, push (35 min)

```bash
python -m pytest tests/test_ui.py -q      # attendu : 3 passed
python -m pytest -q                       # attendu : 45 passed
```

### Contrôle S4 : tout est vert

**45 passed**, soit 38 du TP1, 4 du TP2 et 3 du TP3. Remarquez que les tests d'interface ne lancent pas Streamlit : ils importent `ui/helpers.py`. C'est pour cela que la logique est séparée de l'affichage, et c'est ce que vérifie `test_helpers_importables`.

Écrivez `docs/semaine3.md`, trois phrases : quel seuil d'incertitude vous retenez, combien d'avis cela envoie à un agent sur le jeu de démonstration, et pourquoi ce compromis vous paraît juste.

```bash
git add -A
git commit -m "Semaine 3 : interface de demonstration Streamlit"
git push
```

## Récapitulatif

| Contrôle | Commande | Résultat attendu |
| --- | --- | --- |
| S1 | `streamlit run ui/app.py` | La page s'ouvre sur localhost:8501, trois onglets |
| S2 | Un avis mitigé dans l'onglet 1 | Verdict « à vérifier » sous 60 % de confiance |
| S3 | `data/demo_reviews.csv` dans l'onglet 2 | Trois métriques, graphique, tableau trié, export |
| S4 | `pytest -q` | 45 passed, CI verte |

## En cas de blocage

| Message | Cause | Correction |
| --- | --- | --- |
| `models/sentiment.joblib absent` | Modèle non entraîné sur ce poste | `python src/train.py --allocine` |
| `ModuleNotFoundError: streamlit` | Installation partielle du TP1 | `pip install -r requirements.txt` |
| `Port 8501 is already in use` | Une interface tourne déjà | `Ctrl+C` dans l'autre terminal, ou `streamlit run ui/app.py --server.port 8502` |
| `colonne 'review' absente du fichier` | CSV sans la bonne colonne | Renommez la colonne, ou prenez `data/sample_reviews.csv` comme modèle |
| La page reste blanche | Script lancé avec `python` au lieu de `streamlit` | `streamlit run ui/app.py` |
