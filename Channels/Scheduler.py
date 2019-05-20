# -*- coding: utf-8 -*-
import sys
from  Channels import ExchangeAnalysis
from  Channels import TwitterAnalysis
from  Channels import SalesforceAnalysis



class Scheduler:
    def __init__(self):
        self.userid=sys.argv[1]
        es=ExchangeAnalysis.ExchangeServer(self.userid)
        es.getusercreds()
        es.beforefetch()           
        print('Exchange mails gathered')
        tb=TwitterAnalysis.TwitterBot(self.userid)
        tb.getusercreds()
        tb.beforefetch()
        tb.getTweets('@Cristiano')
        print('Twitter tweets gathered')
        sb=SalesforceAnalysis.SalesforceBot(self.userid)
        sb.getusercreds()
        sb.beforefetch()
        sb.getuserlist()
        sb.getcases()  
        print('Salesforce cases gathered')

#sc=Scheduler()