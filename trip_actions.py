from mongo_db_client import tiger_rides_db

trips_db = tiger_rides_db("trip_details")

def add_trip(trip_info):
    new_trip_id = trips_db.get_next_id()
    trip_info["trip_id"] = new_trip_id
    trip_info["html_version"] = _convert_trip_info_to_html_row(trip_info)
    
    insert_results = trips_db.create(trip_info)
    try:
        trip_internal_id = insert_results.inserted_id
        return True, new_trip_id 
    except Exception as e:
        print(e)
        return False, None
    
def _convert_trip_info_to_html_row(trip_info):
    return ''.join([
        "<tr><td>#", str(trip_info["trip_id"]), "</td>",
        "<td>", trip_info["origin"], "</td>",
        "<td>", trip_info["destination"], "</td>",
        "<td>", trip_info["departure_date"], "</td>", 
        "<td>", trip_info["departure_time"], "</td>", 
        "<td>", str(trip_info["seats_available"]), "</td><tr>"
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

def main():
    test_trip = {
        "origin": "Omaha",
        "departure_date": "2018-02-24",
        "departure_time": "12:20",
        "seats_available": "2",
        "destination": "Princeton University",
        "trip_id": 2
    }
    print(_convert_trip_info_to_html_row(test_trip))

if __name__ == "__main__":
    main()
        
