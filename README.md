# Casting Agency

## Motivation
This project was the final capstone project in the FSND Udacity class. The project includes API hosted on Heroku that allows users to interact with an 'actors' table and 'movies' table. Users can submit GET request to view the data in each table, POST requests to add new observations to each table, DELETE requests to delete observations in each table, and PATCH requests to update values for a particular observation. Depending on a user's role, some of these methods may not be authorized. See the Roles / Authentication section below for more detail.

## URL
https://casting-agency-app-bb.herokuapp.com/

## API Behaviour
This API has 8 endpoints.

1. GET movies
2. GET actors
3. POST movies
4. POST actors
5. DELETE movies
6. DELETE actors
7. PATCH movies
8. PATCH actors


## Roles / Authentication
There are 3 Roles for this API, each with various permissions to access the 8 enpoints mentioned above. The bearer token needed for authorization when testing the various endpoints with each role can be found below.

1. Casting Assistant
Token:
This Role can perform the following:
- GET movies
- GET actors

2. Casting Director
Token:
This Role can perform the following:
- GET movies 
- GET actors
- POST actors
- DELETE actors
- PATCH actors
- PATCH movies

3. Executive Produce
Token:
This Role can perform the following:
- GET movies
- GET actors
- POST movies
- POST actors
- DELETE movies
- DELETE actors
- PATCH movies
- PATCH actors