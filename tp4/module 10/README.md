# README - TP Kubernetes Managé (GKE) - Déploiement Application Web Serverless

## 📋 Objectif du TP

Déployer une application web complète en mode serverless sur Google Kubernetes Engine (GKE) avec :
- Cluster Kubernetes managé
- Application Flask conteneurisée
- Stockage partagé ReadWriteMany (RWX) avec Filestore
- Service LoadBalancer pour exposition publique

---

## 🚀 Étapes de Réalisation

### 1. Configuration Initiale GCP

```bash
# Connexion à GCP
gcloud auth login

# Création du projet
gcloud projects create module10-477208 --name="Module 10 Kubernetes"

# Configuration du projet
gcloud config set project module10-477208

# Association du compte de facturation
gcloud billing projects link module10-477208 --billing-account=01DF91-821B86-1905C1

# Configuration de la région et zone
gcloud config set compute/region europe-west1
gcloud config set compute/zone europe-west1-b

# Activation des APIs nécessaires
gcloud services enable container.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable file.googleapis.com
```

**Résultat :**
```
Operation "operations/acf.p2-630909859364-7b88946e-57c4-4231-a1e6-de49fd251b33" finished successfully.
```

---

### 2. Création du Cluster GKE

```bash
# Création du cluster avec 2 nœuds
gcloud container clusters create tp-k8s-cluster \
    --num-nodes=2 \
    --machine-type=e2-small \
    --disk-size=30 \
    --region=europe-west1 \
    --enable-autoscaling \
    --min-nodes=2 \
    --max-nodes=3
```

**Résultat :**
```
Created [https://container.googleapis.com/v1/projects/module10-477208/zones/europe-west1/clusters/tp-k8s-cluster].
NAME            LOCATION      MASTER_VERSION      MACHINE_TYPE  NODE_VERSION        NUM_NODES  STATUS
tp-k8s-cluster  europe-west1  1.33.5-gke.1201000  e2-small      1.33.5-gke.1201000  6          RUNNING
```

```bash
# Installation du plugin d'authentification GKE
gcloud components install gke-gcloud-auth-plugin

# Récupération des credentials
gcloud container clusters get-credentials tp-k8s-cluster --region=europe-west1

# Vérification des nœuds
kubectl get nodes
```

**Résultat :**
```
NAME                                            STATUS   ROLES    AGE     VERSION
gke-tp-k8s-cluster-default-pool-5bb41ec6-kjlz   Ready    <none>   5m35s   v1.33.5-gke.1201000
gke-tp-k8s-cluster-default-pool-5bb41ec6-rs6g   Ready    <none>   5m36s   v1.33.5-gke.1201000
gke-tp-k8s-cluster-default-pool-d54572cc-k5vs   Ready    <none>   5m34s   v1.33.5-gke.1201000
gke-tp-k8s-cluster-default-pool-d54572cc-txv4   Ready    <none>   5m33s   v1.33.5-gke.1201000
gke-tp-k8s-cluster-default-pool-fe12344a-2sdm   Ready    <none>   5m35s   v1.33.5-gke.1201000
gke-tp-k8s-cluster-default-pool-fe12344a-pw8g   Ready    <none>   5m35s   v1.33.5-gke.1201000
```

---

### 3. Configuration Kubernetes

```bash
# Création du namespace
kubectl create namespace tp-app

# Création du ConfigMap
kubectl create configmap app-config \
    --from-literal=APP_MESSAGE="Bienvenue sur mon application K8s" \
    --from-literal=UPLOAD_ALLOWED_EXT=".txt,.pdf,.jpg" \
    --namespace=tp-app

# Création du Secret
kubectl create secret generic app-secret \
    --from-literal=UPLOAD_PASSWORD="MonMotDePasse123" \
    --namespace=tp-app
```

**Résultat :**
```
namespace/tp-app created
configmap/app-config created
secret/app-secret created
```

---

### 4. Application Python Flask

**Fichiers créés :**

`requirements.txt` :
```txt
Flask==3.0.0
Werkzeug==3.0.1
```

