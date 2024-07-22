import os
import joblib
import numpy as np
import pandas as pd
from google.cloud import storage
import json

# Define a dictionary mapping numerical weather codes to their descriptions
weather_code_mapping = {
    0: "Cloud development not observed or observable",
    1: "Clouds dissolving or becoming less developed",
    2: "State of sky on the whole unchanged",
    3: "Clouds generally forming or developing",
    51: "Drizzle, not freezing, continuous (slight at time of observation)",
    53: "Drizzle, not freezing, continuous (moderate at time of observation)",
    55: "Drizzle, not freezing, continuous (heavy at time of observation)",
    61: "Rain, not freezing, continuous (slight at time of observation)",
    63: "Rain, not freezing, continuous (moderate at time of observation)",
    65: "Rain, not freezing, continuous (heavy at time of observation)"
}

# List of known weather codes
weather_codes = np.array(list(weather_code_mapping.keys()))

# Function to find the closest weather code
def closest_weather_code(predicted_code):
    index = np.abs(weather_codes - predicted_code).argmin()
    return weather_codes[index]

# Load models from Google Cloud Storage
def load_model_from_gcs(bucket_name, model_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(model_path)
    local_model_path = f"/tmp/{os.path.basename(model_path)}"
    blob.download_to_filename(local_model_path)
    model = joblib.load(local_model_path)
    return model

# Load all models
bucket_name = "assignment"  # Replace with your bucket name
temperature_model = load_model_from_gcs(bucket_name, "temperature_model.pkl")
weathercode_model = load_model_from_gcs(bucket_name, "weathercode_model.pkl")
rain_model = load_model_from_gcs(bucket_name, "rain_model.pkl")

def predict_weather(request):
    request_json = request.get_json()

    if not request_json or 'apparent_temperature_mean' not in request_json or 'rain_sum' not in request_json:
        return json.dumps({'error': 'Invalid input'}), 400, {'Content-Type': 'application/json'}

    apparent_temperature_mean = request_json['apparent_temperature_mean']
    rain_sum = request_json['rain_sum']

    input_data = pd.DataFrame({
        'apparent_temperature_mean': [apparent_temperature_mean],
        'rain_sum': [rain_sum]
    })

    predicted_temperature = temperature_model.predict(input_data)[0]
    predicted_weathercode = weathercode_model.predict(input_data)[0]
    predicted_rain = rain_model.predict(input_data)[0]

    closest_code = closest_weather_code(predicted_weathercode)
    predicted_weather_description = weather_code_mapping.get(closest_code, "Unknown weather code")

    result = {
        'predicted_temperature': predicted_temperature,
        'predicted_weathercode': predicted_weathercode,
        'assigned_weather_code_description': predicted_weather_description,
        'predicted_rain': predicted_rain
    }

    return json.dumps(result), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(debug=True)