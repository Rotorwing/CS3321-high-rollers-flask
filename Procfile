web: gunicorn --chdir highrollers_flask app:app --log-file -
worker: flask --app ./highrollers_flask/app.py run