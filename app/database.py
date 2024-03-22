"""
    Dumitrescu Alexandra 343 C1 - SPRC - December 2023
"""

from models import Tari, Orase, Temperaturi, db


def found_country_id(id : int) -> bool:
    # retrieves the list of all available countries with the given id
    country_ids = db.session.query(Tari.id).where(Tari.id == id).count()
    
    # if there is no country with the given id then return not found
    if country_ids == 0:
        return False
    
    return True

def found_city_id(id : int) -> bool:
    # retrieves the list of all available cities with the given id
    cities_ids = db.session.query(Orase.id).where(Orase.id == id).count()
    
    # if there is no city with the given id then return not found
    if cities_ids == 0:
        return False
    
    return True

def found_temperature_id(id: int) -> bool:
    # retrieves the list of all available temperatures with the given id
    temperature_ids = db.session.query(Temperaturi).where(Temperaturi.id == int(id)).count()
    
    # if there is no temperature with the given id then return not found
    if temperature_ids == 0:
        return False
    
    return True

def get_country_by_id(id : int) -> Tari:
    # query the database to obtain the corresponding country to the given id
    return db.session.query(Tari).where(Tari.id == int(id)).first()

def get_cities_by_country_id(id : int) -> Orase:
    # query the database to obtain the corresponding cities having the country specified by id
    return db.session.query(Orase).where(Orase.id_tara == int(id))

def get_city_by_id(id : int) -> Orase:
    # query the database to obtain the corresponding city to the given id
    return db.session.query(Orase).where(Orase.id == int(id)).first()

def get_temperature_by_id(id : int) -> Temperaturi:
    # query the database to obtain the corresponding temperature to the given id
    return db.session.query(Temperaturi).where(Temperaturi.id == int(id)).first()