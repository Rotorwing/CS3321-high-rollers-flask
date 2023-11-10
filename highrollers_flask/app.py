import flask

from flask import Flask, render_template, request
from highrollers_flask.GameManager import GameManager

app = Flask(__name__)

game_manager = GameManager()

@app.route('/')
def view_home():
    return render_template('index.html')

@app.route('/api/test/', methods=['POST'])
def test():
    return game_manager.handle_client_message(request, "test")

