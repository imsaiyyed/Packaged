# -*- coding: utf-8 -*-

import requests
import json
import pickle
from datetime import datetime
from dateutil import parser
import Configuration.config as config
from Classifiers.nnclassifier import SentimentAnalyzer

class SalesforceBot:
    
    def __init__(self,userid):
        self.userid=userid
    
    def getusercreds(self):
        userinfo=requests.get(config.API_ENDPOINT+'api/metadata/SalesforceDetails?UserId='+str(self.userid))
        userinfo=json.loads(userinfo.text)
        self.userinfo=userinfo[0]
    
    def beforefetch(self): 
        self.clientId=self.userinfo['ClientId']
        self.clientSecret=self.userinfo['ClientSecrete']
        self.username=self.userinfo['UserName']
        self.password=self.userinfo['Password']    
        params = {
                "grant_type": "password",
                "client_id":  self.clientId, # Consumer Key
                "client_secret": self.clientSecret, # Consumer Secret
                "username": self.username, # The email you use to login
                "password": self.password # Concat your password and your security token
            }
        responseData = requests.post("https://login.salesforce.com/services/oauth2/token", params=params)
        responseData=json.loads(responseData.text)
        self.access_token= responseData['access_token']
        self.instance_url=responseData['instance_url']
       
    def getuserlist(self):
        self.userList=requests.get(self.instance_url+'/services/data/v44.0/sobjects/User/', headers={'Authorization': 'Bearer '+self.access_token})
        self.userList=json.loads(self.userList.text)
        self.userList=self.userList['recentItems']
        
    def getcases(self):
        analyzer=SentimentAnalyzer()
        response = requests.get(self.instance_url+'/services/apexrest/Cases', headers={'Authorization': 'Bearer '+self.access_token})
        responseString=str(response.text)
        jsonResponse=json.loads(responseString)
        key='Subject'
        for case in jsonResponse:
            if key in case:
                result=analyzer.getSentiments(case[key])
                CreatedDate = parser.parse(case['CreatedDate'])

                for user in self.userList:
                    if user['Id']==case['OwnerId']:
                        owner=user['Name']
                    break
    
                mesg = {
                    "UserId": self.userinfo['UserId'],
                    "CaseNumber": case['CaseNumber'],
                    "Subject": case['Subject'],
                    "CreatedDate": str(str(CreatedDate.month)+'/'+str(CreatedDate.day)+'/'+str(CreatedDate.year)+' '+str(CreatedDate.hour)+':'+str(CreatedDate.minute)+':'+str(CreatedDate.second)),
                    "IsClosed": case['IsClosed'],
                    "IsEscalated": case['IsEscalated'],
                    "Priority": case['Priority'],
                    "Status":  case['Status'],
                    "Reason":  case['Reason'],
                    "Owner":  owner,
                    "Origin":  case['Origin'],
                    "Product":  case['Product__c'],
                    "NeutralProb": str(result[0]),
                    "PositiveProb": str(result[1]),
                    "NegativeProb": str(result[2]),
                    "Classification": str(result[3])
                }
                if 'ClosedDate' in case:
                    ClosedDate=parser.parse(case['ClosedDate'])
                    mesg['ClosedDate']=str(str(ClosedDate.month)+'/'+str(ClosedDate.day)+'/'+str(ClosedDate.year)+' '+str(ClosedDate.hour)+':'+str(ClosedDate.minute)+':'+str(ClosedDate.second))
                else:
                    mesg['ClosedDate']=""
                self.postSentimentData(mesg)
                print(mesg)

    def postSentimentData(self,mesg):
        headers = {
            'Content-Type': 'application/json',
        }
        resp = requests.post(config.API_ENDPOINT+'api/metadata/SalesforceSentimentData/',
                             headers=headers,
                             data=json.dumps(mesg))
        print(resp.text)
    
    
    
    
    
#sb=SalesforceBot(1)
#sb.getusercreds()
#sb.beforefetch()
#sb.getuserlist()
#sb.getcases()  
    
    
    
