import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, abort, jsonify
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant, ChatGrant
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

load_dotenv()
MAX_ALLOWED_SESSION_DURATION = 14400
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')
twilio_client = Client(twilio_api_key_sid, twilio_api_key_secret,
                       twilio_account_sid)

app = Flask(__name__)

@app.route("/")
def my_index():
    return render_template("build/index.html")

@app.route("/token")
def token():
    identity = request.args.get('identity')
    roomName = request.args.get('roomName')
    token = AccessToken(account_sid = twilio_account_sid, signing_key_sid = twilio_api_key_sid, secret=twilio_api_key_secret, ttl= MAX_ALLOWED_SESSION_DURATION)
    token.identity=identity
    videoGrant = VideoGrant(room= roomName)
    token.add_grant(grant=videoGrant)
    
    print('issued token for {} in room {}'.format(identity,roomName))
    return token.to_jwt()



app.run(debug=True)