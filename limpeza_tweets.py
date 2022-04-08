import re

def limpar_tweets(texto):
    text = re.sub(r'@[A-Za-z0-9]+', '', texto) # Remove mencoes
    text = re.sub(r'#','', texto) # Remove simbolo de hashtags
    text = re.sub(r'RT[\s]+','',texto) # Remove Retweets
    text = re.sub(r'https?:/\/\S+','',texto) # Remove URLS

    return texto