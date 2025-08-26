#!/bin/bash
# Railway build script

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Current value of GOOGLE_API_KEY:"
echo $GOOGLE_API_KEY


echo "Build completed successfully!"
