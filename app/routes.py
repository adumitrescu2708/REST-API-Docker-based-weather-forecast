"""
    Dumitrescu Alexandra 343 C1 - SPRC - December 2023
"""
from flask import request, jsonify, Response
import datetime
from sqlalchemy import and_
import format_parser
from models import Tari, Orase, Temperaturi, db
import database

# method called in main method for setting the 3 main routes
def set_routes(app):
    set_country_API(app)
    set_city_API(app)
    set_temperature_API(app)
    

def set_country_API(app):
    @app.route("/api/countries", methods=["POST"])
    def post_country():
        # get country JSON format
        country = request.get_json()
        
        # check if received data respects expected format
        if not format_parser.is_correct_country_format(country):
            return Response(status=format_parser.ERROR_BAD_FORMAT)
        
        # create a new entry
        country = Tari(country['nume'],
                       float(country['lat']),
                       float(country['lon']))
        
        # add a new entry, throw ERROR_CONFLICT in case of database conflict
        try:
            db.session.add(country)
            db.session.commit()
        except:
            return Response(status=format_parser.ERROR_CONFLICT)

        return jsonify({"id" : country.id}), format_parser.SUCCESS_INSERTED



    @app.route("/api/countries", methods=["GET"])
    def get_countries():
        # obtain all entries in database
        list_of_countries = Tari.query.all()
        
        # create a JSON entry for each retrieved country
        json_response = []
        for x in list_of_countries:
            data = {}
            
            data["id"]      = x.id
            data["nume"]    = x.nume_tara
            data["lon"]     = x.longitudine
            data["lat"]     = x.latitudine
            
            json_response.append(data)

        return json_response, format_parser.SUCCESS

    @app.route("/api/countries/<modify_id>", methods=["PUT"])
    def modify_country(modify_id):
        # get received JSON info
        modify = request.get_json()
        
        # check if the JSON corresponds to the expected country format
        if not format_parser.is_correct_country_format_put(modify):
            return Response(status=format_parser.ERROR_BAD_FORMAT)
        
        # check if the parameter id is a valid one - should be int number
        if not format_parser.is_valid_id(modify_id):
            return Response(status=format_parser.ERROR_BAD_FORMAT)
        
        # check if the received id in the JSON is the same with the parameter
        if not format_parser.is_consistent_id(int(modify["id"]), int(modify_id)):
            return Response(status=format_parser.ERROR_BAD_FORMAT)

        # throw NOT_FOUND
        if not database.found_country_id(int(modify_id)):
            return Response(status=format_parser.ERROR_NOT_FOUND)

        # query db to obtain corresponding country
        country_database = database.get_country_by_id(int(modify_id))
        
        # set new attributes to the corresponding entry
        try:
            setattr(country_database, 'nume_tara', modify['nume'])
            setattr(country_database, 'latitudine', float(modify['lat']))
            setattr(country_database, 'longitudine', float(modify['lon']))
            db.session.commit()
        except:
            return Response(status=format_parser.ERROR_CONFLICT)

        return Response(status=format_parser.SUCCESS)


    @app.route("/api/countries/<delete_id>", methods=["DELETE"])
    def delete_country(delete_id):
        # check if the parameter id is a valid one - should be int number
        if not format_parser.is_valid_id(delete_id):
            return Response(status=format_parser.ERROR_BAD_FORMAT)
        
        # throw NOT_FOUND
        if not database.found_country_id(int(delete_id)):
            return Response(status=format_parser.ERROR_NOT_FOUND)
        
        # delete the corresponding entry
        db.session.query(Tari).where(Tari.id == int(delete_id)).delete()
        db.session.commit()
        
        return Response(status=format_parser.SUCCESS)
        
        
        
