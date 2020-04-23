#!/usr/bin/python3

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import RPi.GPIO as GPIO
import time
import pyotp
import atexit

app = Flask(__name__)
secret = pyotp.random_base32()
totp = pyotp.TOTP(secret)

@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    code  = request.form['Body']
    print(str(totp.now()))
    resp = MessagingResponse()
    open_door()
    if(totp.verify(code)):
        #open_door()
        resp.message('Garage door is opening, please stand by...')
    else:
        resp.message('Invalid code...')
    return str(resp)

def open_door():
    GPIO.output(15, GPIO.HIGH)
    time.sleep(10)
    GPIO.output(15, GPIO.LOW)

def cleanup():
    GPIO.cleanup()

if(__name__ == '__main__'):
    atexit.register(cleanup)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(15, GPIO.OUT)
    print('secret is: ' + str(secret))
    app.run()
