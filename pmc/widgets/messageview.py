from IPython import embed_kernel as embed_ipython_kernel
import datetime
import re
import urwid
from pmc.widgets.base import ViewPane

class MessageView(ViewPane):
    def __init__(self,view):
        self.view = view
        self.body = urwid.SimpleFocusListWalker([])
        super(MessageView,self).__init__(view,self.body)

    def set_content(self, message):
        headers = [ MessageHeaderLine(p[0],p[1]) for p in message['email'].items()]
        body = [ MessageBodyLine(message['email'].get_payload()) ]
        self.body = urwid.SimpleFocusListWalker(headers + body)

class MessageHeaderLine(urwid.Button):
    def __init__(self, key, value):
        super(MessageHeaderLine, self).__init__("%s %s" % (key, value))

class MessageBodyLine(urwid.Button):
    def __init__(self, text):
        super(MessageBodyLine, self).__init__(text)
