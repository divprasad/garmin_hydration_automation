# Garmin Hydration Automation

![GitHub repo size](https://img.shields.io/github/repo-size/divprasad/garmin_hydration_automation)
![GitHub stars](https://img.shields.io/github/stars/divprasad/garmin_hydration_automation?style=social)
![GitHub forks](https://img.shields.io/github/forks/divprasad/garmin_hydration_automation?style=social)

A simple and effective way to log your water intake to Garmin Connect using a Home Assistant automation triggered by an NFC tag. This project provides a seamless, one-tap solution to keep your hydration levels updated without manually entering data into the Garmin Connect app.

## The Problem

Logging water intake consistently can be a hassle. While Garmin Connect provides a way to track hydration, it requires opening the app, navigating to the hydration widget, and manually adding water. This friction can lead to inconsistent logging.

## The Solution

This project automates the process by using an NFC tag to trigger a Home Assistant automation. A quick tap of your phone on an NFC tag (e.g., on your water bottle) logs a predefined amount of water (250ml in this implementation) to your Garmin Connect account.

## How It Works

1.  **NFC Tag Trigger**: An NFC tag is scanned by your phone.
2.  **Home Assistant Automation**: The scan triggers an automation in Home Assistant.
3.  **REST Command**: Home Assistant sends a POST request to a lightweight Flask web server.
4.  **Garmin Connect API**: The Flask server runs a Python script that uses the `garminconnect` library to log the hydration to your Garmin Connect account.
5.  **Notification**: Home Assistant sends a notification to your phone with the updated hydration total.

## Project Structure

*   `log_hydration.py`: The core Python script that interacts with the Garmin Connect API.
*   `run_garmin_flask_app.py`: A Flask web server that exposes an endpoint to trigger the hydration logging.
*   `app.py`: CLI helper used during early experiments (not required for the NFC workflow).
*   `requirements.txt`: Project dependencies.

## Prerequisites

*   Home Assistant instance
*   NFC tags
*   Python 3.x
*   A phone with NFC capabilities and the Home Assistant Companion app

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/divprasad/garmin_hydration_automation.git
    cd garmin_hydration_automation
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Configuration

1.  **Create a `.env` file:**
    Create a `.env` file in the project root (there is no template committed yet) and add your Garmin Connect credentials:
    ```
    GARMIN_USERNAME=your_email@example.com
    GARMIN_PASSWORD=your_password
    ```

2.  **Start the DEV Flask server:**
    ```bash
    python run_garmin_flask_app.py
    ```
    The server will run on `http://<your-ip-address>:5001`.

    ```bash
    gunicorn --bind 0.0.0.0:5001 run_garmin_flask_app:hydrate_command_flask_app
    ```

3.  **Configure Home Assistant:**
    Add the following `rest_command` to your `configuration.yaml` file in Home Assistant:
    ```yaml
    rest_command:
      log_hydration:
        url: 'http://<your-ip-address>:5001/log_hydration'
        method: 'POST'
        content_type: 'application/json'
    ```
    Replace `<your-ip-address>` with the IP address of the machine running the Flask server. Restart Home Assistant to apply the changes.

## Usage

1.  **Create a Home Assistant Automation:**
    *   Go to **Settings > Automations & Scenes** and create a new automation.
    *   **Trigger**: Select **Tag** and scan your NFC tag to get its ID.
    *   **Action**: Select **Call service** and choose `rest_command.log_hydration`.

2.  **(Optional) Add a notification:**
    Add another action to the automation to get a notification with the updated hydration total:
    ```yaml
    - service: rest_command.log_hydration
      response_variable: hydration_response
    - service: notify.mobile_app_<your_device_name>
      data:
        message: "Water logged! Your new total is {{ hydration_response.json.total }}ml."
    ```
    Replace `<your_device_name>` with the name of your phone in Home Assistant.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs, feature requests, or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
