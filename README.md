# SQLAlchemy Homework

### Precipitation Analysis

* Design a query to retrieve the last 12 months of precipitation data.

```
# Find last point in data to calculate 1 year ago
lastpoint = session.query(measurement.date).order_by(measurement.date.desc()).first().date
lastpoint
lastpoint=dt.datetime.strptime(lastpoint, "%Y-%m-%d")

# Calculate the date 1 year ago
year_ago = dt.date(2017,8,23) - relativedelta(months=12)
year_ago
```

* Select only the `date` and `prcp` values.
```
last12 = session.query(measurement.prcp, measurement.date).filter(measurement.date >= year_ago).all(
```
* Load the query results into a Pandas DataFrame and set the index to the date column.
* Sort the DataFrame values by `date`.
```

prcp_df = pd.DataFrame(last12, columns=["prcp","date"])
prcp_df['date'] = pd.to_datetime(prcp_df['date'])
prcp_df.set_index('date', inplace=True)

```
* Plot the results using the DataFrame `plot` method.
```
prcp_df.plot()
plt.savefig('Precipitation-Bar.png')

```

  ![precipitation](https://github.com/kmanning1224/sqlalchemy-challenge/blob/master/Precipitation-Bar.png?raw=true)

* Use Pandas to print the summary statistics for the precipitation data.
```
prcp_df.describe()

```
![summarystatistics](https://i.gyazo.com/cfd8c30e7ad3077c37074f9ca18d442f.png)


### Station Analysis

* Design a query to calculate the total number of stations.
```
session.query(station.station).count()
```
* Design a query to find the most active stations.
```
topstations = session.query(measurement.station,func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
```

  * List the stations and observation counts in descending order.
```
session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs),func.count(measurement.tobs)).filter(measurement.station == topstation1).all()
```
  * Which station has the highest number of observations?
  
  USC00519281

* Design a query to retrieve the last 12 months of temperature observation data (TOBS).
  * Filter by the station with the highest number of observations.
```
last12station = session.query(measurement.tobs).filter(measurement.station == topstation1).filter(measurement.date >= year_ago).all()

```
  * Plot the results as a histogram with `bins=12`.
```
stationdf = pd.DataFrame(last12station, columns = ["tobs"])

stationdf.plot.hist(bins = 12)
plt.xlabel('Temperature')
plt.savefig('Histogram-Temp-Bonus.png')
```

 ![station-histogram](https://github.com/kmanning1224/sqlalchemy-challenge/blob/master/Histogram-Temp-Bonus.png?raw=true)

- - -

## Step 2 - Climate App

Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

* Use Flask to create your routes.

### Routes

```
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

# Database Setup

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
```
* Home page.
  
 ```
  
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
 ```

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

  * Return the JSON representation of your dictionary.
  
  
```
  @app.route("/api/v1.0/precipitation")
  def prcp():
   
  #Create our session (link) from Python to the DB
    session = Session(engine)
    # Find last point in data to calculate 1 year ago
    lastpoint = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]

    lastpoint=dt.datetime.strptime(lastpoint, "%Y-%m-%d")

  #Calculate the date 1 year ago from the last data point in the database
    year_ago = dt.date(2017,8,23) - relativedelta(months=12)

    query = session.query(measurement.date,measurement.prcp).\
        filter(measurement.date >= year_ago).all()

  
    #dictionary
    fullprcplist = []
    for date, prcp in query:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        fullprcplist.append(prcp_dict)
        

    return jsonify(fullprcplist)
  ```

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.
 ```
  @app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query stations
    stations = session.query(station.station).order_by(station.station).all()
    stations = list(np.ravel(stations))

    return jsonify(stations)
 ```

* `/api/v1.0/tobs`
  * Query the dates and temperature observations of the most active station for the last year of data.
  
  * Return a JSON list of temperature observations (TOBS) for the previous year.
  
```
    @app.route("/api/v1.0/tobs")
    def tobs():
    #Create our session (link) from Python to the DB
    session = Session(engine)
    #Calculate the date 1 year ago from the last data point in the database
    lastpoint = session.query(measurement.date).order_by(measurement.date.desc()).first().date
    lastpoint
    lastpoint=dt.datetime.strptime(lastpoint, "%Y-%m-%d")
    year_ago = dt.date(2017,8,23) - relativedelta(months=12)

    # Query topstations
    topstations = session.query(measurement.station,func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).\
        filter(measurement.date >= '2016-08-23').all()
    #Under the assumption I need to use the highest row count from query
    topstation1 = (topstations[0])
    topstation1 = (topstation1[0])

    #Using the station id from the previous query, calculate the lowest temperature recorded, 
    #highest temperature recorded, and average temperature of the most active station?
    query = session.query((measurement.date),func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).\
        filter(measurement.station == 'USC00519397').filter(measurement.date >= year_ago).group_by(measurement.date).all()


    toplist = []
    for date, min, avg, max in query:
       loopyboi = {}
       loopyboi["Date"] = date
       loopyboi["Minimum Temp"] = min
       loopyboi["Average Temp"] = avg
       loopyboi["Max Temp"] = max
       toplist.append(loopyboi)

       
    return jsonify(toplist)
```

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
```
     @app.route('/api/v1.0/temp/<start>', defaults={'end': None})
      def temperatures(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

       #Query
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
    
```

## Bonus: Other Recommended Analyses

* The following are optional challenge queries. These are highly recommended to attempt, but not required for the homework.

### Temperature Analysis I

* Use the t-test to determine whether the difference in the means, if any, is statistically significant. Will you use a paired t-test, or an unpaired t-test? Why?


### Temperature Analysis II

* Plot the min, avg, and max temperature from your previous query as a bar chart.

  * Use the average temperature as the bar height.

  * Use the peak-to-peak (TMAX-TMIN) value as the y error bar (YERR).   
```
min = 62.0
avg = 71.23
max = 82.0
error = max - min
plt.figure(figsize=[5,10]);
plt.bar(1, avg, yerr=error, align='center', 
        ecolor='black', capsize=7)
plt.ylabel('Temperature')
plt.title('Trip Avg Temperature')
plt.tick_params(labelbottom=False)
plt.savefig("BONUS-Trip Temp Avg.png")
```

![temperature](https://github.com/kmanning1224/sqlalchemy-challenge/blob/master/BONUS-Trip%20Temp%20Avg.png?raw=true)
### Daily Rainfall Average

* Calculate the rainfall per weather station using the previous year's matching dates.

* Calculate the daily normals. Normals are the averages for the min, avg, and max temperatures.

* You are provided with a function called `daily_normals` that will calculate the daily normals for a specific date. This date string will be in the format `%m-%d`. Be sure to use all historic TOBS that match that date string.

* Create a list of dates for your trip in the format `%m-%d`. Use the `daily_normals` function to calculate the normals for each date string and append the results to a list.

* Load the list of daily normals into a Pandas DataFrame and set the index equal to the date.

```
session.query(station.station, station.name, func.sum(measurement.prcp)).filter(station.station == measurement.station).\
filter(measurement.date >= '2016-08-23').filter(measurement.date <= '2016-08-30').group_by(measurement.station).\
order_by(measurement.prcp.desc()).all()


temps = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%m-%d", measurement.date) == date).all()
```
```    
start = '2016-08-23'
end = '2016-08-30'


startstrip = dt.datetime.strptime(start, '%Y-%m-%d')
endstrip = dt.datetime.strptime(end, '%Y-%m-%d')

dates = []
normals = []


while (startstrip <= endstrip):
    dates.append(startstrip)
    string = dt.datetime.strftime(startstrip, '%m-%d')
    normals.append(list(np.ravel(daily_normals(string))))
    startstrip = startstrip + dt.timedelta(days=1)
normals
```
```
normaltemp = pd.DataFrame(normals, columns = ['Min', 'Avg', 'Max'])
normaltemp['date'] = dates
normaltemp = normaltemp.set_index('date')

ax = normaltemp.plot.area(stacked=False)
ax.legend(frameon=True, loc='lower center', ncol=3, shadow=True, borderpad=1)
plt.figure(figsize=(15,10))
plt.savefig('StackedChart-Bonus.png')
```
!stackedchart](https://github.com/kmanning1224/sqlalchemy-challenge/blob/master/StackedChart-Bonus.png)
