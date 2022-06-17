import tweepy as tw
import pandas as pd
import configparser as cp
from textblob import TextBlob
import re
import palavras
import json


config = cp.ConfigParser()
config.read('config.ini')
api_key = config['twitter_credenciais']['api_key']
api_key_secret = config['twitter_credenciais']['api_key_secret']
access_token = config['twitter_credenciais']['access_token']
access_token_secret = config['twitter_credenciais']['access_token_secret']

auth = tw.OAuthHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)
api = tw.API(auth)

df_tweets_positivos = pd.DataFrame()
df_tweets_negativos = pd.DataFrame()
tweets_cursor_positivos = tw.Cursor(api.search_tweets, q=palavras.positivas, tweet_mode="extended", lang="en").items(250)
tweets_cursor_negativos = tw.Cursor(api.search_tweets, q=palavras.negativas, tweet_mode="extended", lang="en").items(250)

# public_tweets = api.home_timeline()
# for i in public_tweets:
#     print(i._json.keys())

def coletar_tweets_positivos(tweets_cursor_positivos):
    tweets_positivos = []
    global df_tweets_positivos
    for i in tweets_cursor_positivos:
        tweet_id = i.id_str
        tweet_text = i.full_text
        tweet_rts = i.retweet_count
        tweet_favs = i.favorite_count
        tweet_date = i.created_at
        #tweet_lang = ''
        tweet_positivos = {
            'id': tweet_id,
            'text': tweet_text,
            'number_of_retweets': tweet_rts,
            'number_of_favorites': tweet_favs,
            'date': tweet_date,
            #'language': tweet_lang,
            'user_id': i.user.id,
            'user_screen_name': i.user.screen_name
        }
        tweets_positivos.append(tweet_positivos)
    df_tweets_positivos = df_tweets_positivos.append(tweets_positivos, ignore_index=True)

def coletar_tweets_negativos(tweets_cursor_negativos):
    tweets_negativos = []
    global df_tweets_negativos
    for i in tweets_cursor_negativos:
        tweet_id = i.id_str
        tweet_text = i.full_text
        tweet_rts = i.retweet_count
        tweet_favs = i.favorite_count
        tweet_date = i.created_at
        #tweet_lang = ''
        tweet_negativos = {
            'id': tweet_id,
            'text': tweet_text,
            'number_of_retweets': tweet_rts,
            'number_of_favorites': tweet_favs,
            'date': tweet_date,
            #'language': tweet_lang,
            'user_id': i.user.id,
            'user_screen_name': i.user.screen_name
        }
        tweets_negativos.append(tweet_negativos)
    df_tweets_negativos = df_tweets_negativos.append(tweets_negativos, ignore_index=True)

extracao_positivos = coletar_tweets_positivos(tweets_cursor_positivos);
df_tweets_positivos.to_csv('tweets-positivos.csv')
extracao_negativos = coletar_tweets_negativos(tweets_cursor_negativos);
df_tweets_negativos.to_csv('tweets-negativos.csv')

frames = [df_tweets_positivos,df_tweets_negativos]
df = pd.concat(frames)
df =  df.rename({'text':'Tweets'}, axis = 1)



def limpar_tweets(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text) # Remove mencoes
    text = re.sub(r'#','', text) # Remove simbolo de hashtags
    text = re.sub(r'RT[\s]+','',text) # Remove Retweets
    text = re.sub(r'https?:/\/\S+','',text) # Remove URLS

    return text


df['Tweets'] = df['Tweets'].apply(limpar_tweets)

def extrair_subjetividade(text):
    return TextBlob(text).sentiment.subjectivity

def extrair_polaridade(text):
    return TextBlob(text).sentiment.polarity


df['Subjetividade'] = df['Tweets'].apply(extrair_subjetividade)
df['Polaridade'] = df['Tweets'].apply(extrair_polaridade)

pd.set_option('display.max_rows', df.shape[0]+1)
df
df.to_csv('df.csv')