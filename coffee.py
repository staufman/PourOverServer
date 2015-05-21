from delayedresult import clear_queue, queuefunc
from time import sleep

import RPi.GPIO as GPIO

# state machine states
(
	STATE_READY,
	STATE_HEAT_WATER,
	STATE_WET_GROUNDS,
	STATE_WAIT_FOR_BLOOM,
	STATE_FINAL_BREW,
) = range(5)

Motor1A = 16
Motor1B = 18
Motor1E = 22

machine_state = None

WET_GROUNDS_SECONDS = 5
WAIT_FOR_BLOOM_SECONDS = 5
FINAL_BREW_SECONDS = 5


@queuefunc
def setup_machine():
	print "Setup machine..."
	clear_queue()	# stop any previous jobs

	'''
	GPIO.cleanup()

 	GPIO.setmode(GPIO.BOARD)
 
	GPIO.setup(Motor1A, GPIO.OUT)
	GPIO.setup(Motor1B, GPIO.OUT)
	GPIO.setup(Motor1E, GPIO.OUT)
	'''

	machine_state = STATE_READY


@queuefunc
def tear_down_machine():
	print "Tear down machine..."

	machine_state = STATE_READY
	#GPIO.cleanup()


@queuefunc
def heat_water():
	print "Heat water..."
	machine_state = STATE_HEAT_WATER	

	# TODO: wait for water to be hot!
	wet_grounds.delay(5)


@queuefunc
def wet_grounds():
	print "Wet grounds..."
	machine_state = STATE_WET_GROUNDS

	# wet the grounds for a predetermined amount of time (for now)
	wait_for_bloom.delay(WET_GROUNDS_SECONDS)	


@queuefunc
def wait_for_bloom():
	print "Wait for bloom..."
	machine_state = STATE_WAIT_FOR_BLOOM

	# wet the grounds for a predetermined amount of time (for now)
	final_brew.delay(WAIT_FOR_BLOOM_SECONDS)	


@queuefunc
def final_brew():
	print "Final brew..."
	machine_state = STATE_FINAL_BREW

	# brew for a predetermined time and then go back to the ready state
	tear_down_machine.delay(FINAL_BREW_SECONDS)


@queuefunc
def start_brewing():
	print "Start brewing"
	setup_machine()

	heat_water()
 
	#GPIO.output(Motor1A, GPIO.HIGH)
	#GPIO.output(Motor1B, GPIO.LOW)
	# delay 5 seconds
	#task = add.delay(10, 1, 2)
	#print task
	#return task


'''
for i in xrange(5):
	print "Turning motor on"
	GPIO.output(Motor1E, GPIO.HIGH)
 
	sleep(10)
 
	print "Stopping motor"
	GPIO.output(Motor1E, GPIO.LOW)
'''

