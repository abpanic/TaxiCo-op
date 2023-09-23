#Taxi Registraion
#User Registration
#User requesting for Taxi
#trip fullfillment: informing the DB that the taxi is booked

#username=abhilashpanicker111
#password=VdRIDZrRqtNxD2ST


import json
import pymongo

# Initialize DocumentDB (MongoDB) client
client = pymongo.MongoClient("your_documentdb_connection_string")
db = client["your_database_name"]
taxis_collection = db["taxis"]

def user_registration(event, context):
    # Extract user data from the event
    user_id = event['body']['user_id']
    user_name = event['body']['name']
    
    # Store the user details in DocumentDB
    client.insert_one(
        {"user_id": user_id, "name": user_name}
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('User registered successfully!')
    }

def taxi_registration(event, context):
    # Extract taxi data from the event
    taxi_id = event['body']['taxi_id']
    taxi_name = event['body']['name']
    taxi_type = event['body']['type']
    
    # Store the taxi details in DocumentDB
    client.insert_one(
        {"taxi_id": taxi_id, "name": taxi_name, "type": taxi_type}
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Taxi registered successfully!')
    }

def user_taxi_request(event, context):
    # Extract user request data from the event
    user_id = event['body']['user_id']
    user_location = event['body']['location']
    taxi_type_preference = event['body']['type_preference']
    
    # Query DocumentDB to find the nearest available taxis based on user location and type preference
    if taxi_type_preference == "All":
        query = {'location': {"$near": user_location}, 'status': 'available'}
    else:
        query = {'location': {"$near": user_location}, 'type': taxi_type_preference, 'status': 'available'}
    
    nearest_taxis = list(client.find(query).limit(5))  # Get top 5 nearest taxis
    
    return {
        'statusCode': 200,
        'body': json.dumps({'nearest_taxis': nearest_taxis})
    }

def trip_fullfillment(event, context):
    # Extract data from the event
    user_id = event['body']['user_id']
    selected_taxi_id = event['body']['selected_taxi_id']
    
    # Mark the taxi as unavailable in DocumentDB
    result = client.update_one(
        {"taxi_id": selected_taxi_id, "status": "available"},
        {"$set": {"status": "unavailable"}}
    )
    
    if result.modified_count == 0:
        return {
            'statusCode': 400,
            'body': json.dumps('Taxi is already booked or not found!')
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps('Trip started successfully!')
    }