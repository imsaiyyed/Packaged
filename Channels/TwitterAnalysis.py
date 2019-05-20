import json
import Configuration.config as config
from Classifiers.nnclassifier import SentimentAnalyzer
from dateutil import parser
import tweepy
import csv
import requests

class TwitterBot:
    
    def __init__(self,userid):
        self.userid=userid
    
    def getusercreds(self):
        userinfo=requests.get(config.API_ENDPOINT+'api/metadata/TwitterDetails?UserId='+str(self.userid))
        userinfo=json.loads(userinfo.text)
        self.userinfo=userinfo[0]
        
    def getMentionedUsers(self,tweet):
        mentionedUsers = tweet.entities['user_mentions'];
        mentionedUsersString=""
        # print(tweet)
        if len(mentionedUsers) == 0:
            return mentionedUsersString
        else:
            for user in mentionedUsers:
                mentionedUsersString = mentionedUsersString + '' + user['screen_name'] + ','
            return mentionedUsersString
    
    def getHashTags(self,tweet):
        hashTags = tweet.entities['hashtags'];
        hashTasgString = ""
        if len(hashTags) == 0:
            return hashTasgString
        else:
            for hashTag in hashTags:
                hashTasgString = hashTasgString + '' + hashTag['text'] + ','
            return hashTasgString
    
    def postsentimentdata(self,mesg):
        headers = {
                'Content-Type': 'application/json'
                }
        resp = requests.post(config.API_ENDPOINT+'api/metadata/TwitterSentimentData',headers=headers,data=json.dumps(mesg))
        print(resp.text)
        
    def getTweets(self,tag):
        analyzer=SentimentAnalyzer()
        
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        
        csvFile = open('tweetsextracted.csv', 'a')
        csvWriter = csv.writer(csvFile)

        for tweet in tweepy.Cursor(api.search,q=""+tag,lang="en",since_id='2018-01-06').items():
            hashTasgString=self.getHashTags(tweet)
            mentionedUsersString=self.getMentionedUsers(tweet)
            CreatedDate = parser.parse(str(tweet.created_at))
            print('Original:-',tweet.created_at,'  New:=',CreatedDate)
            result=analyzer.getSentiments(tweet.text)
            mesg={
                "UserId": self.userinfo['UserId'],
                "TagId": 1,
                "CreatedAt":str(str(CreatedDate.month)+'/'+str(CreatedDate.day)+'/'+str(CreatedDate.year)+' '+str(CreatedDate.hour)+':'+str(CreatedDate.minute)+':'+str(CreatedDate.second)),
                "TextMessage": tweet.text,
                "HashTags": hashTasgString,
                "UserMentions": mentionedUsersString,
                "UserName": tweet.user.screen_name,
                "RetweetCount": tweet.retweet_count,
                "FavoriteCount": tweet.favorite_count,
                "NeutralProb": str(result[0]),
                "PositiveProb": str(result[1]),
                "NegativeProb": str(result[2]),
                "Classification": str(result[3])
            }
            print(mesg)
            self.postsentimentdata(mesg)
            csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])


    def beforefetch(self):  
        self.consumer_key = 'Xxq6VUwbaKioNssxYMxGTxR5n'
        self.consumer_secret = self.userinfo['Consumer_Secret']
        self.access_token = self.userinfo['Sccess_Token']
        self.access_token_secret = self.userinfo['Access_Token_Secret']


#tb=TwitterBot(1)
#tb.getusercreds()
#tb.beforefetch()
#tb.getTweets('@Cristiano')
