from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is not None:
        app.config.update(test_config)

    @app.get("/")
    def index():
        return jsonify(service="aws-ecs-secure-deployment", status="ok")

    @app.get("/health")
    def health():
        # Liveness only: this application has no external dependencies.
        return jsonify(status="healthy")

    @app.errorhandler(HTTPException)
    def http_error(error):
        response = error.get_response()
        response.data = app.json.dumps({"error": error.name})
        response.content_type = "application/json"
        return response

    @app.errorhandler(500)
    def server_error(error):
        return jsonify(error="Internal Server Error"), 500

    return app
