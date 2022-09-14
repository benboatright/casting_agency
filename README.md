# Casting Agency
##### Followed this example from class to set up this document and remind myself how to use curl: https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/tree/master/5_API_Doc_Review

## Motivation
This project was the final capstone project in the FSND Udacity class. The project includes API hosted on Heroku that allows users to interact with an 'actors' table and 'movies' table. Users can submit GET request to view the data in each table, POST requests to add new observations to each table, DELETE requests to delete observations in each table, and PATCH requests to update values for a particular observation. Depending on a user's role, some of these methods may not be authorized. See the Roles / Authentication section below for more detail.

## URL
https://casting-agency-app-bb.herokuapp.com/

## API Behaviour
This API has 8 endpoints.

1. GET '/movies'
- This endpoint retreives the title and release date of all the movies in the movies table.
- Sample Request: curl https://casting-agency-app-bb.herokuapp.com/movies -H "Authorization: Bearer {auth_token}" (used this article to find how to submit the bear token using curl: https://reqbin.com/req/c-hlt4gkzd/curl-bearer-token-authorization-header-example)
- Sample Output:
[
    {"id": 1,
     "release_date": "Fri, 27 May 2022 00:00:00 GMT",
     "success": true,
     "title": "Top Gun: Maverick"}
]
2. GET '/actors'
- This endpoint retreives the name, age, and gender of all the acotrs in the actors table.
- Sample Request: curl https://casting-agency-app-bb.herokuapp.com/actors -H "Authorization: Bearer {auth_token}"
- Sample Output:
[
    {"age":60,
    "gender":"Male",
    "id":1,
    "name":"Tom Cruise",
    "success":true
    }
    ,
    {"age":51,
    "gender":"Female",
    "id":2,
    "name":"Jennifer Connelly",
    "success":true
    }
]
3. POST '/movies'
- This endpoint adds a movie to the movies table. 
- Sample Request: curl https://casting-agency-app-bb.herokuapp.com/movies -X POST -H "Authorization: Bearer {auth_token}" -H "Content-Type: application/json" -d '{"title":"Top Gun: Maverick","release_date":"2022-05-27"}'
- Sample Output:
{
    "success": true,
    "title": "Top Gun: Maverick",
    "release_date": "2022-05-27"
}
4. POST '/actors'
- This endpoint adds an actor to the actors table.
- Sample Request: curl https://casting-agency-app-bb.herokuapp.com/actors -X POST -H "Authorization: Bearer {auth_token}" -H "Content-Type: application/json" -d '{"name":"Tom Cruise","age":60,"gender":"male"}'
- Sample Output:
{
    "success":true,
    "name":"Tom Cruise",
    "age":60,
    "gender":"male"
}
5. DELETE '/movies/{id}'
- This endpoint deletes a movie from the movies table given the movie id.
- Sample Request: curl https://casting-agency-app-bb.herokuapp.com/movies/1 -X DELETE -H "Authorization: Bearer {auth_token}" 
- Sample Output:
{
    "success":true,
    "id":1
}
6. DELETE '/actors/{id}'
- This endpoint deletes an actor from the actors table given the actor id.
- Sample Request: curl https://casting-agency-app-bb.herokuapp.com/actors/1 -X DELETE -H "Authorization: Bearer {auth_token}"
- Sample Output:
{
    "success":true,
    "id":1
}
7. PATCH '/movies'
- This endpoint allows the user to edit attributes of a specific movie in the movies table given the movie id. 
- Sample Request: curl https://casting-agency-app-bb.herokuapp.com/movies/1 -X PATCH -H "Authorization: Bearer {auth_token}" -H "Content-Type: application/json" -d '{"title":"Top Gun","release_date":"1986-05-16"}'
- Sample Output:
{
    "success":true,
    "id":1
}
8. PATCH '/actors'
- This endpoint allows the user to edit attributes of a specific actor in the actors table given the actor id.
- Sample Request: curl https://casting-agency-app-bb.herokuapp.com/actors/1 -X PATCH -H "Authorization: Bearer {auth_token}" -H "Content-Type: application/json" -d '{"name":"Thomas Cruise"}'
- Sample Output:
{
    "success":true,
    "id":1
}


## Roles / Authentication
There are 3 Roles for this API, each with various permissions to access the 8 enpoints mentioned above. The bearer token needed for authorization when testing the various endpoints with each role can be found below.

