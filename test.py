from flask import Flask
app = Flask(__name__)


def create_store(msg):
    with app.app_context():
        store.create(msg)