from dotenv import load_dotenv
from pymongo import MongoClient
import os
from flask import Flask
from routes.habits import habits
from routes.todo import todo
from routes.matrix import matrix

load_dotenv()


def create_app():
    app = Flask(__name__)

    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.habittrackerapp  # type: ignore[attr-defined]

    app.register_blueprint(habits)
    app.register_blueprint(todo)
    app.register_blueprint(matrix)
    return app
