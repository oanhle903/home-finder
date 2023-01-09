"""Models for home finding app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    favorites = db.relationship("Favorite", back_populates="user")
    schedules = db.relationship("Schedule", back_populates="user")


    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class Property(db.Model):
    """A Property."""

    __tablename__ = "properties"

    zpid = db.Column(db.String, primary_key=True)
    address = db.Column(db.String, unique=True)
    zipcode = db.Column(db.String)
    property_type = db.Column(db.String)
    price = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    lot_area_value = db.Column(db.Float)
    lot_area_unit = db.Column(db.String)
    img_src = db.Column(db.String)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    favorites = db.relationship("Favorite", back_populates="property")
    schedules = db.relationship("Schedule", back_populates="property")
    images = db.relationship("Image", back_populates="property")


    def __repr__(self):
        return f"<Property zpid={self.zpid} address={self.address}>"

    def to_dict(self):
        return {"zpid": self.zpid, "address": self.address, "zipcode": self.zipcode, "property_type": self.property_type, "price": self.price, "bathrooms": self.bathrooms, "bedrooms": self.bedrooms, "lot_area_value": self.lot_area_value, "lot_area_unit": self.lot_area_unit, "img_src": self.img_src, "longitude": self.longitude, "latitude": self.latitude}


class Image(db.Model):
    """A property image."""

    __tablename__ = "images"

    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String)
    zpid = db.Column(db.String, db.ForeignKey("properties.zpid"))
    
    property = db.relationship("Property", back_populates="images")

    def __repr__(self):
        return f"<Image image_id={self.image_id} url={self.url}>"


class Favorite(db.Model):
    """A favorite property ."""

    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    zpid = db.Column(db.String, db.ForeignKey("properties.zpid"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    
    property = db.relationship("Property", back_populates="favorites")
    user = db.relationship("User", back_populates="favorites")
    

    def __repr__(self):
        return f"<Favorite favorite_id={self.favorite_id} >"


class Schedule(db.Model):
    """A booking schedule."""

    __tablename__ = "schedules"

    schedule_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    when = db.Column(db.DateTime)
    zpid = db.Column(db.String, db.ForeignKey("properties.zpid"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    is_active = db.Column(db.Boolean, default=True)
    is_canceled = db.Column(db.Boolean, default=False)
    user = db.relationship("User", back_populates="schedules")
    property = db.relationship("Property", back_populates="schedules")

    def __repr__(self):
        return f"<Scheudle schedule_id={self.schedule_id}  when={self.when}>"



def connect_to_db(flask_app, db_uri="postgresql:///properties", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
