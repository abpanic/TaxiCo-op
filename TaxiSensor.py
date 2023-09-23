import requests
import random
import threading
import logging
import pymongo
from pymongo import MongoClient
import time

# MongoDB Connection
MONGODB_CONNECTION_STRING = '<YOUR_MONGODB_CONNECTION_STRING>'
client = MongoClient(MONGODB_CONNECTION_STRING)
taxi_collection = client['TaxiCoopDB']['Taxis']
location_collection = client['TaxiCoopDB']['location']

# Taxi Names and Types for Simulation
taxi_names = ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot"]
taxi_types = ["Luxury", "Deluxe", "Economy"]

# Define the lat/long box for the service area
LAT_MIN, LAT_MAX = 40.0, 41.0
LONG_MIN, LONG_MAX = -74.0, -73.0

# Setup logging
logging.basicConfig(level=logging.INFO)

# Number of taxis to simulate
NUM_TAXIS = 50

# Base URL for the API that will ingest taxi location updates
#API_URL = "https://your-api-endpoint/taxi/updateLocation"

# Define the lat/long box for the service area
LAT_MIN, LAT_MAX = 40.0, 41.0
LONG_MIN, LONG_MAX = -74.0, -73.0

def simulate_taxi_movement(taxi_id):
    # Generate a random starting point within the service area
    lat = random.uniform(LAT_MIN, LAT_MAX)
    long = random.uniform(LONG_MIN, LONG_MAX)
    
    while True:
        # Simulate taxi movement by adjusting lat/long slightly
        lat += random.uniform(-0.001, 0.001)
        long += random.uniform(-0.001, 0.001)
        
        # Ensure the taxi stays within the service area
        lat = max(min(lat, LAT_MAX), LAT_MIN)
        long = max(min(long, LONG_MAX), LONG_MIN)
        
        # Send the updated location to the API
        payload = {
            "taxi_id": taxi_id,
            "location": {
                "type": "Point",
                "coordinates": [long, lat]
            }
        }
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            logging.info(f"Taxi {taxi_id} updated to {lat}, {long}. Response: {response.text}")
        except requests.RequestException as e:
            logging.error(f"Error updating taxi {taxi_id}: {e}")
        
        # Wait for a minute before the next update
        time.sleep(60)

# Simulate movement for all taxis concurrently
threads = []
for i in range(NUM_TAXIS):
    t = threading.Thread(target=simulate_taxi_movement, args=(i,))
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()
