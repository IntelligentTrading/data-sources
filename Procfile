release: python manage.py migrate
web: waitress-serve settings.wsgi:application
worker: python manage.py trawl_poloniex

