import tweepy
import configparser
import pandas as pd


# Lê as configurações usando configparser
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# Faz a autenticação com o arquivo config.ini (keys da api)
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()

columns = ['Time', 'User', 'Tweet']
data = []
for tweet in public_tweets:
    data.append([tweet.user.screen_name, tweet.text, tweet.user.followers_count])

df = pd.DataFrame(data, columns=columns)

df.to_csv('tweets.csv')