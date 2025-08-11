# Training Edge AI - Générateur d'Images IA

Une application web professionnelle pour générer des images à partir de texte utilisant l'API Hugging Face et Flask.

![Training Edge AI](https://img.shields.io/badge/Training%20Edge%20AI-Generator-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![Flask](https://img.shields.io/badge/Flask-Latest-red)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

## 🚀 Fonctionnalités

- **Génération d'images IA** : Transformez vos idées en images avec l'IA
- **8+ modèles disponibles** : FLUX.1, Stable Diffusion 3, SDXL, et plus
- **Interface professionnelle** : UI moderne avec Bootstrap 5
- **Galerie interactive** : Visualisez et gérez vos créations
- **API RESTful** : Intégration facile avec d'autres applications
- **Déploiement Docker** : Installation simple avec Docker

## 🎨 Modèles IA Supportés

- **Stable Diffusion 3 Medium** - Modèle haute qualité (Recommandé)
- **FLUX.1 Schnell** - Génération ultra-rapide
- **Stable Diffusion XL** - Images haute résolution
- **Stable Diffusion 1.5** - Modèle populaire et fiable
- **Dreamlike Diffusion** - Style artistique et onirique
- **OpenJourney** - Style Midjourney
- **Analog Diffusion** - Style photographie vintage

## 🛠 Technologies

- **Backend** : Flask, SQLAlchemy, Gunicorn
- **Frontend** : Vanilla JavaScript, Bootstrap 5, CSS3
- **IA** : API Hugging Face (gratuite)
- **Base de données** : SQLite (PostgreSQL supporté)
- **Déploiement** : Docker, Docker Compose

## 📦 Installation Rapide

### Avec Docker (Recommandé)

1. **Clonez le repository**
```bash
git clone https://github.com/caid-and-cubs/3images.git
cd 3images
```

2. **Configurez les variables d'environnement**
```bash
cp .env.example .env
# Éditez .env et ajoutez votre clé API Hugging Face
```

3. **Lancez avec Docker Compose**
```bash
docker-compose up -d
```

4. **Accédez à l'application**
```
http://localhost:5000
```

### Installation Manuelle

1. **Prérequis**
- Python 3.11+
- pip ou uv

2. **Installation**
```bash
git clone https://github.com/caid-and-cubs/3images.git
cd 3images

# Avec uv (recommandé)
uv sync

# Ou avec pip
pip install -r requirements.txt
```

3. **Configuration**
```bash
export HUGGINGFACE_API_KEY="your-hf-token"
export SESSION_SECRET="your-secret-key"
```

4. **Lancement**
```bash
gunicorn --bind 0.0.0.0:5000 main:app
```

## 🔑 Configuration

### Clé API Hugging Face (Gratuite)

1. Allez sur [Hugging Face Tokens](https://huggingface.co/settings/tokens)
2. Créez un compte gratuit
3. Générez un nouveau token avec permissions "Read"
4. Ajoutez-le dans votre fichier `.env` :

```env
HUGGINGFACE_API_KEY=hf_votre_token_ici
```

### Variables d'Environnement

```env
# Obligatoire
HUGGINGFACE_API_KEY=hf_your_token_here

# Optionnel
SESSION_SECRET=your-secret-key
DATABASE_URL=sqlite:///texttoimage.db
```

## 🖥 Utilisation

### Interface Web

1. Ouvrez `http://localhost:5000`
2. Entrez votre description d'image
3. Choisissez un modèle IA
4. Cliquez sur "Generate Image"
5. Téléchargez ou consultez la galerie

### API REST

**Générer une image**
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Un paysage de montagne au coucher du soleil",
    "model_name": "stabilityai/stable-diffusion-3-medium-diffusers"
  }'
```

**Lister les modèles**
```bash
curl http://localhost:5000/api/models
```

## 🐳 Déploiement Docker

### Docker Compose (Production)

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "80:5000"
    environment:
      - HUGGINGFACE_API_KEY=${HUGGINGFACE_API_KEY}
      - SESSION_SECRET=${SESSION_SECRET}
    volumes:
      - ./static/generated:/app/static/generated
    restart: unless-stopped
```

### Commandes Docker

```bash
# Construction
docker build -t training-edge-ai .

# Lancement
docker run -p 5000:5000 \
  -e HUGGINGFACE_API_KEY=your_token \
  training-edge-ai

# Avec volume pour persistance
docker run -p 5000:5000 \
  -e HUGGINGFACE_API_KEY=your_token \
  -v $(pwd)/static/generated:/app/static/generated \
  training-edge-ai
```

## 📁 Structure du Projet

```
3images/
├── app.py              # Configuration Flask
├── main.py             # Point d'entrée
├── models.py           # Modèles de base de données
├── routes.py           # Routes et API
├── utils.py            # Logique de génération IA
├── templates/          # Templates HTML
│   ├── base.html
│   ├── index.html
│   └── gallery.html
├── static/             # Fichiers statiques
│   ├── css/
│   ├── js/
│   └── generated/      # Images générées
├── Dockerfile          # Configuration Docker
├── docker-compose.yml  # Orchestration Docker
└── requirements.txt    # Dépendances Python
```

## 🔧 Développement

### Installation pour développement

```bash
git clone https://github.com/caid-and-cubs/3images.git
cd 3images

# Avec uv
uv sync --dev

# Variables d'environnement
export FLASK_ENV=development
export FLASK_DEBUG=1

# Lancement en mode dev
flask run --host=0.0.0.0 --port=5000
```

### Tests

```bash
# Tests unitaires
python -m pytest

# Tests API
curl -X GET http://localhost:5000/api/models
```

## 📸 Captures d'Écran

### Interface Principale
Interface moderne pour la génération d'images avec sélection de modèles.

### Galerie
Galerie interactive avec aperçu, téléchargement et suppression d'images.

## 🆓 API Gratuite

Cette application utilise uniquement des services gratuits :
- **Hugging Face Inference API** - Gratuite avec quotas généreux
- **Modèles open-source** - Tous les modèles sont libres d'utilisation
- **Aucun coût caché** - 100% gratuit pour usage personnel

## 🤝 Contribution

1. Fork le projet
2. Créez votre branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push sur la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Licence

Distribué sous licence MIT. Voir `LICENSE` pour plus d'informations.

## 👥 Auteurs

- **Training Edge AI Team** - *Développement initial*
- **Community** - *Contributions et améliorations*

## 🙏 Remerciements

- [Hugging Face](https://huggingface.co/) pour l'API gratuite
- [Bootstrap](https://getbootstrap.com/) pour l'interface
- [Flask](https://flask.palletsprojects.com/) pour le framework web
- [Black Forest Labs](https://blackforestlabs.ai/) pour les modèles FLUX

## 📞 Support

- 🐛 [Signaler un bug](https://github.com/caid-and-cubs/3images/issues)
- 💡 [Demander une fonctionnalité](https://github.com/caid-and-cubs/3images/issues)
- 📧 Contact : support@trainingedgeai.com

---

⭐ **N'oubliez pas de mettre une étoile si ce projet vous aide !**