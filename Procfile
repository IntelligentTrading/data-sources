release: python manage.py migrate
web: waitress-serve --port=$PORT settings.wsgi:application
worker: python manage.py trawl_poloniex
worker: python manage.py run_info_bot

