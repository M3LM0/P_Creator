
"""
Templates de frameworks pour P_Creator
Reproduit l'expérience PyCharm/PhpStorm avec des structures complètes
"""

import os
from typing import Dict, List, Any

class FrameworkTemplates:
    """Gestionnaire des templates de frameworks"""
    
    TEMPLATES = {
        "Python": {
            "Django": {
                "name": "Django Web Framework",
                "description": "Framework web Python complet avec ORM, admin, et authentification",
                "structure": {
                    "dirs": [
                        "config",
                        "apps", 
                        "static",
                        "templates",
                        "media",
                        "locale"
                    ],
                    "files": {
                        "manage.py": """#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
""",
                        "requirements.txt": """Django>=4.2.0
python-decouple>=3.8
django-cors-headers>=4.0.0
psycopg2-binary>=2.9.0
pillow>=10.0.0
django-extensions>=3.2.0
""",
                        "config/__init__.py": "",
                        "config/settings.py": """from decouple import config
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_extensions',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
    },
    'root': {
        'handlers': ['file'],
    },
}
""",
                        "config/urls.py": """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
""",
                        "config/wsgi.py": """import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
""",
                        "config/asgi.py": """import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_asgi_application()
""",
                        ".env.example": """SECRET_KEY=django-insecure-change-me-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
""",
                        "README.md": """# Projet Django

## 🚀 Installation rapide

1. **Activez l'environnement virtuel :**
```bash
source .venv/bin/activate  # Linux/Mac
# ou
.venv\\Scripts\\activate   # Windows
```

2. **Installez les dépendances :**
```bash
pip install -r requirements.txt
```

3. **Appliquez les migrations :**
```bash
python manage.py migrate
```

4. **Créez un superutilisateur :**
```bash
python manage.py createsuperuser
```

5. **Lancez le serveur :**
```bash
python manage.py runserver
```

## 📁 Structure du projet

- `config/` : Configuration Django (settings, urls, wsgi)
- `apps/` : Applications Django
- `static/` : Fichiers statiques (CSS, JS, images)
- `templates/` : Templates HTML
- `media/` : Fichiers uploadés par les utilisateurs
- `locale/` : Fichiers de traduction

## 🛠 Commandes utiles

```bash
# Créer une nouvelle app
python manage.py startapp nom_app

# Créer des migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic

# Shell Django
python manage.py shell

# Tests
python manage.py test
```

## 🔧 Configuration

Le projet utilise `python-decouple` pour la gestion des variables d'environnement.
Copiez `.env.example` vers `.env` et modifiez les valeurs selon vos besoins.

## 📝 Développement

- **Admin Django :** http://localhost:8000/admin/
- **API :** http://localhost:8000/api/
- **Documentation :** https://docs.djangoproject.com/
"""
                    }
                },
                "dependencies": [
                    "Django>=4.2.0",
                    "python-decouple>=3.8", 
                    "django-cors-headers>=4.0.0",
                    "psycopg2-binary>=2.9.0",
                    "pillow>=10.0.0",
                    "django-extensions>=3.2.0"
                ],
                "run_command": "python manage.py runserver",
                "dev_port": 8000
            },
            
            "FastAPI": {
                "name": "FastAPI Framework",
                "description": "Framework web moderne et rapide avec documentation automatique",
                "structure": {
                    "dirs": [
                        "app",
                        "app/routers",
                        "app/models", 
                        "app/schemas",
                        "app/core",
                        "app/db",
                        "tests"
                    ],
                    "files": {
                        "main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import api

app = FastAPI(
    title="API FastAPI",
    description="API créée avec FastAPI",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(api.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hello FastAPI!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
""",
                        "requirements.txt": """fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
sqlalchemy>=2.0.0
alembic>=1.12.0
python-multipart>=0.0.6
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-decouple>=3.8
""",
                        "app/__init__.py": "",
                        "app/core/config.py": """from decouple import config

class Settings:
    PROJECT_NAME: str = "FastAPI Project"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)
    
    # Database
    DATABASE_URL: str = config("DATABASE_URL", default="sqlite:///./app.db")
    
    # CORS
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
    ]

settings = Settings()
""",
                        "app/routers/__init__.py": "",
                        "app/routers/api.py": """from fastapi import APIRouter
from app.schemas.health import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy", message="API is running")
""",
                        "app/schemas/__init__.py": "",
                        "app/schemas/health.py": """from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    message: str
""",
                        ".env.example": """SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./app.db
""",
                        "README.md": """# Projet FastAPI

## 🚀 Installation rapide

1. **Activez l'environnement virtuel :**
```bash
source .venv/bin/activate  # Linux/Mac
# ou
.venv\\Scripts\\activate   # Windows
```

2. **Installez les dépendances :**
```bash
pip install -r requirements.txt
```

3. **Lancez le serveur :**
```bash
python main.py
# ou
uvicorn main:app --reload
```

## 📚 Documentation

- **API Docs :** http://localhost:8000/docs
- **ReDoc :** http://localhost:8000/redoc
- **OpenAPI JSON :** http://localhost:8000/openapi.json

## 🛠 Commandes utiles

```bash
# Développement avec rechargement automatique
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn main:app --host 0.0.0.0 --port 8000

# Tests
pytest

# Linting
black .
flake8 .
```

## 📁 Structure du projet

- `app/` : Code principal de l'application
- `app/routers/` : Routes API
- `app/models/` : Modèles de données
- `app/schemas/` : Schémas Pydantic
- `app/core/` : Configuration et utilitaires
- `app/db/` : Configuration base de données
- `tests/` : Tests unitaires

## 🔧 Configuration

Le projet utilise `python-decouple` pour la gestion des variables d'environnement.
Copiez `.env.example` vers `.env` et modifiez les valeurs selon vos besoins.
"""
                    }
                },
                "dependencies": [
                    "fastapi>=0.104.0",
                    "uvicorn[standard]>=0.24.0", 
                    "pydantic>=2.5.0",
                    "sqlalchemy>=2.0.0",
                    "alembic>=1.12.0",
                    "python-multipart>=0.0.6",
                    "python-jose[cryptography]>=3.3.0",
                    "passlib[bcrypt]>=1.7.4",
                    "python-decouple>=3.8"
                ],
                "run_command": "uvicorn main:app --reload",
                "dev_port": 8000
            },
            
            "Flask": {
                "name": "Flask Micro-framework",
                "description": "Micro-framework Python léger et flexible pour applications web",
                "structure": {
                    "dirs": [
                        "app",
                        "app/templates",
                        "app/static",
                        "app/static/css",
                        "app/static/js",
                        "app/static/images",
                        "tests",
                        "instance"
                    ],
                    "files": {
                        "app.py": """from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Flask app is running'})

@app.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        data = request.get_json()
        # Logique de création d'utilisateur
        return jsonify({'message': 'User created', 'data': data}), 201
    else:
        # Logique de récupération des utilisateurs
        return jsonify({'users': []})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
""",
                        "requirements.txt": """Flask>=2.3.0
Flask-SQLAlchemy>=3.0.0
Flask-Migrate>=4.0.0
Flask-CORS>=4.0.0
python-dotenv>=1.0.0
Werkzeug>=2.3.0
""",
                        "app/templates/base.html": """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Flask App{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <a href="{{ url_for('index') }}" class="nav-brand">Flask App</a>
            <ul class="nav-menu">
                <li><a href="{{ url_for('index') }}">Accueil</a></li>
                <li><a href="{{ url_for('health') }}">API</a></li>
            </ul>
        </div>
    </nav>
    
    <main class="main-content">
        {% block content %}{% endblock %}
    </main>
    
    <footer class="footer">
        <p>&copy; 2024 Flask App. Créé avec Flask.</p>
    </footer>
    
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
""",
                        "app/templates/index.html": """{% extends "base.html" %}

{% block title %}Accueil - Flask App{% endblock %}

{% block content %}
<div class="hero">
    <h1>Bienvenue dans votre application Flask</h1>
    <p>Votre application Flask est prête à être développée !</p>
    <div class="actions">
        <button onclick="testAPI()" class="btn btn-primary">Tester l'API</button>
        <button onclick="loadUsers()" class="btn btn-secondary">Charger les utilisateurs</button>
    </div>
</div>

<div class="features">
    <div class="feature">
        <h3>🚀 Rapide</h3>
        <p>Flask est léger et performant</p>
    </div>
    <div class="feature">
        <h3>🔧 Flexible</h3>
        <p>Architecture modulaire et extensible</p>
    </div>
    <div class="feature">
        <h3>📚 Documenté</h3>
        <p>Documentation excellente et communauté active</p>
    </div>
</div>

<div id="api-response" class="api-response"></div>
{% endblock %}
""",
                        "app/static/css/style.css": """/* Styles pour l'application Flask */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f4f4f4;
}

.navbar {
    background: #2c3e50;
    color: white;
    padding: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-brand {
    font-size: 1.5rem;
    font-weight: bold;
    color: white;
    text-decoration: none;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-menu a {
    color: white;
    text-decoration: none;
    transition: color 0.3s;
}

.nav-menu a:hover {
    color: #3498db;
}

.main-content {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 2rem;
}

.hero {
    text-align: center;
    padding: 4rem 0;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
    color: #2c3e50;
}

.hero p {
    font-size: 1.2rem;
    color: #666;
    margin-bottom: 2rem;
}

.actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

.btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s;
    text-decoration: none;
    display: inline-block;
}

.btn-primary {
    background: #3498db;
    color: white;
}

.btn-primary:hover {
    background: #2980b9;
}

.btn-secondary {
    background: #95a5a6;
    color: white;
}

.btn-secondary:hover {
    background: #7f8c8d;
}

.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin: 2rem 0;
}

.feature {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    text-align: center;
}

.feature h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: #2c3e50;
}

.api-response {
    margin-top: 2rem;
    padding: 1rem;
    background: #ecf0f1;
    border-radius: 4px;
    display: none;
}

.footer {
    background: #2c3e50;
    color: white;
    text-align: center;
    padding: 2rem 0;
    margin-top: 4rem;
}

@media (max-width: 768px) {
    .nav-container {
        flex-direction: column;
        gap: 1rem;
    }
    
    .hero h1 {
        font-size: 2rem;
    }
    
    .actions {
        flex-direction: column;
        align-items: center;
    }
}
""",
                        "app/static/js/app.js": """// JavaScript pour l'application Flask
document.addEventListener('DOMContentLoaded', function() {
    console.log('Flask app loaded successfully!');
});

function testAPI() {
    fetch('/api/health')
        .then(response => response.json())
        .then(data => {
            showAPIResponse('API Health Check:', data);
        })
        .catch(error => {
            showAPIResponse('Erreur API:', { error: error.message });
        });
}

function loadUsers() {
    fetch('/api/users')
        .then(response => response.json())
        .then(data => {
            showAPIResponse('Utilisateurs:', data);
        })
        .catch(error => {
            showAPIResponse('Erreur utilisateurs:', { error: error.message });
        });
}

function showAPIResponse(title, data) {
    const responseDiv = document.getElementById('api-response');
    responseDiv.innerHTML = `
        <h3>${title}</h3>
        <pre>${JSON.stringify(data, null, 2)}</pre>
    `;
    responseDiv.style.display = 'block';
}
""",
                        ".env.example": """SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
FLASK_ENV=development
FLASK_DEBUG=True
""",
                        "README.md": """# Projet Flask

## 🚀 Installation rapide

1. **Activez l'environnement virtuel :**
```bash
source .venv/bin/activate  # Linux/Mac
# ou
.venv\\Scripts\\activate   # Windows
```

2. **Installez les dépendances :**
```bash
pip install -r requirements.txt
```

3. **Configurez l'environnement :**
```bash
cp .env.example .env
# Modifiez les valeurs dans .env
```

4. **Initialisez la base de données :**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. **Lancez l'application :**
```bash
python app.py
```

## 📁 Structure du projet

- `app/` : Code principal de l'application
- `app/templates/` : Templates HTML
- `app/static/` : Fichiers statiques (CSS, JS, images)
- `tests/` : Tests unitaires
- `instance/` : Fichiers d'instance (base de données locale)

## 🛠 Commandes utiles

```bash
# Développement
python app.py

# Tests
python -m pytest tests/

# Migration de base de données
flask db migrate -m "Description"
flask db upgrade

# Shell Flask
flask shell

# Créer un superutilisateur
flask create-admin
```

## 🔧 Configuration

Le projet utilise `python-dotenv` pour la gestion des variables d'environnement.
Copiez `.env.example` vers `.env` et modifiez les valeurs selon vos besoins.

## 📚 Documentation

- **Flask :** https://flask.palletsprojects.com/
- **Flask-SQLAlchemy :** https://flask-sqlalchemy.palletsprojects.com/
- **Flask-Migrate :** https://flask-migrate.readthedocs.io/
"""
                    }
                },
                "dependencies": [
                    "Flask>=2.3.0",
                    "Flask-SQLAlchemy>=3.0.0",
                    "Flask-Migrate>=4.0.0",
                    "Flask-CORS>=4.0.0",
                    "python-dotenv>=1.0.0",
                    "Werkzeug>=2.3.0"
                ],
                "run_command": "python app.py",
                "dev_port": 5000
            }
        },
        
        "PHP": {
            "Laravel": {
                "name": "Laravel Framework",
                "description": "Framework PHP élégant avec ORM Eloquent et artisan",
                "structure": {
                    "dirs": [
                        "app",
                        "app/Http/Controllers",
                        "app/Models",
                        "app/Http/Middleware",
                        "config",
                        "database/migrations",
                        "resources/views",
                        "resources/css",
                        "resources/js",
                        "routes",
                        "public",
                        "storage",
                        "tests"
                    ],
                    "files": {
                        "composer.json": """{
    "name": "laravel/laravel",
    "type": "project",
    "description": "The skeleton application for the Laravel framework.",
    "keywords": ["laravel", "framework"],
    "license": "MIT",
    "require": {
        "php": "^8.1",
        "guzzlehttp/guzzle": "^7.2",
        "laravel/framework": "^10.10",
        "laravel/sanctum": "^3.2",
        "laravel/tinker": "^2.8"
    },
    "require-dev": {
        "fakerphp/faker": "^1.9.1",
        "laravel/pint": "^1.0",
        "laravel/sail": "^1.18",
        "mockery/mockery": "^1.4.4",
        "nunomaduro/collision": "^7.0",
        "phpunit/phpunit": "^10.1",
        "spatie/laravel-ignition": "^2.0"
    },
    "autoload": {
        "psr-4": {
            "App\\\\": "app/",
            "Database\\\\Factories\\\\": "database/factories/",
            "Database\\\\Seeders\\\\": "database/seeders/"
        }
    },
    "autoload-dev": {
        "psr-4": {
            "Tests\\\\": "tests/"
        }
    },
    "scripts": {
        "post-autoload-dump": [
            "Illuminate\\\\Foundation\\\\ComposerScripts::postAutoloadDump",
            "@php artisan package:discover --ansi"
        ],
        "post-update-cmd": [
            "@php artisan vendor:publish --tag=laravel-assets --ansi --force"
        ],
        "post-root-package-install": [
            "@php -r \\"file_exists('.env') || copy('.env.example', '.env');\\""
        ],
        "post-create-project-cmd": [
            "@php artisan key:generate --ansi"
        ]
    },
    "extra": {
        "laravel": {
            "dont-discover": []
        }
    },
    "config": {
        "optimize-autoloader": true,
        "preferred-install": "dist",
        "sort-packages": true,
        "allow-plugins": {
            "pestphp/pest-plugin": true,
            "php-http/discovery": true
        }
    },
    "minimum-stability": "stable",
    "prefer-stable": true
}""",
                        "artisan": """#!/usr/bin/env php
<?php

define('LARAVEL_START', microtime(true));

require __DIR__.'/vendor/autoload.php';

$app = require_once __DIR__.'/bootstrap/app.php';

$kernel = $app->make(Illuminate\\Contracts\\Console\\Kernel::class);

$status = $kernel->handle(
    $input = new Symfony\\Component\\Console\\Input\\ArgvInput,
    new Symfony\\Component\\Console\\Output\\ConsoleOutput
);

$kernel->terminate($input, $status);

exit($status);
""",
                        "README.md": """# Projet Laravel

## 🚀 Installation rapide

1. **Installez les dépendances :**
```bash
composer install
```

2. **Configurez l'environnement :**
```bash
cp .env.example .env
php artisan key:generate
```

3. **Configurez la base de données dans `.env`**

4. **Lancez les migrations :**
```bash
php artisan migrate
```

5. **Lancez le serveur :**
```bash
php artisan serve
```

## 🛠 Commandes utiles

```bash
# Créer un contrôleur
php artisan make:controller NomController

# Créer un modèle
php artisan make:model NomModel

# Créer une migration
php artisan make:migration nom_migration

# Créer un seeder
php artisan make:seeder NomSeeder

# Lancer les tests
php artisan test

# Optimiser l'application
php artisan optimize
```

## 📁 Structure du projet

- `app/` : Code principal de l'application
- `app/Http/Controllers/` : Contrôleurs
- `app/Models/` : Modèles Eloquent
- `config/` : Configuration
- `database/` : Migrations et seeders
- `resources/` : Vues, CSS, JS
- `routes/` : Routes de l'application
- `public/` : Point d'entrée web
- `storage/` : Fichiers de stockage
- `tests/` : Tests

## 🔧 Configuration

Le projet utilise le fichier `.env` pour la configuration.
Copiez `.env.example` vers `.env` et modifiez les valeurs selon vos besoins.
"""
                    }
                },
                "dependencies": [
                    "laravel/framework",
                    "laravel/sanctum",
                    "laravel/tinker"
                ],
                "run_command": "php artisan serve",
                "dev_port": 8000
            }
        },
        
        "JavaScript": {
            "Vue.js": {
                "name": "Vue.js Framework",
                "description": "Framework JavaScript progressif pour construire des interfaces utilisateur",
                "structure": {
                    "dirs": [
                        "src",
                        "src/components",
                        "src/views",
                        "src/router",
                        "src/store",
                        "src/assets",
                        "src/assets/css",
                        "src/assets/images",
                        "public"
                    ],
                    "files": {
                        "package.json": """{
  "name": "vue-app",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "serve": "vue-cli-service serve",
    "build": "vue-cli-service build",
    "lint": "vue-cli-service lint"
  },
  "dependencies": {
    "vue": "^3.3.0",
    "vue-router": "^4.2.0",
    "vuex": "^4.1.0",
    "axios": "^1.4.0"
  },
  "devDependencies": {
    "@vue/cli-plugin-eslint": "~5.0.0",
    "@vue/cli-plugin-router": "~5.0.0",
    "@vue/cli-plugin-vuex": "~5.0.0",
    "@vue/cli-service": "~5.0.0",
    "@vue/eslint-config-standard": "^8.0.0",
    "eslint": "^8.0.0",
    "eslint-plugin-import": "^2.25.0",
    "eslint-plugin-node": "^11.0.0",
    "eslint-plugin-promise": "^6.0.0",
    "eslint-plugin-vue": "^9.0.0"
  }
}""",
                        "vue.config.js": """const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8080,
    open: true
  }
})""",
                        "src/main.js": """import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