`main.py` :
```python
from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

APP_MESSAGE = os.environ.get('APP_MESSAGE', 'Hello')
UPLOAD_ALLOWED_EXT = os.environ.get('UPLOAD_ALLOWED_EXT', '.txt').split(',')
UPLOAD_PASSWORD = os.environ.get('UPLOAD_PASSWORD', 'password')
UPLOAD_FOLDER = '/data'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return any(filename.endswith(ext) for ext in UPLOAD_ALLOWED_EXT)

@app.route('/', methods=['GET'])
def list_files():
    try:
        files = os.listdir(UPLOAD_FOLDER)
        return jsonify({
            'message': APP_MESSAGE,
            'files': files,
            'count': len(files)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    password = request.form.get('password', '')
    if password != UPLOAD_PASSWORD:
        return jsonify({'error': 'Mot de passe incorrect'}), 403
    
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier fourni'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Nom de fichier vide'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'error': f'Extension non autorisée. Extensions acceptées: {UPLOAD_ALLOWED_EXT}'
        }), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    return jsonify({
        'message': 'Fichier uploadé avec succès',
        'filename': filename
    }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

`Dockerfile` :
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

RUN mkdir -p /data

EXPOSE 8000

CMD ["python", "main.py"]
```

---

### 5. Conteneurisation et Registry

```bash
# Création du repository Artifact Registry
gcloud artifacts repositories create tp-k8s-repo \
    --repository-format=docker \
    --location=europe-west1 \
    --description="Repository for TP Kubernetes"

# Configuration Docker
gcloud auth configure-docker europe-west1-docker.pkg.dev

# Build de l'image
docker build -t tp-k8s-app .

# Tag de l'image
docker tag tp-k8s-app europe-west1-docker.pkg.dev/module10-477208/tp-k8s-repo/tp-k8s-app:v1

# Push vers Artifact Registry
docker push europe-west1-docker.pkg.dev/module10-477208/tp-k8s-repo/tp-k8s-app:v1
```

**Résultat :**
```
v1: digest: sha256:bebafb4cde5ff69dce9372f680c469a563952d3db1eb56c25ef95f7c4e0857f1 size: 856
```

---

### 6. Configuration du Stockage Filestore RWX

```bash
# Activation du driver Filestore CSI sur le cluster
gcloud container clusters update tp-k8s-cluster \
    --update-addons=GcpFilestoreCsiDriver=ENABLED \
    --region=europe-west1
```

**Création de la StorageClass** (`filestore-sc.yaml`) :
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard-rwx
provisioner: filestore.csi.storage.gke.io
volumeBindingMode: Immediate
allowVolumeExpansion: true
parameters:
  tier: standard
  network: default
```

```bash
kubectl apply -f filestore-sc.yaml
```

**Création du PVC** (`pvc.yaml`) :
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: shared-pvc
  namespace: tp-app
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: filestore-rwx
  resources:
    requests:
      storage: 1Gi
```

```bash
kubectl apply -f pvc.yaml
kubectl get pvc -n tp-app
```

**Résultat :**
```
NAME         STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS    AGE
shared-pvc   Bound    pvc-d66036b7-c40e-4924-a709-f7910e833064   100Gi      RWX            filestore-rwx   10m
```

---

### 7. Déploiement de l'Application

**Fichier Deployment** (`deployment.yaml`) :
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tp-app-deployment
  namespace: tp-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: tp-app
  template:
    metadata:
      labels:
        app: tp-app
    spec:
      containers:
      - name: tp-app
        image: europe-west1-docker.pkg.dev/module10-477208/tp-k8s-repo/tp-k8s-app:v1
        ports:
        - containerPort: 8000
        env:
        - name: APP_MESSAGE
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: APP_MESSAGE
        - name: UPLOAD_ALLOWED_EXT
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: UPLOAD_ALLOWED_EXT
        - name: UPLOAD_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: UPLOAD_PASSWORD
        volumeMounts:
        - name: data-volume
          mountPath: /data
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: shared-pvc
```

```bash
kubectl apply -f deployment.yaml
kubectl get pods -n tp-app
```

**Résultat :**
```
NAME                                READY   STATUS    RESTARTS   AGE
tp-app-deployment-5b77d7c68-p6cgk   1/1     Running   0          5s
tp-app-deployment-5b77d7c68-pc2vh   1/1     Running   0          6s
```

---

### 8. Exposition via LoadBalancer

**Fichier Service** (`service.yaml`) :
```yaml
apiVersion: v1
kind: Service
metadata:
  name: tp-app-service
  namespace: tp-app
