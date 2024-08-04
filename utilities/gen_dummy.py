import random
import json
import base64
import time
import uuid
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import sys

# Configurations
FIREBASE_DB_URL = 'https://fish-farm-ed34b-default-rtdb.firebaseio.com'
TIME_INTERVAL = 5  # Interval in seconds between records
TEMPERATURE_MIN = 20  # Minimum temperature
TEMPERATURE_MAX = 30  # Maximum temperature
PH_MIN = 6.5  # Minimum pH
PH_MAX = 8.5  # Maximum pH
ANOMALY_CHANCE = 0.02  # Chance of an anomaly
ANOMALY_MAGNITUDE = 5  # Magnitude of temperature anomaly
PERSISTENCE = 0.8

# Load public key
def load_public_key(filename):
    with open(filename, "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read())

public_key = load_public_key("public_key.pem")

# Encrypt data using the public key
def encrypt_data(data, public_key):
    encrypted = public_key.encrypt(
        data.encode('utf-8'),
        padding.PKCS1v15()
    )
    return base64.b64encode(encrypted).decode('utf-8')

def generate_realistic_data(start_time, user_id):
    # Initial values
    temperature = random.uniform(TEMPERATURE_MIN, TEMPERATURE_MAX)
    ph = random.uniform(PH_MIN, PH_MAX)

    while True:
        data = {}
        timestamp = start_time  # Use the controlled timestamp

        # Simulate temperature fluctuations
        temperature = temperature * PERSISTENCE + random.uniform(-0.1, 0.1) * (1 - PERSISTENCE)
        temperature = max(min(temperature, TEMPERATURE_MAX), TEMPERATURE_MIN)
        temp1 = temperature + random.uniform(-0.1, 0.1)
        temp2 = temperature + random.uniform(-0.1, 0.1)

        # Simulate pH fluctuations
        ph += random.uniform(-0.1, 0.1)
        ph = max(min(ph, PH_MAX), PH_MIN)

        # Introduce occasional anomalies
        if random.random() < ANOMALY_CHANCE:
            temperature += random.choice([-ANOMALY_MAGNITUDE, ANOMALY_MAGNITUDE])
            temp1 += random.choice([-ANOMALY_MAGNITUDE, ANOMALY_MAGNITUDE])
            temp2 += random.choice([-ANOMALY_MAGNITUDE, ANOMALY_MAGNITUDE])

        record_key = str(uuid.uuid4())
        record = {
            "temperature": temperature,
            "temp1": temp1,
            "temp2": temp2,
            "ph": ph,
            "timestamp": timestamp.isoformat()
        }
        encrypted_record = encrypt_data(json.dumps(record), public_key)
        data[record_key] = encrypted_record

        # Sleep to simulate real-time data generation
        time.sleep(TIME_INTERVAL)

        ref = db.reference(f'sensorData/{user_id}')
        ref.update(data)
        print(f"Data successfully uploaded to Firebase for user: {user_id}")

        # Sleep to simulate real-time data generation
        time.sleep(TIME_INTERVAL)

        # Increment the timestamp
        start_time += timedelta(seconds=TIME_INTERVAL)

if __name__ == "__main__":
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('servicekey.json')  # Replace with the path to your service account key
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_DB_URL
    })

    user_id = sys.argv[1]
    start_time = datetime.now()

    generate_realistic_data(start_time, user_id)

