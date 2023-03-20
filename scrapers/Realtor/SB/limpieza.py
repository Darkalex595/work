from distutils.log import info


def eliminate_b(info_json):
    return info_json.replace("b'", "")

def eliminate_backslash(info_json):
    return info_json.replace('\\', '')

def eliminate_firstScript(info_json):
    return info_json.replace('<script id="__NEXT_DATA__" type="application/json">', '')

def eliminate_lastScript(info_json):
    return info_json.replace('</script>', "")

def eliminate_lastChar(info_json):
    return info_json.rstrip(info_json[-1])

def eliminate_outer(info_json):
    return info_json.replace('{"scripts": "', '')

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