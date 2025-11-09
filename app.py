import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
)

app = Flask(__name__)

# Configure logging
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

def log_hydration_to_garmin():
    """Logs 250ml of water to Garmin Connect and returns hydration status."""
    load_dotenv()
    try:
        # Get credentials from environment variables
        username = os.getenv("GARMIN_USERNAME")
        password = os.getenv("GARMIN_PASSWORD")

        if not username or not password:
            app.logger.error("GARMIN_USERNAME and GARMIN_PASSWORD environment variables are not set.")
            return False, {"message": "Credentials not set."}

        # Initialize Garmin client
        client = Garmin(username, password)

        # Login to Garmin Connect
        client.login()

        # Log hydration
        today = datetime.now().strftime("%Y-%m-%d")
        app.logger.info(f"Adding 250ml of hydration for {today}")
        client.add_hydration_data(250)

        # Get today's hydration data
        hydration_data = client.get_hydration_data(today)
        goal = hydration_data["goalInML"]
        current = hydration_data["valueInML"]
        remaining = goal - current

        hydration_stats = {
            "added": 250,
            "total": current,
            "goal": goal,
            "remaining": remaining
        }
        app.logger.info(f"Hydration update: {hydration_stats}")
        return True, hydration_stats

    except GarminConnectAuthenticationError as e:
        app.logger.error(f"Authentication failed: {e}")
        return False, {"message": f"Authentication failed: {e}"}
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return False, {"message": f"An error occurred: {e}"}

@app.route('/log_hydration', methods=['POST'])
def trigger_log_hydration():
    """Triggers the hydration logging."""
    success, data = log_hydration_to_garmin()
    if success:
        return jsonify({"status": "success", **data}), 200
    else:
        return jsonify({"status": "error", **data}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
