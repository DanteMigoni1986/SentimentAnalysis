import tweepy
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

# Authenticate
consumer_key = "tTlEffOs0QEi71O7Av8G0frLj"
consumer_secret = "PjWk3gn9mZA8NnllmYz1ugTfXWuu6M1NpDESqOe2mvanHMc6L8"
access_token = "865314952470560768-6afbAYDaUAuqq8dazPOV6aF0IJOmGdZ"
access_token_secret = "W8maSRUbiMGx7MOcN98cbKpQ22DxiTtMuEScDGAMAci7v"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Retrieve Tweets
public_tweets = api.search_tweets(q='8DeMarzo', count= 5, lang='es')

print('El numero de tweets son:', len(public_tweets))

for tweet in public_tweets:
    print('Contenido del tweet:', tweet.text)
    print('Estructura de los datos del tweet:')
    for attr, value in tweet.__dict__.items():
        print('Propiedad:', attr, ', Tipo de dato:', type(value))
    
    #Step 4 Perform Sentiment Analysis on Tweets
    analysis1 = TextBlob(tweet.text)
    analysis2 = TextBlob(tweet.text, analyzer=NaiveBayesAnalyzer())
    print(analysis1.sentiment)
    print(analysis2.sentiment)
    
    