# Project: Garmin Hydration Logger

## Objective

The main objective of this project is to create a simple way to log 250ml of water to a Garmin Connect account, triggered from Home Assistant by scanning an NFC tag.

## Current Implementation

*   **`log_hydration.py`**: A Python script that uses the `garminconnect` library to handle the authentication and logging of hydration. It reads credentials securely from a `.env` file.
*   **`run_garmin_flask_app.py`**: A lightweight Flask web application that exposes a single endpoint (`/log_hydration`). When a POST request is made to this endpoint, it calls the `log_hydration` function from `log_hydration.py` and returns the current hydration status as a JSON response. This allows other services, like Home Assistant, to trigger the hydration logging.
*   **`requirements.txt`**: Lists the project dependencies, including `Flask` and `garminconnect`.
*   **Virtual Environment (`garmin_env`)**: Isolates project dependencies.

## Home Assistant Integration

The script is triggered from a Home Assistant automation. Here’s how to set it up:

### 1. Exposing the Script to Home Assistant

We are using a web service to expose the script to Home Assistant. The `run_garmin_flask_app.py` Flask application runs on your network and listens for POST requests on the `/log_hydration` endpoint.

To start the service, run the following command in your project directory:

```bash
/path/to/your/garmin_env/bin/python run_garmin_flask_app.py
```

Make sure to replace `/path/to/your/garmin_env/bin/python` with the actual path to the Python interpreter in your virtual environment. The service will run on `http://<your-ip-address>:5001`.

### 2. Home Assistant Automation

This automation will be triggered when you scan an NFC tag with your phone.

#### a. Configure the `shell_command` in Home Assistant

In your `configuration.yaml` file in Home Assistant, add the following `rest_command` configuration. This command will send the POST request to your Flask application.

```yaml
rest_command:
  log_hydration:
    url: 'http://192.168.1.138:5001/log_hydration'
    method: 'POST'
    content_type: 'application/json'
    # The response from the curl command will be available in the 'response' variable
    # of the action sequence.
    # e.g. {{ trigger.event.data.response }}
```

Replace `<your-ip-address>` with the IP address of the machine running the `run_garmin_flask_app.py` script. After adding this, restart Home Assistant to apply the changes.

#### b. Create the Automation in Home Assistant

1.  **Go to Settings > Automations & Scenes** in Home Assistant and create a new automation.
2.  **Set the Trigger:**
    *   Select **Tag** as the trigger type.
    *   You will need to scan an NFC tag with the Home Assistant Companion app on your phone to get its ID. Once you scan it, you can select it here.
3.  **Set the Action:**
    *   Select **Call service** as the action type.
    *   Choose the `rest_command.log_hydration` service that you created in the previous step.
4.  **Save the automation.**

### 3. Capturing and Displaying the Output

The response from the `rest_command` will contain the JSON payload from your Flask app (e.g., `{"status": "success", "total": 2250.0, ...}`).

To display this as a notification on your Android phone:

1.  **Add another action to your automation:**
    *   Select **Call service** as the action type.
    *   Choose the `notify.mobile_app_<your_device_name>` service (replace `<your_device_name>` with the name of your phone in Home Assistant).
2.  **Configure the notification:**
    *   In the **Message** field, you can use a template to display the information from the response. For example:

    ```jinja
    Water logged! Your new total is {{ response.total }}ml.
    ```

    You will need to first capture the response from the `rest_command`. Here is how you can do it:

    ```yaml
    - service: rest_command.log_hydration
      response_variable: hydration_response
    - service: notify.mobile_app_<your_device_name>
      data:
        message: "Water logged! Your new total is {{ hydration_response.json.total }}ml."
    ```

This setup will allow you to scan an NFC tag, trigger the hydration logging, and receive a notification on your phone with the updated hydration total.
