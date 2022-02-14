from Realtor.constants import type_search, Counties


# Base URL from which the program can run for different cities and different states
BASE_URL = 'https://www.realtor.com/{search}/{city}_{code}'

# Function to determine which state needs to be scrape

def determine_city(State):
    
    aux = []
    
    for County in Counties:
        if County["State"] == State:
            aux.append(County)
            
    return aux

