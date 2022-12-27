import os
import json

from flask import Flask, request
from flask_wtf.csrf import CSRFProtect
from flask_cors import cross_origin

from events_collector.config.log_conf import logger
from events_collector.config.config import settings
from events_collector.apps.worker.services import EventsHandler
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SESSION_COOKIE_SECURE"] = settings.SESSION_COOKIE_SECURE
app.config['WTF_CSRF_ENABLED'] = settings.CSRF_ENABLED

csrf = CSRFProtect()
csrf.init_app(app)

mimetype = 'application/json'


def execute():
    """
    Main function to start Flask application
    """
    app.run(host='0.0.0.0', port='8080')


@app.route('/health/readiness', methods=["GET"])
def readiness():
    """
    Текущее состояние готовности сервиса
    """
    logger.info("Readiness checking started")
    return app.response_class(
        response={"status": "UP"},
        status=200,
        mimetype=mimetype
    )


@app.route('/health/liveness', methods=["GET"])
def liveness():
    """
    Возвращает информацию о работоспособности сервиса
    """
    logger.info("Liveness checking started")
    return app.response_class(
        response={"status": "UP"},
        status=200,
        mimetype=mimetype
    )


@app.route('/metrics', methods=["GET"])
def metrics():
    """
    Возвращает метрики сервиса
    """
    return app.response_class(
        response=generate_latest(),
        status=200,
        mimetype='text/plain',
        content_type=CONTENT_TYPE_LATEST
    )


@app.route('/api', methods=["GET"])
def api_routes():
    return {
        "openapi:": "3.0.0",
        "info": {
            "title": "Событийный шлюз",
            "version": "0.3",
        },
        "paths": {}
        }


@app.route("/api/force-update", methods=["POST"])
@cross_origin(origins=["0.0.0.0"], methods=["POST", "OPTIONS"])
def force_update():
    incoming_data: dict = json.loads(request.get_data(as_text=True))
    logger.info(f"Incoming request: {incoming_data}")
    handler = EventsHandler(
        event=incoming_data.get("data").get("feed"),
        source_message=incoming_data.get("data").pop("source_message")
    )
    handler.check_event_matching()
    return app.response_class(
        response={"status": "FINISHED"},
        status=200,
        mimetype=mimetype
    )
