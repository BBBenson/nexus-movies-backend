# #!/bin/sh

# if [ "$DATABASE" = "postgres" ] 
# then
#     echo "Check if database is running..."

#     while ! nc -z $SQL_HOST $SQL_PORT; do
#         sleep 0.1
#     done

#     echo "The database is up and running :-D"
# fi

# python manage.py makemigrations
# python manage.py migrate

# exec "$@"


# Create a new entrypoint.sh file
cat > entrypoint.sh << 'EOF'
#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is ready!"

# Run Django migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Execute the main command
exec "$@"
EOF

# Set proper permissions
chmod +x entrypoint.sh