from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to Climate App!"

@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_result = session.query(Measurement.date, Measurement.prcp).all()
    prcp_dict = {}
    for result in prcp_result:
        prcp_dict[result[0]] = result[1]   
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    station_list = session.query(Station.name).all()
    station_list = [s[0] for s in station_list]
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    last_row = session.query(Measurement).order_by(Measurement.id.desc()).first()
    last_date = last_row.date
    split_date = last_date.split('-')
    one_year_before = str(int(split_date[0])-1)
    one_year_before_date = '-'.join([one_year_before, split_date[1], split_date[2]])
    last_12months = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_before_date).all()
    return jsonify(last_12months)

@app.route("/api/v1.0/<start>")
def temps_start(start):
    temp_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),\
        func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>/<end>")
def temps_start_end(start, end):
    temp_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),\
        func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(temp_data)

if __name__ == "__main__":
    app.run(debug=True)