# Paradise - Project Pitch

An app to allow users to search for properties and track their favorite properties; also to see all of their booking schedules.

## Background

While there are many great applications out there to search for properties and book tours, there are not any great applications for tracking a combination of all booking schedules, so I was inspired to make one for myself.

## Table of contents


* [MVP](#mvp)
* [Tech Stack](#tech-stack)
* [Features](#features)
* [Roadmap](#roadmap)
* [Installation](#installation)


## <a name="mvp"></a>MVP

- As a user, I want to be able to search for properties.
- As a user, I want to be able to view the details of each property.
- As a user, I want to be able to favorite properties.
- As a user, I want to be able to access my favorite items by clicking on a favorites category.
- As a user, I want to be able to book tours.
- As a user, I want to be able to access, cancel, and update my schedules by clicking on a schedules category.
- As a user, I want to be able to create an account and login to my account.


## <a name="tech-stack"></a>Tech Stack

- **Database:** PostgreSQL
- **Backend:** Python (Flask), SQLAlchemy
- **Frontend:** Jinja2, HTML, CSS, JavaScript (JSON, AJAX), Bootstrap, Tailwind

### Dependencies

- Python packages:
  - SQLAlchemy ORM
  - Flask
  - Jinja2
  - Requests
  
- APIs/external data sources:
  - Zillow API: used to search for properties. 'https://zillow-com1.p.rapidapi.com/propertyExtendedSearch', 
  - Zillow API: used to search for property's images. 'https://zillow-com1.p.rapidapi.com/images', 
  - Google Map Javascript API: used to render locations on map. https://maps.googleapis.com/maps/api/js

- Browser/client-side dependencies:
  - Bootstrap


## <a name="features"></a>Features

Homepage

![Homepage](https://user-images.githubusercontent.com/68570059/215597009-e52fc51c-f170-43c5-abe8-33364e532e80.mp4)
<br/><br/><br/>

All properties page. Users can search properties by zipcode and filters.

![All propertie spage](https://user-images.githubusercontent.com/68570059/215601413-94d0284e-8417-4262-aa5a-ccca802ba023.mp4)
<br/><br/><br/>

Login - Signup. User can favorite and create schedules after logging in successfully.

![Login](https://user-images.githubusercontent.com/68570059/215603377-e9405aa0-aef9-4422-a5d8-95dfedb4be0d.mp4)
<br/><br/><br/>

Favorite a property. On favorite page, users can unfavortie those properties and utilize the sorting method to save time.

![Favorite page](https://user-images.githubusercontent.com/68570059/215606505-9420d3cb-79d2-4804-b879-6cf1ef9fca6f.mp4)
<br/><br/><br/>


Create a schedule. 

![Create schedule](https://user-images.githubusercontent.com/68570059/215610446-4ce5dbc4-56fe-4eb1-a365-82fea914b1ee.mp4)
<br/><br/><br/>


On schedule page, users can cancel and update schedules.

![Schedule Page](https://user-images.githubusercontent.com/68570059/215610457-7f838c48-cc87-43e2-a95b-609794b734e8.mp4)
<br/><br/><br/>


## <a name="roadmap"></a>Roadmap

### Sprint 1

- Create models
- Create view templates
- Pull property data from Zillow API and seed them into my database
- User registration and authentication
- Add functionality to favorite an item and add it to a favorited category
- Add functionality to search for properties by zipcode

### Sprint 2

- Google Map Javascipt API integration: render location and streetview of a property on google map
- Add functionality to create, update, and cancel schedules
- Favorite page to display all favorite properties a user has created, with links to each property detail page
- Scheudle page to display all schedules a user has created, with links to each property detail page


## <a name= "installation"></a>Installation

### Requirements

* Install requirements.txt
* Python 3
* PostgreSQL


To run this web application locally on your device, follow the below steps.

Step 1: Clone this repository
```
$ git clone https://github.com/oanhle903/home-finder.git
```
Step 2: Create and activate a virtual environment
```
 $ pip3 install virtualenv
 $ virtualenv env
 $ source env/bin/activate
 ```
Step 3: Install dependencies
 ```
 $ pip3 install -r requirements.txt
 ```
Step 4: create a secrets.sh file to save secret keys
 ```
 export "API_KEY" = "putYourGoogleMapAPIKey" 
 ```
Step 5: Activate the secrets.sh
 ```
 (env) $ source secrets.sh
 ```
Step 6: Seed the database
```
(env) $ python3 seed_database.py
```
Step 7: Run the server
```
(env) $ python3 server.py
```
Step 8: To view locally, click http://127.0.0.1:5000 on the terminal or type localhost:5000 on local browser
