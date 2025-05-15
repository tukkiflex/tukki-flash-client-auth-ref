
# 🔐 tukki API

Une mini API d’authentification SMS par code à 4 chiffres Tukki.  
Utilise **Flask** + **PostgreSQL** + **JWT**.  
Le code est généré, stocké et affiché dans la console (pas encore d'envoi réel par SMS).

---

## 🚀 Fonctionnalités

- Demande de code par numéro de téléphone
- Vérification du code
- Enregistrement de l'utilisateur
- Génération de token JWT
- Connexion automatique si l'utilisateur existe

---

## 📦 Stack utilisée

- Python 3.x
- Flask
- PostgreSQL
- SQLAlchemy
- JWT (pyjwt)

---

## ⚙️ Installation

### 1. Cloner le repo

```bash
git clone https://github.com/ton-projet/flash-auth-api.git
cd flash-auth-api
````

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Créer la base de données

Assure-toi que PostgreSQL tourne sur ta machine.

```sql
CREATE DATABASE tukki;
```

### 4. Configurer l'app

copier le fichier `.env.example` en `.env` et remplir les variables d'environnement.

```bash
cp .env.example .env
```

ajoute les variables d'environnement au fichier `.env` .


### 5. Lancer le serveur

```bash
flask run --host 0.0.0.0
```

---

## 🔁 Endpoints

### ✅ POST `/auth/request-code`

Demande un code de vérification.

**Body JSON** :

```json
{
  "phone": "+221771234567"
}
```

**Réponse** :

```json
{
  "message": "Code sent"
}
```

→ Le code s’affiche dans la console.

---

### ✅ POST `/auth/verify-code`

Vérifie le code à 4 chiffres.

**Body JSON** :

```json
{
  "phone": "+221771234567",
  "code": "1234"
}
```

**Réponse (si utilisateur existe)** :

```json
{
  "token": "xxx.yyy.zzz",
  "user": {
    "id": 1,
    "phone": "+221771234567",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

**Réponse (si utilisateur non inscrit)** :

```json
{
  "message": "User not registered"
}
```

---

### ✅ POST `/auth/register`

Crée un utilisateur après validation du code.

**Body JSON** :

```json
{
  "phone": "+221771234567",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Réponse** :

```json
{
  "token": "xxx.yyy.zzz",
  "user": {
    "id": 2,
    "phone": "+221771234567",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

---

## 🧠 Améliorations possibles

* 🔐 Expiration du code (5 minutes)
* 🔁 Refresh token + blacklisting
* 📲 Intégration d’un fournisseur SMS (Twilio, Orange, etc.)
* 🛡 Rate limiting (pour éviter les abus)
* 🌍 Déploiement en production (Docker, Gunicorn, Nginx…)

---

## 🧪 Test rapide avec curl

```bash
curl -X POST http://localhost:5000/auth/request-code \
  -H "Content-Type: application/json" \
  -d '{"phone": "+221771234567"}'
```

---

## 🧑‍💻 Auteur

Mouhameth Lamotte

---

## ⚖️ Licence

MIT

---
