import os
import twitter
from requests_oauthlib import OAuth1Session
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
TWITTER_REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
TWITTER_ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"


@app.route("/request_token")
def request_oauth_token():
    request_token = OAuth1Session(
        client_key=CONSUMER_KEY, client_secret=CONSUMER_SECRET, callback_uri="http://localhost:3000/following"
    )
    data = request_token.get(TWITTER_REQUEST_TOKEN_URL)
    if data.status_code == 200:
        request_token = str.split(data.text, '&')
        oauth_token = str.split(request_token[0], '=')[1]
        oauth_callback_confirmed = str.split(request_token[2], '=')[1]
        return {
            "oauth_token": oauth_token,
            "oauth_callback_confirmed": oauth_callback_confirmed,
        }
    else:
        return {
            "oauth_token": None,
            "oauth_callback_confirmed": "false",
        }

@app.route("/access_token")
def request_access_token():
    oauth_token = OAuth1Session(
        client_key=CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=request.args.get("oauth_token"),
    )
    data = {"oauth_verifier": request.args.get("oauth_verifier")}
    response = oauth_token.post(TWITTER_ACCESS_TOKEN_URL, data=data)
    access_token = str.split(response.text, '&')
    access_token_key = str.split(access_token[0], '=')[1]
    access_token_secret = str.split(access_token[1], '=')[1]
    api = twitter.Api(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token_key=access_token_key,
        access_token_secret=access_token_secret,
    )
    friends = api.GetFriends()
    return {
        "followings": [
            {
                "name": u.name,
                "img": u.profile_image_url_https,
                "description": u.description,
            }
            for u in friends
        ]
    }

if __name__ == "__main__":
    app.run()
