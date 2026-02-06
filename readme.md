# 🤖 Assistant RAG pour Support IT

[![Pipeline CI/CD](https://github.com/yourusername/rag-it-assistant/workflows/CI-CD/badge.svg)](https://github.com/yourusername/rag-it-assistant/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table des matières

- [Présentation](#présentation)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Stack Technique](#stack-technique)
- [Structure du Projet](#structure-du-projet)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Documentation API](#documentation-api)
- [Déploiement](#déploiement)
- [Monitoring](#monitoring)
- [Tests](#tests)

## Présentation

Un assistant intelligent de support IT basé sur la technologie RAG (Retrieval-Augmented Generation). Ce système prêt pour la production permet aux techniciens IT d'interroger la documentation interne (procédures, incidents et FAQ au format PDF) et de recevoir des réponses précises et contextualisées.

### Objectifs Principaux

-  Réponses rapides aux questions récurrentes du support IT
-  Base de connaissances centralisée à partir de documents PDF
-  Apprentissage continu via clustering des questions utilisateurs
-  Déploiement cloud-native sur Kubernetes

## ✨ Fonctionnalités

### Capacités Principales

- **Pipeline RAG** : Récupération et génération basées sur LangChain
- **Recherche Sémantique** : Base de données vectorielle ChromaDB pour une recherche documentaire efficace
- **Authentification** : Contrôle d'accès sécurisé basé sur JWT
- **Historique des Requêtes** : Traçabilité complète des interactions utilisateurs
- **Clustering ML** : Apprentissage non supervisé pour identifier les thématiques fréquentes
- **Faible Latence** : Suivi des temps de réponse

### Fonctionnalités MLOps

- **Suivi d'Expériences** : Intégration MLflow pour la reproductibilité
- **Automatisation CI/CD** : Pipeline GitHub Actions
- **Orchestration** : Déploiement Kubernetes avec Minikube/Lens

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   FastAPI   │─────▶│ Moteur RAG   │─────▶│  ChromaDB   │
│   Backend   │      │ (LangChain)  │      │  Vecteurs   │
└─────────────┘      └──────────────┘      └─────────────┘
       │                     │
       │                     ▼
       │              ┌──────────────┐
       │              │  Modèle LLM  │
       │              │ (Gemini/HF)  │
       │              └──────────────┘
       ▼
┌─────────────┐      ┌──────────────┐
│ PostgreSQL  │      │    MLflow    │
│Base de données│    │   Tracking   │
└─────────────┘      └──────────────┘
```

### Flux de Données

1. **Ingestion PDF** : Le pdf est découpés en chunks et vectorisé
2. **Stockage Vectoriel** : Les embeddings sont stockés dans ChromaDB
3. **Traitement des Requêtes** : Les questions utilisateurs récupèrent les chunks pertinents
4. **Génération de Réponses** : Le LLM génère des réponses à partir du contexte
5. **Logging** : Requêtes, réponses et métriques sauvegardés dans PostgreSQL
6. **Clustering** : Analyse périodique pour identifier les thématiques communes

## 🛠️ Stack Technique

### Backend & API
- **FastAPI** : Framework web asynchrone haute performance
- **Python 3.10+** : Langage de programmation principal
- **Pydantic** : Validation des données et gestion des configurations

### Stack IA/ML
- **LangChain** : Orchestration du pipeline RAG
- **ChromaDB** : Base de données vectorielle pour les embeddings
- **HuggingFace** : Modèles d'embeddings
- **Gemini/HuggingFace** : LLM pour la génération de réponses
- **scikit-learn** : Clustering **KMeans** pour l'analyse des questions

### MLOps & Déploiement
- **MLflow** : Suivi d'expériences et registre de modèles
- **Kubernetes** : Orchestration de conteneurs (Minikube)
- **Lens Desktop** : Visualisation du cluster K8s
- **GitHub Actions** : Automatisation CI/CD

### Stockage de Données
- **PostgreSQL** : Données utilisateurs et historique des requêtes
- **ChromaDB** : Persistance des embeddings vectoriels

## Structure du Projet

```
.
├── app/
│   ├── main.py                 # Point d'entrée de l'application FastAPI
│   ├── dependencies.py         # Dépendances partagées (DB, auth)
│   ├── schemas.py              # Modèles Pydantic
│   ├── db/                     # Modèles et connexion base de données
│   ├── model/                  # Définitions des modèles ML/IA
│   └── routes/                 # Points de terminaison API
│       ├── auth.py            # Endpoints d'authentification
│       ├── query.py           # Endpoints de requêtes RAG
│       └── history.py         # Endpoints d'historique
├── core/
│   ├── rag_pipeline.py        # Implémentation du RAG
│   └── services/              # Logique métier
├── saved_model/               # Modèles entraînés et artefacts
├── tests/                     # Tests unitaires et d'intégration
├── .github/
│   └── workflows/             # Définitions des pipelines CI/CD
├── infra/                     # Manifestes Kubernetes
│ 
├── dataset/                   # Documentation PDF
├── requirements.txt           # Dépendances Python
├── Dockerfile                 # Définition de l'image conteneur
├── docker-compose.yml         # Configuration développement local
└── README.md                  # Ce fichier
```

## Installation

### Prérequis

- Python 3.10 
- Docker et Docker Compose
- Minikube (pour le déploiement Kubernetes)
- kubectl
- Lens Desktop (optionnel, pour la visualisation K8s)

### Configuration de l'Environnement de Développement Local

1. **Cloner le dépôt**
   ```bash
   git clone git@github.com:Maryemelb/chatbot-rag.git
   cd rag-it-assistant
   ```

2. **Créer l'environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement**
   ```bash
   cp .env.example .env
   # Éditer .env avec votre configuration
   ```

5. **Lancer l'application**
   ```bash
   uvicorn app.main:app --reload
   ```

L'API sera accessible à `http://localhost:8000`

## ⚙️ Configuration

### Variables d'Environnement

Créer un fichier `.env` à la racine du projet :

```env
# Base de données
copy .env.example file and complete it
```

## Utilisation

### Exemples d'Utilisation de l'API

**1. Inscription d'un Utilisateur**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "utilisateur@entreprise.com",
    "password": "motdepassesecurise"
  }'
```

**2. Connexion**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "utilisateur@entreprise.com",
    "password": "motdepassesecurise"
  }'
```

**3. Interroger le Système RAG**
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Authorization: Bearer VOTRE_TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Comment réinitialiser un mot de passe utilisateur dans Active Directory ?"
  }'
```

**4. Récupérer l'Historique des Requêtes**
```bash
curl -X GET "http://localhost:8000/history" \
  -H "Authorization: Bearer VOTRE_TOKEN_JWT"
```

## Documentation API

Une fois l'application en cours d'exécution, accédez à :

- **Documentation API interactive (Swagger UI)** : http://localhost:8000/docs


### Endpoints Principaux

| Méthode | Endpoint | Description | Auth Requise |
|---------|----------|-------------|--------------|
| POST | `/auth/register` | Créer un nouveau compte utilisateur | Non |
| POST | `/auth/login` | Authentification et obtention du token JWT | Non |
| POST | `/query` | Poser une question au système RAG | Oui |
| GET | `/history` | Récupérer l'historique des requêtes | Oui |
| GET | `/health` | Vérifier l'état de santé du service | Non |

## 🔬 Pipeline MLOps

### Suivi avec MLflow

Le système suit automatiquement :
- **Paramètres** : Température du LLM, nom du modèle, taille des chunks, k de récupération
- **Métriques** : Latence des réponses, scores de similarité, précision de récupération
- **Artefacts** : Réponses générées, chunks récupérés, prompts

Accès à l'interface MLflow : `http://localhost:5000`

### Registre de Modèles

```python
# Enregistrer le pipeline RAG comme un modèle
import mlflow
mlflow.set_tracking_uri("http://localhost:5000")

with mlflow.start_run(run_name="rag-pipeline-v1"):
    mlflow.log_param("llm_model", "gemini-pro")
    mlflow.log_param("embedding_model", "all-MiniLM-L6-v2")
    mlflow.log_metric("avg_latency_ms", 450)
    
    # Logger le pipeline RAG
    mlflow.pyfunc.log_model("rag_model", python_model=rag_pipeline)
```



## Monitoring

### Métriques de la Base de Données

La table `queries` trace :
- **latency_ms** : Temps de réponse pour chaque requête
- **cluster** : Catégorie de question (issu du clustering ML)
- **created_at** : Horodatage pour l'analyse des tendances

### Vérification de Santé

```bash
curl http://localhost:8000/health
```

Réponse :
```json
{
  "status": "healthy",
  "database": "connected",
  "vector_db": "ready",
  "timestamp": "2026-02-06T10:30:00Z"
}
```

### Surveillance des Performances

Surveiller les métriques clés :
- Latence moyenne des requêtes
- Latence au 95e percentile
- Questions par cluster
- Tendances d'engagement utilisateur

## Tests

### Exécuter Tous les Tests

```bash
pytest tests/ -v
```

### Couverture des Tests

```bash
pytest tests/ --cov=app --cov-report=html
```

### Catégories de Tests

- **Tests Unitaires** : Test des composants individuels


---

**Durée du Projet** : 26 janvier 2026 - 6 février 2026  

## Modèle de Données PostgreSQL

### Table `users`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER | Identifiant unique (clé primaire) |
| `email` | VARCHAR | Email de l'utilisateur (unique) |
| `hashed_password` | VARCHAR | Mot de passe hashé |
| `is_active` | BOOLEAN | Statut du compte |
| `created_at` | TIMESTAMP | Date de création |

### Table `queries`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER | Identifiant unique (clé primaire) |
| `user_id` | INTEGER | Référence à l'utilisateur (clé étrangère) |
| `question` | TEXT | Question posée |
| `answer` | TEXT | Réponse générée par le RAG |
| `cluster` | INTEGER | Numéro de cluster (ML) |
| `latency_ms` | FLOAT | Temps de réponse en ms |
| `created_at` | TIMESTAMP | Date et heure de la requête |

### Relations

- Un utilisateur peut poser plusieurs questions (relation 1:N)
- Chaque question est associée à un seul utilisateur
- Les clusters sont assignés après analyse ML périodique

## 🔄 Pipeline CI/CD

Le workflow GitHub Actions automatise :

1. **Déclencheurs** : Push sur `main` ou `develop`
2. **Étapes** :
   - Installation des dépendances Python
   - Linting du code (optionnel)
   - Exécution des tests unitaires et d'intégration
   - Construction de l'image Docker
   - Push vers le registre (Docker Hub / GitHub Container Registry)
   - Déploiement sur Kubernetes (si tests réussis)

