from exchangelib import DELEGATE, Account, Credentials,IMPERSONATION,ServiceAccount,Configuration
from bs4 import BeautifulSoup
import Configuration.config as config
import requests
import json
import Utilities.utilities as utility
from Classifiers.nnclassifier import SentimentAnalyzer
import csv
from datetime import datetime
class ExchangeServer:
    def __init__(self,userid):
        self.userid=userid
        
    def getusercreds(self):
        userInfo=requests.get(config.API_ENDPOINT+'api/metadata/ExchangeServerDetails?UserId='+str(self.userid))
        userInfo=json.loads(userInfo.text)
        self.userinfo=userInfo[0]
    
    def postsentimentdata(self,email):
        headers = {
                'Content-Type': 'application/json'
                }
        resp = requests.post(config.API_ENDPOINT+'api/metadata/exchangeData',headers=headers,data=json.dumps(email))
        print(resp.text)
        
    def __fetchmails(self,emaillist):
        csvFile = open('tweetsextracted.csv', 'a')
        csvWriter = csv.writer(csvFile)
        analyzer=SentimentAnalyzer()
        for email in emaillist:
            account = Account(primary_smtp_address=email['Email'], credentials=self.usercreds,autodiscover=False,config=self.config, access_type=IMPERSONATION)
            for item in account.inbox.all().order_by('-datetime_received'):
                local_datetime_received=utility.utc_to_local(item.datetime_received)
                
                datetime_received=datetime.strptime(utility.datetimeconverter(item.datetime_received), '%Y-%m-%d %H:%M:%S%z')
                local_datetime_received=datetime.strptime(utility.datetimeconverter(local_datetime_received), '%Y-%m-%d %H:%M:%S%z')
                
                datetime_received=str(str(datetime_received.month)+'/'+str(datetime_received.day)+'/'+str(datetime_received.year)+' '+str(datetime_received.hour)+':'+str(datetime_received.minute)+':'+str(datetime_received.second))
                local_datetime_received=str(str(local_datetime_received.month)+'/'+str(local_datetime_received.day)+'/'+str(local_datetime_received.year)+' '+str(local_datetime_received.hour)+':'+str(local_datetime_received.minute)+':'+str(local_datetime_received.second))
                tolist=[]
                cclist=[]
                for reciepent in item.to_recipients:
                    tolist.append(reciepent.email_address)
                if item.cc_recipients:
                    for ccreciepent in item.cc_recipients:
                        cclist.append(ccreciepent.email_address)
                body=str(item.text_body)
                body=body.replace('\r\n','')
                
                resultbody=analyzer.getSentiments(body)
                resultsubject=analyzer.getSentiments(item.subject)
                sentiment=self.__getsentiment(resultbody)
                email={
                        "Subject":item.subject,
                        "Body":body,
                        "ConversationId":item.conversation_id.id,
                        "From":item.sender.email_address,
                        "ReceivedDate":datetime_received,
                        "LocalReceivedDate":local_datetime_received,
                        "ToList":",".join(tolist),
                        "CCList":",".join(cclist),
                        "NeutralProbBody": str(resultbody[0]),
                        "PositiveProbBody": str(resultbody[1]),
                        "NegativeProbBody": str(resultbody[2]),
                        "NeutralProbSubject": str(resultsubject[0]),
                        "PositiveProbSubject": str(resultsubject[1]),
                        "NegativeProbSubject": str(resultsubject[2]),
                        "Classification": str(resultbody[3]),
                        "Sentiment":sentiment
                        }
                self.postsentimentdata(email)
                csvWriter.writerow([email])
                break
            break

    def beforefetch(self):
        self.usercreds=ServiceAccount(
                username=self.userinfo['ServiceAccountEmail'],  # Or myusername@example.com for O365
                password=self.userinfo['ServiceAccountPassword'])
        self.config = Configuration(server='outlook.office365.com', credentials=self.usercreds)

        emaillist=requests.get(config.API_ENDPOINT+'api/metadata/emaillist?UserId='+str(self.userid))
        emaillist=json.loads(emaillist.text)
        self.__fetchmails(emaillist)
        
    
    def __getsentiment(self,proba):
        if proba[3]==0:
            return "Neutral"
        elif proba[3]==1:
            return "Positive"
        else:
            return "Negative"
    

    
#    es=ExchangeServer(1)
#    es.getusercreds()
#    data=es.beforefetch()
