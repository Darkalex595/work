from audioop import add
from Realtor.constants import States, type_search
import sys

def transform_city(city):
    aux_city = city.replace(" ", "-")
    return aux_city

def transformLink(link, type_build):
    position = link.find("/pg")
    
    return link[:position] + "/" + "type-" + type_build + link[position:]

def getTypeSearch(search):
    
    if search.find("rental") != -1:
        return type_search[1]
    elif search.find("buy") != -1:
        return type_search[0]
    else:
        sys.exit("Type of search not available")

def getBuildType(search):
    
    if search.find("condo") != -1:
        return "condo"
    elif search.find("apartment") != -1:
        return "apartments"
    else:
        sys.exit("Type of building not available")
        
    
        
        
# Function to determine which state needs to be scrape
def determine_city(selected_state, selected_county,selected_city):

    cities = []
    counties = []
    
    aux_state = None
    aux_county = None
    aux_city = []
    

    for state in States:
        if state["Name"] == selected_state:
            aux_state = state
            break
        
    if aux_state != None:
        counties = aux_state["Counties"]
        
        for county in counties:
            if county["County"] == selected_county:
                aux_county = county
                break
        
        if aux_county != None:
            cities = aux_county["Cities"]
            
            if selected_city == "all":
                for city in cities:
                    aux_city.append(city)
                
                if len(aux_city) > 0:
                    return aux_city
                else:
                    sys.exit("Cities not available")
            else:
                for city in cities:
                    if city == selected_city:
                        aux_city.append(city)
                        break
                
                if len(aux_city) > 0:
                    return aux_city
                else:
                    sys.exit("City not available")
            
        else:
            sys.exit("County not available")
        
    else:
        sys.exit("State not available") 
    
    return aux_city

    
def getCode(state):
    for aux_state in States:
        if aux_state["Name"] == state:
            return aux_state["Code"]
        
    return None


def getUseState(details):
    
    use_state = "N/A"
    
    for dets in details:
        if dets["parent_category"] == "Features" and dets["category"] == "Building and Construction":
            description = dets["text"]
            
    for desc in description:
        if desc.find("Year Built Details") != -1:
            use_state = desc.replace("Year Built Details: ", "")
        
            
    return use_state


def getAddress(s_number, s_direction, s_name, s_suffix, s_post_direction, postal_code):
    
    address = ""
    
    if s_number != None:
        address = address + " " + s_number
    else:
        print("Street Number not available")
    
    if s_direction != None:
        address = address + " " + s_direction
    else:
        print("Street Direction not available")
    
    if s_name != None:
        address = address + s_name
    else:
        print("Street Name not available")
    
    if s_suffix != None:
        address = address + " " + s_suffix
    else:
        print("Street Suffix not available") 
        
    if s_post_direction != None:  
        address = address + " " + s_post_direction
    else:
        print("Street Post Direction not available")  
        
    if postal_code != None:
        postal_code = address + " ," + postal_code
    else:
        print("Postal Code not available")
    
    
    return address

def getTotalBaths(full_baths, half_baths):
    baths = full_baths
    
    baths = baths + (half_baths*0.5)
    
    return baths