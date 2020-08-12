import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import and_, or_
from os import environ, path

from flask import Flask, jsonify
from dateutil.relativedelta import *
app = Flask(__name__)
Base = automap_base()
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:////Users/katma/Documents/GitHub/Trilogoy/Homework/sqlalchemy-challenge/Resources/hawaii.sqlite")

# reflect an existing database into a new model

# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()
# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################


@app.route("/")
def welcome():
    
    """List all available api routes."""
    return (
        f"Available Climate API Routes:<br/></br></br>"
        f"Follow this for information Stations: </br></br>"
        f"/api/v1.0/stations</br></br>"
        f"Follow this for information on Precipitation: </br></br>"
        f"/api/v1.0/precipitation</br></br>"
        f"Follow this for information Temperature: </br></br>"
        f"/api/v1.0/tobs</br></br>"
        f"Follow this to review set Start date averages: </br></br>"
        f"/api/v1.0/temp/<start></br></br>"
        f"Follow this for a set start and end date average: </br></br>"
        f"/api/v1.0/temp/<start>/<end></br></br>"
    )

#Convert the query results to a dictionary using date as the key and prcp as the value.

#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def prcp():
   
#     # Create our session (link) from Python to the DB
    session = Session(engine)
    # Find last point in data to calculate 1 year ago
    lastpoint = session.query(measurement.date).order_by(measurement.date.desc()).first().date

    lastpoint=dt.datetime.strptime(lastpoint, "%Y-%m-%d")

# Calculate the date 1 year ago from the last data point in the database
    year_ago = dt.date(2017,8,23) - relativedelta(months=12)

    query = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).all()
   
    
    #I tried doing a dict but it was only returing one date.
    fullprcplist = []
    for date, prcp in query:
        prcp_dict = {}
        prcp_dict["Precipitation"] = prcp
        prcp_dict["Date"] = date
        fullprcplist.append(prcp_dict)

    #using the list function returned all prcp values for the past year
        prcplist2 = list(np.ravel(query))
        return jsonify(prcplist2)
     
    

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query percipitation
    stations = session.query(station.station).all()


    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    lastpoint = session.query(measurement.date).order_by(measurement.date.desc()).first().date
    lastpoint
    lastpoint=dt.datetime.strptime(lastpoint, "%Y-%m-%d")
    year_ago = dt.date(2017,8,23) - relativedelta(months=12)
    # Calculate the date 1 year ago from the last data point in the database
    year_ago = dt.date(2017,8,23) - relativedelta(months=12)
    # Query percipitation
    topstations = session.query(measurement.station,func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    #Under the assumption I need to use the highest row count from query
    topstation1 = (topstations[0])
    topstation1 = (topstation1[0])

# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature of the most active station?
    session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs),func.count(measurement.tobs)).filter(measurement.station == topstation1).all()
    top_station = session.query(measurement.tobs).\
    filter(measurement.station == topstation1).filter(measurement.date >= year_ago).all()
    return jsonify(top_station)




@app.route('/api/v1.0/temp/<start>', defaults={'end': None})

def temperatures(start, end):
    session = Session(engine)

    
    query = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()

    session.close()

   #create list
    templist = {}
    for mini, avge, maxi in query:
       
       templist["Minimum Temp"] = mini
       templist["Average Temp"] = avge
       templist["Max Temp"] = maxi
       
    
    return jsonify(templist)


@app.route('/api/v1.0/temp/<start>/<end>')
def temperatures2(start, end):
    session = Session(engine)

    
    query1 = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).group_by(measurement.date).all()

    session.close()

   #create list
    templist = []
    for mini, avge, maxi in query1:
       loopyboi = {}
       loopyboi["Minimum Temp"] = mini
       loopyboi["Average Temp"] = avge
       loopyboi["Max Temp"] = maxi
       templist.append(loopyboi)
       
   
    return jsonify(templist)
if __name__ == '__main__':
    app.run(debug=True)
