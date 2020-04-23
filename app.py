#!/usr/bin/python3

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import RPi.GPIO as GPIO
import time
import pyotp
import atexit

app = Flask(__name__)
totp = pyotp.TOTP(pyotp.random_base32())

@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    code  = request.form['Body']
    print(str(totp.now()))
    resp = MessagingResponse()
    if(totp.verify(code)):
        open_door()
        resp.message('Garage door is opening, please stand by...')
    else:
        resp.message('Invalid code...')
    return str(resp)

def open_door():
    GPIO.output(10, GPIO.HIGH)
    time.sleep(10)
    GPIO.output(10, GPIO.LOW)

def cleanup():
    GPIO.cleanup()

if(__name__ == '__main__'):
    atexit.register(cleanup)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(10, GPIO.OUT)
    GPIO.output(10, GPIO.LOW)
    print('provision with: ' + str(totp.provisioning_uri()))
    app.run()
