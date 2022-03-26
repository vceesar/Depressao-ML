import tweepy as tw
import pandas as pd
import configparser as cp
import palavras


config = cp.ConfigParser()
config.read('config.ini')
api_key = config['twitter_credenciais']['api_key']
api_key_secret = config['twitter_credenciais']['api_key_secret']
access_token = config['twitter_credenciais']['access_token']
access_token_secret = config['twitter_credenciais']['access_token_secret']

auth = tw.OAuthHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)
api = tw.API(auth)


tweets = tw.Cursor(api.search_tweets, q=palavras.positivas).items(10)

for tweet in tweets:
    print(tweet.created_at),
    print(tweet.text)