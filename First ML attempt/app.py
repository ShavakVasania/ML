import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import numpy as np

from helpers import apology, login_required, usd
from datetime import datetime
import pickle


from tensorflow.keras.models import load_model
model2 = load_model(os.path.join(".", "neuralnetwork.h5"))


s_scaler = pickle.load(open('scaler.pkl', 'rb'))


now = datetime.now()

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///housing.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


neighbourhoods = db.execute("SELECT DISTINCT(neighbourhood) FROM airbnb")
room_types = db.execute("SELECT DISTINCT(room_type) FROM airbnb")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        # get all saved airbnbs
        selectAir = db.execute("SELECT * FROM selectAir WHERE user_id=?", session["user_id"])
        # get all saved houses
        selectHouse = db.execute("SELECT * FROM selectHouse WHERE user_id=?", session["user_id"])
        return render_template("index.html", selectAir=selectAir, selectHouse=selectHouse)
    # get id of the house/airbnbs to be deleted
    deleted = int(request.form.get("deleted"))
    # figure out if the user wants to delete a house or airbnb
    delete_type = request.form.get("identify")
    # delete specified huose
    if delete_type == "airbnb":
        db.execute("DELETE FROM selectAir WHERE id=? AND user_id=?", deleted, session["user_id"])
    else:
        db.execute("DELETE FROM selectHouse WHERE id=? AND user_id=?", deleted, session["user_id"])
    return redirect("/")


# names of all the inputs from user
input_names = ["bedrooms", "bathrooms", "sqft living", "sqft lot", "floors",
               "waterfront(1=yes,0=no)", "view", "condition(1-5)", "grade(1-10)", "sqft above", "sqft basement", "year built(at least)",
               "sqft living neighbours", "sqft lot neighbours"]


@app.route("/customise", methods=["GET", "POST"])
@login_required
def customise():
    if request.method == "POST":
        input_values = []
        for x in input_names:
            # append all inputs from the user into a list
            if request.form.get(x):
                input_values.append(int(request.form.get(x)))
            else:
                return apology("you must enter all values", 403)
        # create 2D array so it can be inserted into ML model
        input_values = [input_values]
        # convert into numpy array
        predictions = np.array(input_values)
        # scale data using already fit scaler
        predictions = s_scaler.transform(predictions.astype(np.float))
        # get prediction
        predicted = usd(int(model2.predict(predictions)[0][0]))
        return render_template("customise.html", predicted=predicted, input_names=input_names)

    return render_template("customise.html", input_names=input_names)


@app.route("/selectAirbnb", methods=["GET", "POST"])
@login_required
def selectAirbnb():
    # get id of airbnb to be saved from user
    chosen = request.form.get("house_id")
    information = db.execute("SELECT * FROM airbnb WHERE id=?", chosen)
    if len(information) == 0:
        return apology("input a valid airbnb id", 403)
    information = information[0]
    # insert specified airbnb into selectAir table so it can be displayed in the "/" route
    db.execute("INSERT INTO selectAir(id,name,host_id,host_name,neighbourhood_group,neighbourhood,room_type,price,minimum_nights, user_id) VALUES(?,?,?,?,?,?,?,?,?,?)",
               chosen, information["name"], information["host_id"], information["host_name"], information["neighbourhood_group"], information["neighbourhood"], information["room_type"],
               information["price"], information["minimum_nights"], session["user_id"])
    return redirect("/airbnb")


@app.route("/selectHouse", methods=["GET", "POST"])
@login_required
def selectHouse():
    # get id of airbnb to be saved from user
    chosen = int(request.form.get("house_id"))
    information = db.execute("SELECT * FROM houses WHERE id=?", chosen)
    if len(information) == 0:
        return apology("input a valid house id", 403)
    information = information[0]
    # insert specified house into selectHouse table so it can be displayed in the "/" route
    db.execute("INSERT INTO selectHouse(id,price,bedrooms,sqft_living,floors,waterfront,view,condition,yr_built, zipcode, user_id) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
               chosen, information["price"], information["bedrooms"], information["sqft_living"], information["floors"], information["waterfront"], information["view"],
               information["condition"], information["yr_built"], information["zipcode"], session["user_id"])
    return redirect("/houses")


@app.route("/airbnb", methods=["GET", "POST"])
@login_required
def airbnb():
    if request.method == "POST":
        price_max = request.form.get("price")
        nights = request.form.get("nights")
        # set default for price_max if no input
        if not price_max:
            price_max = 1000
        else:
            price_max = int(price_max)
        # set default for price_max if no input
        if not nights:
            nights = 1000
        else:
            nights = int(nights)

        neighbourhood_selection = request.form.get("neighbourhood")
        room_selection = request.form.get("room_type")

        # create list of all neighbourhoods and room types
        neighbourhood = list(set().union(*(d.values() for d in neighbourhoods)))
        room_type = list(set().union(*(d.values() for d in room_types)))
        neighbourhood.append("Any")
        room_type.append("Any")

        # check if the selected neighbourhood and room type are valid(user didn't change html)
        if neighbourhood_selection not in neighbourhood:
            return apology("select valid neighbourhood", 403)
        if room_selection not in room_type:
            return apology("select valid room type", 403)

        # select specific houses based on filters entered by user
        if neighbourhood_selection == "Any" and room_selection == "Any":
            houses = db.execute("SELECT * FROM airbnb WHERE price<=? AND minimum_nights<=? AND neighbourhood IN (SELECT DISTINCT(neighbourhood) FROM airbnb) AND room_type IN (SELECT DISTINCT(room_type) FROM airbnb) LIMIT 50",
                                price_max, nights)
        elif neighbourhood_selection == "Any":
            houses = db.execute("SELECT * FROM airbnb WHERE price<=? AND minimum_nights<=? AND neighbourhood IN (SELECT DISTINCT(neighbourhood) FROM airbnb) AND room_type IN (?) LIMIT 50",
                                price_max, nights, room_selection)
        elif room_selection == "Any":
            houses = db.execute("SELECT * FROM airbnb WHERE price<=? AND minimum_nights<=? AND neighbourhood IN (?) AND room_type IN (SELECT DISTINCT(room_type) FROM airbnb) LIMIT 50",
                                price_max, nights, neighbourhood_selection)
        else:
            houses = db.execute("SELECT * FROM airbnb WHERE price<=? AND minimum_nights<=? AND neighbourhood IN (?) AND room_type IN (?) LIMIT 50",
                                price_max, nights, neighbourhood_selection, room_selection)

        return render_template("airbnbs.html", houses=houses, neighbourhoods=neighbourhoods, room_types=room_types)

    # if using GET method
    houses = db.execute("SELECT * FROM airbnb LIMIT 30")
    return render_template("airbnbs.html", neighbourhoods=neighbourhoods, room_types=room_types, houses=houses)


@app.route("/houses", methods=["GET", "POST"])
@login_required
def houses():
    if request.method == "POST":
        price_max = request.form.get("price")
        bedrooms = request.form.get("bedrooms")
        waterfront = request.form.get("waterfront")
        view = request.form.get("view")
        # if no input set value extremely high so all houses are displayed
        if not price_max:
            price_max = 999999999
        else:
            price_max = int(price_max)
        if not bedrooms:
            bedrooms = 99
        else:
            bedrooms = int(bedrooms)
        # if checkboxes are not ticked, set values to zero
        if waterfront == None:
            waterfront = 0
        if view == None:
            view = 0

        # select filtered houses
        houses = db.execute("SELECT * FROM houses WHERE price<=? AND bedrooms<=? AND waterfront>=? AND view>=?",
                            price_max, bedrooms, waterfront, view)

        return render_template("houses.html", houses=houses)
    # without filters
    houses = db.execute("SELECT * FROM houses LIMIT 30")
    return render_template("houses.html", houses=houses)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()

    if request.method == "POST":
        # get user input of password and username
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        usernames_check = db.execute("SELECT * FROM users WHERE username=?", username)
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        passwords_check = db.execute("SELECT * FROM users WHERE hash=?", hashed_password)

        # perform validation checks
        if not username:
            return apology("must provide username", 400)

        elif not password:
            return apology("must provide password", 400)

        elif not confirm_password:
            return apology("please confirm password", 400)

        elif password != confirm_password:
            return apology("Passwords must match!", 400)

        elif len(usernames_check) > 0 or len(passwords_check) > 0:
            return apology("This username or password already exists", 400)

        # if no errors then insert the username and password(hashed) into the database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashed_password)
        # set the sessions user_id to the id of the inserted user
        session["user_id"] = db.execute("SELECT id FROM users WHERE username = ? AND hash=?", username, hashed_password)[0]["id"]

        return redirect("/")

    return render_template("register.html")

    """Register user"""