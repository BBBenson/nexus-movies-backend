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


#!/bin/sh

# Wait for PostgreSQL database to be ready
echo "Check if database is running..."

# Use default PostgreSQL values if environment variables are not set
SQL_HOST=${SQL_HOST:-db}
SQL_PORT=${SQL_PORT:-5432}

while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
done

echo "The database is up and running :-D"

# Run Django migrations
python manage.py makemigrations
python manage.py migrate

# Execute the command passed to the container
exec "$@"