import tweepy
from pymongo import MongoClient
import dataset
import sys
import pymongo
from textblob import TextBlob

# List of mental health words derived from NHS

words = ['#mentalhealth','#depressed','#depression', '#dementia', '#Schizophrenia', 'mental health','mental illness','suicide',
                            '#bipolar','bipolar','depression','suicidal','psychosis', 'Anxiety', 'substance dependence', 'autism', 'ADHD', 'personality disorder'
                            'drug addiction', 'Alzheimer','pyromania','dementia']

# Twitter API keys
CONSUMER_KEY = "your consumer key"
CONSUMER_SECRET = "your consumer secret"
ACCESS_TOKEN = "your access token"
ACCESS_TOKEN_SECRET = "your access token secret"

class StreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener,self).__init__()

        #name of the Database in mongodb
        self.db = pymongo.MongoClient().TwitterStream

    def on_status(self, status):
        if status.retweeted:
            return

        data = {}
        text = status.text #collect the text from a tweet
        data['text'] = status.text # import into column 'text'
        data['created_at'] = status.created_at # collect when tweet was created 'created_at'
        blob = TextBlob(text)
        sent = blob.sentiment
        data['polarity'] = sent.polarity
        data['subjectivity'] = sent.subjectivity

        #name of the collection in mongodb
        self.db.tweets.insert(data)

    def on_error(self, status_code):
        print(sys.stderr, 'Status code error:', status_code)
        return True

    def on_timeout(self):
        print(sys.stderr, 'Timed out...')
        return True

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


sapi = tweepy.streaming.Stream(auth, StreamListener(api))
sapi.filter(track=words)