from mongo_db_client import tiger_rides_db
import trip_actions

user_db = tiger_rides_db("attendee_details")

def is_in_db(key_val_pair):
    if user_db.read(key_val_pair) is not None:
        return True 
    else:
        return False

def get_trips(user_id):
    
    search_result = user_db.read({"user_id": user_id})
    trips = {}
    
    if search_result is None:
        return trips
    
    trips["trips_owned"] = search_result["trips_owned"]
    trips["trips_joined"] = search_result["trips_joined"]
    
    return trips

def register_user(user_details):
    new_user_id = user_db.get_next_id()
    user_details["user_id"] = new_user_id
    
    trip_info_in_registration = [
        "origin", "departure_date", "departure_time", "seats_available"
    ]
    trip_info = {}
    for key in trip_info_in_registration:
        value = user_details.pop(key, None)
        if value != "":
            trip_info[key] = value
    
    if len(trip_info) != 0:
        trip_id = trip_actions.add_trip(trip_info)
        user_details["trips_owned"] = [trip_id]
        
    user_details["trips_joined"] = []
    
    insert_results = user_db.create(user_details)
    try:
        user_internal_id = insert_results.inserted_id
        return True, new_user_id 
    except Exception as e:
        print(e)
        return False, None
    
    
    
    