1. Casting Assistant
Token:'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZnR3RoZnp0ZnVfa05yUmpQQzVIciJ9.eyJpc3MiOiJodHRwczovL2Rldi1keTA4Nnowbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjMxNjUyMGU3MmE0NWM1MDc4MTY4MTZmIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY2MzE5NDU2MCwiZXhwIjoxNjYzMjgwOTYwLCJhenAiOiJ6MWpQUE1QdHBteXlEbXJPRnNOc1JJSDdyZEhEZEQ5eCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.duMfVaJ0uAQtIJfYQGwxKLKbU1Qgd53gUUm8I1JMDvw76hYAf7Bt96W63apKT8Z2UTM5NeFmLdGFO3K3u0OYiRGm8Bf79POlKdwjAsFULfUfVHNWyhdK_VmQu3g4jaqfQI1TJyPSeorZUtXPw7A6od04sEFSQbGYzMZt_FOZqdElw7UnvPm15wqjF9tF7jV2GzyEyjgL1L61xC8-Ndj39EvpokXcqDzHpM1EzQjTVxvAAA9vjW8Hi8KYx0gDkWB1CphOBbNZHj9fWiX-mTvJl_36jivRQeaDkWuPvCjgmzYTs10yBIXTFaHovRKAe4z9fFbCbn24U7TZ4A3YZtqluw'
This Role can perform the following:
- GET movies
- GET actors

2. Casting Director
Token:'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZnR3RoZnp0ZnVfa05yUmpQQzVIciJ9.eyJpc3MiOiJodHRwczovL2Rldi1keTA4Nnowbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjMxNjUyNGVkZTgwZDg5Zjc3NzdlNGJiIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY2MzE5NDY5MiwiZXhwIjoxNjYzMjgxMDkyLCJhenAiOiJ6MWpQUE1QdHBteXlEbXJPRnNOc1JJSDdyZEhEZEQ5eCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.mVxePBB6JETZ9fhQulVVjD8qt8KxMNA769lKkgcmbIYd7M6L0rCAVojsd3YmaJ-uI8fmgONNhAqfu1FR-GiUHwsFseqrHVRRUY9pEk-AwGX9gFwx7OMoBqEAjR2BRibl-nwrBeUAsOaqke_3ts_tuGr2C4JEMKYWDXL4IAYQWJjC3x1VRwvKzrwQqatSIQ0x760sEjk9q8alTLfxLT63Aq46wcACQWXxy7JnH89jlE20Av33O1VjQJh8m6XousZPOe5Bss3SAh2q4ymolPnKBGp9mva72NIyVHjaKWC2_gvDn2OaJw493qx1abd1nTB17AxardtRm3KYIfa9bZ8b6g'
This Role can perform the following:
- GET movies 
- GET actors
- POST actors
- DELETE actors
- PATCH actors
- PATCH movies

3. Executive Produce
Token: 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZnR3RoZnp0ZnVfa05yUmpQQzVIciJ9.eyJpc3MiOiJodHRwczovL2Rldi1keTA4Nnowbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjMxNjUyN2ZiZGVhODBmYzY1ZWIxYTM3IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY2MzE5NDc3NiwiZXhwIjoxNjYzMjgxMTc2LCJhenAiOiJ6MWpQUE1QdHBteXlEbXJPRnNOc1JJSDdyZEhEZEQ5eCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.PYDdlDijykF1v4yuZGGEbof7oYMM-BW02SoKcVIMh-9m4cJap7czBz_1_gN9QhxCEZ3c5fGytmQ73hqlMNaYGp6TET8cNj5OZvIaQiOFyK7nxdwZXMv1BzQTq15SKFQXobhLAptgxj_gfPSdzhqPZON-_3yoTVXc5efGjUxX9vx43qivGHjxvzfEA8OJELazrEVMDnxuE9DOzzbWxaEYJYIon1vvs5RJA5F2amz6324EQi_YYj1_iPp_Qo0mPcmRGTZsflB3eyDBf9HYmPjWGk-m3yknNbcKcoEalFDpmqfFcJV4DKirmREFaLmIw_AOJUUAD2PMcgt8ILuQrd-hqg'
This Role can perform the following:
- GET movies
- GET actors
- POST movies
- POST actors
- DELETE movies
- DELETE actors
- PATCH movies
- PATCH actors

## Errors
This API includes 4 types of errors (404(resource not found), 403(do not have permissions), 401(missing authentication), and 400(bad syntax))
- Sample Output:
{
    "success":False,
    "error_code":403,
    "error_message": " You do not have permission to access the resource you requested"
}

