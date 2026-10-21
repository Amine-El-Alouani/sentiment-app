# Du cadrage à l'interface : TP1, TP2, TP3

**Module :** Développement et déploiement d'applications intelligentes
**Auteur :** A. Larhlimi
**Public :** binômes d'étudiants · **Durée :** trois séances de 2 h

Ce document enchaîne les trois premières séances sur un seul dépôt. Il a été **rejoué intégralement sur un poste Windows** : les commandes, les résultats et les incidents qu'il décrit ont tous été observés, pas supposés. La section 9 recense ces incidents avec leur message exact.

---

## 1. Vue d'ensemble

| Séance | Ce que le binôme produit | Contrôles | Tests cumulés |
| --- | --- | --- | --- |
| TP1 | Dépôt structuré, environnement reproductible, trois fiches de cadrage | T0 à T7 | 38 |
| TP2 | Le modèle : entraînement, évaluation, métriques versionnées | C1 à C5 | 42 |
| TP3 | L'interface de démonstration Streamlit | S1 à S4 | 45 |

Le besoin métier : une équipe relation client reçoit des milliers d'avis par jour et les traite dans l'ordre d'arrivée. On veut faire remonter les **avis négatifs** en tête de file.

Le problème est volontairement simple côté modèle. La difficulté est ailleurs, et c'est le sujet du module : rendre ce modèle reproductible, testé, surveillé, utilisable par quelqu'un d'autre.

### Les trois kits

| Archive | Contenu | Se pose sur |
| --- | --- | --- |
| `sentiment-app.zip` | Le dépôt de départ : structure, scripts, 38 tests, CI, six documents | rien, c'est la base |
| `tp2-semaine2-kit.zip` | `src/` (quatre scripts), `tests/test_model.py`, notebook Colab | le dépôt du TP1 |
| `tp3-streamlit-kit.zip` | `ui/`, `tests/test_ui.py`, notebook Colab, documents du compte rendu | le dépôt après le TP2 |

Les deux derniers s'installent par un script, depuis le dossier du kit décompressé **à côté** du dépôt :

```powershell
python appliquer_tp2.py ..\sentiment-app --simulation   # voir sans rien écrire
python appliquer_tp2.py ..\sentiment-app                # copier pour de bon
```

> **Leçon du terrain.** Les kits doivent venir du **même entrepôt**. Un `tp2-kit.zip` d'une version antérieure mélangé à un `tp3-streamlit-kit.zip` récent fait échouer un test d'interface : la fonction `predict()` ne renvoie pas exactement les mêmes champs d'une version à l'autre. Décompressez les trois depuis le même `tp1-tp2-tp3.zip`.

---

## 2. Avant de commencer

### Les outils

Python 3.11 (3.10 toléré, **évitez 3.12 et 3.13**), Git, un éditeur, un compte GitHub.

```powershell
python --version                    # 3.11.x attendu ; sinon py -3.11 --version
git --version                       # si « commande inconnue », rouvrez le terminal
```

### Les quatre réglages

```powershell
git config --global user.name "Prénom Nom"
git config --global user.email "prenom.nom@ecole.ma"
git config --global init.defaultBranch main
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

`user.name` est inscrit comme auteur dans chaque commit : c'est lui, et non l'adresse, que compte le contrôle T5. `--global` écrit dans votre fichier personnel, valable pour tous vos dépôts ; `--local` n'écrit que dans le dépôt courant et **exige d'y être**, sinon Git répond `--local can only be used inside a git repository`.

`init.defaultBranch main` évite de devoir renommer `master`. `Set-ExecutionPolicy` autorise l'activation du venv ; sans elle, `Activate.ps1` est refusé.

### Trois leçons du terrain

**Un seul compte GitHub par poste.** Si plusieurs comptes cohabitent, les erreurs d'autorisation deviennent illisibles : `gh auth switch` échoue sur un compte jamais connecté, le navigateur réautorise le mauvais compte, et Windows rejoue un jeton périmé. Voir la section 9.

**Remplacez les espaces réservés.** Toute URL écrite `<organisation>` ou `votre-compte` dans un énoncé doit être remplacée par votre vrai compte. Le plus sûr est de copier l'URL depuis le bouton vert **Code** de la page du dépôt, jamais de la retaper.

**Le message LF/CRLF est normal.** Il apparaît au premier `git add` sous Windows et n'empêche rien.

---

## 3. TP1 : cadrer et préparer l'environnement

> **Objectif :** décider quelle approche employer pour trois besoins métier, et monter un dépôt que l'enseignant peut cloner sur une machine vierge et faire tourner en trois commandes.

### Étape 1. Décompresser le kit (5 min, chacun)

```powershell
Expand-Archive -Path sentiment-app.zip -DestinationPath . -Force
cd sentiment-app
ls
ls -Force | findstr gitignore
```

**Contrôle T0 :** sept dossiers (`app`, `data`, `docs`, `models`, `scripts`, `tests`, `ui`), les documents, et `.gitignore`, qui ne s'affiche pas avec un `ls` ordinaire. C'est le seul rempart contre l'erreur de T3.

L'archive crée un dossier du même nom : un chemin `sentiment-app\sentiment-app` est normal, descendez jusqu'à celui qui contient `README.md`.

### Étape 2. L'environnement virtuel (10 min, chacun)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pandas scikit-learn pytest
python -m pytest -q
```

