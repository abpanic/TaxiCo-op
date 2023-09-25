import os
import pymongo
import random
import time
from pymongo import MongoClient

# MongoDB Connection
MONGODB_CONNECTION_STRING = 'mongodb://localhost:27017/'
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client['TaxiCoopDB']
taxi_collection = db['Taxis']
location_collection = db['location']
user_collection = db['users']  

# Define the lat/long box for the service area
LAT_MIN, LAT_MAX = 40.0, 41.0
LONG_MIN, LONG_MAX = -74.0, -73.0

# Taxi Names and Types for Simulation
taxi_names = ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliet"]
taxi_types = ["Luxury", "Deluxe", "Economy"]

# Generate initial taxi data for 50 taxis
taxis = []
for i in range(50):
    taxi = {
        'name': random.choice(taxi_names) + str(i),
        'number': "MH" + str(random.randint(1000, 9999)),
        'type': random.choice(taxi_types),
        'alwaysMoving': random.choice(['T', 'F']),
        'Zone': 'Mumbai',
        'booked': random.choice(['Y', 'N']),
        'location': {
            'type': "Point",
            'coordinates': [random.uniform(LAT_MIN, LAT_MAX), random.uniform(LONG_MIN, LONG_MAX)]
        }
    }
    taxis.append(taxi)

# Insert initial taxi data into MongoDB
taxi_collection.insert_many(taxis)

# Create and populate the location collection with dummy target locations
def create_and_populate_location_collection():
    location_collection.delete_many({})
    taxis = taxi_collection.find({})
    for taxi in taxis:
        target_location = {
            "type": "Point",
            "coordinates": [random.uniform(LAT_MIN, LAT_MAX), random.uniform(LONG_MIN, LONG_MAX)]
        }
        location_collection.insert_one({
            "taxi_id": taxi["_id"],
            "target_location": target_location
        })

create_and_populate_location_collection()

# Define a function to calculate the next step towards the target
def calculate_next_step(current, target, step_size=0.001):
    lat_direction = 1 if target[0] > current[0] else -1
    long_direction = 1 if target[1] > current[1] else -1
    new_lat = current[0] + (lat_direction * step_size)
    new_long = current[1] + (long_direction * step_size)
    return [new_lat, new_long]

# Simulate taxi movement within the defined boundaries
def simulate_taxi_movement(taxi):
    target_location_entry = location_collection.find_one({"taxi_id": taxi["_id"]})
    if not target_location_entry:
        return taxi
    target_location = target_location_entry["target_location"]["coordinates"]
    current_location = taxi["location"]["coordinates"]
    next_location = calculate_next_step(current_location, target_location)
    taxi['location']['coordinates'] = next_location
    return taxi

# Register a new user
def register_user(user_details):
    user_collection.insert_one(user_details)

# Check if a user is registered
def is_user_registered(user_id):
    user = user_collection.find_one({"_id": user_id})
    return user is not None

# Handle a trip request
def handle_trip_request(user_id, source, destination):
    if not is_user_registered(user_id):
        print(f"User with ID {user_id} is not registered.")
        return

    # Find a suitable taxi for the trip
    taxi = find_suitable_taxi(source)
    if taxi:
        taxi_collection.update_one({'_id': taxi['_id']}, {'$set': {'booked': 'Y', 'destination': destination}})
        user_collection.update_one({'_id': user_id}, {'$set': {'current_trip': taxi['_id']}})

# End a trip
def end_trip(user_id):
    user = user_collection.find_one({"_id": user_id})
    if user and 'current_trip' in user:
        taxi_id = user['current_trip']
        taxi_collection.update_one({'_id': taxi_id}, {'$set': {'booked': 'N', 'destination': None}})
        user_collection.update_one({'_id': user_id}, {'$unset': {'current_trip': ""}})

# Find a suitable taxi
def find_suitable_taxi(source):
    # This is a placeholder. Implement your logic to find a suitable taxi.
    return taxi_collection.find_one({"booked": "N"})

# Main loop for taxi simulation
def taxi_simulation():
    while True:
        # Simulate movement for all taxis
        taxis = taxi_collection.find({})
        for taxi in taxis:
            if taxi['alwaysMoving'] == 'T':
                updated_taxi = simulate_taxi_movement(taxi)
                taxi_collection.update_one({'_id': updated_taxi['_id']}, {'$set': {'location': updated_taxi['location']}})
        time.sleep(60)

# Start the taxi simulation
taxi_simulation()
