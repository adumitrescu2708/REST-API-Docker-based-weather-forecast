# Microservices & Docker - SPRC Tema 2

> Name: *Dumitrescu Alexandra*
>
> Date: *December 2023*

## Content
<ol>
  <li>Relevant implementation details
    <ol>
      <li>Configurations</li>
      <li>Optimizations in configuration</li>
      <li>Run command</li>
      <li>Project structure</li>
      <li>API</li>    
    </ol>
  </li>
</ol>

## Configurations
For implementation I used **Flask, PostgreSQL - SQLAlchemy and Dbeaver**  
Flask server runs on port 6000  
Dbeaver runs on port 8080, and I used the following image - docker pull dbeaver/cloudbeaver:23.2.5
The username and passowrd and database credetials are environment variables in the app.env file.  
Server's main source files, along with the Dockerfile and requirements.txt are in the /src folder  


## Optimizations in configuration
I used environment variables for credetials, specified in the app.env.  
I used volumes for persistency in the database container.  
I used named-DNS for reffering the containers (specified the container names).

## Run command
docker-compose up --build  

## Project structure
**./app/app.py**      -> main source code  
**./app/format_parser.py**   -> source that validates and ivalidates received data formats  
**./app/database.py**   -> source for queries in database  
**./app/models.py** -> model tables in database  
**./app/routes.py** -> source describing implemented routes  
**./app/requirements.txt**  



## API  
When the application is initialised, there are 3 sets of routes being set:
1. /api/countries  
  **[POST/GET]    /api/countries**      - adds a new country entry/retrieves all countries in database     
  **[PUT/DELETE]  /api/countries/:id**  - updates/deletes the country with the given id  
2. /api/cities  
  **[POST/GET]    /api/cities**         - adds a new city entry/retrieves all cities in database     
  **[GET]         /api/cities/country/:id_Tara**   - retrieves all cities in the country specified by the id  
  **[DELETE/PUT]  /api/cities/:id**     - updates/deletes the city with the given id  
3. /api/temperatures
  **[POST/GET]    /api/temperatures**      - adds a new temperature entry/retrieves all temperatures in database  
  **[DELETE/PUT]  /api/cities/:id**        - updates/deletes the temperature with the given id  
  **[GET] /api/temperatures?lat=Double&lon=Double&from=Date&until=Date**
  **[GET] /api/temperatures/cities/:id_oras?from=Date&until=Date**
  **[GET] /api/temperatures/countries/:id_tara?from=Date&until=Date**