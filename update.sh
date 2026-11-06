git pull
python manage.py makemigrations app
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py load_initial_data
redis-server --daemonize yes
sudo systemctl restart apache2
