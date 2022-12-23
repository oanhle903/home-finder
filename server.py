"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from datetime import datetime
import json
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined
app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


app.app_context().push()

# Replace this with routes and view functions!
@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')

@app.route('/properties')
def all_properties():
    """View all properties"""

    properties = crud.get_properties()

    return render_template('all_properties.html', properties=properties)


@app.route('/properties/<zpid>')
def movie_details(zpid):
    """View details of a property"""

    property = crud.get_property_by_zpid(zpid)

    return render_template('property_details.html', property=property)


@app.route('/properties/search')
def find_properties():
    """Search for properties"""

    zipcode = request.args.get('zipcode', '')

    properties = crud.get_properties_by_zipcode(zipcode)
    # if properties == "" return render_template('discover page')
    return render_template('search_results.html',
                           results=properties)



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

    return render_template('user_favorites.html', user=user)


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
        flash("You must log in to rate a movie.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        property = crud.get_property_by_zpid(zpid)

        favorite = crud.create_favorite(user, property)
        db.session.add(favorite)
        db.session.commit()

        flash(f"You added this property to favorites.")

    return redirect(f"/properties/{zpid}")



# @app.route('/properties/<zpid>/favorites', methods=["DELETE"])
# def remove_favorite(zpid):
#     """Remove a favorite property."""
#     logged_in_email = session.get("user_email")
#     user = crud.get_user_by_email(logged_in_email)
#     property = crud.get_property_by_zpid(zpid)
#     TODO: write function to get that favorite need to be deleted
#     favorite = crud.create_favorite(user, property) 
#     db.session.delete(favorite)
#     db.session.commit()

#     flash(f"You removed this property to favorites.")

#     return redirect(f"/properties/{zpid}")

@app.route('/properties/<zpid>', methods=["POST"])
def create_schedule(zpid):
    """Create a new schedule to tour the property."""

    logged_in_email = session.get("user_email")

    if logged_in_email is None:
        flash("You must log in to book a tour.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        property = crud.get_property_by_zpid(zpid)
        when = datetime.strptime(f'2022-12-14', '%Y-%m-%d')

        schedule = crud.create_schedule(user, property, when)
        db.session.add(schedule)
        db.session.commit()

        flash(f"You booked this time to tour the property")

    return redirect(f"/properties/{zpid}")



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
