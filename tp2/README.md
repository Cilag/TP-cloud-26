# TP2 CLOUD – Flask API + Frontend

Ce TP contient :
- Une API Python Flask exposant `GET /hello` (CORS activé)
- Un frontend statique (`index.html`, `script.js`) avec un bouton qui appelle l’API et affiche la réponse
- Un Dockerfile pour construire l’image et déployer sur Cloud Run

## Lancer en local

1. (Optionnel) Créez un environnement virtuel :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Installez les dépendances :

```powershell
pip install -r requirements.txt
```

3. Lancez l’API :

```powershell
python .\api.py
```

L’API écoute sur http://127.0.0.1:8080/hello

4. Servez le frontend (dans un autre terminal) :

```powershell
python -m http.server 5500
```

Ouvrez http://127.0.0.1:5500 puis cliquez sur "Appeler l’API".

> Par défaut `script.js` pointe vers l’URL Cloud Run. Pour tester en local, remplacez l’URL par `http://127.0.0.1:8080/hello`.

## Construire l’image Docker

```powershell
docker build -t flask-api .
```

Tester en local :

```powershell
docker run --rm -p 8080:8080 flask-api
```

Puis ouvrez http://127.0.0.1:8080/hello

## Déploiement Cloud Run (exemple)

Variables d’exemple :
- Région : `europe-west1`
- Projet : `tp2cloud-477208`
- Image : `europe-west1-docker.pkg.dev/tp2cloud-477208/flask-api-repo/flask-api:latest`

Étapes (résumé) :

```powershell
# Auth et projet
gcloud auth login
gcloud config set project tp2cloud-477208

# Activer APIs (si nécessaire)
gcloud services enable run.googleapis.com artifactregistry.googleapis.com

# Créer dépôt Artifact Registry (si pas créé)
gcloud artifacts repositories create flask-api-repo --repository-format=docker --location=europe-west1 --description="Flask API"

# Tag & push l’image
docker tag flask-api europe-west1-docker.pkg.dev/tp2cloud-477208/flask-api-repo/flask-api:latest
docker push europe-west1-docker.pkg.dev/tp2cloud-477208/flask-api-repo/flask-api:latest

# Déployer sur Cloud Run (public)
gcloud run deploy flask-api ^
  --image europe-west1-docker.pkg.dev/tp2cloud-477208/flask-api-repo/flask-api:latest ^
  --platform managed ^
  --region europe-west1 ^
  --allow-unauthenticated
```

L’URL de service Cloud Run est affichée à la fin (ex : `https://flask-api-xxxxxx.europe-west1.run.app`).

Mettez à jour `script.js` avec cette URL :

```javascript
const API_URL = 'https://flask-api-xxxxxx.europe-west1.run.app/hello';
```

## Publication sur GitHub

```powershell
git init
 git add .
 git commit -m "TP2: API Flask /hello + front + Dockerfile"
 git branch -M main
 git remote add origin https://github.com/<votre-utilisateur>/<votre-repo>.git
 git push -u origin main
```

## Dépannage
- CORS: `Flask-Cors` est activé. Évitez d’ajouter des headers inutiles (ex: `Content-Type` sur GET) qui déclenchent un preflight.
- Ports occupés: changez de port (`app.run(port=8081)`), adaptez l’URL.
- Pare-feu: autorisez Python/Docker si Windows le demande.
- Dockerfile introuvable: assurez-vous que le fichier s’appelle `Dockerfile` (majuscules) ou utilisez `-f dockerfile`.
