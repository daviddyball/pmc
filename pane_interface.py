from IPython import embed_kernel as embed_ipython_kernel
import datetime
import getpass
import urwid
import sys
from imap_provider import IMAPProvider

class ViewPane(urwid.ListBox):
    def __init__(self, view, body):
        """
        :param view: A reference to the parent view
        :type view: instance(EmailView)
        """
        self.view = view
        self.show = True
        super(ViewPane, self).__init__(body)

    def toggle_view(self):
        if self.show:
            self.show = False
        else:
            self.show = True


class FolderListBox(ViewPane):
    def __init__(self, view):
        """
        Widget to display a list of email folders

        :param view: A reference to the current view owning this widget
        :type view: an urwid.Widget

        :returns: instance of FolderListBox widget
        :type: urwid.Widget
        """
        self.body = urwid.SimpleFocusListWalker([])
        super(FolderListBox,self).__init__(view, self.body)
        self.body = urwid.SimpleFocusListWalker(self.get_folders())

    def get_folders(self):
        """
        Retrieve a list of IMAP folders from self.view.provider

        :returns: A list of FolderListItem instances
        :rtype: [ FolderListItem(), ]
        """
        folders = self.view.provider.list_folders()
        self.folders = [FolderListItem(folder,self.view_folder) for folder in folders]
        return self.folders

    def view_folder(self, folder):
        """
        Open a folders contents in FolderListBox
        
        :param folder: The button triggering this callback
        :type folder: pmc.FolderListItem
        """
        self.view.set_status('%s Opened' % folder.folder)
        self.reset_selections()
        folder.select()

    def reset_selections(self):
        """
        Iterate through the available folders and reset their
        font settings/highlighting
        """
        for folder in self.body:
            folder.deselect()


class FolderListItem(urwid.Button):
    def  __init__(self, folder, callback):
        """
        Folder Item for display in FolderListBox

        :param folder: Name of the folder this object represents
        :type folder: str

        :param callback: Function to call when clicked
        :type callback: function

        :returns: Instance
        :rtype: pmc.FolderListItem
        """
        super(FolderListItem, self).__init__(folder)
        self.folder = folder
        urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(folder, 2), None,
				'highlighted')

    def select(self):
        """
        Toggle the font settings for this folder item so it shows
        as selected (bold)
        """
        self.set_label(self.folder)

    def deselect(self):
        """
        Toggle the font settings for this folder item so it shows
        as normal
        """
        self.set_label(('reversed',self.folder))


class MessageListBox(ViewPane):
    def __init__(self,view):
        super(MessageListBox,self).__init__(view,urwid.SimpleFocusListWalker([]))
        self.messages = self.get_messages('INBOX')
        self.body = urwid.SimpleFocusListWalker(self.messages)

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

    def get_message_details(self):
        sender = self._email.get('From')
        subject = self._email.get('Subject')
        send_date = self._email.get('Date')
        return "%s  |  %s  |  %s" % (type(send_date),sender,subject)


class MessageViewBox(ViewPane):
    def __init__(self,view):
        self.view = view
        self.body = urwid.SimpleFocusListWalker([])
        super(MessageViewBox,self).__init__(view,self.body)

