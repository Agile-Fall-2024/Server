# Variables
DJANGO_MANAGE = python manage.py
ENV ?= .env

# Targets
.PHONY: run migrate migrations superuser shell test clean

# Start the development server
run:
	$(DJANGO_MANAGE) runserver

# Apply migrations
migrate:
	$(DJANGO_MANAGE) migrate

# Create new migrations
migrations:
	$(DJANGO_MANAGE) makemigrations

# Create a superuser
superuser:
	$(DJANGO_MANAGE) createsuperuser

# Open the Django shell
shell:
	$(DJANGO_MANAGE) shell

# Run tests
test:
	$(DJANGO_MANAGE) test

# Clean up pyc files and caches
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete