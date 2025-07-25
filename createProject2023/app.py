from flask import Flask, render_template, request
from flask_session import Session
import requests
import json
import calendar
import datetime


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/search", methods=["GET", "POST"])
def search():

    # a procedure that takes the raw date from the search result and modifies the date into a legible format
    def datecreated(rawdate):
        result = []
        today = datetime.datetime.now()

        for item in rawdate:

            year = int(item[0:4])
            month = int(item[5:7])
            day = item[8:10]
            if(year == today.year):
                recentness = "This Year"
                result.append(recentness)
            else:
                recentness = "About " + str(today.year-year) + " year(s) ago"
                date = calendar.month_name[month] + " " + day + ", " + str(year) + ",  " + recentness
                result.append(date)

        return result


    # Harvests the input data
    searchresult = {}
    queue = request.form.get("searchqueue")
    country = request.form.get("country")

    # Checks to see which country's data is being requested and sends a request based on the country
    if(country == "USA"):
        search = requests.get(f"https://catalog.data.gov/api/3/action/package_search?q={queue}")
    if(country == "UK"):
        search = requests.get(f"https://data.gov.uk/api/3/action/package_search?q={queue}")
    if(country == "Canada"):
        search = requests.get(f"https://open.canada.ca/data/en/api/3/action/package_search?q={queue}")

    searchresult = json.loads(search.text)

    # takes the dates of each database that is returned from the search and puts it in a list
    dates = []
    for item in searchresult["result"]["results"]:
        dates.append(item["metadata_created"])


    # returns the response from the database search and a list of transformed dates
    return render_template("search.html", searchresultt=searchresult, datescreated=datecreated(dates)), 400




@app.route("/readmore", methods=["GET", "POST"])
def moreinfo():

    # Takes the information (hidden and visible) submitted through the form after the 'More Info' button is pressed
    data_name = request.form.get("article_title")
    organization_name = request.form.get("organization_title")
    data_notes = request.form.get("notes")
    data_download = request.form.get("data")

    # renders a new template with all the data taken from the form
    return render_template("moreinfo.html", dataname=data_name, organizationname=organization_name, datanotes=data_notes, datadownload=data_download)

@app.route("/instructions", methods=["GET"])
def instructions():
    return render_template("instructions.html")