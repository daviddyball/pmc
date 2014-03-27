import email

class TestProvider(object):
    def login(self, server, username, password, use_ssl=False, **kwargs):
        return (True,'OK')

    def list_folders(self):
        return ['INBOX','INBOX/People','INBOX/Monitoring']

    def get_messages_in_folder(self, folder):
        return [ self.get_message(p,p) for p in range(20) ]

    def get_folder_status(self, folder):
        return (20,10)

    def get_message(self, folder, uid):
        return {'uid': 1,
                'folder': folder,
                'flags': ['UNSEEN'],
                #'email': email.email.message_from_string('Date: 2014-01-01\nFrom:Test\nTo:David\nSubject: Meesage #{}-------------------ASDASDASDASDASDASDASDASDASDASDSASDASDRASDASDASD\n\nTest'.format(folder))}
                'email': email.email.message_from_string("""Return-path: <root@pointi.com>
Envelope-to: my*address@mydomain.com
Delivery-date: Thu, 29 Jul 2004 10:30:16 -0400
Received: from [211.174.58.68] (helo=pointi.com)
    by star.deerfieldhosting.net with esmtp (Exim 4.34 (FreeBSD))
    id 1BqBvD-000D14-TV
    for my*address@mydomain.com; Thu, 29 Jul 2004 10:30:16 -0400
Received: from pointi.com (localhost [127.0.0.1])
    by pointi.com (8.12.11/8.12.11) with ESMTP id i6TEUN5T021884
    for <my*address@mydomain.com>; Thu, 29 Jul 2004 23:30:24 +0900
Received: (from root@localhost)
    by pointi.com (8.12.11/8.12.11/Submit) id i6TEUNPB021882;
    Thu, 29 Jul 2004 23:30:23 +0900
Date: Thu, 29 Jul 2004 23:30:23 +0900
Message-Id: <200407291430.i6TEUNPB021882@pointi.com>
To: my*address@mydomain.com
Subject: ***Renew Your Records***
From: "renew@USBank.com"<renew@USBank.com>
Content-Type: text/html


<FONT face="Courier New" color=#000000 size=2>
<DIV><B>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp; </B><FONT 

size=3><B>Dear U.S. Bank valued membe</B>r,</FONT></DIV>
<DIV>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Due to concerns, for the safety and 

integrity of the Internet Banking community we have</DIV>
<DIV>issued this warning message.</DIV>
<DIV>&nbsp;</DIV>
<DIV>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; It has come to our attention that your 

account information needs to be updated due to</DIV>
<DIV>inactive accounts, frauds and spoof reports. If you could please take 5-10 

minutes out of</DIV> 
<DIV>your online experience and renew your records you will not run into any future 

problems</DIV>
<DIV>with the online service. However, failure to update your records will result in 

account</DIV>
<DIV>deletation. </DIV>
<DIV>&nbsp;</DIV>
<DIV>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Once you have updated your account records 

your online banking account will not be</DIV>
<DIV>interrupted and will continue as normal.</DIV> 
<DIV>&nbsp;</DIV>
<DIV>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp; Please 

follow the link below and renew your account information.</DIV>
<DIV>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <A
href="http://www.akhlesh.com/stats/.access/requestCmdId/USBank/internet
Banking/DisplayLoginPage/RequestRouter/"><FONT
color=#0000ff><U>http://www.usbank.com/cgi_w/cfm/personal/account_access/
account_access.cfm</U></FONT></A></DIV>
<DIV>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </DIV>
<DIV><FONT 

size=3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&n

bsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <U><B>U.S. Bank Internet 

Banking</B></U></FONT></DIV>
<DIV>&nbsp;</DIV>
</FONT>""")}
