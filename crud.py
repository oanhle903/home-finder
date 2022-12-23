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


def create_property(zpid, address, zipcode, property_type, price, bathrooms, bedrooms, lot_area_value, lot_area_unit):
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
        lot_area_unit=lot_area_unit
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


# def remove_favorite(property):
#     """Remove and return a favorite"""



def create_schedule(user, property, when):
    """Create and return a schedule"""

    schedule = Schedule(user=user, property=property, when=when)
    
    return schedule


if __name__ == '__main__':
    from server import app
    connect_to_db(app)