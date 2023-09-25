# TaxiCo-op
## TaxiSensor.py
Explanation:
##### 1. User Registration and Trip Handling:

The register_user, is_user_registered, handle_trip_request, and end_trip functions are used for user registration and handling trip requests.
handle_trip_request checks if the user is registered and finds a suitable taxi for the trip.
end_trip ends a trip for a user by updating the taxi_collection and user_collection.
##### 2. Finding a Suitable Taxi (find_suitable_taxi function):

This function is a placeholder for your logic to find a suitable taxi.
Currently, it just finds the first unbooked taxi.
##### 3.Taxi Simulation (taxi_simulation function):

This function is the main loop for taxi simulation.
It fetches all taxis from the taxi_collection and simulates movement for taxis that have alwaysMoving set to 'T'.
It then updates the taxi location in the taxi_collection.
The calculate_next_step function calculates the next step towards the target location for a taxi.
The simulate_taxi_movement function fetches the target location for a taxi from the location_collection and calculates the next location. It then updates the taxi's location.

##### 4.Starting the Taxi Simulation:

The taxi_simulation function is called to start the taxi simulation.

##### 3. Taxi Data Generation:

The LAT_MIN, LAT_MAX, LONG_MIN, and LONG_MAX constants define the boundaries for the taxi service area.
taxi_names and taxi_types are lists used to randomly assign names and types to taxis.
A loop generates initial data for 50 taxis and inserts them into the taxi_collection in MongoDB.
Location Collection Population:

The create_and_populate_location_collection function clears the location_collection and populates it with random target locations for each taxi.

#### 4. Location Collection Population:

The create_and_populate_location_collection function clears the location_collection and populates it with random target locations for each taxi.
Taxi Movement Simulation:

The calculate_next_step function calculates the next step towards the target location for a taxi.
The simulate_taxi_movement function fetches the target location for a taxi from the location_collection and calculates the next location. It then updates the taxi's location.
