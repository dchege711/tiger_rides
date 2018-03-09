from mongo_db_client import tiger_rides_db
import trip_actions

users_db = tiger_rides_db("attendee_details")

def is_in_db(key_val_pair):
    """
    Check whether the given key value pair is in the users database.

    Args:

        `key_val_pair` :JSON:: The query to make to the database

    Returns:

        :bool:: True if the key value pair exists in the DB, False 
        otherwise.

    """
    if users_db.read(key_val_pair) is not None:
        return True 
    else:
        return False

def get_trips(user_id):
    """
    Get the trips associated with this user ID.

    Args:

        `user_id` :int:: The user's ID

    Returns:

        :JSON: Trip IDs of the trips owned and those joined.

    """
    
    user_profile = users_db.read({"user_id": user_id})
    trips = {}
    
    if user_profile is None:
        return trips
    
    trips["trips_owned"] = user_profile["trips_owned"]
    trips["trips_joined"] = user_profile["trips_joined"]
    
    return trips

def update_user_append(user_info):
    """
    Update information on a user's profile by appending to the
    values in the existing field.

    e.g. {"trips_owned": [1, 3, 4]} --> {"trips_owned": [1, 3, 4, 6]}

    Args:

        `user_info` :JSON:: Key-value pairs that need to be appended
        to the existing values. The user_id field must be included.

    Returns:

        :JSON:: If the overwrite was successful, `user_info` will not 
        be False

    """

    user_id = user_info.pop("user_id", None)
    query = {"user_id": user_id}
    user = users_db.read(query)

    if user is not None:
        try:
            for key in user_info:
                # This is an inplace function!
                user[key].append(user_info[key])
                user_info[key] = user[key]
                
            user_info["user_id"] = user_id 
            return update_user(user_info)

        except KeyError:
            return {"user_info": False}
    else:
        return {"user_info": False}

def update_user(new_user_info):
    """
    Update information on a user's profile by overwriting the
    values in the existing field.

    Args:

        `user_info` :JSON:: Key-value pairs that need to be appended
        to the existing values. The user_id field must be included.

    Returns:

        :JSON:: If the overwrite was successful, `user_info` will not 
        be False

    """
    query = {"user_id": new_user_info["user_id"]}
    update_results = {}
    
    result = users_db.update(query, new_user_info)
    if result.modified_count == 1:
        update_results["user_info"] = new_user_info
    else:
        update_results["user_info"] = False
            
    return update_results    
     
def get_user(key_val_pairs):
    """
    Get the user associated with the key_val_pairs.

    Args:

        `key_val_pairs` :JSON:: Identifier attributes of a user.

    Returns:

        :JSON:: The user's account details if the user exists. 

        `NoneType`: If the user doesn't exist.

    """
    return users_db.read(key_val_pairs)

def delete_user(user_id):
    """
    Delete a user's account from the Tiger Rides database.

    Args:

        `user_id` :(int):: The id of the user

    Returns:

        :int: 1 if user's account was successfully deleted
    """
    return users_db.delete({"user_id": user_id}).deleted_count

def register_user(user_details):
    """
    Register a new user into Tiger Rides.

    Args:

        `user_details` :(JSON):: Expected keys are `first_name, last_name, email_address, password`.

    Returns:

        :bool:: True if the registration was successful, false otherwise.

        :int:: The user's ID if registration was successful, false otherwise.

    """
    new_user_id = users_db.get_next_id()
    user_details["user_id"] = new_user_id
    user_details["trips_joined"] = []
    user_details["trips_owned"] = []
    insert_results = users_db.create(user_details)
    
    trip_info_in_registration = [
        "origin", "departure_date", "departure_time", "seats_available", "destination"
    ]
    trip_info = {}
    for key in trip_info_in_registration:
        value = user_details.pop(key, None)
        if value != "":
            trip_info[key] = value
    if len(trip_info) == 5:
        trip_info["trip_owner"] = new_user_id
        trip_actions.add_trip(trip_info)
    
    try:
        user_internal_id = insert_results.inserted_id
        return True, new_user_id 
    except Exception as e:
        print(e)
        return False, None
    
def main():
    new_user = {
        "first_name": "Test User",
        "last_name": "Why",
        "email_address": "unique1@gmail.com",
        "password": "this_is_long_enough",
        "origin": "Naples New",
        "destination": "Silicy",
        "departure_date": "2018-02-27",
        "departure_time": "12:00",
        "seats_available": 12
    }
    success, user_id = register_user(new_user)
    

if __name__ == "__main__":
    main()    
    
