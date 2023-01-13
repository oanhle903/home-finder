"""Server for home finder app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from datetime import datetime
import json
from model import connect_to_db, db, Schedule, Property, User
import crud
import os

from jinja2 import StrictUndefined
app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


app.app_context().push()

MAP_API_KEY = os.environ.get('MAP_API')

@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')


@app.route('/properties')
def all_properties():
    """View all properties"""
    properties = crud.get_properties()


    return render_template('all_properties.html', search=False, MAP_API_KEY=MAP_API_KEY, properties=properties)



@app.route('/properties/<zpid>')
def property_details(zpid):
    """View details of a property"""

    property = crud.get_property_by_zpid(zpid)
    
    """
    check if property is already in the favorites table
    query the favortie table given that zpid and return is_favorite yes or no?
    """
    is_favorite = crud.is_favorite(zpid)
    # is_scheduled = crud.is_scheduled(zpid)
    now = datetime.now()
    is_scheduled = Schedule.query.filter_by(zpid=zpid, is_canceled=False).filter(Schedule.when > now).first()
    

    return render_template('property_details.html', property=property, is_favorite=is_favorite, is_scheduled=is_scheduled,  MAP_API_KEY=MAP_API_KEY)



@app.route('/properties/search/api')
def find_searched_properties():
    """Search for properties"""

    zipcode = request.args.get('zipcode')

    properties = crud.get_properties()
    properties_by_zipcode = crud.get_properties_by_zipcode(zipcode)

    if not properties_by_zipcode:
        return render_template('all_properties.html', search=False, MAP_API_KEY=MAP_API_KEY, properties=properties)
    else:
        return render_template('all_properties.html', search=True, MAP_API_KEY=MAP_API_KEY, properties_by_zipcode=properties_by_zipcode)



@app.route('/properties.json')
def propertiess():
    """Return list of properties dictionary"""

    properties = crud.get_properties()

    # Convert the list of objects to a list of dictionaries
    dict_list = [obj.to_dict() for obj in properties]

    return jsonify(dict_list)



@app.route('/users')
def all_users():
    """View all users"""

    users = crud.get_users()

    return render_template('all_users.html', users=users)


@app.route('/users/<user_id>')
def user_details(user_id):
    """View details of a user"""

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)



@app.route('/users/<user_id>/schedules')
def user_schedules(user_id):
    """View details of a user's schedules"""

    user = crud.get_user_by_id(user_id)
    schedules = user.schedules
    canceled_schedules = [s for s in schedules if s.is_canceled]

    current_schedules = []
    past_schedules = []
    future_schedules = []

    for schedule in schedules:
        tour_date = schedule.when  
        now = datetime.now()
        days = tour_date - now  # = datetime.timedelta(days=2, seconds=57433, microseconds=667989)
        
        # days.days == 0 means same day
        if days.days == 0 and tour_date >= now:
            current_schedules.append(schedule)
        elif tour_date < now:
            past_schedules.append(schedule)
        else:
            future_schedules.append(schedule)

    return render_template('user_schedules.html', user=user, current_schedules=current_schedules, past_schedules=past_schedules, future_schedules=future_schedules, canceled_schedules=canceled_schedules)


@app.route('/users', methods=['POST'])
def register_user():
    """Create a new user"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")


@app.route('/login', methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email and id in session
        session["user_email"] = user.email
        session["user_id"] = user.user_id
        flash(f"Welcome back, {user.email}!")

    return redirect("/")



@app.route('/logout')
def process_logout():
    """Process user logout."""

    del session["user_id"]
    del session["user_email"]

    return redirect("/")

    

@app.route('/check_login')
def check_login(): 
    """Check if user is logged in"""

    logged_in_email = session.get("user_email")
    
    if logged_in_email:
        return 'logged_in'
    else:
        return 'logged_out'



@app.route('/users/<user_id>/favorites')
def show_user_favorites(user_id):
    """View details of a user's favorites"""

    user = crud.get_user_by_id(user_id)
    favorites = user.favorites
  
    return render_template('user_favorites.html', user=user, favorites=favorites)