createApp(App).use(store).use(router).mount('#app')""",
                        "src/App.vue": """<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <router-link to="/" class="nav-brand">Vue App</router-link>
        <ul class="nav-menu">
          <li><router-link to="/">Accueil</router-link></li>
          <li><router-link to="/about">À propos</router-link></li>
          <li><router-link to="/contact">Contact</router-link></li>
        </ul>
      </div>
    </nav>
    
    <main class="main-content">
      <router-view />
    </main>
    
    <footer class="footer">
      <p>&copy; 2024 Vue App. Créé avec Vue.js</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.navbar {
  background: #2c3e50;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 2rem;
}

.nav-menu a {
  color: white;
  text-decoration: none;
  transition: color 0.3s;
}

.nav-menu a:hover {
  color: #42b883;
}

.main-content {
  min-height: calc(100vh - 200px);
}

.footer {
  background: #2c3e50;
  color: white;
  text-align: center;
  padding: 2rem 0;
}
</style>""",
                        "src/router/index.js": """import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('../views/Contact.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router""",
                        "src/store/index.js": """import { createStore } from 'vuex'

export default createStore({
  state: {
    count: 0,
    user: null
  },
  mutations: {
    increment (state) {
      state.count++
    },
    decrement (state) {
      state.count--
    },
    setUser (state, user) {
      state.user = user
    }
  },
  actions: {
    increment ({ commit }) {
      commit('increment')
    },
    decrement ({ commit }) {
      commit('decrement')
    },
    setUser ({ commit }, user) {
      commit('setUser', user)
    }
  },
  getters: {
    doubleCount: state => state.count * 2
  }
})""",
                        "src/views/Home.vue": """<template>
  <div class="home">
    <div class="hero">
      <h1>Bienvenue dans votre application Vue.js</h1>
      <p>Votre application Vue.js est prête à être développée !</p>
      
      <div class="counter">
        <h3>Compteur: {{ count }}</h3>
        <div class="actions">
          <button @click="increment" class="btn btn-primary">+</button>
          <button @click="decrement" class="btn btn-secondary">-</button>
        </div>
        <p>Double: {{ doubleCount }}</p>
      </div>
    </div>
    
    <div class="features">
      <div class="feature">
        <h3>🚀 Réactif</h3>
        <p>Vue.js est réactif et performant</p>
      </div>
      <div class="feature">
        <h3>🔧 Flexible</h3>
        <p>Architecture modulaire et extensible</p>
      </div>
      <div class="feature">
        <h3>📚 Documenté</h3>
        <p>Documentation excellente et communauté active</p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  name: 'Home',
  computed: {
    ...mapState(['count']),
    ...mapGetters(['doubleCount'])
  },
  methods: {
    ...mapActions(['increment', 'decrement'])
  }
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.hero {
  text-align: center;
  padding: 4rem 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.hero p {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 2rem;
}

.counter {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.counter h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #42b883;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin: 1rem 0;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.btn-primary {
  background: #42b883;
  color: white;
}

.btn-primary:hover {
  background: #369870;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.feature {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
}

.feature h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}
</style>""",
                        "README.md": """# Projet Vue.js

## 🚀 Installation rapide

1. **Installez les dépendances :**
```bash
npm install
```

2. **Lancez le serveur de développement :**
```bash
npm run serve
```

3. **Ouvrez votre navigateur :**
http://localhost:8080

## 🛠 Commandes utiles

```bash
# Développement
npm run serve

# Build de production
npm run build

# Linting
npm run lint
```

## 📁 Structure du projet

- `src/` : Code source de l'application
- `src/components/` : Composants Vue
- `src/views/` : Pages de l'application
- `src/router/` : Configuration du routage
- `src/store/` : Gestion d'état Vuex
- `src/assets/` : Fichiers statiques
- `public/` : Fichiers publics

## 🔧 Technologies utilisées

- **Vue 3** : Framework JavaScript progressif
- **Vue Router** : Routage côté client
- **Vuex** : Gestion d'état centralisée
- **Axios** : Client HTTP
- **Vue CLI** : Outils de développement
"""
                    }
                },
                "dependencies": [
                    "vue",
                    "vue-router",
                    "vuex",
                    "axios"
                ],
                "run_command": "npm run serve",
                "dev_port": 8080
            },
            
            "Angular": {
                "name": "Angular Framework",
                "description": "Framework JavaScript enterprise pour applications web complexes",
                "structure": {
                    "dirs": [
                        "src",
                        "src/app",
                        "src/app/components",
                        "src/app/services",
                        "src/app/models",
                        "src/app/guards",
                        "src/app/interceptors",
                        "src/assets",
                        "src/environments"
                    ],
                    "files": {
                        "package.json": """{
  "name": "angular-app",
  "version": "1.0.0",
  "scripts": {
    "ng": "ng",
    "start": "ng serve",
    "build": "ng build",
    "watch": "ng build --watch --configuration development",
    "test": "ng test"
  },
  "dependencies": {
    "@angular/animations": "^16.0.0",
    "@angular/common": "^16.0.0",
    "@angular/compiler": "^16.0.0",
    "@angular/core": "^16.0.0",
    "@angular/forms": "^16.0.0",
    "@angular/platform-browser": "^16.0.0",
    "@angular/platform-browser-dynamic": "^16.0.0",
    "@angular/router": "^16.0.0",
    "rxjs": "~7.8.0",
    "tslib": "^2.3.0",
    "zone.js": "~0.13.0"
  },
  "devDependencies": {
    "@angular-devkit/build-angular": "^16.0.0",
    "@angular/cli": "^16.0.0",
    "@angular/compiler-cli": "^16.0.0",
    "@types/jasmine": "~4.3.0",
    "jasmine-core": "~4.6.0",
    "karma": "~6.4.0",
    "karma-chrome-launcher": "~3.1.0",
    "karma-coverage": "~2.2.0",
    "karma-jasmine": "~5.1.0",
    "karma-jasmine-html-reporter": "~2.1.0",
    "typescript": "~5.1.0"
  }
}""",
                        "angular.json": """{
  "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
  "version": 1,
  "newProjectRoot": "projects",
  "projects": {
    "angular-app": {
      "projectType": "application",
      "schematics": {},
      "root": "",
      "sourceRoot": "src",
      "prefix": "app",
      "architect": {
        "build": {
          "builder": "@angular-devkit/build-angular:browser",
          "options": {
            "outputPath": "dist/angular-app",
            "index": "src/index.html",
            "main": "src/main.ts",
            "polyfills": "src/polyfills.ts",
            "tsConfig": "tsconfig.app.json",
            "assets": [
              "src/favicon.ico",
              "src/assets"
            ],
            "styles": [
              "src/styles.css"
            ],
            "scripts": []
          },
          "configurations": {
            "production": {
              "budgets": [
                {
                  "type": "initial",
                  "maximumWarning": "500kb",
                  "maximumError": "1mb"
                },
                {
                  "type": "anyComponentStyle",
                  "maximumWarning": "2kb",
                  "maximumError": "4kb"
                }
              ],
              "outputHashing": "all"
            },
            "development": {
              "buildOptimizer": false,
              "optimization": false,
              "vendorChunk": true,
              "extractLicenses": false,
              "sourceMap": true,
              "namedChunks": true
            }
          },
          "defaultConfiguration": "production"
        },
        "serve": {
          "builder": "@angular-devkit/build-angular:dev-server",
          "configurations": {
            "production": {
              "buildTarget": "angular-app:build:production"
            },
            "development": {
              "buildTarget": "angular-app:build:development"
            }
          },
          "defaultConfiguration": "development"
        }
      }
    }
  }
}""",
                        "src/main.ts": """import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule } from './app/app.module';

platformBrowserDynamic().bootstrapModule(AppModule)
  .catch(err => console.error(err));""",
                        "src/app/app.module.ts": """import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';
import { AboutComponent } from './components/about/about.component';
import { ContactComponent } from './components/contact/contact.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    AboutComponent,
    ContactComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }""",
                        "src/app/app.component.ts": """import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Angular App';
}""",
                        "src/app/app.component.html": """<nav class="navbar">
  <div class="nav-container">
    <a routerLink="/" class="nav-brand">{{ title }}</a>
    <ul class="nav-menu">
      <li><a routerLink="/">Accueil</a></li>
      <li><a routerLink="/about">À propos</a></li>
      <li><a routerLink="/contact">Contact</a></li>
    </ul>
  </div>
</nav>

<main class="main-content">
  <router-outlet></router-outlet>
</main>

<footer class="footer">
  <p>&copy; 2024 Angular App. Créé avec Angular.</p>
</footer>""",
                        "src/app/app.component.css": """/* Styles globaux pour l'application Angular */
.navbar {
  background: #2c3e50;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 2rem;
}

.nav-menu a {
  color: white;
  text-decoration: none;
  transition: color 0.3s;
}

.nav-menu a:hover {
  color: #e74c3c;
}

.main-content {
  min-height: calc(100vh - 200px);
}

.footer {
  background: #2c3e50;
  color: white;
  text-align: center;
  padding: 2rem 0;
}""",
                        "README.md": """# Projet Angular

## 🚀 Installation rapide

1. **Installez les dépendances :**
```bash
npm install
```

2. **Lancez le serveur de développement :**
```bash
npm start
```

3. **Ouvrez votre navigateur :**
http://localhost:4200

## 🛠 Commandes utiles

```bash
# Développement
npm start

# Build de production
npm run build

# Tests
npm test

# Générer un composant
ng generate component nom-composant

# Générer un service
ng generate service nom-service
```

## 📁 Structure du projet

- `src/app/` : Code principal de l'application
- `src/app/components/` : Composants Angular
- `src/app/services/` : Services Angular
- `src/app/models/` : Modèles TypeScript
- `src/assets/` : Fichiers statiques
- `src/environments/` : Configuration d'environnement

## 🔧 Technologies utilisées

- **Angular 16** : Framework JavaScript enterprise
- **TypeScript** : Typage statique
- **RxJS** : Programmation réactive
- **Angular CLI** : Outils de développement
"""
                    }
                },
                "dependencies": [
                    "@angular/core",
                    "@angular/common",
                    "@angular/router",
                    "rxjs"
                ],
                "run_command": "npm start",
                "dev_port": 4200
            },
            
            "Express.js": {
                "name": "Express.js Framework",
                "description": "Framework Node.js minimal et flexible pour applications web et APIs",
                "structure": {
                    "dirs": [
                        "src",
                        "src/routes",
                        "src/controllers",
                        "src/models",
                        "src/middleware",
                        "src/config",
                        "src/utils",
                        "public",
                        "tests"
                    ],
                    "files": {
                        "package.json": """{
  "name": "express-app",
  "version": "1.0.0",
  "description": "Express.js application",
  "main": "src/app.js",
  "scripts": {
    "start": "node src/app.js",
    "dev": "nodemon src/app.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.0",
    "cors": "^2.8.5",
    "helmet": "^7.0.0",
    "morgan": "^1.10.0",
    "dotenv": "^16.3.0",
    "mongoose": "^7.4.0",
    "bcryptjs": "^2.4.3",
    "jsonwebtoken": "^9.0.0"
  },
  "devDependencies": {
    "nodemon": "^3.0.0",
    "jest": "^29.6.0",
    "supertest": "^6.3.0"
  }
}""",
                        "src/app.js": """const express = require('express')
const cors = require('cors')
const helmet = require('helmet')
const morgan = require('morgan')
require('dotenv').config()

const app = express()
const PORT = process.env.PORT || 3000

// Middleware
app.use(helmet())
app.use(cors())
app.use(morgan('combined'))
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

// Routes
app.get('/', (req, res) => {
  res.json({
    message: 'Bienvenue dans votre API Express.js',
    version: '1.0.0',
    status: 'running'
  })
})

app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  })
})

// Routes API
app.use('/api/users', require('./routes/users'))
app.use('/api/auth', require('./routes/auth'))

// Middleware de gestion d'erreurs
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).json({
    error: 'Quelque chose s\'est mal passé!',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Erreur interne du serveur'
  })
})

// Route 404
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Route non trouvée',
    message: `La route ${req.originalUrl} n'existe pas`
  })
})

app.listen(PORT, () => {
  console.log(`🚀 Serveur Express.js démarré sur le port ${PORT}`)
  console.log(`📱 URL: http://localhost:${PORT}`)
  console.log(`🔍 Health check: http://localhost:${PORT}/api/health`)
})

module.exports = app""",
                        "src/routes/users.js": """const express = require('express')
const router = express.Router()

// GET /api/users - Récupérer tous les utilisateurs
router.get('/', (req, res) => {
  res.json({
    users: [],
    message: 'Liste des utilisateurs (vide pour l\'instant)'
  })
})

// GET /api/users/:id - Récupérer un utilisateur par ID
router.get('/:id', (req, res) => {
  const { id } = req.params
  res.json({
    user: {
      id,
      name: 'Utilisateur exemple',
      email: 'user@example.com'
    }
  })
})

// POST /api/users - Créer un nouvel utilisateur
router.post('/', (req, res) => {
  const { name, email } = req.body
  
  if (!name || !email) {
    return res.status(400).json({
      error: 'Nom et email requis'
    })
  }
  
  res.status(201).json({
    message: 'Utilisateur créé avec succès',
    user: {
      id: Date.now(),
      name,
      email
    }
  })
})

module.exports = router""",
                        "src/routes/auth.js": """const express = require('express')
const router = express.Router()

// POST /api/auth/login - Connexion
router.post('/login', (req, res) => {
  const { email, password } = req.body
  
  if (!email || !password) {
    return res.status(400).json({
      error: 'Email et mot de passe requis'
    })
  }
  
  // Simulation d'authentification
  if (email === 'admin@example.com' && password === 'password') {
    res.json({
      message: 'Connexion réussie',
      token: 'jwt-token-example',
      user: {
        id: 1,
        email,
        name: 'Administrateur'
      }
    })
  } else {
    res.status(401).json({
      error: 'Identifiants invalides'
    })
  }
})

// POST /api/auth/register - Inscription
router.post('/register', (req, res) => {
  const { name, email, password } = req.body
  
  if (!name || !email || !password) {
    return res.status(400).json({
      error: 'Nom, email et mot de passe requis'
    })
  }
  
  res.status(201).json({
    message: 'Utilisateur enregistré avec succès',
    user: {
      id: Date.now(),
      name,
      email
    }
  })
})

module.exports = router""",
                        ".env.example": """NODE_ENV=development
PORT=3000
JWT_SECRET=your-jwt-secret-here
MONGODB_URI=mongodb://localhost:27017/express-app
""",
                        "README.md": """# Projet Express.js

## 🚀 Installation rapide

1. **Installez les dépendances :**
```bash
npm install
```

2. **Configurez l'environnement :**
```bash
cp .env.example .env
# Modifiez les valeurs dans .env
```

3. **Lancez le serveur de développement :**
```bash
npm run dev
```

4. **Ou lancez en production :**
```bash
npm start
```

## 🛠 Commandes utiles

```bash
# Développement avec rechargement automatique
npm run dev

# Production
npm start

# Tests
npm test

# Linting
npm run lint
```

## 📁 Structure du projet

- `src/` : Code source de l'application
- `src/routes/` : Routes de l'API
- `src/controllers/` : Contrôleurs
- `src/models/` : Modèles de données
- `src/middleware/` : Middleware personnalisé
- `src/config/` : Configuration
- `src/utils/` : Fonctions utilitaires
- `public/` : Fichiers statiques
- `tests/` : Tests unitaires

## 🔧 Technologies utilisées

- **Express.js** : Framework web Node.js
- **CORS** : Gestion des CORS
- **Helmet** : Sécurité HTTP
- **Morgan** : Logging des requêtes
- **Mongoose** : ODM MongoDB
- **JWT** : Authentification
- **Jest** : Tests unitaires

## 📚 Documentation API

### Endpoints disponibles

- `GET /` - Page d'accueil
- `GET /api/health` - Health check
- `GET /api/users` - Liste des utilisateurs
- `POST /api/users` - Créer un utilisateur
- `POST /api/auth/login` - Connexion
- `POST /api/auth/register` - Inscription
"""
                    }
                },
                "dependencies": [
                    "express",
                    "cors",
                    "helmet",
                    "morgan",
                    "dotenv",
                    "mongoose",
                    "bcryptjs",
                    "jsonwebtoken"
                ],
                "run_command": "npm run dev",
                "dev_port": 3000
            },
            
            "Next.js": {
                "name": "Next.js Framework",
                "description": "Framework React full-stack avec rendu côté serveur",
                "structure": {
                    "dirs": [
                        "src",
                        "src/app",
                        "src/components",
                        "src/lib",
                        "src/styles",
                        "public",
                        "tests"
                    ],
                    "files": {
                        "package.json": """{
  "name": "nextjs-app",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "13.4.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "@next/font": "13.4.0"
  },
  "devDependencies": {
    "typescript": "5.1.0",
    "@types/node": "20.4.0",
    "@types/react": "18.2.0",
    "@types/react-dom": "18.2.0",
    "eslint": "8.45.0",
    "eslint-config-next": "13.4.0"
  }
}""",
                        "next.config.js": """/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  images: {
    domains: ['localhost'],
  },
}

module.exports = nextConfig""",
                        "src/app/layout.tsx": """import './globals.css'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Next.js App',
  description: 'Application Next.js créée avec P_Creator',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fr">
      <body className={inter.className}>
        <nav className="navbar">
          <div className="nav-container">
            <a href="/" className="nav-brand">Next.js App</a>
            <ul className="nav-menu">
              <li><a href="/">Accueil</a></li>
              <li><a href="/about">À propos</a></li>
              <li><a href="/contact">Contact</a></li>
            </ul>
          </div>
        </nav>
        
        <main className="main-content">
          {children}
        </main>
        
        <footer className="footer">
          <p>&copy; 2024 Next.js App. Créé avec Next.js.</p>
        </footer>
      </body>
    </html>
  )
}""",
                        "src/app/page.tsx": """'use client'

import { useState } from 'react'

export default function Home() {
  const [count, setCount] = useState(0)

  return (
    <div className="home">
      <div className="hero">
        <h1>Bienvenue dans votre application Next.js</h1>
        <p>Votre application Next.js est prête à être développée !</p>
        
        <div className="counter">
          <h3>Compteur: {count}</h3>
          <div className="actions">
            <button 
              onClick={() => setCount(count + 1)}
              className="btn btn-primary"
            >
              +
            </button>
            <button 
              onClick={() => setCount(count - 1)}
              className="btn btn-secondary"
            >
              -
            </button>
          </div>
        </div>
      </div>
      
      <div className="features">
        <div className="feature">
          <h3>🚀 SSR</h3>
          <p>Rendu côté serveur pour de meilleures performances</p>
        </div>
        <div className="feature">
          <h3>🔧 Full-Stack</h3>
          <p>API routes intégrées avec React</p>
        </div>
        <div className="feature">
          <h3>📚 Optimisé</h3>
          <p>Optimisations automatiques et code splitting</p>
        </div>
      </div>
    </div>
  )
}""",
                        "src/app/globals.css": """/* Styles globaux pour Next.js */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  line-height: 1.6;
  color: #333;
  background-color: #f4f4f4;
}

.navbar {
  background: #2c3e50;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 2rem;
}

.nav-menu a {
  color: white;
  text-decoration: none;
  transition: color 0.3s;
}

.nav-menu a:hover {
  color: #0070f3;
}

.main-content {
  min-height: calc(100vh - 200px);
}

.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.hero {
  text-align: center;
  padding: 4rem 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.hero p {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 2rem;
}

.counter {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.counter h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #0070f3;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin: 1rem 0;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.btn-primary {
  background: #0070f3;
  color: white;
}

.btn-primary:hover {
  background: #0051cc;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.feature {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
}

.feature h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.footer {
  background: #2c3e50;
  color: white;
  text-align: center;
  padding: 2rem 0;
}
""",
                        "README.md": """# Projet Next.js

## 🚀 Installation rapide

1. **Installez les dépendances :**
```bash
npm install
```

2. **Lancez le serveur de développement :**
```bash
npm run dev
```

3. **Ouvrez votre navigateur :**
http://localhost:3000

## 🛠 Commandes utiles

```bash
# Développement
npm run dev

# Build de production
npm run build

# Production
npm start

# Linting
npm run lint
```

## 📁 Structure du projet

- `src/app/` : Pages et layouts (App Router)
- `src/components/` : Composants React réutilisables
- `src/lib/` : Utilitaires et configuration
- `src/styles/` : Styles CSS
- `public/` : Fichiers statiques
- `tests/` : Tests unitaires

## 🔧 Technologies utilisées

- **Next.js 13** : Framework React full-stack
- **React 18** : Bibliothèque UI
- **TypeScript** : Typage statique
- **App Router** : Nouveau système de routage
- **Server Components** : Composants côté serveur

## 📚 Fonctionnalités Next.js

- **SSR/SSG** : Rendu côté serveur et statique
- **API Routes** : API intégrées
- **Image Optimization** : Optimisation automatique des images
- **Code Splitting** : Division automatique du code
- **Performance** : Optimisations automatiques
"""
                    }
                },
                "dependencies": [
                    "next",
                    "react",
                    "react-dom"
                ],
                "run_command": "npm run dev",
                "dev_port": 3000
            },
            
            "React Native": {
                "name": "React Native Framework",
                "description": "Framework pour développer des applications mobiles natives avec React",
                "structure": {
                    "dirs": [
                        "src",
                        "src/components",
                        "src/screens",
                        "src/navigation",
                        "src/services",
                        "src/utils",
                        "src/assets",
                        "src/assets/images",
                        "android",
                        "ios"
                    ],
                    "files": {
                        "package.json": """{
  "name": "react-native-app",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "android": "react-native run-android",
    "ios": "react-native run-ios",
    "start": "react-native start",
    "test": "jest",
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx"
  },
  "dependencies": {
    "react": "18.2.0",
    "react-native": "0.72.0",
    "@react-navigation/native": "^6.1.0",
    "@react-navigation/stack": "^6.3.0",
    "@react-navigation/bottom-tabs": "^6.5.0",
    "react-native-screens": "^3.25.0",
    "react-native-safe-area-context": "^4.7.0",
    "react-native-gesture-handler": "^2.12.0",
    "react-native-vector-icons": "^10.0.0",
    "axios": "^1.4.0"
  },
  "devDependencies": {
    "@babel/core": "^7.20.0",
    "@babel/preset-env": "^7.20.0",
    "@babel/runtime": "^7.20.0",
    "@react-native/eslint-config": "^0.72.0",
    "@react-native/metro-config": "^0.72.0",
    "@tsconfig/react-native": "^3.0.0",
    "@types/react": "^18.0.24",
    "@types/react-test-renderer": "^18.0.0",
    "babel-jest": "^29.2.1",
    "eslint": "^8.19.0",
    "jest": "^29.2.1",
    "metro-react-native-babel-preset": "0.76.5",
    "prettier": "^2.4.1",
    "react-test-renderer": "18.2.0",
    "typescript": "4.8.4"
  },
  "jest": {
    "preset": "react-native"
  }
}""",
                        "App.tsx": """import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'react-native';

import HomeScreen from './src/screens/HomeScreen';
import AboutScreen from './src/screens/AboutScreen';
import ContactScreen from './src/screens/ContactScreen';

const Stack = createStackNavigator();

const App = () => {
  return (
    <NavigationContainer>
      <StatusBar barStyle="dark-content" backgroundColor="#ffffff" />
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerStyle: {
            backgroundColor: '#2c3e50',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      >
        <Stack.Screen 
          name="Home" 
          component={HomeScreen} 
          options={{ title: 'Accueil' }}
        />
        <Stack.Screen 
          name="About" 
          component={AboutScreen} 
          options={{ title: 'À propos' }}
        />
        <Stack.Screen 
          name="Contact" 
          component={ContactScreen} 
          options={{ title: 'Contact' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;""",
                        "src/screens/HomeScreen.tsx": """import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Alert,
} from 'react-native';

const HomeScreen = ({ navigation }) => {
  const [count, setCount] = useState(0);

  const showAlert = () => {
    Alert.alert(
      'Bienvenue!',
      'Votre application React Native est prête!',
      [{ text: 'OK' }]
    );
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.hero}>
        <Text style={styles.title}>Bienvenue dans votre application React Native</Text>
        <Text style={styles.subtitle}>
          Votre application mobile est prête à être développée!
        </Text>
        
        <View style={styles.counter}>
          <Text style={styles.counterTitle}>Compteur: {count}</Text>
          <View style={styles.actions}>
            <TouchableOpacity
              style={[styles.button, styles.primaryButton]}
              onPress={() => setCount(count + 1)}
            >
              <Text style={styles.buttonText}>+</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.button, styles.secondaryButton]}
              onPress={() => setCount(count - 1)}
            >
              <Text style={styles.buttonText}>-</Text>
            </TouchableOpacity>
          </View>
        </View>
        
        <TouchableOpacity style={styles.alertButton} onPress={showAlert}>
          <Text style={styles.alertButtonText}>Tester l'alerte</Text>
        </TouchableOpacity>
      </View>
      
      <View style={styles.features}>
        <View style={styles.feature}>
          <Text style={styles.featureIcon}>🚀</Text>
          <Text style={styles.featureTitle}>Natif</Text>
          <Text style={styles.featureDescription}>
            Performance native sur iOS et Android
          </Text>
        </View>
        
        <View style={styles.feature}>
          <Text style={styles.featureIcon}>🔧</Text>
          <Text style={styles.featureTitle}>Flexible</Text>
          <Text style={styles.featureDescription}>
            Développement cross-platform avec React
          </Text>
        </View>
        
        <View style={styles.feature}>
          <Text style={styles.featureIcon}>📚</Text>
          <Text style={styles.featureTitle}>Documenté</Text>
          <Text style={styles.featureDescription}>
            Documentation excellente et communauté active
          </Text>
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f4f4f4',
  },
  hero: {
    padding: 20,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2c3e50',
    textAlign: 'center',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 30,
  },
  counter: {
    backgroundColor: '#ffffff',
    padding: 20,
    borderRadius: 10,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  counterTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#007AFF',
    textAlign: 'center',
    marginBottom: 15,
  },
  actions: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 15,
  },
  button: {
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 5,
    minWidth: 50,
    alignItems: 'center',
  },
  primaryButton: {
    backgroundColor: '#007AFF',
  },
  secondaryButton: {
    backgroundColor: '#95a5a6',
  },
  buttonText: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 18,
  },
  alertButton: {
    backgroundColor: '#2c3e50',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 8,
    marginTop: 20,
  },
  alertButtonText: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  features: {
    padding: 20,
  },
  feature: {
    backgroundColor: '#ffffff',
    padding: 20,
    borderRadius: 10,
    marginBottom: 15,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  featureIcon: {
    fontSize: 30,
    marginBottom: 10,
  },
  featureTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 5,
  },
  featureDescription: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
  },
});

export default HomeScreen;""",
                        "README.md": """# Projet React Native

## 🚀 Installation rapide

1. **Installez les dépendances :**
```bash
npm install
```

2. **Pour Android :**
```bash
npm run android
```

3. **Pour iOS :**
```bash
npm run ios
```

4. **Démarrer Metro :**
```bash
npm start
```

## 🛠 Commandes utiles

```bash
# Android
npm run android

# iOS
npm run ios

# Metro bundler
npm start

# Tests
npm test

# Linting
npm run lint
```

## 📁 Structure du projet

- `src/` : Code source de l'application
- `src/screens/` : Écrans de l'application
- `src/components/` : Composants réutilisables
- `src/navigation/` : Configuration de navigation
- `src/services/` : Services et API
- `src/utils/` : Fonctions utilitaires
- `src/assets/` : Images et ressources
- `android/` : Code Android natif
- `ios/` : Code iOS natif

## 🔧 Technologies utilisées

- **React Native** : Framework mobile cross-platform
- **React Navigation** : Navigation entre écrans
- **TypeScript** : Typage statique
- **Metro** : Bundler JavaScript
- **Jest** : Tests unitaires

## 📱 Plateformes supportées

- **Android** : API 21+ (Android 5.0+)
- **iOS** : iOS 11.0+
- **Web** : React Native Web (optionnel)

## 🚀 Déploiement

### Android
```bash
# Build de production
cd android
./gradlew assembleRelease
```

### iOS
```bash
# Build de production
cd ios
xcodebuild -workspace App.xcworkspace -scheme App -configuration Release
```
"""
                    }
                },
                "dependencies": [
                    "react-native",
                    "@react-navigation/native",
                    "@react-navigation/stack",
                    "react-native-screens",
                    "react-native-safe-area-context",
                    "react-native-gesture-handler",
                    "react-native-vector-icons",
                    "axios"
                ],
                "run_command": "npm run android",
                "dev_port": 8081
            },
            
            "React": {
                "name": "React Application",
                "description": "Application React moderne avec Vite et TypeScript",
                "structure": {
                    "dirs": [
                        "src",
                        "src/components",
                        "src/pages",
                        "src/hooks",
                        "src/services",
                        "src/utils",
                        "src/types",
                        "public"
                    ],
                    "files": {
                        "package.json": """{
  "name": "react-app",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@typescript-eslint/eslint-plugin": "^6.14.0",
    "@typescript-eslint/parser": "^6.14.0",
    "@vitejs/plugin-react": "^4.2.1",
    "eslint": "^8.55.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "typescript": "^5.2.2",
    "vite": "^5.0.8"
  }
}""",
                        "vite.config.ts": """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true
  }
})""",
                        "tsconfig.json": """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}""",
                        "src/main.tsx": """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)""",
                        "src/App.tsx": """import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App""",
                        "README.md": """# Projet React

## 🚀 Installation rapide

1. **Installez les dépendances :**
```bash
npm install
```

2. **Lancez le serveur de développement :**
```bash
npm run dev
```

3. **Ouvrez votre navigateur :**
http://localhost:3000

## 🛠 Commandes utiles

```bash
# Développement
npm run dev

# Build de production
npm run build

# Linting
npm run lint

# Prévisualisation du build
npm run preview
```

## 📁 Structure du projet

- `src/` : Code source de l'application
- `src/components/` : Composants React
- `src/pages/` : Pages de l'application
- `src/hooks/` : Hooks personnalisés
- `src/services/` : Services et API
- `src/utils/` : Fonctions utilitaires
- `src/types/` : Types TypeScript
- `public/` : Fichiers publics

## 🔧 Technologies utilisées

- **React 18** : Bibliothèque UI
- **TypeScript** : Typage statique
- **Vite** : Build tool rapide
- **React Router** : Routage
- **Axios** : Client HTTP
"""
                    }
                },
                "dependencies": [
                    "react",
                    "react-dom",
                    "react-router-dom",
                    "axios"
                ],
                "run_command": "npm run dev",
                "dev_port": 3000
            }
        }
    }
    
    @classmethod
    def get_languages(cls) -> List[str]:
        """Retourne la liste des langages supportés"""
        return list(cls.TEMPLATES.keys())
    
    @classmethod
    def get_frameworks(cls, language: str) -> List[Dict[str, Any]]:
        """Retourne la liste des frameworks pour un langage"""
        if language not in cls.TEMPLATES:
            return []
        
        frameworks = []
        for key, template in cls.TEMPLATES[language].items():
            frameworks.append({
                "key": key,
                "name": template["name"],
                "description": template["description"]
            })
        return frameworks
    
    @classmethod
    def get_template(cls, language: str, framework: str) -> Dict[str, Any]:
        """Retourne le template complet pour un framework"""
        if language not in cls.TEMPLATES:
            raise ValueError(f"Langage {language} non supporté")
        
        if framework not in cls.TEMPLATES[language]:
            raise ValueError(f"Framework {framework} non supporté pour {language}")
        
        return cls.TEMPLATES[language][framework]
    
    @classmethod
    def get_dependencies(cls, language: str, framework: str) -> List[str]:
        """Retourne les dépendances pour un framework"""
        template = cls.get_template(language, framework)
        return template.get("dependencies", [])
    
    @classmethod
    def get_run_command(cls, language: str, framework: str) -> str:
        """Retourne la commande de lancement pour un framework"""
        template = cls.get_template(language, framework)
        return template.get("run_command", "")
    
    @classmethod
    def get_dev_port(cls, language: str, framework: str) -> int:
        """Retourne le port de développement pour un framework"""
        template = cls.get_template(language, framework)
        return template.get("dev_port", 8000)
