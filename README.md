# SQLAlchemy Homework - Surfs Up!

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

* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

  * Return the JSON representation of your dictionary.

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * Query the dates and temperature observations of the most active station for the last year of data.
  
  * Return a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

## Hints

* You will need to join the station and measurement tables for some of the queries.

* Use Flask `jsonify` to convert your API data into a valid JSON response object.

- - -

## Bonus: Other Recommended Analyses

* The following are optional challenge queries. These are highly recommended to attempt, but not required for the homework.

### Temperature Analysis I

* Hawaii is reputed to enjoy mild weather all year. Is there a meaningful difference between the temperature in, for example, June and December?

* You may either use SQLAlchemy or pandas's `read_csv()` to perform this portion.

* Identify the average temperature in June at all stations across all available years in the dataset. Do the same for December temperature.

* Use the t-test to determine whether the difference in the means, if any, is statistically significant. Will you use a paired t-test, or an unpaired t-test? Why?

### Temperature Analysis II

* The starter notebook contains a function called `calc_temps` that will accept a start date and end date in the format `%Y-%m-%d`. The function will return the minimum, average, and maximum temperatures for that range of dates.

* Use the `calc_temps` function to calculate the min, avg, and max temperatures for your trip using the matching dates from the previous year (i.e., use "2017-01-01" if your trip start date was "2018-01-01").

* Plot the min, avg, and max temperature from your previous query as a bar chart.

  * Use the average temperature as the bar height.

  * Use the peak-to-peak (TMAX-TMIN) value as the y error bar (YERR).

    ![temperature](Images/temperature.png)

### Daily Rainfall Average

* Calculate the rainfall per weather station using the previous year's matching dates.

* Calculate the daily normals. Normals are the averages for the min, avg, and max temperatures.

* You are provided with a function called `daily_normals` that will calculate the daily normals for a specific date. This date string will be in the format `%m-%d`. Be sure to use all historic TOBS that match that date string.

* Create a list of dates for your trip in the format `%m-%d`. Use the `daily_normals` function to calculate the normals for each date string and append the results to a list.

* Load the list of daily normals into a Pandas DataFrame and set the index equal to the date.

* Use Pandas to plot an area plot (`stacked=False`) for the daily normals.

  ![daily-normals](Images/daily-normals.png)

### Copyright

Trilogy Education Services © 2020. All Rights Reserved.
