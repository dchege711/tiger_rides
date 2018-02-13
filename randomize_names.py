import filter_trips
from random import sample, shuffle

data_with_real_names = filter_trips.trips_from_given_state

def _fetch_names(file_name):
    names = []
    with open("./static/data/" + file_name, "r") as list_of_names:
        for items in list_of_names:
            names.append(items.split()[0].title())
    shuffle(names)
    return names

# Read in all the random names 
male_first_names = _fetch_names("male_first_names.txt")
female_first_names = _fetch_names("female_first_names.txt")
last_names = _fetch_names("last_names_census.txt")

next_is_male = True
male_index, female_index, lastname_index = 0, 0, 0

def _helper_randomize_name(name):
    global next_is_male, male_index, female_index, lastname_index
    new_name = []
    insert_last_name = False
    for sub_name in name.split():
        if sub_name == "with" or sub_name == "and":
            new_name.append(sub_name)
            insert_last_name = False
        elif insert_last_name:
            new_name.append(last_names[lastname_index])
            lastname_index += 1
            insert_last_name = False
        else:
            new_name.append(_get_either_male_or_female_name())
            insert_last_name = True
            
    return " ".join(new_name)

def _get_either_male_or_female_name():
    global next_is_male, male_index, female_index
    if next_is_male:
        result = male_first_names[male_index]
        male_index += 1
    else:
        result = female_first_names[female_index]
        female_index += 1
    next_is_male = not next_is_male
    return result

def randomize_names():
    output_file = open("./static/data/people_coming_randomized_names.csv", "w")
    for key in data_with_real_names.keys():
        for group in data_with_real_names[key]:
            new_name = _helper_randomize_name(group[0])
            output_file.write(",".join([
                new_name, group[1], group[2], group[3], group[4] + "\n"
            ]))

if __name__ == "__main__":
    randomize_names()
                
