from flask_api import FlaskAPI
from flask import request
import vl
import pandas as pd
from flask_cors import CORS, cross_origin

app = FlaskAPI(__name__)
CORS(app)

@app.route('/parking-route/', methods=['GET'])
def parking_route():
    args = request.args
    try:
        destination = args['destination']
        walking = args['walking']
    except KeyError:
        return { 
            'error': 'Expecting `destination` and `walking` parameters to be defined',
            'code': 1
        }
    lat, lng = destination.split(',')
    lat, lng = float(lat), float(lng)
    walking = float(walking)
    travel_speed = 3.5
    minutes_per_meter = 60.0/1000.0/travel_speed
    maxtime = max(3, walking*minutes_per_meter)
    df = pd.read_csv('vl/vagas.csv')
    waypoints_list = vl.get_waypoints_by_lat_long(lat, lng, maxtime=maxtime, vagas_df=df)
    waypoints_list = [w for w in waypoints_list if w is not None]
    # distance(destination, waypoints_list[0][0]) < 100 meters # Sanity check
    waypoints_list = [ waypoints[1:] for waypoints in waypoints_list] # Removes destination
    sorted(waypoints_list, key=len, reverse=True)
    longest_path = waypoints_list[0]
    print("Longest path: " + str(longest_path))
    print("Number of paths: " + str(len(waypoints_list)))
    return { 'waypoints': waypoints_list }

if __name__ == "__main__":
    app.run(host='0.0.0.0')