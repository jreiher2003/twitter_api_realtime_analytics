# this is the main file to bring in the twitter feed
import os
import json
from kafka import SimpleProducer, KafkaClient 
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET=os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN=os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET=os.environ["ACCESS_TOKEN_SECRET"]

topic = b'twitter-stream'
kafka = KafkaClient('localhost:9092')
producer = SimpleProducer(kafka)


#This is a basic listener that just put received tweets to kafka cluster.
class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send_messages(topic, data.encode('utf-8'))
        print data
        print "*********************************************"
        print type(data)
        tweet = json.loads(data)
        print tweet 
        print type(tweet)
        print tweet['text']
        return True

    def on_error(self, status):
        print status


WORDS_TO_TRACK = "the to and is in it you of for on my that at with me do have just this be so are not was but out up what now new from your like good no get all about we if time as day will one how can some an am by going they go or has know today there love more work too got he back think did when see really had great off would need here thanks been still people who night want why home should well much then right make last over way does getting watching its only her post his morning very she them could first than better after tonight our again down news man looking us tomorrow best into any hope week nice show yes where take check come fun say next watch never bad free life".split()

if __name__ == '__main__':
    print 'running the twitter-stream python code'
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, l)
    # Goal is to keep this process always going
    while True:
        try:
           # stream.sample()
            #stream.filter(languages=["en"], track=WORDS_TO_TRACK)
            stream.filter(follow=['1467718945'])
        except:
            pass