spec:
  type: LoadBalancer
  selector:
    app: tp-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

```bash
kubectl apply -f service.yaml
kubectl get service tp-app-service -n tp-app
```

**Résultat :**
```
NAME             TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)        AGE
tp-app-service   LoadBalancer   34.118.238.34   35.187.43.243   80:32202/TCP   35s
```

---

## ✅ Tests et Validation

### Test 1 : Vérification RWX - Écriture Pod 1

```bash
kubectl exec -n tp-app tp-app-deployment-5b77d7c68-p6cgk -- sh -c "echo 'RWX fonctionne!' > /data/success.txt"
kubectl exec -n tp-app tp-app-deployment-5b77d7c68-p6cgk -- ls -la /data
```

**Résultat :**
```
total 28
drwxr-xr-x 3 root root  4096 Nov 25 11:03 .
drwxr-xr-x 1 root root  4096 Nov 25 11:02 ..
drwx------ 2 root root 16384 Nov 25 10:59 lost+found
-rw-r--r-- 1 root root    16 Nov 25 11:03 success.txt
```

### Test 2 : Vérification RWX - Lecture Pod 2

```bash
kubectl exec -n tp-app tp-app-deployment-5b77d7c68-pc2vh -- ls -la /data
```

**Résultat :**
```
total 28
drwxr-xr-x 3 root root  4096 Nov 25 11:03 .
drwxr-xr-x 1 root root  4096 Nov 25 11:02 ..
drwx------ 2 root root 16384 Nov 25 10:59 lost+found
-rw-r--r-- 1 root root    16 Nov 25 11:03 success.txt
```

**✅ Les deux pods voient le même fichier !**

### Test 3 : Écriture croisée Pod 2

```bash
kubectl exec -n tp-app tp-app-deployment-5b77d7c68-pc2vh -- sh -c "echo 'Ecrit par Pod 2' > /data/from-pod2.txt"
kubectl exec -n tp-app tp-app-deployment-5b77d7c68-p6cgk -- ls -la /data
```

**Résultat :**
```
total 32
drwxr-xr-x 3 root root  4096 Nov 25 11:04 .
drwxr-xr-x 1 root root  4096 Nov 25 11:02 ..
-rw-r--r-- 1 root root    16 Nov 25 11:04 from-pod2.txt
drwx------ 2 root root 16384 Nov 25 10:59 lost+found
-rw-r--r-- 1 root root    16 Nov 25 11:03 success.txt
```

**✅ Pod 1 voit le fichier créé par Pod 2 !**

### Test 4 : Upload via API

```bash
echo "Test final RWX API" > final-test.txt
curl -X POST -F "password=MonMotDePasse123" -F "file=@final-test.txt" http://35.187.43.243/upload
```

**Résultat :**
```json
{"filename":"final-test.txt","message":"Fichier uploadé avec succès"}
```

```bash
curl http://35.187.43.243/
```

**Résultat (3 requêtes identiques) :**
```json
{"count":4,"files":["lost+found","success.txt","from-pod2.txt","final-test.txt"],"message":"Bienvenue sur mon application K8s"}
```

**✅ Toutes les requêtes retournent les mêmes fichiers !**

### Test 5 : Résilience - Suppression Pod

```bash
kubectl delete pod tp-app-deployment-5b77d7c68-p6cgk -n tp-app
curl http://35.187.43.243/
```

**Résultat :**
```json
{"count":4,"files":["lost+found","success.txt","from-pod2.txt","final-test.txt"],"message":"Bienvenue sur mon application K8s"}
```

**✅ Le service continue de fonctionner !**

```bash
kubectl get pods -n tp-app
```

**Résultat :**
```
NAME                                READY   STATUS    RESTARTS   AGE
tp-app-deployment-5b77d7c68-pc2vh   1/1     Running   0          5m14s
tp-app-deployment-5b77d7c68-wrkvh   1/1     Running   0          57s
```

