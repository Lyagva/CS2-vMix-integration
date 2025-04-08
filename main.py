import json
import webbrowser

from config_manager import config
from export_handlers import export_csv, preparation, export_json, export_excel

from flask import Flask, request, jsonify, render_template

import logging
from logging_handler import export_logger, preparation_logger, stream_handler, file_handler


app = Flask(__name__)

# Disable Flask's built-in logger handlers
app.logger.handlers = []
app.logger.propagate = False

# Redirect Werkzeug logs to your custom logger
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.name = "network"
werkzeug_logger.handlers = []
werkzeug_logger.propagate = False
if config.get("LOG.network_terminal_logging"):
    werkzeug_logger.addHandler(stream_handler)
werkzeug_logger.addHandler(file_handler)


latest_data = {}

@app.route('/', methods=['POST'])
def handle_data():
    global latest_data
    latest_data = request.json
    werkzeug_logger.info("Received new data payload")

    if config.get("DEBUG.debug_mode"):
        debug_file = config.get("DEBUG.save_file")
        with open(debug_file, mode="w+", encoding="UTF-8") as f:
            json.dump(latest_data, f)
        export_logger.debug(f"Saved data to debug file: {debug_file}")

    data = preparation.flatten_dict(preparation.prepare_data(latest_data))
    preparation_logger.debug(f"Prepared data: {data}")
    if config.get("CSV.export"):
        export_csv.write_csv(data)
        export_logger.info("Exported data to CSV")
    if config.get("JSON.export"):
        export_json.write_json(data)
        export_logger.info("Exported data to JSON")
    if config.get("EXCEL.export"):
        export_excel.write_excel(data)
        export_logger.info("Exported data to Excel")

    return jsonify(success=True)


@app.route('/dashboard')
def dashboard():
    werkzeug_logger.debug("Dashboard accessed")
    return render_template('dashboard.html', update_period=config.get("API.update_period"))

@app.route('/data', methods=['GET'])
def get_data():
    global latest_data

    if config.get("DEBUG.debug_mode"):
        debug_file = config.get("DEBUG.save_file")
        export_logger.debug(f"Reading data from debug file: {debug_file}")
        return jsonify(json.load(open(debug_file, mode="r"))), 200

    werkzeug_logger.debug("Returning latest data")
    return jsonify(latest_data), 200


if __name__ == '__main__':
    werkzeug_logger.info("Starting Flask server...")
    # webbrowser.open("http://127.0.0.1:5000/dashboard")
    app.run(port=5000, debug=config.get("NETWORK.flask_debug"))
