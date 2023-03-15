import tweepy
import mysql.connector
from googletrans import Translator
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

# Authenticate
consumer_key = "tTlEffOs0QEi71O7Av8G0frLj"
consumer_secret = "PjWk3gn9mZA8NnllmYz1ugTfXWuu6M1NpDESqOe2mvanHMc6L8"
access_token = "865314952470560768-6afbAYDaUAuqq8dazPOV6aF0IJOmGdZ"
access_token_secret = "W8maSRUbiMGx7MOcN98cbKpQ22DxiTtMuEScDGAMAci7v"
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Ironboy9/",
    database = "tweetdatabase"
)

mycursor = db.cursor()
# mycursor.execute("DROP TABLE TweetContent")
# db.commit()
mycursor.execute("CREATE DATABASE IF NOT EXISTS tweetdatabase")
db.commit()
mycursor.execute("CREATE TABLE IF NOT EXISTS TweetContent (tweetMessage VARCHAR(500) NOT NULL, polaridad DOUBLE NOT NULL, subjetividad DOUBLE NOT NULL, positivismo DOUBLE NOT NULL, negatividad DOUBLE NOT NULL, predominante VARCHAR(10) NOT NULL,id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
db.commit()

translator = Translator()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Retrieve Tweets
public_tweets = api.search_tweets(q='jungkook', count= 10000, lang='es')

# print('El numero de tweets son:', len(public_tweets))

Query = "INSERT INTO TweetContent (tweetMessage, polaridad, subjetividad, positivismo, negatividad, predominante) VALUES (%s, %s, %s, %s, %s, %s)"

for tweet in public_tweets:
    # print('Contenido del tweet:', tweet.text)
    # print('Estructura de los datos del tweet:')
    # for attr, value in tweet.__dict__.items():
    #     print('Propiedad:', attr, ', Tipo de dato:', type(value))

    tweetEnglish = translator.translate(tweet.text, src='es', dest='en')

    print(tweetEnglish.text)
    analysis1 = TextBlob(tweetEnglish.text)
    analysis2 = TextBlob(tweetEnglish.text, analyzer=NaiveBayesAnalyzer())
    print(analysis1.sentiment, "-", analysis1.sentiment[0], "-", analysis1.sentiment[1])
    print(analysis2.sentiment, "-", analysis2.sentiment[0], "-", analysis2.sentiment[1], "-", analysis2.sentiment[2])
    mycursor.execute(Query, (tweetEnglish.text, analysis1.sentiment[0], analysis1.sentiment[1], analysis2.sentiment[1], analysis2.sentiment[2], analysis2.sentiment[0]))
    
db.commit()

mycursor.execute("SELECT * FROM TweetContent")
for x in mycursor:
    print(x)
    
    