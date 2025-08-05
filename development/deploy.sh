#!/bin/bash

# Deployment script for NexusAI

echo "Starting deployment..."
echo

# Update dependencies
echo "Updating dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Restart services
echo "Restarting services..."
sudo systemctl restart nexusai.service

# Clear cache
echo "Clearing cache..."
sudo systemctl restart memcached

# Run tests
echo "Running tests..."
python manage.py test

echo
echo "Deployment completed successfully!"