**Contrôle T1 : `3 failed, 31 passed, 4 skipped`.** Ce rouge est voulu. Les trois échecs sont les fiches vides, les quatre ignorés attendent le dépôt Git, les 31 verts confirment structure, paquets et `.gitignore`.

Votre invite doit afficher `(.venv)`. Écrivez `python -m pytest` plutôt que `pytest` : la première forme passe par l'interpréteur courant et ne dépend pas du PATH.

### Étape 3. Les trois fiches de cadrage (50 min, à deux)

La grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur. L'arbre, dans l'ordre : logique connue et stable ? **règles métier**. Données étiquetées ? **machine learning**. Réponse à tirer de documents et à citer ? **RAG**. Sinon seulement, **génératif seul**.

| Fiche | Le cas | Réponse attendue |
| --- | --- | --- |
| `cas1-pharmacie.md` | Ordonnances incomplètes | Règles métier : (a) pas d'étiquettes, (b) explicabilité, (d) erreur grave |
| `cas2-reglement.md` | Règlement intérieur | RAG : (b) citer l'article, (a) pas d'étiquettes, (c) volume faible |
| `cas3-avis-negatifs.md` | Avis négatifs | ML : (a) étiquettes gratuites, (c) volume, (d) erreur peu grave |

Trois règles vérifiées par les tests : une seule case `- [x]` ; au moins deux critères cités **par leur lettre** ; chaque rubrique obligatoire d'au moins une phrase.

```powershell
python -m pytest tests\test_cadrage.py -q
```

**Contrôle T2 : `12 passed`.** Les messages d'échec nomment la fiche et la rubrique fautives.

### Étape 4. Créer le dépôt et pousser (25 min, membre A)

Sur github.com : New repository, nom `sentiment-app`, **Private**, aucune case cochée. Settings, Collaborators : membre B en **Write**, enseignant en **Read**.

```powershell
git init
git add -A
git status
```

**Contrôle T3 : aucune ligne `.venv/` dans la sortie.** Si elle apparaît, arrêtez-vous : le `.gitignore` manque. Une fois poussé, le dépôt pèse 300 Mo et le test reste rouge même après correction, car il lit tout l'historique.

Profitez-en pour repérer tout fichier parasite, une archive ou un PDF déposé dans le dossier : `git rm --cached "le fichier"`, et une ligne `*.zip` dans le `.gitignore`.

> **Message normal à cette étape :** `warning: in the working copy of 'docs/cadrage/cas1-pharmacie.md', LF will be replaced by CRLF`. Git pour Windows convertit les fins de ligne. Pour le faire taire : `git config --global core.autocrlf input`.

```powershell
git commit -m "Semaine 1 : structure du depot et kit TP1"
git branch -M main
git remote add origin https://github.com/VOTRE-COMPTE/sentiment-app.git
git remote -v
git push -u origin main
```

**Remplacez `VOTRE-COMPTE`.** Laisser l'espace réservé donne `Repository not found`, et laisser des chevrons donne `error: 400`.

Au premier push, le mot de passe du compte est refusé : il faut un **jeton d'accès personnel** (Settings, Developer settings, Personal access tokens, Tokens classic, portée `repo`). Alternative : `gh auth login` puis `gh auth setup-git`.

### Étape 5. L'installation complète (15 min, les deux)

```powershell
git clone https://github.com/VOTRE-COMPTE/sentiment-app.git
cd sentiment-app
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
python scripts\check_setup.py
```

**Contrôle T4 : `0 erreur(s)`.** Comptez 5 à 10 minutes. L'avertissement « 1 auteur seulement » est normal ici. `requirements.lock` est régénéré sur chaque poste : **un seul membre le commite**.

