"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb properties")
# More code will go here

# re-creating the database
os.system('dropdb properties')
os.system('createdb properties')

# connect to the database and call db.create_all()
model.connect_to_db(server.app)
model.db.create_all()

# Load properties data from JSON file
with open('data/properties.json') as f:
    property_data = json.loads(f.read())


# Create properties, store them in list so we can use them
# to create fake favorites later
properties_in_db = []
for property in property_data:
    # Get the zpid, adress, property_type, price, bathrooms, bedrooms, 
    # lot_area_value and lot_area_unit from the property dictionary

    zpid = property['zpid']
    address = property['address']
    zipcode = property['address'][-5:]
    property_type = property['propertyType']
    price = property['price']
    bathrooms = property['bathrooms']
    bedrooms = property['bedrooms']
    lot_area_value = property['lotAreaValue']
    lot_area_unit = property['lotAreaUnit']

    # Create a property here and append it to properties_in_db
    db_property = crud.create_property(zpid, address, zipcode, property_type, price, bathrooms, bedrooms, lot_area_value, lot_area_unit)
    properties_in_db.append(db_property)


# Load images data from JSON file
with open('data/images.json') as f:
    image_data = json.loads(f.read())

# Create images, store them in list so we can use them
# to create fake favorites later
images_in_db = []
for zpid in image_data:
    image_urls = image_data[zpid]
    for url in image_urls:
        db_image = crud.create_image(zpid, url)
        images_in_db.append(db_image)
    

model.db.session.add_all(images_in_db)
model.db.session.add_all(properties_in_db)
model.db.session.commit()

# Create 10 users; each user will make 5 favorite properties and 5 schedules

for n in range(10):
    email = f'user{n+1}@test.com'  # Voila! A unique email!
    password = 'test'

    # Create a user here
    db_user = crud.create_user(email, password)
    model.db.session.add(db_user)

    # Create 5 favorite properties and 5 schedules for the user
    for i in range(5):
        random_property = choice(properties_in_db)
        properties_in_db.remove(random_property)
        when = datetime.strptime(f'2022-12-14', '%Y-%m-%d')

        db_favorite = crud.create_favorite(db_user, random_property)
        db_schedule = crud.create_schedule(db_user, random_property, when)
        model.db.session.add(db_favorite)
        model.db.session.add(db_schedule)


model.db.session.commit()