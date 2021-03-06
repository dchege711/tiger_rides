from pprint import pprint

trips_from_given_state = {}

with open("./static/data/people_coming_randomized_names.csv") as people_coming:
    headers = people_coming.readline()
    for line in people_coming:
        name, number_of_people, city, state, state_abbr = line.strip().split(",")
        
        if state_abbr not in trips_from_given_state.keys():
            trips_from_given_state[state_abbr] = []
            
        trips_from_given_state[state_abbr].append([
            name, number_of_people, city, state, state_abbr
        ])
            
def get_travellers_from_state(state):
    assert isinstance(state, str), "State should be a string"
    state = state.upper()
    results = []
    try:
        for trip in trips_from_given_state[state]:
            results.append({
                "name": trip[0],
                "size": trip[1],
                "city": trip[2],
                "state_abbr": trip[4]
            })
        return results
    except KeyError:
        return results 
        
