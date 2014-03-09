import datetime
import getpass
import urwid
from imap_provider import IMAPProvider

class FolderListItem(urwid.Button):
    def  __init__(self, name):
        super(FolderListItem, self).__init__("")
        urwid.connect_signal(self, 'click', self.update_label, folder)
        self._w = urwid.AttrMap(urwid.SelectableIcon(name, 1), None, focus_map='reversed')

    def update_label(self, user_data):
        self.label = '%s-1' % self.label

class MessageListItem(urwid.Button):
    def __init__(self, _id, email):
        super(MessageListItem, self).__init__("")
        self._id = _id
        self._email = email
        self._name = self.get_message_details()
        urwid.connect_signal(self, 'click', update_message_view, self._email)
        self._w = urwid.AttrMap(urwid.SelectableIcon(self._name, 1), None, focus_map='reversed')

    def get_message_details(self):
        sender = self._email['From']
        subject = self._email['Subject']
        send_date = self._email['Date']
        return "%s|%s|%s" % (type(send_date),sender,subject)

def update_message_list(widget,folder):
    status_bar.set_text("Switching to folder: %s" % folder)
    while len(message_list.original_widget.body) > 0:
        message_list.original_widget.body.pop()
    for message in provider.get_messages_in_folder(folder):
        message_list.original_widget.body.append(MessageListItem(message['uid'],message['email']))

def update_message_view(_id,email):
    status_bar.set_text("Viewing Message ID: %s" % _id)
    while len(message_view.original_widget.body) > 0:
        message_view.original_widget.body.pop()
    for n in range(1,10):
        message_view.original_widget.body.append(urwid.Text("%s" % email))

def unhandled_input(key):
    if key == 'ctrl q':
        raise urwid.EndMainLoop()

global provider
global status_bar
global folder_list
global message_list
global message_view
global message_pane
global columns

provider = IMAPProvider('mail.tangentlabs.co.uk','david.dyball@tangentlabs.co.uk',getpass.getpass(),use_ssl=True)

folder_list = urwid.LineBox(urwid.ListBox(urwid.SimpleFocusListWalker([ FolderListItem(folder) for folder in provider.list_folders() ])),title='Folders')
message_list = urwid.LineBox(urwid.ListBox(urwid.SimpleFocusListWalker([])),title='Message List')
message_view = urwid.LineBox(urwid.ListBox(urwid.SimpleFocusListWalker([])),title='Message View')
message_pane = urwid.Pile([("weight",1,message_list),("weight",1,message_view)])
columns = urwid.Columns([("weight",2,folder_list),("weight",4,message_pane)],dividechars=0)
status_bar = urwid.Text("Status:")
frame = urwid.Frame(columns,footer=status_bar)


main_loop = urwid.MainLoop(urwid.Frame(columns,footer=status_bar),palette=[('reversed','standout','')])

main_loop.run()
#except:
#    import ipdb
#    ipdb.set_trace()