class View(urwid.Frame):
    def __init__(self, main):
        self.main = main
    
    def unhandled_input(self, key):
        pass

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
        """
        EmailView
        :param main: pmc.Main() object
        :param provider: IMAPProvider() object
        """
        self.main = main
        self.provider = provider
        self.logged_in = True


        self.footer = urwid.Text('')
        self.folder_list = urwid.LineBox(FolderListBox(self))
        self.message_list = urwid.LineBox(MessageListBox(self))
        self.message_view = urwid.LineBox(MessageViewBox(self))
        self.columns = urwid.Columns([])
        self.message_pane = urwid.Pile([])
        self.rebuild_view()
        super(EmailView, self).__init__(self.body,urwid.Text('Hotkeys:'),self.footer)

    def keypress(self, size, key):
        """
        Handle Keypresses or pass to super.keypress()
        """
        if key == "v":
            self.focus_messageview()
            self.set_status('Message View Focused')
        elif key == "f":
            self.focus_folderlist()
            self.set_status('Folder-List Focused')
        elif key == "l":
            self.focus_messagelist()
            self.set_status('Message-List Focused')
        elif key == "ctrl f":
            self.folder_list.base_widget.toggle_view()
            self.set_status('Folder-List Toggled (%s)' % self.folder_list.base_widget.show)
        elif key == "ctrl l":
            self.message_list.base_widget.toggle_view()
            self.set_status('Message-List Toggled (%s)' % self.message_list.base_widget.show)
        elif key == "ctrl v":
            self.message_view.base_widget.toggle_view()
            self.set_status('Message View Toggled (%s)' % self.message_view.base_widget.show)
        else:
            return super(EmailView,self).keypress(size,key)

        self.rebuild_view()
        self._invalidate()

    def focus_folderlist(self):
        """
        Set Focus to the FolderListBox Widget

        - Toggle Folder list if hidden
        - Set EmailView focus to body
        - Set LHS columns focus to Folder List
        """
        if not self.folder_list.base_widget.show:
            self.folder_list.base_widget.show = True
            self.rebuild_view()
        self.focus_item = self.body
        self.columns.set_focus(self.folder_list)

    def focus_messagelist(self):
        """
        Set Focus to the MessageListBox Widget

        - Toggle Message list if hidden
        - Set EmailView focus to body
        - Set RHS columns focus to Message List
        """
        if not self.message_list.base_widget.show:
            self.message_list.base_widget.show = True
            self.rebuild_view()
        self.focus_item = self.body
        self.columns.set_focus(self.message_pane)
        self.message_pane.set_focus(self.message_list)

    def focus_messageview(self):
        """
        Set Focus to the MessageViewBox Widget

        - Toggle Message view if hidden
        - Set EmailView focus to body
        - Set RHS columns focus to Message view
        """
        if not self.message_view.base_widget.show:
            self.message_view.base_widget.show = True
            self.rebuild_view()
        self.focus_item = self.body
        self.columns.set_focus(self.message_pane)
        self.message_pane.set_focus(self.message_view)

    def set_status(self, message):
        """
        Update Status Bar Message

        :param message: (str) Message to display
        """
        self.footer.set_text(message)

    def view_folder(self, folder):
        """
        Display contents of :param folder: in MessageListBox

        :param folder: Folder to display the contents of
        :type folder: str
        """
        pass

    def toggle_messagelist(self):
        """
        Show/Hide the MessageListBox widget
        """
        self.message_list.toggle_view()
        self.rebuild_view()

    def toggle_folderlist(self):
        """
        Show/Hide the FolderListBox widget
        """
        self.folder_list.toggle_view()
        self.rebuild_view()

    def toggle_messageview(self):
        """
        Show/Hide the MessageViewBox widget
        """
        self.message_view.toggle_view()
        self.rebuild_view()

    def rebuild_view(self):
        """
        Rebuild the pane interface showing/hiding
        items depending on toggled status
        """

        self.message_pane = urwid.Pile([])
        if self.message_list.base_widget.show:
            self.message_pane.contents.append((self.message_list,
                                               self.message_pane.options('weight',1)))
        if self.message_view.base_widget.show:
            self.message_pane.contents.append((self.message_view,
                                               self.message_pane.options("weight",1)))
        self.columns.contents = []
        self.columns.contents.insert(0,(self.message_pane,
                                        self.columns.options("weight",2)))
        if self.folder_list.base_widget.show:
            self.columns.contents.insert(0,(self.folder_list,
                                         self.columns.options("weight",1)))
        self.body = self.columns


class Main(object):
    def __init__(self, **kwargs):
        """
        pmc.Main Application Object

        :param debug: Whether to enable ipython kernel
        :type debug: bool
        """
        self.palette = [('reversed',    'standout',''),
                        ('normal',      'white','black'),
                        ('highlighted', 'black','white'),
                        ]
        self.stack = [LoginView(self)]
        self.loop = urwid.MainLoop(self.stack[-1],self.palette,
                                   unhandled_input=self.unhandled_input)
        if 'debug' in kwargs:
            if kwargs['debug']:
                embed_ipython_kernel()

    def push_view(self, view):
        """
        Add View object to main application stack

        :param view: View to add to the stack
        :type view: urwid.Widget()
        """
        self.stack.append(view)
        self.update_view()

    def pop_view(self):
        """
        Remove top-most widget off of the stack
        """
        self.stack.pop()
        self.update_view()

    def update_view(self):
        """
        Set Main.body to the top-most widget in the stack
        """
        if len(self.stack) < 1:
            raise urwid.ExitMainLoop()
            print "Stack Empty. Exiting...."
        self.loop.widget.set_body(self.stack[-1])

    def unhandled_input(self, key):
        """
        Capture and process key-input

        :param key: key pressed
        :type key: str
        """
        if key == "Q":
            raise urwid.ExitMainLoop()
            print "User Initiated Quit. Exiting...."

    def run(self):
        """
        Run the Main application
        """
        self.loop.run()


if __name__ == '__main__':
    debug = False
    if '-d' in sys.argv:
        debug=True
    Main(debug=debug).run()
