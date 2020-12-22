#!/usr/bin/python3

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import RPi.GPIO as GPIO
import time
import pyotp
import atexit

app = Flask(__name__)
totp = pyotp.TOTP(pyotp.random_base32())
setup_mode = True

@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    msg  = request.form['Body']
    resp = MessagingResponse()
    if(msg == "SETUP" and setup_mode):
        resp.message(totp.provisioning_uri(""))
    elif(msg == "STOP_SETUP"):
        setup_mode = False
        resp.message('Setup is now stopped.')
    elif(totp.verify(msg)):
        open_door()
        resp.message('Garage activated, please stand by...')
    else:
        resp.message('Invalid code or action...')
    return str(resp)

def open_door():
    GPIO.output(10, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(10, GPIO.LOW)

def cleanup():
    GPIO.cleanup()

if(__name__ == '__main__'):
    atexit.register(cleanup)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(10, GPIO.OUT)
    GPIO.output(10, GPIO.LOW)
    app.run()
