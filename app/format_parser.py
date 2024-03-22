"""
    Dumitrescu Alexandra 343 C1 - SPRC - Dec 2023
"""

import json
from datetime import datetime

# Specific http requests status codes
ERROR_BAD_FORMAT    = 400
ERROR_NOT_FOUND     = 404
ERROR_CONFLICT      = 409
SUCCESS             = 200
SUCCESS_INSERTED    = 201



# Method for checking if the received id can be casted to a valid float
def is_valid_float(id) -> bool:
    try:
        float(id)
    except:
        return False
    return True



# Method for checking if the received id can be casted to a valid int
def is_valid_id(id) -> bool:
    try:
        int(id)
    except:
        return False
    return True



# Method for checking if the received country has valid format       
def is_correct_country_format(country) -> bool:
    # dump received JSON info
    country_loaded = json.dumps(country)
    
    # check if the fields "nume", "lat", "lon" exist in the received JSON
    if not "nume" in country_loaded or not "lat" in country_loaded or not "lon" in country_loaded:
        return False
    
    # check if lat and lon are valid float numbers
    try:
        float(country["lat"])
        float(country["lon"])
    except:
        return False
    
    # check if nume is a valid string
    if not isinstance(country["nume"], str):
        return False
    
    return True



# Method for checking if the received country has valid format
# In the PUT request, the country JSON has an additional field "id"       
def is_correct_country_format_put(country) -> bool:
    # dump received JSON info
    country_loaded = json.dumps(country)
    
    # check if the fields "nume", "lat", "lon", "id" exist in the received JSON
    if not "nume" in country_loaded or not "lat" in country_loaded or not "lon" in country_loaded or not "id" in country_loaded:
        return False
    
    # check if lat and lon are valid float numbers and id valid int number
    try:
        int(country["id"])
        float(country["lat"])
        float(country["lon"])
    except:
        return False

    # check if nume is a valid string
    if not isinstance(country["nume"], str):
        return False
        
    return True



# Method for checking city format
def is_correct_city_format(city) -> bool:
    # dump received JSON info
    city_loaded = json.dumps(city)

    # check if the fields "idTara", "lat", "lon", "nume" exist in the received JSON
    if not "idTara" in city_loaded or not "nume" in city_loaded or not "lat" in city_loaded or not "lon" in city_loaded:
        return False
    
    # check if lat and lon are valid float numbers and idTara valid int number
    try:
        int(city["idTara"])
        float(city["lat"])
        float(city["lon"])
    except:
        return False
    
    return True



# Method for checking city format for put requests
def is_correct_city_format_put(city) -> bool:
    # dump received JSON info
    city_loaded = json.dumps(city)

    # check if the fields "id", "idTara", "lat", "lon", "nume" exist in the received JSON
    if not "idTara" in city_loaded or not "nume" in city_loaded or not "lat" in city_loaded or not "lon" in city_loaded or not "id" in city_loaded:
        return False
    
    # check if lat and lon are valid float numbers and id and idTara valid int number
    try:
        int(city["id"])
        int(city["idTara"])
        float(city["lat"])
        float(city["lon"])
    except:
        return False
    
    return True



# Method for checking temperature format
def is_correct_temperature_format(temperature) -> bool:
    # dump received JSON info
    temperature_loaded = json.dumps(temperature)
    
    # check if the fields "idOras", "valoare" exist in the received JSON
    if not "idOras" in temperature_loaded or not "valoare" in temperature_loaded:
        return False
    
    # check if valoare is valid float number and id valid int number
    try:
        int(temperature["idOras"])
        float(temperature["valoare"])
    except:
        return False
    
    return True



# Method for checking temperature format for PUT requests
def is_correct_temperature_format_put(temperature) -> bool:
    # dump received JSON info
    temperature_loaded = json.dumps(temperature)
    
    # check if the fields "idOras", "valoare", "id" exist in the received JSON
    if not "idOras" in temperature_loaded or not "valoare" in temperature_loaded or not "id" in temperature_loaded:
        return False
    
    # check if valoare is valid float number and id and idOras valid int numbers
    try:
        int(temperature["id"])
        int(temperature["idOras"])
        float(temperature["valoare"])
    except:
        return False
    
    return True



# Method for checking date format
def check_date_format(date) -> bool:
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except:
        return False
    return True

# Method for checking in the put requests if the received id in the JSON body is the same with the parameter received
def is_consistent_id(given_id : int, expected_id : int) -> bool:
    if given_id == expected_id:
        return True
    return False