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
