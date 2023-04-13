# Instagram Scraper Web API with FastAPI
This is a Python program that implements a web API using FastAPI to scrape Instagram user information and store cookies in a MongoDB database. The web API uses authentication to ensure that only authorized users can access it, and allows users to set their Instagram account and password to retrieve cookies that are used for scraping.
## Add Authentication For Login
### Setup
To get started, you will need to install the necessary dependencies for this project:  
```console
pip install fastapi
pip install uvicorn
pip install pymongo
pip install requests
```
You will also need to create a MongoDB database to store the scraped user information and cookies.
## Running the Web API
To run the web API, you can use the following command:
```console
uvicorn main:app --reload
```
This will start the web API on http://localhost:8000.

## Authentication

To access the web API, users will need to authenticate by providing their Instagram account and password. Once authenticated, the user's cookies will be retrieved and stored in the MongoDB database.

## Scraping Instagram User Information

Once authenticated, users can use the web API to scrape information about a particular Instagram user. The user's followers and following lists will be retrieved and stored in the MongoDB database.

The web API uses the requests `library` to make HTTP requests to the Instagram website and retrieve user information. The scraped data is then parsed and stored in the `MongoDB` database using the pymongo library.

## API Endpoints

The following endpoints are available in the web API:
### /auth

This endpoint is used for authentication. Users must provide their Instagram account and password to receive their cookies.
### /scrape/{username}

This endpoint is used to scrape information about a particular Instagram user. The user's followers and following lists will be retrieved and stored in the MongoDB database.
