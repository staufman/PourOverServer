 #!/usr/bin/python
 # coding: utf-8

from flask import jsonify, Flask
from redis import Redis

import coffee
import delayedresult

app = Flask(__name__)
app.config['REDIS_QUEUE_KEY'] = delayedresult.QUEUE_KEY

redis = Redis()

@app.route('/v1/status.json')
def status():
    return jsonify({
    	'status': 'success',
    	'state': redis.get(coffee.MACHINE_STATE_KEY),
    	'data': {},
    	})

@app.route('/v1/ping.json')
def ping():
    return jsonify({
    	'status': 'success',
    	'data': {},
    	})

# TODO: make this a POST. Use GET for now to test.
#, methods=['POST']
@app.route('/v1/start_brewing.json')
def start_brewing():
	brew_task = coffee.start_brewing()
	return jsonify({
    	'status': 'success',
    	'data': {},
    	})


if __name__ == "__main__":
	print "Running server..."
	app.debug = True
	app.run(host='0.0.0.0', port=4567)