def set_city_API(app):
    @app.route("/api/cities", methods=["POST"])
    def add_city():
        # retieve given JSON data
        body = request.get_json()
        
        # check if the JSON data has the expected format
        if not format_parser.is_correct_city_format(body):
            return Response(status=format_parser.ERROR_BAD_FORMAT)
        
        # throw NOT_FOUND in case of a non existent country
        if not database.found_country_id(int(body['idTara'])):
            return Response(status=format_parser.ERROR_NOT_FOUND)
        
        # create a new entry
        city = Orase(int(body['idTara']), body['nume'], float(body['lat']), float(body['lon']))
        
        # commit the new country to the database
        try:
            db.session.add(city)
            db.session.commit()            
        except:
            return Response(status=format_parser.ERROR_CONFLICT)
        
        return jsonify({"id": city.id}), format_parser.SUCCESS_INSERTED
    
    
    @app.route("/api/cities", methods=["GET"])
    def get_city():
        # obtain all cities in the database
        list_of_cities = Orase.query.all()
        
        # create a JSON entry for each retrieved city
        json_response = []
        for city in list_of_cities:
            data = {}
            
            data["id"]      = city.id
            data["idTara"]  = city.id_tara
            data["nume"]    = city.nume_oras
            data["lat"]     = city.latitudine
            data["lon"]     = city.longitudine
            
            json_response.append(data)
            
        return json_response, format_parser.SUCCESS
    
    
    @app.route("/api/cities/country/<id_Tara>", methods=["GET"])
    def get_city_by_country(id_Tara):
        # retrieve all cities from the database having the parent country corresponding to the given id
        list_of_cities = database.get_cities_by_country_id(int(id_Tara))
        
        # create a JSON entry for each retrieved city
        json_response = []
        for city in list_of_cities:
            data = {}
            
            data["id"]      = city.id
            data["idTara"]  = city.id_tara
            data["nume"]    = city.nume_oras
            data["lat"]     = city.latitudine
            data["lon"]     = city.longitudine
            
            json_response.append(data)
        return json_response, format_parser.SUCCESS        
        
        
    @app.route("/api/cities/<id>", methods=["PUT"])    
    def put_city(id):
        # get received JSON info
        modify = request.get_json()
        
        # check if the JSON corresponds to the expected city format
        if not format_parser.is_correct_city_format_put(modify):
            return Response(status=format_parser.ERROR_BAD_FORMAT)
        
        # check if the parameter id is a valid one - should be int number
        if not format_parser.is_valid_id(id):
            return Response(status=format_parser.ERROR_BAD_FORMAT)
        
        # check if the received id in the JSON is the same with the parameter
        if not format_parser.is_consistent_id(int(modify["id"]), int(id)):
            return Response(status=format_parser.ERROR_BAD_FORMAT)
        
        # check if NOT_FOUND
        if not database.found_city_id(int(id)) or not database.found_country_id(int(modify['idTara'])):
            return Response(status=format_parser.ERROR_NOT_FOUND)
        
        # retrieve the city having the corresponding id from database
        city_database = database.get_city_by_id(int(id))
        
        # set new attributes to the corresponding entry        
        try:
            setattr(city_database, 'id_tara', int(modify['idTara']))
            setattr(city_database, 'nume_oras', modify['nume'])
            setattr(city_database, 'latitudine', float(modify['lat']))
            setattr(city_database, 'longitudine', float(modify['lon']))
            db.session.commit()
        except:
            return Response(status=format_parser.ERROR_CONFLICT)
        
        return Response(status=format_parser.SUCCESS)
    
    @app.route("/api/cities/<id>", methods=["DELETE"])    
    def delete_city(id):
        # check if the parameter id is a valid one - should be int number
        if not format_parser.is_valid_id(id):
            return Response(status=format_parser.ERROR_BAD_FORMAT)
        
        # check NOT_FOUND
        if not database.found_city_id(int(id)):
            return Response(status=format_parser.ERROR_NOT_FOUND)
        
        # delete the corresponding entry
        db.session.query(Orase).where(Orase.id == int(id)).delete()
        db.session.commit()
        
        return Response(status=format_parser.SUCCESS)    


