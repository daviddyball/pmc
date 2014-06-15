import email
from pmc.providers.base import BaseProvider

class TestProvider(BaseProvider):
    def login(self, server, username, password, use_ssl=False, **kwargs):
        return (True,'OK')

    def list_folders(self):
        return ['INBOX','INBOX/People','INBOX/Monitoring']

    def get_messages_in_folder(self, folder):
        return [ self.get_message(folder,p) for p in range(20) ]

    def get_folder_status(self, folder):
        return (20,10)

    def get_message(self, folder, uid):
        return {'uid': 1,
                'folder': folder,
                'flags': ['UNSEEN'],
#                'email': email.email.message_from_string('Date: 2014-01-01\nFrom:Test\nTo:David\nSubject: Message # [{}] -------------------ASDASDASDASDASDASDASDASDASDASDSASDASDRASDASDASD\n\nTest'.format(folder))}
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
From: "renew@USBank.com"<renew@USBank.com>
Content-Type: text/html
Subject: {} ***Renew Your Records***


<FONT face="Courier New" color=#000000 size=2>
<DIV>&nbsp;</DIV>
</FONT>""".format(folder))}