#    
#    
#    
#    
#def combine(y1,y2,y3):
#    row_prob=[]
#    for i in range(0,len(y1)):
#        for j in range(0,len(y1[i])):
#            row_prob.append(y1[i][j])
#            row_prob.append(y2[i][j])
#            row_prob.append(y3[i][j])
#        ovr_prob.append(row_prob)
#        row_prob=[]
#
#
#def getSentiment(text):
#    prediction= {"NeutralProb": '', "PositiveProb": '', "NegativeProb": '', "Classification": ''}
#    X1 = nb_vectorizer.transform([text]).toarray()
#    X2 = svm_vectorizer.transform([text]).toarray()
#    X3 = lr_vectorizer.transform([text]).toarray()
#
#    nb_pred = nb_classifier.predict_proba(X1)
#    svm_pred = svm_classifier.predict_proba(X2)
#    lr_pred = lr_classifier.predict_proba(X3)
#
#    combine(nb_pred, svm_pred, lr_pred)
#
#    probabilityPred=svm_classifier_top.predict_proba(ovr_prob)
#    classPred = svm_classifier_top.predict(ovr_prob)
#    # print(probabilityPred[0][0],probabilityPred[0][1])
#    # print(classPred)
#    prediction=(probabilityPred[0][0], probabilityPred[0][1], probabilityPred[0][2], classPred[0])
#    ovr_prob.clear()
#    return prediction
#
#
#
#userInfo=requests.get('https://einterceptorapi.azurewebsites.net/api/metadata/SalesforceDetails')
## userInfo=json.loads(userInfo.text[0])
#userInfo=json.loads(userInfo.text)
## print(userInfo[0]['UserName'])
#
#
#clientId=userInfo[0]['ClientId']
#clientSecret=userInfo[0]['ClientSecrete']
#username=userInfo[0]['UserName']
#password=userInfo[0]['Password']
#
#params = {
#    "grant_type": "password",
#    "client_id": clientId, # Consumer Key
#    "client_secret": clientSecret, # Consumer Secret
#    "username": username, # The email you use to login
#    "password": password # Concat your password and your security token
#}
#responseData = requests.post("https://login.salesforce.com/services/oauth2/token", params=params)
## print(responseData.text)
#responseData=json.loads(responseData.text)
#access_token= responseData['access_token']
#instance_url=responseData['instance_url']
## print(responseData)
#userList=requests.get(instance_url+'/services/data/v44.0/sobjects/User/', headers={'Authorization': 'Bearer '+access_token})
#userList=json.loads(userList.text)
#userList=userList['recentItems']
#print(userList)
#response = requests.get(instance_url+'/services/apexrest/Cases', headers={'Authorization': 'Bearer '+access_token})
## print(response.text)
#responseString=str(response.text)
#jsonResponse=json.loads(responseString)
#key='Subject'
## print(jsonResponse)
#
#
#def postSentimentData(mesg):
#    headers = {
#        'Content-Type': 'application/json',
#    }
#    resp = requests.post('https://einterceptorapi.azurewebsites.net/api/metadata/SalesforceSentimentData/',
#                         headers=headers,
#                         data=json.dumps(mesg))
#
#for case in jsonResponse:
#    if key in case:
#        result=getSentiment(case[key])
#        CreatedDate = parser.parse(case['CreatedDate'])
#
#        for user in userList:
#            if user['Id']==case['OwnerId']:
#                owner=user['Name']
#                break
#
#        mesg = {
#            "UserId": userInfo[0]['UserId'],
#            "CaseNumber": case['CaseNumber'],
#            "Subject": case['Subject'],
#            "CreatedDate": str(str(CreatedDate.month)+'/'+str(CreatedDate.day)+'/'+str(CreatedDate.year)+' '+str(CreatedDate.hour)+':'+str(CreatedDate.minute)+':'+str(CreatedDate.second)),
#            "IsClosed": case['IsClosed'],
#            "IsEscalated": case['IsEscalated'],
#            "Priority": case['Priority'],
#            "Status":  case['Status'],
#            "Reason":  case['Reason'],
#            "Owner":  owner,
#            "Origin":  case['Origin'],
#            "Product":  case['Product__c'],
#            "NeutralProb": str(result[0]),
#            "PositiveProb": str(result[1]),
#            "NegativeProb": str(result[2]),
#            "Classification": str(result[3])
#        }
#        if 'ClosedDate' in case:
#            ClosedDate=parser.parse(case['ClosedDate'])
#            mesg['ClosedDate']=str(str(ClosedDate.month)+'/'+str(ClosedDate.day)+'/'+str(ClosedDate.year)+' '+str(ClosedDate.hour)+':'+str(ClosedDate.minute)+':'+str(ClosedDate.second))
#        else:
#            mesg['ClosedDate']=""
#
#        postSentimentData(mesg)
#        print(mesg)
#
#
#
