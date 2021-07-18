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

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitaion<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )


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


if __name__ == '__main__':
    app.run(debug=True)
