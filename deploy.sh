#!/bin/bash

# Training Edge AI - Script de déploiement
echo "🚀 Training Edge AI - Configuration GitHub"

# Vérifier si git est initialisé
if [ ! -d ".git" ]; then
    echo "📦 Initialisation du repository Git..."
    git init
    git branch -M main
fi

# Ajouter le remote GitHub
echo "🔗 Configuration du remote GitHub..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/caid-and-cubs/2images.git

# Ajouter tous les fichiers
echo "📁 Ajout des fichiers..."
git add .

# Commit
echo "💾 Commit des changements..."
git commit -m "🎨 Training Edge AI - Générateur d'images IA complet

✨ Fonctionnalités:
- Interface web professionnelle avec Bootstrap 5
- 8+ modèles IA gratuits (FLUX.1, Stable Diffusion 3, SDXL)
- Galerie interactive avec gestion d'images
- API REST complète
- Support Docker et Docker Compose
- Configuration déploiement production

🛠 Technologies:
- Flask + Vanilla JavaScript
- API Hugging Face (gratuite)
- SQLite/PostgreSQL
- Gunicorn + Docker

🎯 Prêt pour déploiement"

# Instructions pour le push
echo ""
echo "✅ Repository configuré avec succès!"
echo ""
echo "📋 Pour pousser vers GitHub, exécutez:"
echo "   git push -u origin main"
echo ""
echo "🐳 Pour tester avec Docker:"
echo "   docker-compose up --build"
echo ""
echo "🌐 URL du repository: https://github.com/caid-and-cubs/2images"
echo ""
echo "🔑 N'oubliez pas de configurer votre HUGGINGFACE_API_KEY!"