@app.route('/properties/<zpid>/favorite', methods=["POST"])
def create_favorite(zpid):
    """Create a new favorite for the property."""

    logged_in_email = session.get("user_email")

    if logged_in_email is None:
        flash("You must log in to favorite this item.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        property = crud.get_property_by_zpid(zpid)

        favorite = crud.create_favorite(user, property)
        db.session.add(favorite)
        db.session.commit()

        flash(f"You added this property to favorites.")

    return redirect(f"/properties/{zpid}")



@app.route('/properties/favorites/sort/<sort_order>', methods=["GET"])
def sort_favorite(sort_order):
    """Sort favorite properties by price."""

    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)

    if sort_order == 'low':
        user.favorites = sorted(user.favorites, key=lambda x: x.property.price)
    elif sort_order == 'high':
        user.favorites = sorted(user.favorites, key=lambda x: x.property.price, reverse=True)


    return render_template("user_favorites.html", user=user, favorites=user.favorites)




@app.route('/properties/<zpid>/unfavorite', methods=["POST"])
def remove_favorite(zpid):
    """Remove a favorite property."""
    
    # Get the logged in user and the property
    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)
    property = crud.get_property_by_zpid(zpid)

    # Get the favorite object from the database
    favorite = crud.get_favorite_by_user_and_property(user, property)

    # Delete the favorite object from the database
    db.session.delete(favorite)
    db.session.commit()

    return redirect(f"/users/{user.user_id}/favorites")
    


@app.route('/properties/<zpid>/schedule/create', methods=["POST"])
def create_schedule(zpid):
    """Create a new schedule to tour the property."""

    logged_in_email = session.get("user_email")
    request_datetime = request.form.get("datetime")
    user = crud.get_user_by_email(logged_in_email)
    property = crud.get_property_by_zpid(zpid)
    when = datetime.strptime(request_datetime, '%Y-%m-%d %H:%M')
    schedule = crud.create_schedule(user, property, when)
    db.session.add(schedule)
    db.session.commit()
    flash(f"You booked this time to tour the property")
    return redirect(f"/properties/{zpid}")
 


@app.route('/properties/<zpid>/schedule/update', methods=["POST"])
def update_schedule(zpid):
    """Updates an existing schedule with a new datetime."""
    logged_in_email = session.get("user_email")
    request_datetime = request.form.get("datetime")
    when = datetime.strptime(request_datetime, '%Y-%m-%d %H:%M')
    user = crud.get_user_by_email(logged_in_email)
    property = crud.get_property_by_zpid(zpid)

    now = datetime.now()
    exist_schedule = Schedule.query.filter_by(user_id=user.user_id, zpid=property.zpid, is_canceled=False).filter(Schedule.when > now).first()

    """Updates an existing schedule with a new datetime."""
    tour_date = exist_schedule.when 
    days = tour_date - now

    # > 24 hours
    if days.days*86400 + days.seconds > 86400: 
        exist_schedule.when = when
        db.session.commit()
        flash(f"Your schedule has been updated successfully.")
    else:
        flash(f"You cannot reschedule it before 24 hours")

    return redirect(f"/users/{user.user_id}/schedules")
    


@app.route('/cancel', methods=["POST"])
def cancel_schedule():
    """Cancel a schedule."""
    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)

    schedule_id = request.form.get('schedule_id')
    schedule = crud.get_schedule_by_schedule_id(schedule_id)

    now = datetime.now()
    tour_date = schedule.when 
    days = tour_date - now
    # > 24 hours
    if days.days*86400 + days.seconds > 86400: 
        schedule.is_canceled = True
        schedule.is_active = False
        db.session.commit()
        flash(f"cancelled successfully")
    else:
        flash(f"You cannot cancel it before 24 hours")

    return redirect(f"/users/{user.user_id}/schedules")



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
