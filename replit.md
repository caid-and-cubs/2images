# Overview

This is a Flask-based AI Image Generator web application that allows users to create images from text prompts using Hugging Face's text-to-image models. The application features a clean web interface for generating images, a gallery to view previously generated images, and REST API endpoints for programmatic access. Users can select from multiple AI models including Stable Diffusion variants and other specialized models, with all generated images stored locally and tracked in a database.

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

- **Hugging Face Inference API**: Primary service for text-to-image generation using models like Stable Diffusion 2.1, Stable Diffusion 1.5, OpenJourney, and Analog Diffusion
- **PIL/Pillow**: Image processing and manipulation library for handling generated images
- **Bootstrap CDN**: Frontend styling and components via CDN
- **Font Awesome**: Icon library for UI elements
- **Flask Extensions**: SQLAlchemy for ORM, CORS for cross-origin support, Werkzeug for middleware and utilities