"""CRUD operations."""

from model import db, User, Property, Image, Favorite, Schedule, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Get a user by id"""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Get a user by email"""

    return User.query.filter(User.email == email).first()


def create_property(zpid, address, zipcode, property_type, price, bathrooms, bedrooms, lot_area_value, lot_area_unit, img_src, longitude, latitude):
    """Create and return a property."""

    property = Property(
        zpid=zpid, 
        address=address,
        zipcode=zipcode,
        property_type=property_type, 
        price=price, 
        bathrooms=bathrooms, 
        bedrooms=bedrooms, 
        lot_area_value=lot_area_value,
        lot_area_unit=lot_area_unit,
        img_src=img_src,
        longitude=longitude,
        latitude=latitude
    )

    return property


def get_properties():
    """Return all properties."""

    return Property.query.all()


def get_property_by_zpid(zpid):
    """Get a movie by id"""

    return Property.query.get(zpid)

def get_properties_by_zipcode(zipcode):
    """Return all properties by zipcode"""

    return Property.query.filter(Property.zipcode == zipcode).all()


def create_image(zpid, url):
    """Create and return a property."""

    image = Image(zpid=zpid, url=url)

    return image


def create_favorite(user, property):
    """Create and return a favorite"""

    favorite = Favorite(user=user, property=property)

    return favorite 


def get_favorite_by_user_and_property(user, property):
    """Get a favorite object from the database by user and property."""
    # Query the database for the favorite object
    favorite = db.session.query(Favorite).filter(
        Favorite.user == user, Favorite.property == property).first()

    # Return the favorite object if it exists, or None if it does not
    return favorite


def get_schedule_by_user_and_property(user, property):
    """Get a schedule object from the database by user and property."""
    # Query the database for the schedule object
    schedule = Schedule.query.filter(
        Schedule.user == user, Schedule.property == property).first()

    return schedule

def create_schedule(user, property, when):
    """Create and return a schedule"""

    schedule = Schedule(user=user, property=property, when=when)
    
    return schedule

def update(cls, rating_id, new_score):
        """ Update a rating given rating_id and the updated score. """
        rating = cls.query.get(rating_id)
        rating.score = new_score


if __name__ == '__main__':
    from server import app
    connect_to_db(app)