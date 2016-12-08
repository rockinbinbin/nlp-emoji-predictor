# Adapted from https://data.library.utoronto.ca/scraping-tweets-using-python

import oauth2 as oauth
import urllib2 as urllib
import json
import re
import time

api_key = "o3YGAI1eYrgPsaU3KVxjs4utX"
api_secret = "zTzF4ofNFnYtR80WDj65RDCIkWR49ePMEF2XRLqfUwjPXOiLV1"
access_token_key = "373132640-4AJkR2Ic1LVQJaelOja93hMV6SVFLEVl7NK26aDe"
access_token_secret = "PtkLPGlviXQLH8le1QkbkAPg6N3W621zgJA99a7JWE9UY"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitter_req(url, method, parameters):
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                                token=oauth_token,
                                                http_method=http_method,
                                                http_url=url,
                                                parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response

# From https://github.com/jessicabowden/intro-to-nlp/blob/master/notes.ipynb
def has_emoji(text):
    try:
        ranges = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    except re.error:
        ranges = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')

    return ranges.findall(text)


def fetch_tweets():
    url = "https://stream.twitter.com/1.1/statuses/sample.json"
    parameters = []
    response = twitter_req(url, "GET", parameters)

    with open('tweets2.csv', 'w') as outFile:
        for line in response:
            dict = json.loads(line)

            # Only English and non-retweet tweets
            if dict.get('lang') == 'en' and dict.get('retweeted_status') is None:

                # Has emoji
                if has_emoji(dict['text']):
                    text = dict['text'].encode('unicode-escape')

                    try:
                        outFile.write(dict['id_str'] + ',"' + text + '"\n')

                    except Exception as e:
                        print(e)
                        print(dict)
                        assert 3 == 4


if __name__ == '__main__':
  fetch_tweets()