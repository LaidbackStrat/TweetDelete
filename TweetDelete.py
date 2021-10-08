from requests_oauthlib import OAuth1Session
import os
import json
import time

consumer_key = 'myconsumerkey'
consumer_secret = 'meyconsumersecret'
access_token = 'access-token'
access_token_secret = 'access-token-secret'

request_token_url = "https://api.twitter.com/oauth/request_token"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)


try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print(
        "There may have been an issue with the consumer_key or consumer_secret you entered."
    )

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)


oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)


with open('./tweet.json', errors="ignore") as f:
  data = json.load(f, encoding="utf8")
count = 0;

for tweet in data:
    

    tweet_id = tweet['tweet']['id']
    
    try:
        response = oauth.post("https://api.twitter.com/1.1/statuses/destroy/"+tweet_id+".json")
        count = count+1
    
    except response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    print("Response code: {}".format(response.status_code))
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))
    print("COUNT:"+str(count))
    if(count > 2999):
        break
