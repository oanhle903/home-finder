"""Server for home finder app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from datetime import datetime
import json
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined
app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


app.app_context().push()


@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')


@app.route('/properties')
def all_properties():
    """View all properties"""

    return render_template('all_properties.html', search=False)


@app.route('/properties.json')
def propertiess():
    """Return list of properties dictionary"""

    properties = crud.get_properties()

    # Convert the list of objects to a list of dictionaries
    dict_list = [obj.to_dict() for obj in properties]

    return jsonify(dict_list)


@app.route('/properties/<zpid>')
def property_details(zpid):
    """View details of a property"""

    property = crud.get_property_by_zpid(zpid)

    return render_template('property_details.html', property=property)


@app.route('/properties/search/api')
def find_searched_properties():
    """Search for properties"""

    zipcode = request.args.get('zipcode')

    properties = crud.get_properties_by_zipcode(zipcode)
    if not properties:
        return render_template('all_properties.html', search=False)
    else:
        dict_list = [obj.to_dict() for obj in properties]
        json_data = json.dumps(dict_list, indent=2)
        with open('static/data/results.json', 'w') as f:
            # Write the JSON string to the file
            f.write(json_data)

        return render_template('all_properties.html', search=True)


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


@app.route('/users/<user_id>/favorites')
def user_favorites(user_id):
    """View details of a user's favorites"""

    user = crud.get_user_by_id(user_id)
    favorites = user.favorites
    count = 0
    for favorite in favorites:
        count += 1

    return render_template('user_favorites.html', user=user, count=count)


@app.route('/users/<user_id>/schedules')
def user_schedules(user_id):
    """View details of a user's schedules"""

    user = crud.get_user_by_id(user_id)

    return render_template('user_schedules.html', user=user)


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
        # User is logged in
        return 'logged_in'
    else:
        # User is not logged in
        return 'logged_out'


@app.route('/properties/<zpid>', methods=["POST"])
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

@app.route('/properties/<zpid>/favorites', methods=["POST"])
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

    return redirect(f"/properties/{zpid}")
 



@app.route('/properties/<zpid>/book', methods=["POST"])
def create_schedule(zpid):
    """Create a new schedule to tour the property."""

    logged_in_email = session.get("user_email")

    if logged_in_email is None:
        flash("You must log in to book a tour.")
    else:
        request_datetime = request.form.get("datetime")
        user = crud.get_user_by_email(logged_in_email)
        property = crud.get_property_by_zpid(zpid)
        when = datetime.strptime(request_datetime, '%Y-%m-%d %H:%M')

        schedule = crud.create_schedule(user, property, when)
        db.session.add(schedule)
        db.session.commit()

        flash(f"You booked this time to tour the property")

    return redirect(f"/properties/{zpid}")


@app.route('/properties/<zpid>/cancel', methods=["POST"])
def cancel_schedule(zpid):
    """Cancel a schedule."""
    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)
    property = crud.get_property_by_zpid(zpid)
    schedule = crud.get_schedule_by_user_and_property(user, property)

    now = datetime.now()
    tour_date = schedule.when 
    days = tour_date - now
    if days.days > 1:
        db.session.delete(schedule)
        db.session.commit()
        flash(f"cancelled successfully")
    else:
        flash(f"You cannot cancel it before 24 hours")

    return redirect(f"/users/{user.user_id}/schedules")

# @app.route('/properties/<zpid>/book', methods=["POST"])
# def update_schedule(zpid):
#     logged_in_email = session.get("user_email")
#     user = crud.get_user_by_email(logged_in_email)
#     property = crud.get_property_by_zpid(zpid)

#     if logged_in_email is None:
#         flash("You must log in to book a tour.")
#     else:
#         # Retrieve the existing schedule
#         schedule = crud.get_schedule_by_user_and_property(user, property)
#         if schedule is None:
#             flash("You have not booked a tour for this property.")
#             return redirect(f"/properties/{zpid}")
        
#         # Update the schedule
#         request_datetime = request.form.get("datetime")
#         when = datetime.strptime(request_datetime, '%Y-%m-%d %H:%M')
#         schedule.when = when
#         db.session.commit()
    
#     flash(f"You have updated the tour time for this property")
#     return redirect(f"/properties/{zpid}")

# @app.route("/reschedule", methods=["POST"])
# def reschedule():
#     schedule_id = request.json["schedule_id"]
#     updated_score = request.json["updated_score"]
#     Rating.update(schedule_id, updated_score)
#     db.session.commit()

#     return "Success"


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
