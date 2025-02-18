import json
import webbrowser
from flask import Flask, request, jsonify, render_template
from config_manager import config

app = Flask(__name__)
latest_data = {}

@app.route('/', methods=['POST'])
def handle_data():
    global latest_data
    if not config.get('DEBUG.debug_mode'):
        latest_data = request.json
        save_path = config.get('DEBUG.save_file')
        with open(save_path, mode="w") as f:
            json.dump(latest_data, f)
    return jsonify(success=True)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', update_period=config.get("API.update_period"))

@app.route('/data', methods=['GET'])
def get_data():
    if config.get('DEBUG.debug_mode'):
        save_path = config.get('DEBUG.save_file')
        try:
            with open(save_path, mode="r") as f:
                data = json.load(f)
            return jsonify(data)
        except FileNotFoundError:
            return jsonify(error="Save file not found"), 404
        except json.JSONDecodeError:
            return jsonify(error="Error decoding JSON from save file"), 400
    else:
        return jsonify(latest_data)

if __name__ == '__main__':
    # webbrowser.open(f"http://{config.get('ip')}:{config.get('port')}/dashboard")
    app.run(
        host=config.get('NETWORK.ip'),
        port=config.get('NETWORK.port'),
        debug=config.get('NETWORK.flask_debug')
    )