def set_temperature_API(app):
    @app.route("/api/temperatures", methods=["POST"])    
    def post_temperature():
        # get temperature JSON format
        body = request.get_json()
        
        # check if received data respects expected format
        if not format_parser.is_correct_temperature_format(body):
            return Response(status=format_parser.ERROR_BAD_FORMAT)
        
        # check if the corresponding city exists
        if not database.found_city_id(int(body["idOras"])):
            return Response(status=format_parser.ERROR_NOT_FOUND)
        
        # create a new temperature
        temperature = Temperaturi(float(body["valoare"]), int(body["idOras"]))
        
        # add a new entry, throw ERROR_CONFLICT in case of database conflict
        try:
            db.session.add(temperature)
            db.session.commit()            
        except:
            return Response(status=format_parser.ERROR_CONFLICT)
        
        return jsonify({"id": temperature.id}), format_parser.SUCCESS_INSERTED
    
    
    
    @app.route("/api/temperatures", methods=["GET"])    
    def get_temperature():
        # retrieve the arguments
        latitudine  = request.args.get("lat")
        longitudine = request.args.get("lon")
        start       = request.args.get("from")
        end         = request.args.get("until")
        
        # check if there is a start date and if it has a correct format
        if start and not format_parser.check_date_format(start):
            return [], format_parser.SUCCESS

        # check if there is an end date and if it has a correct format
        if end and not format_parser.check_date_format(end):
            return [], format_parser.SUCCESS
        
        # treat the get_all case, where all arguments are null        
        if not latitudine and not longitudine and not start and not end:
            # retrieve all temperatures from the database
            list_of_temperatures = Temperaturi.query.all()
            
            # create a JSON entry for each retrieved temperature
            json_response = []
            for temperature in list_of_temperatures:
                data = {}
                
                data["id"]          = temperature.id
                data["valoare"]     = temperature.valoare
                data["timestamp"]   = temperature.timestamp
                data["oras_id"]     = temperature.id_oras
                
                
                json_response.append(data)
            return json_response, format_parser.SUCCESS 

        # gather all conditions in a list
        conditions = []
        
        # 'latitudine' parameter condition
        if latitudine:
            latitudine_condition = Orase.latitudine == float(latitudine)
            conditions.append(latitudine_condition)
        
        # 'longitudine' parameter condition
        if longitudine:
            longitudine_condition = Orase.longitudine == float(longitudine)
            conditions.append(longitudine_condition)
        
        # start date parameter condition
        if start:
            start_condition = Temperaturi.timestamp > datetime.datetime.strptime(start, "%Y-%m-%d")
            conditions.append(start_condition)
        
        # end date parameter condition
        if end:
            end_condition = Temperaturi.timestamp < datetime.datetime.strptime(end, "%Y-%m-%d")
            conditions.append(end_condition)
            
        # apply an and function between all conditions
        final_condition = conditions[0]
        for condition in conditions[1:]:
            final_condition = and_(final_condition, condition)
        
        # query the database to retrieve the temperatures with all given restrictions
        list_of_temperatures = db.session.query(Temperaturi.id, Temperaturi.valoare, Temperaturi.timestamp).select_from(
            Temperaturi).join(Orase, Temperaturi.id_oras == Orase.id).where(final_condition)
        
        # create a JSON entry for each retrieved temperature
        json_response = []
        for temperature in list_of_temperatures:
            data = {}
            
            data["id"]          = temperature.id
            data["valoare"]     = temperature.valoare
            data["timestamp"]   = temperature.timestamp
            
            json_response.append(data)     
        
        return json_response, format_parser.SUCCESS
           
        
    @app.route("/api/temperatures/cities/<id_city>", methods=["GET"])
    def get_temperature_cities(id_city):
        # retrieve the arguments
        start       = request.args.get("from")
        end         = request.args.get("until")
        
        # gather all conditions in a list
        conditions = []
        
        # check if there is a start date and if it has a correct format
        if start and not format_parser.check_date_format(start):
            return [], format_parser.SUCCESS
        
        # check if there is an end date and if it has a correct format
        if end and not format_parser.check_date_format(end):
            return [], format_parser.SUCCESS
        
        final_condition = Orase.id == int(id_city)
    
        # # start date parameter condition
        if start:
            final_condition = and_(Temperaturi.timestamp > datetime.datetime.strptime(start, "%Y-%m-%d"), final_condition)
        
        # # end date parameter condition
        if end:
            final_condition = and_(Temperaturi.timestamp < datetime.datetime.strptime(end, "%Y-%m-%d"), final_condition)
        
        # query the database to retrieve the temperatures with all given restrictions
        list_of_temperatures = db.session.query(Temperaturi.id, Temperaturi.valoare, Temperaturi.timestamp).select_from(
            Temperaturi).join(Orase, Temperaturi.id_oras == Orase.id).where(final_condition)
        
         # create a JSON entry for each retrieved temperature
        json_response = []
        for temperature in list_of_temperatures:
            data = {}
            
            data["id"]          = temperature.id
            data["valoare"]     = temperature.valoare
            data["timestamp"]   = temperature.timestamp
            
            json_response.append(data)
        
        return json_response, format_parser.SUCCESS
    
    @app.route("/api/temperatures/countries/<id_country>", methods=["GET"])    
    def get_temperature_country(id_country):
        # retrieve the arguments
        start       = request.args.get("from")
        end         = request.args.get("until")
            
        # check if there is a start date and if it has a correct format
        if start and not format_parser.check_date_format(start):
            return [], format_parser.SUCCESS
        
        # check if there is an end date and if it has a correct format
        if end and not format_parser.check_date_format(end):
            return [], format_parser.SUCCESS
        
        # in final_restriction we add all restrictions
        final_condition = (Orase.id_tara == int(id_country))
        
        # start date parameter condition
        if start:
            final_condition = and_(Temperaturi.timestamp > datetime.datetime.strptime(start, "%Y-%m-%d"), final_condition)
        
        # end date parameter condition
        if end:
            final_condition = and_(Temperaturi.timestamp < datetime.datetime.strptime(end, "%Y-%m-%d"), final_condition)
        
        # query the database to retrieve the temperatures with all given restrictions
        list_of_temperatures = db.session.query(Temperaturi.id, Temperaturi.valoare, Temperaturi.timestamp).select_from(
            Temperaturi).join(Orase, Temperaturi.id_oras == Orase.id).where(final_condition)
        
        # create a JSON entry for each retrieved temperature
        json_response = []
        
        for temperature in list_of_temperatures:
            data = {}
            
            data["id"]          = temperature.id
            data["valoare"]     = temperature.valoare
            data["timestamp"]   = temperature.timestamp
            
            json_response.append(data)       
        
        return json_response, format_parser.SUCCESS


    @app.route("/api/temperatures/<id_temp>", methods=["PUT"])    
    def update_temp(id_temp):
        # get received JSON info
        modify = request.get_json()
        
        # check if the JSON corresponds to the expected temperature format
        if not format_parser.is_correct_temperature_format_put(modify):
            return Response(status=format_parser.ERROR_BAD_FORMAT)
        
        # check if the parameter id is a valid one - should be int number
        if not format_parser.is_valid_id(id_temp):
            return Response(status=format_parser.ERROR_BAD_FORMAT)
        
        # check if the received id in the JSON is the same with the parameter
        if not format_parser.is_consistent_id(int(modify["id"]), int(id_temp)):
            return Response(status=format_parser.ERROR_BAD_FORMAT)
        
        # check if temperature or city is NOT_FOUND
        if not database.found_temperature_id(int(id_temp)) or not database.found_city_id(int(modify["idOras"])):
            return Response(status=format_parser.ERROR_NOT_FOUND)
        
        # retrieve the temperature having the corresponding id from database
        temperature = database.get_temperature_by_id(int(id_temp))
        
        # set new attributes to the corresponding entry   
        try:
            setattr(temperature, 'id_oras', int(modify['idOras']))
            setattr(temperature, 'valoare', float(modify['valoare']))
            db.session.commit()
        except:
            return Response(status=format_parser.ERROR_CONFLICT)
        
        return Response(status=format_parser.SUCCESS)
    
    @app.route("/api/temperatures/<id_temp>", methods=["DELETE"])    
    def delete_temp(id_temp):
        # check if the parameter id is a valid one - should be int number
        if not format_parser.is_valid_id(id_temp):
            return Response(status=format_parser.ERROR_BAD_FORMAT)
        
        if not database.found_temperature_id(int(id_temp)):
            return Response(status=format_parser.ERROR_NOT_FOUND)
        
        # delete the corresponding entry
        db.session.query(Temperaturi).where(Temperaturi.id == int(id_temp)).delete()
        db.session.commit()
        
        return Response(status=format_parser.SUCCESS)