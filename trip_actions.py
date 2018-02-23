from mongo_db_client import tiger_rides_db

trips_db = tiger_rides_db("trip_details")

def add_trip(trip_info):
    new_trip_id = trips_db.get_next_id()
    trip_info["trip_id"] = new_trip_id
    insert_results = trips_db.create(trip_info)
    trip_info["html_version"] = _convert_trip_info_to_html_row(trip_info) 
    try:
        trip_internal_id = insert_results.inserted_id
        return True, new_trip_id 
    except Exception as e:
        print(e)
        return False, None
    
def _convert_trip_info_to_html_row(trip_info):
    return ''.join([
        "<tr><td>#", trip_info["trip_id"], "</td>",
        "<td>", trip_info["origin"], "</td>",
        "<td>", trip_info["destination"], "</td>",
        "<td>", trip_info["departure_date"], "</td>", 
        "<td>", trip_info["departure_time"], "</td>", 
        "<td>", trip_info["seats_available"], "</td><tr>"
    ])
    
def get_trips(trip_ids):
    relevant_trips = []
    for trip_id in trip_ids:
        trip = trips_db.read({"trip_id": trip_id})
        if trip is not None:
            relevant_trips.append({
                "trip_id": trip["trip_id"],
                "as_a_table_row": trip["html_version"]
            })
    return relevant_trips
        
