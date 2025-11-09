# 🔐 TP3 - Gestion des Identités et des Rôles sur Google Cloud Platform

**Projet GCP:** `tp3partie1et2`  
**Date:** 09 novembre 2025  
**Étudiant:** Guillaume Ozoux

---

## 📑 Table des matières

1. [Exercice 1 - Créer les identités de base](#exercice-1)
2. [Exercice 2 - Explorer IAM et les rôles](#exercice-2)
3. [Exercice 3 - Portée des rôles et permissions](#exercice-3)
4. [Exercice 4 - Rôle personnalisé Cloud Run](#exercice-4)
5. [Exercice 5 - Comptes de service applicatifs](#exercice-5)
6. [Exercice 6 - Impersonation](#exercice-6)
7. [Exercice 7 - Accès temporaire](#exercice-7)
8. [Exercice 8 - Audit et traçabilité](#exercice-8)

---

## Exercice 1

### Ajouter un utilisateur Viewer

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud projects add-iam-policy-binding tp3partie1et2 --member="user:guillaumeozoux33@gmail.com" --role="roles/viewer"
Updated IAM policy for project [tp3partie1et2].
bindings:
- members:
  - user:ozouxguillaume@gmail.com
  role: roles/owner
- members:
  - user:guillaumeozoux33@gmail.com
  role: roles/viewer
etag: BwZDJrTp6KU=
version: 1
```

---

### Ajouter un utilisateur Editor

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud projects add-iam-policy-binding tp3partie1et2 --member="user:collaborateur0013@gmail.com" --role="roles/editor"
Updated IAM policy for project [tp3partie1et2].
bindings:
- members:
  - user:collaborateur0013@gmail.com
  role: roles/editor
- members:
  - user:ozouxguillaume@gmail.com
  role: roles/owner
- members:
  - user:guillaumeozoux33@gmail.com
  role: roles/viewer
etag: BwZDJsvzitU=
version: 1
```

---

### Créer le compte de service app-backend

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud iam service-accounts create app-backend --display-name="ApplicationBackend"
Created service account [app-backend].
```

---

### Lister les comptes de service

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud iam service-accounts list
DISPLAY NAME        EMAIL                                              DISABLED
ApplicationBackend  app-backend@tp3partie1et2.iam.gserviceaccount.com  False
```

---

## Exercice 2

### Afficher la politique IAM du projet

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud projects get-iam-policy tp3partie1et2
bindings:
- members:
  - user:collaborateur0013@gmail.com
  role: roles/editor
- members:
  - user:ozouxguillaume@gmail.com
  role: roles/owner
- members:
  - user:guillaumeozoux33@gmail.com
  role: roles/viewer
etag: BwZDJsvzitU=
version: 1
```

---

## Exercice 3

### Décrire le rôle Storage Object Viewer

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud iam roles describe roles/storage.objectViewer
description: Grants access to view objects and their metadata, excluding ACLs. Can
  also list the objects in a bucket.
etag: AA==
includedPermissions:
- resourcemanager.projects.get
- resourcemanager.projects.list
- storage.folders.get
- storage.folders.list
- storage.managedFolders.get
- storage.managedFolders.list
- storage.objects.get
- storage.objects.list
name: roles/storage.objectViewer
stage: GA
title: Storage Object Viewer
```

---

### Créer un bucket Cloud Storage

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gsutil mb -p tp3partie1et2 gs://nom-bucket-unique/
Creating gs://nom-bucket-unique/...
```

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>echo "test" > test.txt
```

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gsutil cp test.txt gs://nom-bucket-unique/
Copying file://test.txt [Content-Type=text/plain]...
/ [1 files][    9.0 B/    9.0 B]
Operation completed over 1 objects/9.0 B.
```

---

### Lister les permissions testables sur le bucket

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud iam list-testable-permissions //storage.googleapis.com/projects/_/buckets/nom-bucket-unique
---
name: resourcemanager.hierarchyNodes.createTagBinding
stage: GA
---
name: resourcemanager.hierarchyNodes.deleteTagBinding
stage: GA
---
name: resourcemanager.hierarchyNodes.listEffectiveTags
stage: GA
---
name: resourcemanager.hierarchyNodes.listTagBindings
stage: GA
---
name: resourcemanager.resourceTagBindings.create
primaryPermission: resourcemanager.hierarchyNodes.createTagBinding
stage: GA
---
name: resourcemanager.resourceTagBindings.delete
primaryPermission: resourcemanager.hierarchyNodes.deleteTagBinding
stage: GA
---
name: resourcemanager.resourceTagBindings.list
primaryPermission: resourcemanager.hierarchyNodes.listTagBindings
stage: GA
---
name: storage.anywhereCaches.create
stage: BETA
title: Create GCS Anywhere Caches
---
name: storage.anywhereCaches.disable
stage: BETA
title: Disable GCS Anywhere Caches
---
name: storage.anywhereCaches.get
stage: BETA
title: Get GCS Anywhere Caches Metadata
---
name: storage.anywhereCaches.list
stage: BETA
title: Get GCS Anywhere Caches Metadata
---
name: storage.anywhereCaches.pause
stage: BETA
title: Pause GCS Anywhere Caches
---
name: storage.anywhereCaches.resume
stage: BETA
title: Resume GCS Anywhere Caches
---
name: storage.anywhereCaches.update
stage: BETA
title: Update GCS Anywhere Caches
---
name: storage.bucketOperations.cancel
stage: GA
title: Cancel GCS Bucket Long-running Operation
---
name: storage.bucketOperations.get
stage: GA
title: Get GCS Bucket Long-running Operation
---
name: storage.bucketOperations.list
stage: GA
title: List GCS Bucket Long-running Operations
---
name: storage.buckets.createTagBinding
stage: GA
title: Create Tag Bindings on GCS Bucket
---
name: storage.buckets.delete
stage: GA
title: Delete GCS Bucket
---
name: storage.buckets.deleteTagBinding
stage: GA
title: Delete Tag Bindings on GCS Bucket
---
name: storage.buckets.enableObjectRetention
stage: GA
title: Enable Object Retention on GCS Bucket
---
name: storage.buckets.exemptFromIpFilter
stage: BETA
title: Exempt From IP filtering
---
name: storage.buckets.get
stage: GA
title: Read GCS Bucket Metadata
---
name: storage.buckets.getIamPolicy
stage: GA
title: Read GCS Bucket IAM Policy
---
name: storage.buckets.getIpFilter
stage: BETA
title: Read GCS Bucket Ip Filtering Configuration
---
name: storage.buckets.getObjectInsights
stage: GA
title: Collect insights for all the objects in the bucket
---
name: storage.buckets.listEffectiveTags
stage: GA
title: List Effective Tag Bindings on GCS Bucket
---
name: storage.buckets.listTagBindings
stage: GA
title: List Tag Bindings on GCS Bucket
---
name: storage.buckets.relocate
stage: BETA
title: Relocate GCS Bucket
---
name: storage.buckets.restore
stage: GA
title: Restore GCS Bucket
---
name: storage.buckets.setIamPolicy
stage: GA
title: Set GCS Bucket IAM Policy
---
name: storage.buckets.setIpFilter
stage: BETA
title: Set GCS Bucket Ip Filtering Configuration
---
name: storage.buckets.update
stage: GA
title: Update GCS Bucket Metadata
---
name: storage.folders.create
stage: GA
title: Create GCS Folder
---
name: storage.folders.delete
stage: GA
title: Delete GCS Folder
---
name: storage.folders.get
stage: GA
title: Get GCS Folder Metadata
---
name: storage.folders.list
stage: GA
title: List GCS Folder
---
name: storage.folders.rename
stage: GA
title: Rename GCS Folder
---
name: storage.managedFolders.create
stage: GA
title: Create GCS Managed Folders
---
name: storage.managedFolders.delete
stage: GA
title: Delete GCS Managed Folders
---
name: storage.managedFolders.get
stage: GA
title: Get GCS Managed Folders Metadata
---
name: storage.managedFolders.getIamPolicy
stage: GA
title: Read GCS Managed Folders IAM Policy
---
name: storage.managedFolders.list
stage: GA
title: List GCS Managed Folders
---
name: storage.managedFolders.setIamPolicy
stage: GA
title: Set GCS Managed Folders IAM Policy
---
name: storage.multipartUploads.abort
stage: GA
title: Abort GCS Multipart Upload
---
name: storage.multipartUploads.create
stage: GA
title: Create GCS Multipart Upload
---
name: storage.multipartUploads.list
stage: GA
title: List GCS Multipart Uploads
---
name: storage.multipartUploads.listParts
stage: GA
title: List GCS Multipart Upload Parts
---
name: storage.objects.create
stage: GA
title: Create GCS Object
---
name: storage.objects.createContext
stage: BETA
title: Create GCS Object Contexts
---
name: storage.objects.delete
stage: GA
title: Delete GCS Object
---
name: storage.objects.deleteContext
stage: BETA
title: Delete GCS Object Contexts
---
name: storage.objects.get
stage: GA
title: Read GCS Object Data and Metadata
---
name: storage.objects.getIamPolicy
stage: GA
title: Get GCS Object IAM Policy
---
name: storage.objects.list
stage: GA
title: List GCS Objects
---
name: storage.objects.move
stage: GA
title: Move GCS Object
---
name: storage.objects.overrideUnlockedRetention
stage: GA
title: Override Unlocked GCS Object Retention
---
name: storage.objects.restore
stage: GA
title: Restore GCS Object
---
name: storage.objects.setIamPolicy
stage: GA
title: Set GCS Object IAM Policy
---
name: storage.objects.setRetention
stage: GA
title: Set GCS Object Retention
---
name: storage.objects.update
stage: GA
title: Update GCS Object Metadata
---
name: storage.objects.updateContext
stage: BETA
title: Update GCS Object Contexts
```

---

### Accorder le rôle Storage Object Viewer sur le bucket

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gsutil iam ch user:collaborateur0013@gmail.com:roles/storage.objectViewer gs://nom-bucket-unique
```

---

### Vérifier la politique IAM du bucket

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gsutil iam get gs://nom-bucket-unique
{
  "bindings": [
    {
      "members": [
        "projectEditor:tp3partie1et2",
        "projectOwner:tp3partie1et2"
      ],
      "role": "roles/storage.legacyBucketOwner"
    },
    {
      "members": [
        "projectViewer:tp3partie1et2"
      ],
      "role": "roles/storage.legacyBucketReader"
    },
    {
      "members": [
        "user:collaborateur0013@gmail.com"
      ],
      "role": "roles/storage.objectViewer"
    }
  ],
  "etag": "CAI="
}
```

---

### Tester l'accès avec le compte collaborateur

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud auth login
Your browser has been opened to visit:

    https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=32555940559.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8085%2F&scope=openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fappengine.admin+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fsqlservice.login+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcompute+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Faccounts.reauth&state=ODXUimeGodCk0nCsUmL5OBnnSk8hwL&access_type=offline&code_challenge=2g9PqorxEpc1b5G6nGhTcIb4TkfI6Utid_Tm7RetrJA&code_challenge_method=S256


You are now logged in as [collaborateur0013@gmail.com].
Your current project is [tp3cloud-477409a].  You can change this setting by running:
  $ gcloud config set project PROJECT_ID


Updates are available for some Google Cloud CLI components.  To install them,
please run:
  $ gcloud components update
```

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud config set project tp3partie1et2
Updated property [core/project].
```

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gsutil ls gs://nom-bucket-unique/
gs://nom-bucket-unique/test.txt
```

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gsutil cp gs://nom-bucket-unique/test.txt .
Copying gs://nom-bucket-unique/test.txt...
/ [1 files][    9.0 B/    9.0 B]
Operation completed over 1 objects/9.0 B.
```

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gsutil ls gs://autre-bucket/
BucketNotFoundException: 404 gs://autre-bucket bucket does not exist.
```

---

## Exercice 4

### Créer le fichier YAML du rôle personnalisé

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>notepad custom-cloud-run-role.yaml
```

**Contenu du fichier :**
```yaml
title: "Custom Cloud Run Deployer"
description: "Permet de deployer, lister et supprimer des services Cloud Run"
stage: "GA"
includedPermissions:
- run.services.create
- run.services.delete
- run.services.get
- run.services.list
- run.services.update
- run.operations.get
- run.operations.list
- run.locations.list
```

---

### Créer le rôle personnalisé

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud iam roles create customCloudRunDeployer --project=tp3partie1et2 --file=custom-cloud-run-role.yaml
WARNING: API is not enabled for permissions: [run.services.create, run.services.delete, run.services.get, run.services.list, run.services.update, run.operations.get, run.operations.list, run.locations.list]. Please enable the corresponding APIs to use those permissions.

Created role [customCloudRunDeployer].
description: Permet de deployer, lister et supprimer des services Cloud Run
etag: BwZDKAIYoHQ=
includedPermissions:
- run.locations.list
- run.operations.get
- run.operations.list
- run.services.create
- run.services.delete
- run.services.get
- run.services.list
- run.services.update
name: projects/tp3partie1et2/roles/customCloudRunDeployer
stage: GA
title: Custom Cloud Run Deployer
```

---

### Lister les rôles personnalisés

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud iam roles list --project=tp3partie1et2
---
description: Permet de deployer, lister et supprimer des services Cloud Run
etag: BwZDKAIYoHQ=
name: projects/tp3partie1et2/roles/customCloudRunDeployer
stage: GA
title: Custom Cloud Run Deployer
```

---

### Activer l'API Cloud Run

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud services enable run.googleapis.com
Operation "operations/acf.p2-402564488059-33c8e610-5008-465f-98d4-3cb51a2dc04c" finished successfully.
```

---

### Attribuer le rôle au collaborateur

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud projects add-iam-policy-binding tp3partie1et2 --member="user:collaborateur0013@gmail.com" --role="projects/tp3partie1et2/roles/customCloudRunDeployer"
Updated IAM policy for project [tp3partie1et2].
bindings:
- members:
  - user:collaborateur0013@gmail.com
  role: projects/tp3partie1et2/roles/customCloudRunDeployer
- members:
  - serviceAccount:service-402564488059@containerregistry.iam.gserviceaccount.com
  role: roles/containerregistry.ServiceAgent
- members:
  - serviceAccount:402564488059-compute@developer.gserviceaccount.com
  role: roles/editor
- members:
  - user:ozouxguillaume@gmail.com
  role: roles/owner
- members:
  - serviceAccount:service-402564488059@gcp-sa-pubsub.iam.gserviceaccount.com
  role: roles/pubsub.serviceAgent
- members:
  - serviceAccount:service-402564488059@serverless-robot-prod.iam.gserviceaccount.com
  role: roles/run.serviceAgent
- members:
  - user:guillaumeozoux33@gmail.com
  role: roles/viewer
etag: BwZDKAiIgAE=
version: 1
```

---

### Vérifier l'attribution du rôle

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud projects get-iam-policy tp3partie1et2 --flatten="bindings[].members" --filter="bindings.role:customCloudRunDeployer"
---
bindings:
  members: user:collaborateur0013@gmail.com
  role: projects/tp3partie1et2/roles/customCloudRunDeployer
etag: BwZDKAiIgAE=
version: 1
```

---

### Restaurer le rôle supprimé

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud iam roles undelete customCloudRunDeployer --project=tp3partie1et2
description: Permet de deployer, lister et supprimer des services Cloud Run
etag: BwZDKCHBcq0=
includedPermissions:
- run.locations.list
- run.operations.get
- run.operations.list
- run.services.create
- run.services.delete
- run.services.get
- run.services.list
- run.services.update
name: projects/tp3partie1et2/roles/customCloudRunDeployer
stage: GA
title: Custom Cloud Run Deployer
```

---

### Mettre à jour le rôle personnalisé

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud iam roles update customCloudRunDeployer --project=tp3partie1et2 --file=custom-cloud-run-role.yaml
The specified role does not contain an "etag" field identifying a specific version to
 replace. Updating a role without an "etag" can overwrite concurrent role changes.

Replace existing role (Y/n)?  y

description: Permet de deployer, lister et supprimer des services Cloud Run
etag: BwZDKCNuXqw=
includedPermissions:
- run.locations.list
- run.operations.get
- run.operations.list
- run.services.create
- run.services.delete
- run.services.get
- run.services.list
- run.services.update
name: projects/tp3partie1et2/roles/customCloudRunDeployer
stage: GA
title: Custom Cloud Run Deployer
```

---

### Réattribuer le rôle

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud projects add-iam-policy-binding tp3partie1et2 --member="user:collaborateur0013@gmail.com" --role="projects/tp3partie1et2/roles/customCloudRunDeployer"
Updated IAM policy for project [tp3partie1et2].
bindings:
- members:
  - user:collaborateur0013@gmail.com
  role: projects/tp3partie1et2/roles/customCloudRunDeployer
- members:
  - serviceAccount:service-402564488059@containerregistry.iam.gserviceaccount.com
  role: roles/containerregistry.ServiceAgent
- members:
  - serviceAccount:402564488059-compute@developer.gserviceaccount.com
  role: roles/editor
- members:
  - user:ozouxguillaume@gmail.com
  role: roles/owner
- members:
  - serviceAccount:service-402564488059@gcp-sa-pubsub.iam.gserviceaccount.com
  role: roles/pubsub.serviceAgent
- members:
  - serviceAccount:service-402564488059@serverless-robot-prod.iam.gserviceaccount.com
  role: roles/run.serviceAgent
- members:
  - user:guillaumeozoux33@gmail.com
  role: roles/viewer
etag: BwZDKCT0Mso=
version: 1
```

---

## Exercice 5

### Accorder permissions Cloud Build - Logging

```
PS C:\Users\ozoux\tp3cloud> gcloud projects add-iam-policy-binding tp3partie1et2 --member="serviceAccount:402564488059@cloudbuild.gserviceaccount.com" --role="roles/logging.logWriter"
Updated IAM policy for project [tp3partie1et2].
bindings:
- members:
  - user:collaborateur0013@gmail.com
  role: projects/tp3partie1et2/roles/customCloudRunDeployer
- members:
  - serviceAccount:service-402564488059@gcp-sa-artifactregistry.iam.gserviceaccount.com
  role: roles/artifactregistry.serviceAgent
- members:
  - serviceAccount:402564488059@cloudbuild.gserviceaccount.com
  role: roles/cloudbuild.builds.builder
- members:
  - serviceAccount:service-402564488059@gcp-sa-cloudbuild.iam.gserviceaccount.com
  role: roles/cloudbuild.serviceAgent
- members:
  - serviceAccount:service-402564488059@containerregistry.iam.gserviceaccount.com
  role: roles/containerregistry.ServiceAgent
- members:
  - serviceAccount:402564488059-compute@developer.gserviceaccount.com
  role: roles/editor
- members:
  - serviceAccount:402564488059@cloudbuild.gserviceaccount.com
  role: roles/logging.logWriter
- members:
  - user:ozouxguillaume@gmail.com
  role: roles/owner
- members:
  - serviceAccount:service-402564488059@gcp-sa-pubsub.iam.gserviceaccount.com
  role: roles/pubsub.serviceAgent
- members:
  - serviceAccount:service-402564488059@serverless-robot-prod.iam.gserviceaccount.com
  role: roles/run.serviceAgent
- members:
  - user:guillaumeozoux33@gmail.com
  role: roles/viewer
etag: BwZDKJmeJvQ=
version: 1
```

---

### Accorder permissions Cloud Build - Storage Admin

```
PS C:\Users\ozoux\tp3cloud> gcloud projects add-iam-policy-binding tp3partie1et2 --member="serviceAccount:402564488059@cloudbuild.gserviceaccount.com" --role="roles/storage.admin"
Updated IAM policy for project [tp3partie1et2].
bindings:
- members:
  - user:collaborateur0013@gmail.com
  role: projects/tp3partie1et2/roles/customCloudRunDeployer
- members:
  - serviceAccount:service-402564488059@gcp-sa-artifactregistry.iam.gserviceaccount.com
  role: roles/artifactregistry.serviceAgent
- members:
  - serviceAccount:402564488059@cloudbuild.gserviceaccount.com
  role: roles/artifactregistry.writer
- members:
  - serviceAccount:402564488059@cloudbuild.gserviceaccount.com
  role: roles/cloudbuild.builds.builder
- members:
  - serviceAccount:service-402564488059@gcp-sa-cloudbuild.iam.gserviceaccount.com
  role: roles/cloudbuild.serviceAgent
- members:
  - serviceAccount:service-402564488059@containerregistry.iam.gserviceaccount.com
  role: roles/containerregistry.ServiceAgent
- members:
  - serviceAccount:402564488059-compute@developer.gserviceaccount.com
  role: roles/editor
- members:
  - serviceAccount:402564488059@cloudbuild.gserviceaccount.com
  role: roles/logging.logWriter
- members:
  - user:ozouxguillaume@gmail.com
  role: roles/owner
- members:
  - serviceAccount:service-402564488059@gcp-sa-pubsub.iam.gserviceaccount.com
  role: roles/pubsub.serviceAgent
- members:
  - serviceAccount:service-402564488059@serverless-robot-prod.iam.gserviceaccount.com
  role: roles/run.serviceAgent
- members:
  - serviceAccount:402564488059@cloudbuild.gserviceaccount.com
  role: roles/storage.admin
- members:
  - user:guillaumeozoux33@gmail.com
  role: roles/viewer
etag: BwZDKJyiU3c=
version: 1
```

---

### Accorder permissions Cloud Build - Artifact Registry Writer

```
PS C:\Users\ozoux\tp3cloud> gcloud projects add-iam-policy-binding tp3partie1et2 --member="serviceAccount:402564488059@cloudbuild.gserviceaccount.com" --role="roles/artifactregistry.writer"
Updated IAM policy for project [tp3partie1et2].
bindings:
- members:
  - user:collaborateur0013@gmail.com
  role: projects/tp3partie1et2/roles/customCloudRunDeployer
- members:
  - serviceAccount:service-402564488059@gcp-sa-artifactregistry.iam.gserviceaccount.com
  role: roles/artifactregistry.serviceAgent
- members:
  - serviceAccount:402564488059@cloudbuild.gserviceaccount.com
  role: roles/artifactregistry.writer
- members:
  - serviceAccount:402564488059@cloudbuild.gserviceaccount.com
  role: roles/cloudbuild.builds.builder
- members:
  - serviceAccount:service-402564488059@gcp-sa-cloudbuild.iam.gserviceaccount.com
  role: roles/cloudbuild.serviceAgent
- members:
  - serviceAccount:service-402564488059@containerregistry.iam.gserviceaccount.com
  role: roles/containerregistry.ServiceAgent
- members:
  - serviceAccount:402564488059-compute@developer.gserviceaccount.com
  role: roles/editor
- members:
  - serviceAccount:402564488059@cloudbuild.gserviceaccount.com
  role: roles/logging.logWriter
- members:
  - user:ozouxguillaume@gmail.com
  role: roles/owner
- members:
  - serviceAccount:service-402564488059@gcp-sa-pubsub.iam.gserviceaccount.com
  role: roles/pubsub.serviceAgent
- members:
  - serviceAccount:service-402564488059@serverless-robot-prod.iam.gserviceaccount.com
  role: roles/run.serviceAgent
- members:
  - serviceAccount:402564488059@cloudbuild.gserviceaccount.com
  role: roles/storage.admin
- members:
  - user:guillaumeozoux33@gmail.com
  role: roles/viewer
etag: BwZDKJ_YF9o=
version: 1
```

---

### Déployer le service Cloud Run

```
PS C:\Users\ozoux\tp3cloud> gcloud run deploy run-backend --source . --region=europe-west1 --service-account=run-backend@tp3partie1et2.iam.gserviceaccount.com --set-env-vars=BUCKET_NAME=nom-bucket-unique --allow-unauthenticated
Deploying from source requires an Artifact Registry Docker repository to store built containers. A repository named
[cloud-run-source-deploy] in region [europe-west1] will be created.
Do you want to continue (Y/n)?  y
Building using Dockerfile and deploying container to Cloud Run service [run-backend] in project [tp3partie1et2] region [europe-west1]
X  Building and deploying new service... Uploading sources.
  OK Creating Container Repository...
  OK Validating Service...
  OK Uploading sources...
  .  Building Container...
  .  Creating Revision...
  .  Routing traffic...
  .  Setting IAM Policy...
Deployment failed
ERROR: (gcloud.run.deploy) PERMISSION_DENIED: Build failed because the default service account is missing required IAM permissions. Follow the instructions at https://cloud.google.com/build/docs/cloud-build-service-account-updates#get_the_current_default_service_account_for_a_project to get the default service account for your project, and see https://cloud.google.com/run/docs/configuring/services/build-service-account for more details. could not resolve source: Get "https://storage.googleapis.com/storage/v1/b/run-sources-tp3partie1et2-europe-west1/o/services%2Frun-backend%2F1762691403.693896-49d37d2889d64bada76d8683a61093ca.zip?alt=json&prettyPrint=false": generic::permission_denied: IAM permission denied for service account 402564488059-compute@developer.gserviceaccount.com. . This command is authenticated as ozouxguillaume@gmail.com which is the active account specified by the [core/account] property.
```

---

### Obtenir l'URL du service

```
PS C:\Users\ozoux\tp3cloud> gcloud run services describe run-backend --region=europe-west1 --format='value(status.url)'
https://run-backend-uwwndjnimq-ew.a.run.app
```

---

## Exercice 6

### Créer le compte de service deploy-automation

```
PS C:\Users\ozoux\tp3cloud> gcloud iam service-accounts create deploy-automation --display-name="Deployment Automation"
Created service account [deploy-automation].
```

---

### Accorder permission serviceAccountUser

```
PS C:\Users\ozoux\tp3cloud> gcloud iam service-accounts add-iam-policy-binding deploy-automation@tp3partie1et2.iam.gserviceaccount.com --member="user:ozouxguillaume@gmail.com" --role="roles/iam.serviceAccountUser"
Updated IAM policy for serviceAccount [deploy-automation@tp3partie1et2.iam.gserviceaccount.com].
bindings:
- members:
  - user:ozouxguillaume@gmail.com
  role: roles/iam.serviceAccountUser
etag: BwZDKMvLoko=
version: 1
```

---

### Accorder permission serviceAccountTokenCreator

```
PS C:\Users\ozoux\tp3cloud> gcloud iam service-accounts add-iam-policy-binding deploy-automation@tp3partie1et2.iam.gserviceaccount.com --member="user:ozouxguillaume@gmail.com" --role="roles/iam.serviceAccountTokenCreator"
Updated IAM policy for serviceAccount [deploy-automation@tp3partie1et2.iam.gserviceaccount.com].
bindings:
- members:
  - user:ozouxguillaume@gmail.com
  role: roles/iam.serviceAccountTokenCreator
- members:
  - user:ozouxguillaume@gmail.com
  role: roles/iam.serviceAccountUser
etag: BwZDKMv7DjQ=
version: 1
```

---

### Tester l'impersonation - Projects list

```
PS C:\Users\ozoux\tp3cloud> gcloud projects list --impersonate-service-account=deploy-automation@tp3partie1et2.iam.gserviceaccount.com
WARNING: This command is using service account impersonation. All API calls will be executed as [deploy-automation@tp3partie1et2.iam.gserviceaccount.com].
API [cloudresourcemanager.googleapis.com] not enabled on project [402564488059]. Would you like to enable and retry
(this will take a few minutes)? (y/N)?  y
Enabling service [cloudresourcemanager.googleapis.com] on project [402564488059]...
WARNING: This command is using service account impersonation. All API calls will be executed as [deploy-automation@tp3partie1et2.iam.gserviceaccount.com].
ERROR: (gcloud.projects.list) PERMISSION_DENIED: Permission denied to enable service [cloudresourcemanager.googleapis.com]
Help Token: AXcLsyA_nWssd1NR8P395vxQgm2XzkXHoxp0UEWsyK66qZc0Pyz0Exg8RmstIZMgGB-7VlqMDYQVu3l1PksAThxf7_P66t4arMZ71cS362vxIJuk. This command is authenticated as ozouxguillaume@gmail.com which is the active account specified by the [core/account] property. Impersonation is used to impersonate deploy-automation@tp3partie1et2.iam.gserviceaccount.com
- '@type': type.googleapis.com/google.rpc.ErrorInfo
  domain: serviceusage.googleapis.com
  reason: AUTH_PERMISSION_DENIED
```

---

### Tester l'impersonation - Storage ls

```
PS C:\Users\ozoux\tp3cloud> gcloud storage ls --impersonate-service-account=deploy-automation@tp3partie1et2.iam.gserviceaccount.com
WARNING: This command is using service account impersonation. All API calls will be executed as [deploy-automation@tp3partie1et2.iam.gserviceaccount.com].
ERROR: (gcloud.storage.ls) HTTPError 403: deploy-automation@tp3partie1et2.iam.gserviceaccount.com does not have storage.buckets.list access to the Google Cloud project. Permission 'storage.buckets.list' denied on resource (or it may not exist). This command is authenticated as ozouxguillaume@gmail.com which is the active account specified by the [core/account] property. Impersonation is used to impersonate deploy-automation@tp3partie1et2.iam.gserviceaccount.com.
```

---

## Exercice 7

### Créer le fichier de condition temporelle

```
PS C:\Users\ozoux\tp3cloud> @"
expression: request.time < timestamp("2025-11-09T14:08:00Z")
title: Acces temporaire Cloud Run
description: Expire a 14h08 UTC
"@ | Out-File -FilePath condition-expire.yaml -Encoding utf8
```

---

### Appliquer la condition IAM

```
PS C:\Users\ozoux\tp3cloud> gcloud projects add-iam-policy-binding tp3partie1et2 --member="user:collaborateur0013@gmail.com" --role="roles/run.admin" --condition-from-file=condition-expire.yaml
WARNING: Adding binding with condition to a policy without condition will change the behavior of add-iam-policy-binding and remove-iam-policy-binding commands.
Updated IAM policy for project [tp3partie1et2].
bindings:
- members:
  - user:collaborateur0013@gmail.com
  role: projects/tp3partie1et2/roles/customCloudRunDeployer
- members:
  - serviceAccount:service-402564488059@gcp-sa-artifactregistry.iam.gserviceaccount.com
  role: roles/artifactregistry.serviceAgent
- members:
  - serviceAccount:402564488059@cloudbuild.gserviceaccount.com
  role: roles/artifactregistry.writer
- members:
  - serviceAccount:402564488059@cloudbuild.gserviceaccount.com
  role: roles/cloudbuild.builds.builder
- members:
  - serviceAccount:service-402564488059@gcp-sa-cloudbuild.iam.gserviceaccount.com
  role: roles/cloudbuild.serviceAgent
- members:
  - serviceAccount:service-402564488059@containerregistry.iam.gserviceaccount.com
  role: roles/containerregistry.ServiceAgent
- members:
  - serviceAccount:402564488059-compute@developer.gserviceaccount.com
  role: roles/editor
- members:
  - serviceAccount:402564488059@cloudbuild.gserviceaccount.com
  role: roles/logging.logWriter
- members:
  - user:ozouxguillaume@gmail.com
  role: roles/owner
- members:
  - serviceAccount:service-402564488059@gcp-sa-pubsub.iam.gserviceaccount.com
  role: roles/pubsub.serviceAgent
- condition:
    description: Expire a 14h08 UTC
    expression: request.time < timestamp("2025-11-09T14:08:00Z")
    title: Acces temporaire Cloud Run
  members:
  - user:collaborateur0013@gmail.com
  role: roles/run.admin
- members:
  - serviceAccount:service-402564488059@serverless-robot-prod.iam.gserviceaccount.com
  role: roles/run.serviceAgent
- members:
  - serviceAccount:402564488059@cloudbuild.gserviceaccount.com
  role: roles/storage.admin
- members:
  - user:guillaumeozoux33@gmail.com
  role: roles/viewer
etag: BwZDKRYBil0=
version: 3
```

---

### Tester avec le collaborateur - Lister les services

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud run services list --region=europe-west1
Listed 0 items.
```

---

### Tester avec le collaborateur - Déployer un service

```
C:\Users\ozoux\AppData\Local\Google\Cloud SDK>gcloud run deploy test-condition --image=gcr.io/cloudrun/hello --region=europe-west1 --allow-unauthenticated
Deploying container to Cloud Run service [test-condition] in project [tp3partie1et2] region [europe-west1]
OK Deploying new service... Done.
  OK Creating Revision...
  OK Routing traffic...
  OK Setting IAM Policy...
Done.
Service [test-condition] revision [test-condition-00001-lp9] has been deployed and is serving 100 percent of traffic.
Service URL: https://test-condition-402564488059.europe-west1.run.app
```

---

## Exercice 8

### Observer les changements IAM (SetIamPolicy)

```
PS C:\Users\ozoux\tp3cloud> gcloud logging read "protoPayload.methodName=SetIamPolicy" --limit=10 --format=json --project=tp3partie1et2
[
  {
    "insertId": "-61dy9cdpcui",
    "logName": "projects/tp3partie1et2/logs/cloudaudit.googleapis.com%2Factivity",
    "protoPayload": {
      "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
      "authenticationInfo": {
        "oauthInfo": {
          "oauthClientId": "32555940559.apps.googleusercontent.com"
        },
        "principalEmail": "ozouxguillaume@gmail.com",
        "principalSubject": "user:ozouxguillaume@gmail.com"
      },
      "authorizationInfo": [
        {
          "granted": true,
          "permission": "resourcemanager.projects.setIamPolicy",
          "permissionType": "ADMIN_WRITE",
          "resource": "projects/tp3partie1et2",
          "resourceAttributes": {
            "name": "projects/tp3partie1et2",
            "service": "cloudresourcemanager.googleapis.com",
            "type": "cloudresourcemanager.googleapis.com/Project"
          }
        }
      ],
      "methodName": "SetIamPolicy",
      "serviceData": {
        "@type": "type.googleapis.com/google.iam.v1.logging.AuditData",
        "policyDelta": {
          "bindingDeltas": [
            {
              "action": "ADD",
              "condition": {
                "description": "Expire a 14h08 UTC",
                "expression": "request.time < timestamp(\"2025-11-09T14:08:00Z\")",
                "title": "Acces temporaire Cloud Run"
              },
              "member": "user:collaborateur0013@gmail.com",
              "role": "roles/run.admin"
            }
          ]
        }
      },
      "serviceName": "cloudresourcemanager.googleapis.com",
      "status": {},
      "timestamp": "2025-11-09T13:06:41.246951Z"
    },
    "receiveTimestamp": "2025-11-09T13:06:42.980067524Z",
    "resource": {
      "labels": {
        "project_id": "tp3partie1et2"
      },
      "type": "project"
    },
    "severity": "NOTICE"
  }
]
```

---

### Observer les actions du collaborateur

```
PS C:\Users\ozoux\tp3cloud> gcloud logging read 'protoPayload.authenticationInfo.principalEmail="collaborateur0013@gmail.com"' --limit=10 --format=json --project=tp3partie1et2
[
  {
    "insertId": "pjes3gduu2q",
    "logName": "projects/tp3partie1et2/logs/cloudaudit.googleapis.com%2Factivity",
    "protoPayload": {
      "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
      "authenticationInfo": {
        "oauthInfo": {
          "oauthClientId": "32555940559.apps.googleusercontent.com"
        },
        "principalEmail": "collaborateur0013@gmail.com",
        "principalSubject": "user:collaborateur0013@gmail.com"
      },
      "authorizationInfo": [
        {
          "granted": false,
          "permission": "serviceusage.services.enable",
          "permissionType": "ADMIN_WRITE",
          "resource": "projectnumbers/402564488059/services/cloudbuild.googleapis.com",
          "resourceAttributes": {}
        }
      ],
      "methodName": "google.api.serviceusage.v1.ServiceUsage.EnableService",
      "resourceName": "projects/tp3partie1et2/services/cloudbuild.googleapis.com",
      "serviceName": "serviceusage.googleapis.com",
      "status": {
        "code": 7,
        "message": "Permission denied to enable service [cloudbuild.googleapis.com]"
      },
      "timestamp": "2025-11-09T12:28:46.301911Z"
    },
    "receiveTimestamp": "2025-11-09T12:28:46.971398790Z",
    "resource": {
      "labels": {
        "method": "google.api.serviceusage.v1.ServiceUsage.EnableService",
        "project_id": "tp3partie1et2",
        "service": "serviceusage.googleapis.com"
      },
      "type": "audited_resource"
    },
    "severity": "ERROR"
  },
  {
    "insertId": "abm8umdduet",
    "logName": "projects/tp3partie1et2/logs/cloudaudit.googleapis.com%2Factivity",
    "protoPayload": {
      "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
      "authenticationInfo": {
        "oauthInfo": {
          "oauthClientId": "32555940559.apps.googleusercontent.com"
        },
        "principalEmail": "collaborateur0013@gmail.com",
        "principalSubject": "user:collaborateur0013@gmail.com"
      },
      "authorizationInfo": [
        {
          "granted": true,
          "permission": "run.services.delete",
          "permissionType": "ADMIN_WRITE",
          "resource": "namespaces/tp3partie1et2/services/hello-test",
          "resourceAttributes": {}
        }
      ],
      "methodName": "google.cloud.run.v1.Services.DeleteService",
      "resourceName": "namespaces/tp3partie1et2/services/hello-test",
      "serviceName": "run.googleapis.com",
      "timestamp": "2025-11-09T12:20:31.137517Z"
    },
    "receiveTimestamp": "2025-11-09T12:20:31.531334254Z",
    "resource": {
      "labels": {
        "configuration_name": "",
        "location": "europe-west1",
        "project_id": "tp3partie1et2",
        "revision_name": "",
        "service_name": "hello-test"
      },
      "type": "cloud_run_revision"
    },
    "severity": "NOTICE"
  }
]
```

---

### Observer les logs Cloud Run

```
PS C:\Users\ozoux\tp3cloud> gcloud logging read "resource.type=cloud_run_revision" --limit=10 --format=json --project=tp3partie1et2
[
  {
    "insertId": "rqz153d5hpc",
    "logName": "projects/tp3partie1et2/logs/cloudaudit.googleapis.com%2Fsystem_event",
    "protoPayload": {
      "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
      "methodName": "/Services.CreateService",
      "resourceName": "namespaces/tp3partie1et2/services/test-condition",
      "response": {
        "@type": "type.googleapis.com/google.cloud.run.v1.Service",
        "metadata": {
          "annotations": {
            "serving.knative.dev/creator": "ozouxguillaume@gmail.com",
            "serving.knative.dev/lastModifier": "ozouxguillaume@gmail.com"
          },
          "name": "test-condition",
          "namespace": "402564488059"
        },
        "status": {
          "url": "https://test-condition-uwwndjnimq-ew.a.run.app"
        }
      },
      "serviceName": "run.googleapis.com",
      "status": {
        "message": "Ready condition status changed to True for Service test-condition."
      },
      "timestamp": "2025-11-09T12:55:09.355372Z"
    },
    "receiveTimestamp": "2025-11-09T12:55:09.527792984Z",
    "resource": {
      "labels": {
        "configuration_name": "",
        "location": "europe-west1",
        "project_id": "tp3partie1et2",
        "revision_name": "",
        "service_name": "test-condition"
      },
      "type": "cloud_run_revision"
    },
    "severity": "INFO"
  }
]
```

---

### Observer les actions du compte de service run-backend

```
PS C:\Users\ozoux\tp3cloud> gcloud logging read 'protoPayload.authenticationInfo.principalEmail="run-backend@tp3partie1et2.iam.gserviceaccount.com"' --limit=10 --format=json --project=tp3partie1et2
[]
```

---

### Exporter un exemple de log

```
PS C:\Users\ozoux\tp3cloud> gcloud logging read "protoPayload.methodName=SetIamPolicy" --limit=1 --format=json --project=tp3partie1et2 > audit-log-example.json
```

---

## 📊 Résumé final

### Comptes créés

**Utilisateurs :**
- `ozouxguillaume@gmail.com` - roles/owner
- `collaborateur0013@gmail.com` - roles/editor + customCloudRunDeployer + roles/run.admin (temporaire)
- `guillaumeozoux33@gmail.com` - roles/viewer

**Comptes de service :**
- `app-backend@tp3partie1et2.iam.gserviceaccount.com`
- `run-backend@tp3partie1et2.iam.gserviceaccount.com`
- `deploy-automation@tp3partie1et2.iam.gserviceaccount.com`

### Ressources créées

- Bucket Storage : `gs://nom-bucket-unique/`
- Service Cloud Run : `run-backend` (https://run-backend-uwwndjnimq-ew.a.run.app)
- Service Cloud Run : `test-condition` (https://test-condition-402564488059.europe-west1.run.app)
- Rôle personnalisé : `customCloudRunDeployer`

---

**Date de réalisation :** 09 novembre 2025  
**Projet GCP :** tp3partie1et2  
**Étudiant :** Guillaume Ozoux