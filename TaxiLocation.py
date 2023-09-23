import json
import boto3

# Initialize DocumentDB client
client = boto3.client('docdb')

def taxi_location(event, context):
    # Extract taxi location data from the event
    taxi_id = event['body']['taxi_id']
    location = event['body']['location']
    
    # Store the updated location in DocumentDB
    client.update_one(
        {"taxi_id": taxi_id},
        {"$set": {"location": location}},
        upsert=True
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Location updated successfully!')
    }
