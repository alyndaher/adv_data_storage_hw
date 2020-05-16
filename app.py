import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to my 'Home' page!<br/>"
        f'<br/>'
        f'Try the Routes below:<br/>'
        f'<br/>'
        f"/api/v1.0/precipitation<br/>"
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start>')

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    precip = session.query(Measurement.date,Measurement.prcp).all()
    session.close()

    precip_list = []
    for date, prcp in precip:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["precipitation"] = prcp
        precip_list.append(precip_dict)

    return jsonify(precip_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stat = session.query(Measurement.station).group_by(Measurement.station).all()
    session.close()

    stats = list(np.ravel(stat))

    return jsonify(stats)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    date_tobs = session.query(Measurement.tobs).filter(Measurement.date > one_year).filter(Measurement.station == 'USC00519281').all()
    session.close()

    tobs = list(np.ravel(date_tobs))

    return  jsonify(tobs)

@app.route("/api/v1.0/<start>")
def Start(start):
    session = Session(engine)
    sel1 = [Measurement.station,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs),Measurement.date]
    year_temp = session.query(*sel1).group_by(Measurement.station).all()
    session.close()

    year_temp1 = list(np.ravel(year_temp))

    startdate = start
    for date in year_temp1:
        search_term = date["date"]
       
        if startdate == search_term:
            return jsonify(year_temp1)



if __name__ == "__main__":
    app.run(debug=True)