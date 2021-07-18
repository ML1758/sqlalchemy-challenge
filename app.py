import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# =======================================================================
# index route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitaion<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

# =======================================================================
# precipitaion route
@app.route("/api/v1.0/precipitaion")
def precipitaion():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date one year from the last date in data set.
    previous_yr = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    prec_db = session.query(Measurement.date, Measurement.prcp)\
                            .filter(Measurement.date >= previous_yr)\
                            .all()

    # Close session after read
    session.close()

    # Create a dictionary from the row data and set date as the key and prcp as the value
    all_prec = {date: prcp for date, prcp in prec_db}
   
    return jsonify(all_prec)


# =======================================================================
# stations route
@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    stations_db = session.query(Station.station, Station.name)\
                                .order_by(Station.station)\
                                .all()

    # Close session after read
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = {station: name for station, name in stations_db}

    return jsonify(all_stations)

# =======================================================================
# tobs route
@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date one year from the last date in data set.
    previous_yr = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    tobs_db = session.query(Measurement.date, Measurement.tobs)\
                            .filter(Measurement.date >= previous_yr)\
                            .filter(Measurement.station == 'USC00519281')\
                            .all()
    
    # Close session after read
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs = {date: tobs for date, tobs in tobs_db}

    return jsonify(all_tobs)

# =======================================================================
# temp_start route
@app.route("/api/v1.0/<start_dt>")
def temp_start(start_dt):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    tobs_db = session.query(func.min(Measurement.tobs).label("tmin"),\
                            func.avg(Measurement.tobs).label("tavg"),\
                            func.max(Measurement.tobs).label("tmax"))\
                            .filter(Measurement.date >= start_dt)\
                            .all()

    # Close session after read
    session.close()

     # Create a dictionary of summary temperatures and append to a list 
    all_tobs = []
    for tmin, tavg, tmax in tobs_db:
        tobs_dict = {}
        tobs_dict["TMIN"] = tmin
        tobs_dict["TAVG"] = tavg
        tobs_dict["TMAX"] = tmax
        all_tobs.append(tobs_dict) 

    return jsonify(all_tobs)

# =======================================================================
# temp_start_end route
@app.route("/api/v1.0/<start_dt>/<end_dt>")
def temp_start_end(start_dt, end_dt):

    # print the start and end dates
    #start_dt = start_end_dt[:10]
    #end_dt = start_end_dt[-10:]

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    tobs_db = session.query(func.min(Measurement.tobs).label("tmin"),\
                            func.avg(Measurement.tobs).label("tavg"),\
                            func.max(Measurement.tobs).label("tmax"))\
                            .filter(Measurement.date >= start_dt)\
                            .filter(Measurement.date <= end_dt)\
                            .all()

    # Close session after read
    session.close()

     # Create a dictionary of summary temperatures and append to a list
    all_tobs = []
    for tmin, tavg, tmax in tobs_db:
        tobs_dict = {}
        tobs_dict["TMIN"] = tmin
        tobs_dict["TAVG"] = tavg
        tobs_dict["TMAX"] = tmax
        all_tobs.append(tobs_dict) 

    return jsonify(all_tobs)

# =======================================================================
# the main program
if __name__ == '__main__':
    app.run(debug=True)
