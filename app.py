import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
engine = create_engine("sqlite:///C:\Rutgers\Homework\Resources\hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station
app = Flask(__name__)

@app.route("/")
def Hawaii():
   """List all available api routes."""
   return (
       f"Available Routes:<br/>"
       f"/api/v1.0/precipitation<br/>"
       f"/api/v1.0/stations<br/>"
       f"/api/v1.0/tobs<br/>"
       f"/api/v1.0/<start><br/>"
       f"/api/v1.0/<start>/<end>"
   )
@app.route("/api/v1.0/precipitation")
def precipitation():
   
   session = Session(engine)
   """Return a list of all precipitaion with date"""
   
   prcp_data= session.query(Measurement.date, Measurement.prcp).all()
   print(prcp_data)
   session.close()
   
   all_data = []
   for date, prcp in prcp_data:
       prcp_dict = {}
       prcp_dict["date"] = date
       prcp_dict["prcp"] = prcp
       all_data.append(prcp_dict)
   return jsonify(all_data)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    
    results = session.query(Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()
    
    all_stations = []
    for name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)
    return jsonify(all_stations)
@app.route("/api/v1.0/tobs")
def tobs():
 
   session = Session(engine)
   
   tobs_results = session.query(Measurement.station, Measurement.tobs).filter(Measurement.date.between('2016-08-01', '2017-08-01')).all()
   tobs_list=[]
   for tobs in tobs_results:
       tobs_dict = {}
       tobs_dict["station"] = tobs[0]
       tobs_dict["tobs"] = float(tobs[1])
       tobs_list.append(tobs_dict)
   return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
   results = session.query(*data).filter(Measurement.station==Station.station).filter(Measurement.date>=start_date).group_by(Station.name).order_by(func.sum(Measurement.prcp).desc()).all()
   results
@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
   result = session.query(*data).filter(Measurement.station==Station.station).filter(Measurement.date>=start_date).filter(Measurement.date<=end_date).group_by(Station.name).order_by(func.sum(Measurement.prcp).desc()).all()
   result
if __name__ == '__main__':
   app.run(debug=True)