### Étape 6. Un commit par membre (10 min, chacun)

```powershell
git pull
git add README.md
git commit -m "README : ajout de <nom> au tableau du binome"
git push
git shortlog -sn --all
python -m pytest tests\test_git_history.py -q
```

**Contrôle T5 : deux noms distincts, puis `3 passed`.** Si le test ne voit qu'un auteur, soit un membre n'a pas poussé, soit les deux postes partagent le même `user.name`.

### Étapes 7 et 8. Vérification et clone frais (15 min)

```powershell
git pull
python scripts\check_setup.py      # T6 : 0 erreur, 0 avertissement
python -m pytest -q                # T6 : 38 passed
```

Puis l'onglet **Actions** au vert. Enfin, le test de l'enseignant :

```powershell
bash scripts/verif_clone.sh https://github.com/VOTRE-COMPTE/sentiment-app.git
```

**Contrôle T7 : `38 passed` sur un clone frais, sans aucune intervention manuelle.**

---

## 4. TP2 : entraîner, évaluer, sauvegarder

> **Objectif :** produire un modèle reproductible, évalué correctement, sauvegardé dans un fichier que l'interface chargera. Pas un bon modèle : un modèle dont vous savez pourquoi il se trompe.

### Étape A. Installer le kit (15 min)

```powershell
cd ..\tp2-semaine2
python appliquer_tp2.py ..\sentiment-app
cd ..\sentiment-app
python -m pytest -q
```

**Contrôle C1 : `2 failed, 38 passed, 2 skipped`.** Les deux échecs réclament `models/metrics.json`, les deux ignorés attendent le modèle.

### Étape B. Le jeu de démonstration (15 min)

```powershell
python src\make_demo.py
```

**Contrôle C2 : 290 avis, 145 de chaque classe.** Le fichier contient 80 avis nettement positifs, 80 nettement négatifs, 100 **mitigés** et 30 neutres.

Lisez trois avis mitigés : une première moitié d'un sentiment, un retournement (« mais finalement »), une seconde moitié de l'autre. L'étiquette suit la seconde, celle qui conclut. Cette structure explique toutes les erreurs de l'étape D.

### Étape C. Entraîner (25 min)

```powershell
python src\train.py
```

**Contrôle C3 : F1 macro 0,879**, 232 avis d'entraînement, 58 de test, 316 termes de vocabulaire.

```powershell
git status --short
```

`models/metrics.json` apparaît ; `models/sentiment.joblib` et `data/demo_reviews.csv` non. Ce qui se régénère par une commande n'entre pas dans Git ; **seule la mesure est versionnée**.

