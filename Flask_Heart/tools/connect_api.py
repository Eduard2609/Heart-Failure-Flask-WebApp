import requests
import json

def connect_to_api(model, data):
    # Define the base URL for the API
    base_url = "http://127.0.0.1:8000"

    # Define the endpoint based on the selected model
    if model == "logistic_regression":
        endpoint = "/predict_lr"
    elif model == "random_forest":
        endpoint = "/predict_rf"
    elif model == "svm":
        endpoint = "/predict_svm"
    elif model == "dtc":
        endpoint = "/predict_dtc"
    else:
        # Handle invalid model case or set a default endpoint
        endpoint = "/about"

    # Construct the full URL
    url = base_url + endpoint

    # Make a POST request to the API
    response = requests.post(url, json=data)

    # Handle the response
    if response.status_code == 200:
        # Successful request
        result = json.loads(response.text)
        return result
    else:
        # Request failed
        return None
