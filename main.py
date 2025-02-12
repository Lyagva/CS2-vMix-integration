from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Global variable to store the latest JSON data received from CS2.
latest_data = {}

@app.route('/', methods=['POST'])
def handle_data():
    global latest_data
    latest_data = request.json
    print("Received data:", latest_data)
    return jsonify(success=True)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/data', methods=['GET'])
def get_data():
    global latest_data
    return jsonify(latest_data)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
