import json
import webbrowser

from flask import Flask, request, jsonify, render_template
from config_manager import config


app = Flask(__name__)
latest_data = {}
if config.get("DEBUG.debug_mode"):
    path = config.get("DEBUG.save_file")
    latest_data = json.load(open(path, mode="r+"))
    print("Loaded test data from:", path)


@app.route("/", methods=["POST"])
def handle_data():
    global latest_data
    if not config.get("DEBUG.debug_mode"):
        latest_data = request.json
        save_path = config.get("DEBUG.save_file")
        with open(save_path, mode="w") as f:
            json.dump(latest_data, f)
    return jsonify(success=True)


@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html", update_period=config.get("API.update_period"))

@app.route("/get_data", methods=["GET"])
def get_data():
    return jsonify(latest_data)


if __name__ == "__main__":
    app.run(
        host=config.get("NETWORK.ip"),
        port=config.get("NETWORK.port"),
        debug=config.get("NETWORK.flask_debug")
    )