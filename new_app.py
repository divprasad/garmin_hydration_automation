from flask import Flask, jsonify
from log_hydration import log_hydration

app = Flask(__name__)

@app.route('/log_hydration', methods=['POST'])
def log_hydration_route():
    """
    Logs 250ml of water to Garmin Connect and returns hydration status.
    """
    try:
        hydration_stats = log_hydration()
        return jsonify({'status': 'success', **hydration_stats}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