```bash
kubectl exec -n tp-app tp-app-deployment-5b77d7c68-wrkvh -- ls -la /data
```

**Résultat :**
```
total 36
drwxr-xr-x 3 root root  4096 Nov 25 11:05 .
drwxr-xr-x 1 root root  4096 Nov 25 11:06 ..
-rw-r--r-- 1 root root    23 Nov 25 11:05 final-test.txt
-rw-r--r-- 1 root root    16 Nov 25 11:04 from-pod2.txt
drwx------ 2 root root 16384 Nov 25 10:59 lost+found
-rw-r--r-- 1 root root    16 Nov 25 11:03 success.txt
```

**✅ Le nouveau pod voit immédiatement tous les fichiers !**

---

## 🎯 Validation Finale

### Checklist Complète

- ✅ **Cluster GKE** : 6 nœuds répartis sur 3 zones
- ✅ **Namespace** : tp-app créé
- ✅ **ConfigMap & Secret** : Configuration injectée
- ✅ **Application Flask** : Conteneurisée et déployée
- ✅ **Artifact Registry** : Image stockée
- ✅ **PVC RWX** : 100Gi Filestore en mode ReadWriteMany
- ✅ **Deployment** : 2 replicas fonctionnels
- ✅ **Service LoadBalancer** : IP publique 35.187.43.243
- ✅ **Partage RWX** : Les 2 pods voient les mêmes fichiers
- ✅ **Écriture croisée** : Fichiers visibles entre pods
- ✅ **Upload API** : Fichiers accessibles via tous les pods
- ✅ **GET API** : Retourne toujours les mêmes données
- ✅ **Résilience** : Suppression pod → service continue
- ✅ **Persistance** : Nouveau pod voit immédiatement les données

---

## 📊 Architecture Finale

```
Internet
    │
    ▼
LoadBalancer (35.187.43.243:80)
    │
    ├──▶ Pod 1 (Flask:8000) ──┐
    │                          │
    └──▶ Pod 2 (Flask:8000) ──┼──▶ Filestore NFS (100Gi RWX)
                               │    10.214.249.26:/vol1
                               │
                               └──▶ /data (partagé entre tous les pods)
```

---

## 🧹 Nettoyage

```bash
# Supprimer le namespace (supprime tout)
kubectl delete namespace tp-app

# Supprimer le cluster
gcloud container clusters delete tp-k8s-cluster --region=europe-west1 --quiet

# Supprimer le repository
gcloud artifacts repositories delete tp-k8s-repo --location=europe-west1 --quiet
```

---

## 📝 Problèmes Rencontrés et Solutions

### Problème 1 : RWX ne fonctionnait pas initialement

**Cause** : Le `deployment.yaml` utilisait `emptyDir: {}` au lieu de `persistentVolumeClaim`

**Solution** : Modification de la section `volumes` pour référencer le PVC :
```yaml
volumes:
- name: data-volume
  persistentVolumeClaim:
    claimName: shared-pvc
```

### Problème 2 : Pods en `Pending`

**Cause** : PVC non créé ou StorageClass inexistante

**Solution** : 
1. Activation du driver Filestore CSI sur GKE
2. Création de la StorageClass `standard-rwx`
3. Création du PVC avec `storageClassName: filestore-rwx`

---

## 🏆 Conclusion

TP complété avec succès ! Tous les objectifs ont été atteints :
- Application serverless déployée sur GKE
- Stockage partagé RWX fonctionnel avec Filestore
- Haute disponibilité avec 2 replicas
- Résilience validée (suppression/recréation de pods)
- Persistance des données garantie

**Durée totale du TP** : ~2 heures  
**Coût estimé** : ~5-10€ (à supprimer rapidement pour éviter les frais)

---

## 📚 Références

- [Documentation GKE](https://cloud.google.com/kubernetes-engine/docs)
- [Filestore CSI Driver](https://cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/filestore-csi-driver)
- [Kubernetes Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Auteur** : Guillaume Ozoux  
**Date** : 25 Novembre 2025  
**Projet** : module10-477208