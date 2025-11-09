import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_hydration():
    """Login to Garmin Connect and add hydration data."""
    load_dotenv()
    # Get credentials from environment variables
    username = os.getenv("GARMIN_USERNAME")
    password = os.getenv("GARMIN_PASSWORD")

    if not username or not password:
        raise ValueError("GARMIN_USERNAME and GARMIN_PASSWORD environment variables are not set.")

    # Initialize Garmin client
    client = Garmin(username, password)

    # Login to Garmin Connect
    client.login()

    # Log hydration
    today = datetime.now().strftime("%Y-%m-%d")
    logger.info(f"Adding 250ml of hydration for {today}")
    client.add_hydration_data(250)

    # Get today's hydration data
    hydration_data = client.get_hydration_data(today)
    logger.info(f"Raw hydration data from Garmin: {hydration_data}")
    goal = hydration_data["goalInML"]
    current = hydration_data["valueInML"]
    remaining = goal - current

    return {
        "added": 250,
        "total": current,
        "goal": goal,
        "remaining": remaining
    }


if __name__ == "__main__":
    try:
        hydration_stats = log_hydration()
        logger.info(
            f"Water added: {hydration_stats['added']}ml. "
            f"Today's total: {hydration_stats['total']}ml. "
            f"Goal: {hydration_stats['goal']}ml. "
            f"Remaining: {hydration_stats['remaining']}ml."
        )
    except (GarminConnectAuthenticationError, ValueError) as e:
        logger.error(f"Authentication failed: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
