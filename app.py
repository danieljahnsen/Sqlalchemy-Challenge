#Import dependencies from the assignment
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Import flask statement and jsonify from class
from flask import Flask, jsonify

#Create session using the code from the jupyter notebook
engine = create_engine("sqlite:///hawaii.sqlite")
base = automap_base()
base.prepare(engine, reflect = True)
me = base.classes.measurement
st = base.classes.station
session = Session(engine)

#Instantiate Flask
app = Flask(__name__)

#Create the default route for the homepage
@app.route("/")

#Define the home page function
def home_page():
    #Return a list of routes
    return(
        f"SqlAlchemy Challenge Home Page <br/>"
        f"Routes to use: <br/>"
        f"Precipitation: /api/v1.0/precipitation <br/>"
        f"Stations: /api/v1.0/stations <br/r>"
        f"Temperature Observations: /api/v1.0/tobs <br/r>"
        f"Start and Stop Analysis: /api/v1.0/start/end"
    )

#Create the precipitation route
@app.route("/api/v1.0/precipitation")

#Define the precipitation function
def precipitation():
    #Use the precipitation query code from the jupyter notebook
    date = session.query(func.max(me.date)).first()
    start_year = date
    last_year = dt.date(2016,8,23)
    precip_query = session.query(me.date, me.prcp).filter(me.date >= last_year).all()

    #Create the dataframe
    precip_df = pd.DataFrame(precip_query)
    precip_df = precip_df.set_index("date")

    #Create dictionary from the df
    precip_dict = precip_df.to_dict()

    #Return the dictionary jsonified
    return jsonify(precip_dict)


#Create the stations route
@app.route("/api/v1.0/stations")

#Define the station function
def station():
    #Use the station query code from the jupyter notebook
    stations = session.query(st.station).all()

    #Create a station list
    st_list = []

    #Loop through the query and store the stations in the list
    for x in stations:
        st_list.append(x[0])

    #Return the jsonified list
    return jsonify(st_list)


#Create the temperature observations route
@app.route("/api/v1.0/tobs")

#Define the temperature observations function
def tobs():
    #Get the last year date from the precipitation code
    last_year = dt.date(2016,8,23)

    #Query the most active station from last year
    temps_query = session.query(me.tobs).filter(me.station == 'USC00519281').filter(me.date >= last_year).all()

    #Use the ravel code from class to get an array of the temps
    temps_list = list(np.ravel(temps_query))

    return jsonify(temps_list)


#Create the start/end route
@app.route("/api/v1.0/<start>/<end>")

#Define the stat return function
def temp_stats(start, end):

    #Makes the calculation if no end
    if end == "":
        low_temp = session.query(func.min(me.tobs)).filter(me.date >= start).all()
        max_temp = session.query(func.max(me.tobs)).filter(me.date >= start).all()
        avg_temp = session.query(func.avg(me.tobs)).filter(me.date >= start).all()

        #Make a dictionary of results and return the jsonified version
        stats = {
            "Low Temp " : low_temp[0][0],
            "Max Temp " : max_temp[0][0],
            "Average Temp ": avg_temp[0][0]
        }
        return jsonify(stats)

    #Assumes an end is given and queries accordingly
    low_temp = session.query(func.min(me.tobs)).filter(me.date >= start).filter(me.date <= end).all()
    max_temp = session.query(func.max(me.tobs)).filter(me.date >= start).filter(me.date <= end).all()
    avg_temp = session.query(func.avg(me.tobs)).filter(me.date >= start).filter(me.date <= end).all()

    #Make a dictionary of results and return the jsonified version
    stats = {
        "Low Temp " : low_temp[0][0],
        "Max Temp " : max_temp[0][0],
        "Average Temp ": avg_temp[0][0]
        }
    return jsonify(stats)

    



#Run statement from class
if __name__ == '__main__':
    app.run()

