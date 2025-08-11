# Overview

This is "Training Edge AI", a professional Flask-based AI Image Generator web application that allows users to create images from text prompts using Hugging Face's free text-to-image models. The application features a modern web interface for generating images, an interactive gallery to view and manage previously generated images, and comprehensive REST API endpoints for programmatic access. Users can select from 8+ AI models including FLUX.1, Stable Diffusion 3, SDXL, and specialized artistic models. All generated images are stored locally and tracked in a database. The application is fully containerized with Docker and ready for deployment on GitHub.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask for server-side rendering
- **UI Framework**: Bootstrap 5 for responsive design and components
- **JavaScript**: Vanilla JavaScript for client-side interactions and API calls
- **Styling**: Custom CSS with CSS variables for theming and gradient backgrounds
- **Layout**: Base template pattern with block inheritance for consistent navigation and structure

## Backend Architecture
- **Web Framework**: Flask application with factory pattern in `create_app()`
- **Database ORM**: SQLAlchemy with declarative base for model definitions
- **Route Organization**: Modular route registration system separating concerns
- **File Handling**: Local file storage in `static/generated` directory with configurable upload limits
- **Error Handling**: Comprehensive logging and validation for API endpoints

## Data Storage
- **Primary Database**: SQLite for development with PostgreSQL support via DATABASE_URL environment variable
- **Image Storage**: Local filesystem storage with generated filenames
- **Data Model**: Single `GeneratedImage` model tracking prompts, model names, filenames, creation timestamps, and file sizes
- **Connection Pooling**: Configured with pool recycling and pre-ping for production reliability

## Authentication & Security
- **CORS**: Enabled for cross-origin API access
- **File Upload Security**: Secured filenames and size limits (16MB maximum)
- **Proxy Handling**: ProxyFix middleware for deployment behind reverse proxies
- **Session Management**: Flask sessions with configurable secret key

## External Dependencies

- **Hugging Face Inference API**: Primary service for text-to-image generation using free models like FLUX.1 Schnell, Stable Diffusion 3 Medium, SDXL, OpenJourney, and Analog Diffusion
- **PIL/Pillow**: Image processing and manipulation library for handling generated images
- **Bootstrap CDN**: Frontend styling and components via CDN
- **Font Awesome**: Icon library for UI elements
- **Flask Extensions**: SQLAlchemy for ORM, CORS for cross-origin support, Werkzeug for middleware and utilities

## Deployment & DevOps

- **Docker**: Complete containerization with Dockerfile and docker-compose.yml
- **GitHub Integration**: Repository configured for https://github.com/caid-and-cubs/3images.git
- **Production Ready**: Gunicorn WSGI server, health checks, proper error handling
- **Environment Configuration**: .env support for API keys and configuration
- **Free Tier Compatible**: Uses only free APIs and open-source models

## Recent Changes (August 2025)

- Rebranded from "AI Image Generator" to "Training Edge AI"
- Updated to use working Hugging Face models that are free and verified
- Added fallback model logic for better reliability
- Created complete Docker deployment configuration
- Prepared GitHub repository with comprehensive documentation
- Added 3 verified free AI models: SD3 Medium, FLUX.1 Schnell, SDXL
- Implemented automatic model fallback for failed requests  
- Created comprehensive internship report (RAPPORT_DE_STAGE.md) documenting the entire project development
- Validated each model with live API testing to ensure functionality