import tweepy as tw
import pandas as pd
import configparser as cp
import palavras

 # configura os acessos a api utilizando a biblioteca configparser e os keys da api

config = cp.ConfigParser()
config.read('config.ini')
api_key = config['twitter_credenciais']['api_key']
api_key_secret = config['twitter_credenciais']['api_key_secret']
access_token = config['twitter_credenciais']['access_token']
access_token_secret = config['twitter_credenciais']['access_token_secret']

# ------------------------------------------------------------------------------------

auth = tw.OAuthHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)
api = tw.API(auth)

df_tweets = pd.DataFrame()
tweets_cursor = tw.Cursor(api.search_tweets, q=palavras.positivas).items(20)

def coletar_tweets_positivos(tweets_cursor):
    tweets = []
    global df_tweets
    for i in tweets_cursor:
        tweet_id = i.id_str
        tweet_text = i.text
        tweet_rts = i.retweet_count
        tweet_favs = i.favorite_count
        tweet_date = i.created_at
        #tweet_lang = ''
        tweet = {
            'id': tweet_id,
            'text': tweet_text,
            'number_of_retweets': tweet_rts,
            'number_of_favorites': tweet_favs,
            'date': tweet_date,
            #'language': tweet_lang,
            'user_id': i.user.id,
            'user_screen_name': i.user.screen_name
        }
        tweets.append(tweet)
        df_tweets = df_tweets.append(tweets, ignore_index=True)


extracao = coletar_tweets_positivos(tweets_cursor);
print(extracao)
df_tweets.to_csv('tweets-positivos.csv')

