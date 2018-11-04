from flask_api import FlaskAPI
from flask import request

app = FlaskAPI(__name__)

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

    # waypoints = RoutingService(destination, walking)
    return { 'waypoints': [] }


if __name__ == "__main__":
    app.run(debug=True)