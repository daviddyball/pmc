from IPython import embed_kernel as embed_ipython_kernel
import datetime
import getpass
import urwid
import sys
from imap_provider import IMAPProvider

class FolderListBox(urwid.ListBox):
    def __init__(self, view):
        self.view = view
        self.body = urwid.SimpleFocusListWalker(self.get_folders())
        super(FolderListBox,self).__init__(self.body)

    def get_folders(self):
        folders = self.view.provider.list_folders()
        self.folders = [FolderListItem(folder,self.view_folder) for folder in folders]
        return self.folders


class FolderListItem(urwid.Button):
    def  __init__(self, folder, callback)
        self.name = folder
        self.callback = callback
        urwid.connect_signal(self, 'click', self.open_folder)
        self._w = urwid.AttrMap(urwid.SelectableIcon(name, 1), None,
				focus_map='reversed')
        super(FolderListItem, self).__init__(self.name)

    def open_folder(self, button):
        self.

    def update_label(self, user_data):
        self.set_label('%s-1' % self.label)


class MessageListBox(urwid.ListBox):
    def __init__(self,view):
        self.view = view
        self.body = urwid.SimpleFocusListWalker([])
        super(MessageListBox,self).__init__(self.body)


class MessageListItem(urwid.Button):
    def __init__(self, _id, email):
        super(MessageListItem, self).__init__("")
        self._id = _id
        self._email = email
        self._name = self.get_message_details()
        urwid.connect_signal(self, 'click', update_message_view,
			     self._email)
        self._w = urwid.AttrMap(urwid.SelectableIcon(self._name, 1), 
				None, focus_map='reversed')

    def get_message_details(self):
        sender = self._email['From']
        subject = self._email['Subject']
        send_date = self._email['Date']
        return "%s|%s|%s" % (type(send_date),sender,subject)


class MessageViewBox(urwid.ListBox):
    def __init__(self,view):
        self.view = view
        self.body = urwid.SimpleFocusListWalker([])
        super(MessageViewBox,self).__init__(self.body)


class LoginView(urwid.Frame):
    def __init__(self, main):
        self.main = main
        self.server = urwid.Edit('','mail.tangentlabs.co.uk')
        self.username = urwid.Edit('','david.dyball@tangentlabs.co.uk')
        self.password = urwid.Edit(mask='*')
        self.login_button = urwid.Button('Login',on_press=self.do_login)
        self.footer = urwid.Text('Status:')
        self.labels = urwid.Pile([ urwid.Text('Server Name:',align="right"),
                                   urwid.Text('Username:',align="right"),
                                   urwid.Text('Password:',align="right")])
        self.edits  = urwid.Pile([ self.server,
                                   self.username,
                                   self.password,
                                   self.login_button])
        self.body = urwid.Filler(urwid.Columns([self.labels,urwid.Padding(self.edits)],
                                                dividechars=1))
        super(LoginView, self).__init__(self.body,footer=self.footer)        

    def do_login(self, button):
        # Validate Fields
        if self.server.edit_text in (None,''):
            self.set_status('ERROR: Server Name is Required')
            self.body.focus_item = self.server
        elif self.username.edit_text in (None,''):
            self.set_status('ERROR: Username is Required')
            self.dialog.focus_item = self.username
        elif self.password in (None,''):
            self.set_status('ERROR: Password is Required')
            self.dialog.focus_item = self.password
        else:
            self.provider = IMAPProvider()
            (result, msg) = self.provider.login(self.server.edit_text,
                                                self.username.edit_text,
                                                self.password.edit_text)
            if result:
                self.main.push_view(EmailView(self.main,self.provider))
            else:
                self.set_status('ERROR: %s' % msg)
                del(self.provider)

    def set_status(self, message):
        self.footer.set_text(message)

     
class EmailView(urwid.Frame):
    def __init__(self, main, provider):
        self.main = main
        self.provider = provider
        self.logged_in = True
        self.footer = urwid.Text('')
        self.folder_list = urwid.LineBox(FolderListBox(self))
        self.message_list = urwid.LineBox(MessageListBox(self))
        self.message_view = urwid.LineBox(MessageViewBox(self))
        self.message_pane = urwid.Pile([("weight",1,self.message_list),
                                        ("weight",1,self.message_view)])
        self.columns = urwid.Columns([("weight",1,self.folder_list),
                                      ("weight",2,self.message_pane)])
        self.body = self.columns
        super(EmailView, self).__init__(self.body,urwid.Text('Hotkeys:'),self.footer)

    def set_status(self, message):
        self.footer.set_text(message)

    def view_folder(self, folder):
        pass


class Main(object):
    def __init__(self, **kwargs):
        self.palette = [('reversed','standout','')]
        self.stack = [LoginView(self)]
        self.loop = urwid.MainLoop(self.stack[-1],
                                   unhandled_input=self.unhandled_input)
        if 'debug' in kwargs:
            if kwargs['debug']:
                embed_ipython_kernel()

    def push_view(self, view):
        self.stack.append(view)
        self.update_view()

    def pop_view(self):
        self.stack.pop()
        self.update_view()

    def update_view(self):
        if len(self.stack) < 1:
            raise urwid.ExitMainLoop()
            print "Stack Empty. Exiting...."
        self.loop.widget.set_body(self.stack[-1])

    def unhandled_input(self, key):
        if key == "Q":
            raise urwid.ExitMainLoop()
            print "User Initiated Quit. Exiting...."

    def run(self):
        self.loop.run()


if __name__ == '__main__':
    debug = False
    if '-d' in sys.argv:
        debug=True
    Main(debug=debug).run()
