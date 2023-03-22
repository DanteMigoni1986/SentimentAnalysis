import tweepy
import mysql.connector
from googletrans import Translator
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import re
import string


class TweetAnalyzer():
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
    mycursor1 = db.cursor(buffered=True)
    mycursor2 = db.cursor(buffered=True)
    
    def __init__(self, parent = None):
        self.mycursor1.execute("CREATE DATABASE IF NOT EXISTS tweetdatabase")
        self.db.commit()
        
    def createTweetContentTable(self):
        self.mycursor1.execute("CREATE TABLE IF NOT EXISTS TweetContent (tweetMessage VARCHAR(500) NOT NULL, polaridad DOUBLE NOT NULL, subjetividad DOUBLE NOT NULL, positivismo DOUBLE NOT NULL, negatividad DOUBLE NOT NULL, predominante VARCHAR(10) NOT NULL,id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
        self.db.commit()
        
    def dropTweetContentTable(self):
        self.mycursor1.execute("DROP TABLE TweetContent")
        self.db.commit()
        
    def retrieveTweets(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token( self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        public_tweets = api.search_tweets(q='Trump', count= 100, lang='es')
        
        return public_tweets
    
    def insertRawTweetsOnDB(self):
        translator = Translator()
        Query = "INSERT INTO TweetContent (tweetMessage, polaridad, subjetividad, positivismo, negatividad, predominante) VALUES (%s, %s, %s, %s, %s, %s)"
        public_tweets = self.retrieveTweets()

        for i in range(1,51):
            for tweet in public_tweets:
                tweetEnglish = translator.translate(tweet.text, src='es', dest='en')
                print(tweetEnglish.text)
                analysis1 = TextBlob(tweetEnglish.text)
                analysis2 = TextBlob(tweetEnglish.text, analyzer=NaiveBayesAnalyzer())
                print(analysis1.sentiment, "-", analysis1.sentiment[0], "-", analysis1.sentiment[1])
                print(analysis2.sentiment, "-", analysis2.sentiment[0], "-", analysis2.sentiment[1], "-", analysis2.sentiment[2])
                self.mycursor1.execute(Query, (tweetEnglish.text, analysis1.sentiment[0], analysis1.sentiment[1], analysis2.sentiment[1], analysis2.sentiment[2], analysis2.sentiment[0]))
            
        self.db.commit()
        
    def printTweetContentTable(self):
        self.mycursor1.execute("SELECT * FROM TweetContent")
        for x in self.mycursor1:
            print(x)
            
    def cleanText(self, text):
        '''Make text lowercase, remove text in square brackets,remove links,remove punctuation
        and remove words containing numbers.'''
        text = str(text).lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('\w*\d\w*', '', text)
        return text
    
    def createCleanTweetTable(self):
        self.mycursor1.execute("CREATE TABLE IF NOT EXISTS TweetCleanContent (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, tweetMessage VARCHAR(500) NOT NULL, polaridad DOUBLE NOT NULL, subjetividad DOUBLE NOT NULL, positivismo DOUBLE NOT NULL, negatividad DOUBLE NOT NULL, predominante VARCHAR(10) NOT NULL)")
        self.db.commit()
        
    def insertCleanTweetsOnDB(self):
        FetchQuery = "SELECT * FROM TweetContent"
        InsertQuery = "INSERT INTO TweetCleanContent (tweetMessage, polaridad, subjetividad, positivismo, negatividad, predominante) VALUES (%s, %s, %s, %s, %s, %s)"
        
        self.mycursor1.execute(FetchQuery)
        
        for x in self.mycursor1:
            cleanTweetMessage = self.cleanText(x[0])
            analysis1 = TextBlob(cleanTweetMessage)
            analysis2 = TextBlob(cleanTweetMessage, analyzer=NaiveBayesAnalyzer())
            print('Message:',cleanTweetMessage, ' - ',analysis1.sentiment[0],' - ',analysis1.sentiment[1],' - ',analysis2.sentiment[1],' - ',analysis2.sentiment[2],' - ',analysis2.sentiment[0])
            self.mycursor2.execute(InsertQuery, (cleanTweetMessage, analysis1.sentiment[0], analysis1.sentiment[1], analysis2.sentiment[1], analysis2.sentiment[2], analysis2.sentiment[0]))
        
        self.db.commit()
        
    def createWordsTable(self):
        self.mycursor1.execute("CREATE TABLE IF NOT EXISTS Words (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, word VARCHAR(50) NOT NULL, frequency INT NOT NULL)")
        self.db.commit()
        
    def populateWordsTable(self):
        FetchQuery = "SELECT tweetMessage FROM TweetCleanContent"
        self.mycursor1.execute(FetchQuery)
        
        for x in self.mycursor1:
            tweet = x[0]
            wordsInTweet = tweet.split(' ')
            
            for word in wordsInTweet:
                self.mycursor2.execute("SELECT word FROM Words WHERE word= %s",(word,))
                result = self.mycursor2.fetchall()
                
                if len(result) == 0:
                    Query = "INSERT INTO Words (word, frequency) VALUES (%s,%s)"
                    self.mycursor2.execute(Query,(word,1))
                    self.db.commit()
                    
                else:
                    Query= "UPDATE Words SET frequency = frequency+1 WHERE word= %s"
                    self.mycursor2.execute(Query,(word,))
                    self.db.commit()
                    
    def fetchMostPopularWords(self):
        
        Query = "SELECT word, frequency FROM Words ORDER BY frequency DESC LIMIT 20"
        self.mycursor1.execute(Query)
        result = self.mycursor1.fetchall()
        return result
            
    def fetchAveragePositiveReaction(self):
        Query = "SELECT sum(positivismo) FROM TweetCleanContent"
        self.mycursor1.execute(Query)
        result = self.mycursor1.fetchone()
        result = result[0]/self.getTotalRowsCount()
        return result
        
    def fetchAverageNegativeReaction(self):
        Query = "SELECT sum(negatividad) FROM TweetCleanContent"
        self.mycursor1.execute(Query)
        result = self.mycursor1.fetchone()
        result = result[0]/self.getTotalRowsCount()
        return result
    
    def fetchAverageSubjectiveReaction(self):
        Query = "SELECT sum(subjetividad) FROM TweetCleanContent"
        self.mycursor1.execute(Query)
        result = self.mycursor1.fetchone()
        result = result[0]/self.getTotalRowsCount()
        return result
    
    def getTotalRowsCount(self):
        self.mycursor1.execute("SELECT COUNT(*) FROM TweetCleanContent")
        count = self.mycursor1.fetchone()
        return count[0]
    

    
    