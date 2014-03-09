import sys
import urwid
from IPython import embed_kernel
from imap_provider import IMAPProvider

class FolderList(urwid.ListBox):
    def __init__(self, main):
        self.main = main
        self.list = self.get_folders()
        super(FolderList,self).__init__(self.list)

    def get_folders(self):
        return urwid.SimpleFocusListWalker([ FolderListItem("Folder %s" % name, self.main) for name in range(1,20) ])


class FolderListItem(urwid.Button):
    def __init__(self, name, main):
        self.main = main
        super(FolderListItem, self).__init__(name)
        urwid.connect_signal(self, 'click', self.open_folder)
        self._w = urwid.AttrMap(urwid.SelectableIcon(name, 1), None, focus_map='reversed')

    def open_folder(self, folder):
        self.main.push_view(MessageList(folder,self.main))


class MessageList(urwid.ListBox):
    def __init__(self, folder, main):
        self.main = main
        self.get_messages(folder)
        super(MessageList,self).__init__(self.msg_list)

    def get_messages(self, folder):
        self.msg_list = urwid.SimpleFocusListWalker([ MessageListItem("Email: %s" % message, main) for message in range(1,20) ])


class MessageListItem(urwid.Button):
    def __init__(self, email, main):
        self.main = main
        super(MessageListItem,self).__init__("")
        urwid.connect_signal(self, 'click', self.open_message)
        self._w = urwid.AttrMap(urwid.SelectableIcon(email, 1), None, focus_map='reversed')

    def open_message(self, email):
        self.main.push_view(MessageView(email,self.main))

class MessageView(urwid.ListBox):
    def __init__(self, email, main):
        self.main = main
        self.message = urwid.SimpleFocusListWalker([ urwid.Text('From:'), urwid.Text('To: '), urwid.Text('Date: '),
                                                     urwid.Text('Subject: '), urwid.Divider(), urwid.Text('Body') ])
        super(MessageView,self).__init__(self.message)

class LoginView(urwid.Filler):
    def __init__(self, main):
        self.main = main
        self.server = urwid.Edit('Server:   ','')
        self.username = urwid.Edit('Username: ','')
        self.password = urwid.Edit('Password: ','',mask='*')
        self.login = urwid.Button('Login',on_press=self.do_login,user_data={'server':self.server.get_edit_text(),
                                                                            'username':self.username.get_edit_text(),
                                                                            'password':self.password.get_edit_text()})
        self.body = urwid.Pile([ self.server,
                                 self.username,
                                 self.password,
                                 self.login ])
        self.focus_item = 0
        super(LoginView,self).__init__(self.body)

    def do_login(self, button, user_data):
        print user_data
        #raise urwid.ExitMainLoop()


class Main(object):
    def __init__(self, **kwargs):
        self.logged_in = False
        self.stack = [LoginView(self)]
        self.frame = urwid.Frame(self.stack[-1],
                                 urwid.Text('Status: '))
        self.loop = urwid.MainLoop(self.frame,
                                   unhandled_input=self.unhandled_input)
        if 'debug' in kwargs:
            if kwargs['debug']:
                embed_kernel()

    def push_view(self, view):
        self.stack.append(view)
        self.update_view()

    def pop_view(self):
        if len(self.stack) > 1:
            self.stack.pop()
            self.update_view()
        else:
            self.frame.get_footer().set_text('Can\' got back any further')

    def update_view(self):
        self.loop.widget.set_body(self.stack[-1])

    def unhandled_input(self, key):
        if key == "<" or key == "b":
            self.pop_view()
        if key == "Q":
            raise urwid.ExitMainLoop()

    def run(self):
        self.loop.run()

if __name__ == '__main__':
    global main
    main = Main(debug=False)
    main.run()
