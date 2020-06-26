"""
File: post_tweet.py
---------------------------------------------
This program gets prices from
Bitso website public api and post them
into a twitter account.
"""

import tweepy
import requests
import time



def main():
    """ Main function process. """

    while True:
        # Get the access keys from twitter
        consumer_keycode = get_consumer_key()
        consumer_secret_keycode = get_consumer_secret()
        access_token_keycode = get_access_token()
        access_token_secret_keycode = get_access_token_secret()

        # Get the authentication from twitter
        authentication = tweepy.OAuthHandler(consumer_keycode, consumer_secret_keycode)

        # Set the link to get the information from.
        prices_link = "https://api.bitso.com/v3/ticker"

        # Get the info from Bitso public api.
        prices = get_bitso_info(prices_link)

        # Set each value
        btc_to_mxn_value = prices[0]
        btc_to_usd_value = prices[20]
        btc_to_ars_value = prices[17]
        tusd_to_mxn_value = prices[10]
        eth_to_mxn_value = prices[2]
        xrp_to_mxn_value = prices[4]
        ltc_to_mxn_value = prices[6]

        # Format the results as a string.
        message = format_info(btc_to_usd_value, btc_to_mxn_value, btc_to_ars_value,
                              tusd_to_mxn_value, xrp_to_mxn_value, eth_to_mxn_value,
                              ltc_to_mxn_value)

        # Post Tweet
        write_tweet(access_token_keycode, access_token_secret_keycode, authentication, message)


        # Sleep 1 hour
        print("Time before sleep:", time.ctime())
        time.sleep(3600)


def write_tweet(access_token, access_token_secret, auth, text):
    """ Post a tweet in your timeline. """
    # Check for authorization
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Post tweet
    api.update_status(text)
    print("write_tweet() executed!:", text)


def format_info(btc_to_usd, btc_to_mxn, btc_to_ars, tusd_to_mxn, xrp_to_mxn, eth_to_mxn, ltc_to_mxn):
    """ Receives values and format each one to post the as a string. """
    message = "1 #BTC = \n" +\
              "$USD = $" + str(btc_to_usd) + "\n" + \
              "$MXN = $" + str(btc_to_mxn) +  "\n" + \
              "$ARS = $" + str(btc_to_ars) +  "\n" + \
              " " + "\n" \
              "MXN = " + "\n" + \
              "1 $USD = $" + str(tusd_to_mxn) + "\n" + \
              "1 $XRP = $" + str(xrp_to_mxn) +  "\n" + \
              "1 $ETH = $" + str(eth_to_mxn) +  "\n" + \
              "1 $LTC = $" + str(ltc_to_mxn)
    return message


def print_tweets_on_console(access_token, access_token_secret, auth):
    """ Prints the timeline tweets on the console. """
    # Check for authorization
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Print timeline tweets
    print_timeline_tweets(api)


def get_consumer_key():
    """ Get the consumer key. """
    consumer_key = "PUT YOUR CONSUMER KEY HERE"
    return consumer_key


def get_consumer_secret():
    """ Get the consumer secret key. """
    consumer_secret = "PUT YOUR CONSUMER SECRET KEY HERE"
    return consumer_secret


def get_access_token():
    """ Get the access token key. """
    access_token = "PUT YOUR ACCESS TOKEN HERE"
    return access_token


def get_access_token_secret():
    """ Get the access token secret key. """
    access_token_secret = "PUT YOUR ACCESS SECRET KEY HERE"
    return access_token_secret


def print_timeline_tweets(apicode):
    """ Print the timeline tweets. """
    public_tweets = apicode.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)
        print("--" * 75)


def get_bitso_info(link):
    """ Returns the updated price from Bitso link."""
    # Get bitso information
    response = get_info_from_bitso(link)
    json_response = response.json()

    # Create a list to store the prices.
    prices = []

    # Get the prices from Bitso and save them into the list.
    for i in range(21):
        price = get_price(json_response, i)
        prices.append(price)
    return prices


def get_info_from_bitso(link):
    """ Get the info from Bitso website. """
    return requests.get(link)


def get_price(json, index):
    """ Get the price from Bitso website. """
    return json['payload'][index]['last']



if __name__ == "__main__":
    main()