migrate:
	./manage.py makemigrations --noinput
	./manage.py migrate --noinput

static:
	./manage.py collectstatic --noinput

app: migrate
	./manage.py runserver 0.0.0.0:8000

gunicorn: static migrate
	gunicorn \
		--reload \
		--bind 0.0.0.0:8000 \
		--workers 4 \
		dtpmap.wsgi:application
