from IPython import embed_kernel as embed_ipython_kernel
import datetime
import re
import urwid
from pmc.widgets.base import ViewPane

class MessageList(ViewPane):
    def __init__(self,view):
        super(MessageList,self).__init__(view,urwid.SimpleFocusListWalker([]))
        self.messages = self.get_messages('INBOX')
        self.body = urwid.SimpleFocusListWalker(self.messages)
        import ipdb; ipdb.set_trace()

    def get_messages(self, folder):
        messages = []
        for msg in self.view.provider.get_messages_in_folder(folder):
            messages.append(MessageListItem(msg['uid'],
                                            msg['email'],
                                            self.display_message))
        return messages

    def display_message(self, button):
        pass


class MessageListItem(urwid.Button):
    def __init__(self, _id, email, callback):
        super(MessageListItem, self).__init__("")
        self._id = _id
        self._email = email
        self._name = self.get_message_details()
        urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(self._name, 1), 
				None, focus_map='reversed')
        self._w.base_widget.set_wrap_mode('clip')

    def get_message_details(self):
        sender = self._email.get('From')
        subject = self._email.get('Subject')
        send_date = self._email.get('Date')
        return "%s  |  %s  |  %s" % (send_date,sender,subject)