Trois lignes de code à lire : le `train_test_split` **avant** toute vectorisation (sinon le jeu de test fuite dans l'entraînement), le `Pipeline` qui enferme vectoriseur et modèle dans un seul objet, et `random_state=42` qui rend le découpage reproductible.

### Étape D. Évaluer (30 min)

```powershell
python src\evaluate.py
```

**Contrôle C4 : 7 erreurs sur 58.**

```text
            negative  positive
  negative        27         2
  positive         5        24
```

Les deux faux positifs sont le cas qui compte : un client mécontent traité en retard. Toutes les erreurs portent sur des avis mitigés, parce qu'un sac de mots **n'a pas d'ordre** : « bon puis mauvais » et « mauvais puis bon » donnent le même vecteur.

Écrivez `docs/semaine2.md`, trois phrases : quelles erreurs, pourquoi, et ce qu'il faudrait pour les corriger.

### Étape E. Le vrai jeu (35 min)

```powershell
python src\train.py --allocine
python -m pytest -q
```

**Contrôle C5 : F1 macro 0,920, puis `42 passed`, puis CI verte.**

```text
Source : allocine, 20000 avis (10204 négatifs)
16000 avis d'entraînement, 4000 de test
Vocabulaire : 149529 termes
F1 macro sur le jeu de test : 0.920 (seuil 0.85)
```

| | Démonstration | Allociné |
| --- | --- | --- |
| Avis | 290 | 20 000 |
| Vocabulaire | 316 termes | 149 529 termes |
| F1 macro | 0,879 | 0,920 |

Le modèle n'a pas changé : ce sont les données. Et la mesure devient crédible, calculée sur 4 000 avis au lieu de 58.

---

## 5. TP3 : l'interface de démonstration

> **Objectif :** rendre le modèle utilisable par quelqu'un qui n'ouvrira jamais un terminal, sans réécrire une ligne de logique de prédiction.

### Étape A. Installer et lancer (15 min)

```powershell
Expand-Archive -Path .\tp1-tp2-tp3\kits\tp3-streamlit-kit.zip -DestinationPath . -Force
cd tp3-streamlit
python appliquer_tp3.py ..\sentiment-app
cd ..\sentiment-app
python -m pytest -q
streamlit run ui\app.py
```

**Contrôle S1 :** la page s'ouvre sur `http://localhost:8501` avec trois onglets. Si le modèle manque, la page le dit et s'arrête : lancez `python src\train.py --allocine`.

Ce terminal reste occupé tant que l'interface tourne. Ouvrez-en un second pour la suite, arrêtez avec `Ctrl+C`.

### Étape B. L'onglet « Un avis » (30 min)

Testez trois saisies :

```text
Livraison rapide, produit conforme, je recommande.
Produit cassé à l'arrivée et service client injoignable.
Emballage soigné et notice claire, sauf que ensuite application qui plante.
```

**Contrôle S2 :** les deux premières donnent un verdict net, vert puis rouge, avec une confiance élevée. La troisième doit afficher **« À vérifier par un agent »** en orange, la confiance tombant sous 60 %.

### Étape C. L'onglet « Un fichier CSV » (40 min)

Téléversez `data/demo_reviews.csv`.

**Contrôle S3 :** trois métriques (avis analysés, négatifs détectés et leur pourcentage, cas à vérifier), un graphique de répartition, un tableau trié négatifs en tête, un bouton de téléchargement.

Le fichier contient 145 négatifs sur 290, soit 50 % : l'écart avec le pourcentage annoncé par l'interface correspond aux erreurs du modèle sur les avis mitigés.

### Étape D. Tests, documentation, push (35 min)

```powershell
python -m pytest -q
git add -A
git commit -m "Semaine 3 : interface de demonstration Streamlit"
git push
```

**Contrôle S4 : `45 passed`**, puis CI verte.

Écrivez `docs/semaine3.md` : quel seuil vous retenez, combien d'avis cela envoie à un agent, et pourquoi ce compromis vous paraît juste.

---

## 6. L'application Streamlit, commentée

### Ce qu'est Streamlit, en trois idées

**Un script Python devient une page web.** Pas de HTML, pas de JavaScript, pas de serveur à configurer. Chaque appel à `st.title`, `st.text_area` ou `st.dataframe` ajoute un élément à la page, dans l'ordre où il est écrit.

**Chaque interaction réexécute le script de haut en bas.** C'est le modèle de fonctionnement, et il surprend toujours. Cliquer sur un bouton ne déclenche pas une fonction : cela relance tout le fichier, avec la nouvelle valeur du bouton. D'où la nécessité de mettre en cache ce qui coûte cher.

**C'est une démonstration, pas l'application.** Elle sert à montrer le modèle, à récolter des retours, à faire apparaître les cas où il se trompe. C'est l'API, plus tard, qui sera appelée par d'autres programmes.

### Pourquoi deux fichiers

`ui/helpers.py` contient la logique, `ui/app.py` l'affichage. Cette séparation a une raison précise : **les tests importent `helpers.py` sans lancer Streamlit**. Une interface non testable est une interface qu'on casse sans s'en apercevoir.

### ui/helpers.py, ligne par ligne

```python
RACINE = Path(__file__).resolve().parents[1]
MODELE = RACINE / "models" / "sentiment.joblib"
SEUIL_INCERTITUDE = 0.60   # en dessous, on affiche « à vérifier »
```

`parents[1]` remonte de `ui/` à la racine du dépôt : les chemins sont relatifs au fichier, jamais au dossier courant, donc l'interface se lance d'où l'on veut. `SEUIL_INCERTITUDE` est **la seule constante que l'on vous demande de faire varier**, et c'est l'objet du contrôle S2.

```python
def charger_predicteur():
    if not MODELE.exists():
        raise FileNotFoundError(
            "models/sentiment.joblib absent : lancez d'abord python src/train.py")
    sys.path.insert(0, str(RACINE / "src"))
    from predict import predict
    return predict
```

Deux choses à remarquer. L'erreur est **explicite** : elle dit quoi faire, pas seulement ce qui manque. Et l'import de `predict` est **tardif**, placé dans la fonction et non en tête de fichier : il n'a de sens qu'une fois le modèle présent, et cela évite de faire échouer le simple chargement du module.

C'est aussi ici que se joue le principe du TP3 : **l'interface n'invente aucune logique de prédiction**, elle appelle la fonction écrite au TP2. Le jour où l'API arrivera, elle appellera la même.

```python
def classer(texte, predicteur):
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("texte vide")
    resultat = predicteur(texte)
    incertain = resultat["score"] < SEUIL_INCERTITUDE
    resultat["verdict"] = "à vérifier" if incertain else resultat["label"]
    resultat["incertain"] = incertain
    return resultat
```

La fonction enrichit la prédiction brute d'un **verdict lisible par un non-spécialiste**. Le modèle renvoie une étiquette et un score ; l'interface, elle, doit répondre à la question « qu'est-ce que j'en fais ? ». Trois réponses possibles : traiter en priorité, ignorer, ou faire vérifier par un humain.

```python
def predire_lot(df, predicteur, colonne="review"):
    if colonne not in df.columns:
        raise KeyError(f"colonne '{colonne}' absente du fichier")
    lignes = [classer(str(t), predicteur) for t in df[colonne].fillna("") if str(t).strip()]
    if not lignes:
        raise ValueError("aucun avis exploitable dans le fichier")
    sortie = df.loc[df[colonne].fillna("").astype(str).str.strip() != ""].copy()
    sortie["prediction"] = [l["label"] for l in lignes]
    sortie["confiance"] = [round(l["score"], 3) for l in lignes]
    sortie["verdict"] = [l["verdict"] for l in lignes]
    return sortie
```

Le traitement par lot écarte les lignes vides avant de prédire, et refuse un fichier sans la bonne colonne avec un message compréhensible. Ce sont deux cas réels : un CSV exporté d'Excel contient souvent des lignes vides en fin de fichier, et une colonne nommée `texte` au lieu de `review`.

```python
def resumer(df):
    negatifs = int((df["prediction"] == "negative").sum())
    a_verifier = int((df["verdict"] == "à vérifier").sum())
    return {
        "total": len(df),
        "negatifs": negatifs,
        "part_negatifs": round(100 * negatifs / len(df), 1) if len(df) else 0.0,
        "a_verifier": a_verifier,
        "confiance_moyenne": round(float(df["confiance"].mean()), 3) if len(df) else 0.0,
    }
```

Ce résumé est la **métrique produit**, par opposition à la métrique ML du TP2. L'équipe relation client ne regarde pas un F1 : elle regarde combien d'avis arrivent, combien sont négatifs, et combien demandent une relecture. Les gardes `if len(df)` évitent une division par zéro sur un fichier vide.

### ui/app.py, les points qui comptent

```python
@st.cache_resource
def predicteur():
    return charger_predicteur()
```

**Le décorateur le plus important du fichier.** Sans lui, le fichier `joblib` serait relu à chaque clic, puisque le script se réexécute entièrement. `cache_resource` est fait pour les objets lourds et non sérialisables, comme un modèle ; `cache_data` existe pour les données.

```python
try:
    predire = predicteur()
except FileNotFoundError as erreur:
    st.error(str(erreur))
    st.info("Dans un terminal, à la racine du dépôt : `python src/train.py --allocine`")
    st.stop()
```

L'interface **ne plante pas** quand le modèle manque : elle explique et s'arrête proprement. `st.stop()` interrompt l'exécution du script sans trace d'erreur à l'écran. C'est le cas le plus fréquent sur un poste fraîchement cloné, puisque le modèle n'est jamais versionné.

```python
onglet_avis, onglet_lot, onglet_aide = st.tabs(["Un avis", "Un fichier CSV", "Comment ça marche"])
```

Trois onglets, trois usages : la démonstration vivante devant un public, le traitement réel d'un fichier, et la page d'explication qui évite de répéter dix fois la même chose.

```python
if r["incertain"]:
    st.warning(f"À vérifier par un agent (penche vers « {r['label']} »)")
elif r["label"] == "negative":
    st.error("Avis négatif : à traiter en priorité")
else:
    st.success("Avis positif")
st.progress(float(r["score"]))
```

Trois états, trois couleurs, et **la confiance toujours affichée**. Un utilisateur doit voir quand le modèle hésite : afficher un verdict tranché à 51 % de confiance, c'est mentir par omission.

```python
st.metric("Avis négatifs détectés", f"{r['negatifs']} ({r['part_negatifs']} %)")
st.bar_chart(df["prediction"].value_counts())
st.dataframe(df.sort_values(["prediction", "confiance"], ascending=[True, False]))
st.download_button("Télécharger les résultats", df.to_csv(index=False).encode("utf-8"), ...)
```

Le tri place les négatifs en tête, et les plus sûrs d'abord : c'est exactement la file de traitement décrite dans la fiche de cadrage du cas 3. Le bouton de téléchargement rend le résultat exploitable hors de l'écran, ce qui est souvent la seule chose que l'équipe métier demande.

### Le seuil d'incertitude : un arbitrage, pas un réglage

| Seuil | Avis envoyés à un agent | Risque |
| --- | --- | --- |
| 0,50 | peu | Le modèle tranche seul des cas qu'il ne maîtrise pas |
| 0,60 | modéré | Compromis retenu par défaut |
| 0,75 | beaucoup | La file humaine se remplit, l'automatisation perd son intérêt |

Ce curseur ne se décide pas dans le code : il se décide avec l'équipe métier. Modifiez `SEUIL_INCERTITUDE` dans `ui/helpers.py`, enregistrez, et Streamlit propose de relancer : l'effet est immédiat et visible. C'est la question que le compte rendu demande d'argumenter, chiffres à l'appui.

### Sur Google Colab

Streamlit ne s'affiche pas directement dans Colab : le serveur tourne sur la machine virtuelle, que votre navigateur ne peut pas joindre. Le notebook `TP3-colab-streamlit.ipynb` passe par un tunnel.

```python
!curl -s https://loca.lt/mytunnelpassword     # mot de passe du tunnel : l'IP publique
!streamlit run ui/app.py --server.headless true --server.port 8501 &>/content/log &
!npx --yes localtunnel --port 8501            # affiche une adresse loca.lt
```

L'adresse est **publique et temporaire** : aucune donnée réelle ne doit y transiter. Les tests, eux, n'ont pas besoin du tunnel, puisqu'ils importent `helpers.py` sans lancer le serveur.

---

## 7. L'intégration continue

### Le principe

L'intégration continue consiste à faire exécuter vos tests **par une machine neuve, à chaque envoi de code**, au lieu de compter sur « ça marche chez moi ». Chaque push déclenche un robot qui part d'un système vierge, installe tout à partir de votre dépôt, et rejoue l'ensemble.

Elle répond à une question que votre poste ne peut pas trancher : **votre travail fonctionne-t-il ailleurs que chez vous ?** Un paquet installé à la main il y a trois semaines, un fichier jamais poussé, un chemin absolu propre à votre machine : la CI les attrape tous.

### Le fichier

```yaml
on: [push, pull_request]
jobs:
  tp1:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: python -m venv .venv && . .venv/bin/activate && pip install pandas scikit-learn pytest
      - run: . .venv/bin/activate && python scripts/check_setup.py
      - run: . .venv/bin/activate && pytest -q
```

| Élément | Rôle |
| --- | --- |
| `on: [push, pull_request]` | Le déclencheur : à chaque push et à chaque pull request |
| `runs-on: ubuntu-latest` | Une machine Linux neuve, créée pour l'occasion et détruite après |
| `checkout@v4` | Récupère votre dépôt sur cette machine |
| `fetch-depth: 0` | Récupère **tout l'historique**. Par défaut Actions ne clone qu'un commit, et `git shortlog` ne verrait qu'un auteur : le test des deux membres échouerait toujours |
| `setup-python` en 3.11 | La version de référence du cours, quelle que soit la vôtre : c'est ainsi qu'on détecte qu'un binôme a travaillé en 3.13 |
| Le venv recréé dans chaque `run` | Chaque `run` est un shell distinct : l'activation ne se transmet pas d'une étape à l'autre. Sans cela, `test_virtualenv_active` échouerait |
| Les trois paquets seulement | La CI dure une minute ; l'installation complète est vérifiée au clone frais du contrôle T7 |

### Ce qui est vérifié, et quand

| État du dépôt | CI |
| --- | --- |
| Après le premier push du TP1 | **Rouge** : fiches vides ou un seul auteur. C'est attendu |
| Fin du TP1 | Verte : 38 tests |
| Fin du TP2 | Verte : 42 tests |
| Fin du TP3 | Verte : 45 tests |

Si la CI est rouge alors que tout passe chez vous, ouvrez le journal du passage : c'est le même pytest, et le nom du test en échec dit quoi corriger. Les deux causes habituelles sont un fichier non poussé et un seul auteur de commits.

### Le geste MLOps : vérifier un modèle qu'on n'a pas

C'est le point le plus instructif de la séquence. **La machine d'intégration n'a jamais votre modèle** : `models/sentiment.joblib` n'est pas dans le dépôt, parce qu'il est lourd et reconstructible.

| Les 4 tests du modèle | En intégration continue |
| --- | --- |
| Deux lisent `models/metrics.json` | Ils passent : le fichier est versionné |
| Deux appellent `predict()` | Ils sont ignorés : le modèle est absent |

On transporte la **preuve** de la qualité, pas l'artefact. C'est pour cela que `models/metrics.json` fait exception dans le `.gitignore`, et que le seuil d'acceptation y est inscrit à côté de la mesure.

### Trois artefacts, pas un

| Artefact | Dans Git ? | Pourquoi |
| --- | --- | --- |
| Le code | Oui | C'est le travail |
| L'environnement (`.venv/`) | Non | Reconstructible : `pip install -r requirements.txt` |
| Les données (`demo_reviews.csv`) | Non | Reconstructible : `python src/make_demo.py` |
| Le modèle (`sentiment.joblib`) | Non | Reconstructible : `python src/train.py` |
| **La mesure** (`metrics.json`) | **Oui** | Elle ne se reconstruit pas sans réentraîner |

Un logiciel classique versionne une chose : le code. Une application intelligente en versionne trois, et ce tableau est la règle qui décide, pour chacune, où elle vit.

### DevOps et MLOps

| DevOps, dans ces trois TP | MLOps, ce qui s'y ajoute |
| --- | --- |
| Environnement reproductible | Trois artefacts au lieu d'un |
| Tests automatisés | Une validation qui compare une performance à un seuil, au lieu de passer ou d'échouer |
| Versionnage à plusieurs | Des données et un modèle trop lourds pour Git |
| Intégration continue | Une dégradation possible **sans qu'on ait rien modifié** : la dérive |

Un test unitaire passe ou échoue. Un modèle a un F1 à comparer à un seuil, sur un jeu de test figé.

---

## 8. Retour d'expérience : les incidents rencontrés

Tous ces messages ont été observés en rejouant la chaîne sur un poste Windows, dans l'ordre où ils se présentent.

| # | Message | Cause | Correction |
| --- | --- | --- | --- |
| 1 | `pytest n'est pas reconnu` | Venv non activé : l'exécutable vit dans `.venv\Scripts\` | Activer, ou écrire `python -m pytest` |
| 2 | `Activate.ps1 cannot be loaded` | Politique d'exécution PowerShell | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| 3 | `--local can only be used inside a git repository` | `git config --local` lancé hors d'un dépôt | Se placer dans le dépôt, ou utiliser `--global` |
| 4 | `LF will be replaced by CRLF` | Conversion des fins de ligne par Git pour Windows | Rien à faire. Pour le faire taire : `git config --global core.autocrlf input` |
| 5 | `The requested URL returned error: 400` | Les chevrons `<organisation>` sont restés dans l'URL | `git remote set-url origin <vraie URL>` |
| 6 | `Repository not found` | L'espace réservé `votre-compte` est resté, ou le dépôt n'existe pas | Copier l'URL depuis le bouton vert **Code** |
| 7 | `Password authentication is not supported` | GitHub refuse le mot de passe du compte | Jeton d'accès personnel, ou `gh auth login` |
| 8 | `no accounts matched that criteria` | `gh auth switch` vers un compte jamais connecté | `gh auth login` d'abord, puis `gh auth status` pour l'orthographe exacte |
| 9 | `gh auth login` réautorise le mauvais compte | Le navigateur était déjà connecté sous un autre compte | Fenêtre privée, ou flux par code d'appareil, ou `--with-token` |
| 10 | `Everything up-to-date` après un changement de dépôt distant | Les deux dépôts partagent le même historique | Normal : vérifier avec `git remote -v` et la page web |
| 11 | `test_classer_ajoute_un_verdict` échoue | Kits de versions différentes : `predict()` renvoyait un champ en plus | Réinstaller le TP2 depuis le même entrepôt. Le test a été assoupli depuis |
| 12 | `cd ..\tp3-streamlit : chemin introuvable` | Le kit TP3 n'était pas décompressé | `Expand-Archive` depuis `tp1-tp2-tp3\kits\` |

### Les quatre leçons à retenir

**Les espaces réservés tuent.** Deux incidents sur douze viennent d'une URL recopiée telle quelle depuis l'énoncé. Copiez toujours l'URL depuis le bouton **Code** de GitHub.

**Un seul compte GitHub par poste.** Les incidents 7 à 10 viennent tous de la cohabitation de plusieurs comptes. Pour une séance avec des étudiants, cette règle supprime une classe entière de problèmes. Si vous devez malgré tout jongler :

```powershell
gh auth status                   # qui est connu, qui est actif
gh auth login                    # ajouter un compte, en fenêtre privée
gh auth switch --user <compte>   # basculer
gh auth setup-git                # transmettre à Git
gh api user --jq .login          # vérifier
cmdkey /delete:git:https://github.com   # vider le cache Windows en cas de 403
```

**Un même entrepôt pour les trois kits.** Mélanger des versions produit des échecs de tests déroutants, qui n'ont rien à voir avec le travail de l'étudiant.

**Lire le mot qui suit le code d'erreur.** `Password authentication is not supported` est un problème d'authentification, « qui êtes-vous ? ». `403 Forbidden` est un problème d'autorisation, « avez-vous le droit ? ». Les deux se corrigent différemment.

---

## 9. Récapitulatif

### Les dix-sept contrôles

| | Commande | Résultat attendu |
| --- | --- | --- |
| T0 | `ls` et `ls -Force` | 7 dossiers, `.gitignore` présent |
| T1 | `pytest -q` | 3 failed, 31 passed, 4 skipped |
| T2 | `pytest tests/test_cadrage.py -q` | 12 passed |
| T3 | `git status` avant le commit | aucune ligne `.venv/` |
| T4 | `python scripts/check_setup.py` | 0 erreur(s) |
| T5 | `git shortlog -sn --all` puis les tests Git | deux noms, 3 passed |
| T6 | diagnostic et `pytest -q` | 0 erreur, 0 avertissement, 38 passed |
| T7 | la suite sur un clone frais | 38 passed sans intervention |
| C1 | `pytest -q` après le kit TP2 | 2 failed, 38 passed, 2 skipped |
| C2 | `python src/make_demo.py` | 290 avis, 145 de chaque classe |
| C3 | `python src/train.py` | F1 macro 0,879 ; seul `metrics.json` en attente |
| C4 | `python src/evaluate.py` | 7 erreurs sur 58, toutes sur des avis mitigés |
| C5 | `train.py --allocine` puis `pytest -q` | F1 0,920 ; 42 passed ; CI verte |
| S1 | `streamlit run ui/app.py` | la page s'ouvre, trois onglets |
| S2 | un avis mitigé | verdict « à vérifier » sous 60 % |
| S3 | un CSV dans l'onglet 2 | métriques, graphique, tableau trié, export |
| S4 | `pytest -q` | 45 passed, CI verte |

Sur Colab, `test_virtualenv_active` est écarté : les comptes deviennent 37, 41 et 44.

### La structure finale du dépôt

```text
sentiment-app/
├── README.md TP1-ENONCE.md MARCHE-A-SUIVRE.md TESTS.md AIDE-GIT.md DEPANNAGE.md
├── requirements.txt requirements.lock .gitignore .env.example pytest.ini Makefile
├── .github/workflows/ci.yml        intégration continue
├── docs/
│   ├── cadrage/cas1, cas2, cas3    TP1, remplies (livrable noté)
│   ├── semaine2.md                 TP2, analyse des erreurs
│   ├── semaine3.md                 TP3, seuil d'incertitude
│   └── compte-rendu.md             le rendu final, figé par une étiquette Git
├── src/      make_demo, train, evaluate, predict          (TP2)
├── ui/       app.py, helpers.py                           (TP3)
├── tests/    environment (23), cadrage (12), git (3), model (4), ui (3)
├── scripts/  check_setup, setup, init_depot, verif_clone, new_cadrage
├── models/   .gitkeep + metrics.json    le modèle n'est JAMAIS commité
└── data/     sample_reviews.csv         demo_reviews.csv est régénérable
```

### Le compte rendu global

À la fin des trois séances, chaque binôme dépose un compte rendu de quatre à six pages dans `docs/compte-rendu.md`, figé par une étiquette Git :

```powershell
cp docs\compte-rendu-TEMPLATE.md docs\compte-rendu.md
git add docs\compte-rendu.md
git commit -m "Compte rendu global des TP1 a TP3"
git push
git tag -a compte-rendu -m "Version remise le <date>"
git push origin compte-rendu
```

Huit sections, noté sur 20 : cadrage, architecture, modèle, analyse des erreurs, seuil d'incertitude, ce qui a échoué, ce que vous feriez autrement, répartition du travail. L'énoncé complet est dans `ENONCE-COMPTE-RENDU.md`.

Deux exigences qui font la différence : citez **vos** chiffres, ceux de votre `models/metrics.json`, et tirez au moins un exemple d'erreur de vos propres données. Un compte rendu sans aucun échec mentionné n'est pas crédible.
