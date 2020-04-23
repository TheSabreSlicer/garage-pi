#!/usr/bin/python3

from flask import Flask, request
from twilio import twiml
import RPi.GPIO as GPIO
import time
import pyotp

trigger = 7

app = Flask(__name__)
secret = pyotp.random_base32()
totp = pyotp.TOTP(secret)

@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    code  = request.form['Body']
    resp = twiml.Response()
    if(totp.verify(code)):
        open_door()
        resp.message('Garage door is opening, please stand by...')
    else:
        resp.message('Invalid code...')
    return str(resp)

def open_door():
    GPIO.output(trigger, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(trigger, GPIO.LOW)

if(__name__ == "__main__"):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(trigger, GPIO.OUT)
    app.run()
