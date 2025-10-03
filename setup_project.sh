#!/bin/bash
# Creates the structure for the Joke Generator project

# Create backend directories
mkdir -p backend/app/services
touch backend/app/__init__.py backend/app/services/__init__.py

# Create backend files
touch backend/app/main.py
touch backend/app/services/joke_service.py
touch backend/requirements.txt

# Create frontend directories
mkdir -p frontend/static/css
mkdir -p frontend/static/js

# Create frontend files
touch frontend/index.html
touch frontend/static/css/style.css
touch frontend/static/js/script.js

echo "Joke Generator project structure created successfully!"