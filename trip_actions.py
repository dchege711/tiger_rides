from mongo_db_client import tiger_rides_db

trips_db = tiger_rides_db("trip_details")

def add_trip(trip_info):
    new_trip_id = trips_db.get_next_id()
    trip_info["trip_id"] = new_trip_id
    insert_results = trips_db.create(user_details)
    try:
        trip_internal_id = insert_results.inserted_id
        return True, new_trip_id 
    except Exception as e:
        print(e)
        return False, None
