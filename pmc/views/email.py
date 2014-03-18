from IPython import embed_kernel as embed_ipython_kernel
import urwid
import sys
from pmc.widgets import *

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


        self.folder_list = urwid.LineBox(FolderListBox(self))
        self.message_list = urwid.LineBox(MessageListBox(self))
        self.message_view = urwid.LineBox(MessageViewBox(self))
        self.columns = urwid.Columns([])
        self.message_pane = urwid.Pile([])
        self.footer = urwid.Text('')
        self.rebuild_view()
        super(EmailView, self).__init__(self.body,footer=self.footer)

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
            self.folder_list.toggle_view()
            self.set_status('Folder-List Toggled (%s)' % self.folder_list.base_widget.show)
        elif key == "ctrl l":
            self.message_list.toggle_view()
            self.set_status('Message-List Toggled (%s)' % self.message_list.base_widget.show)
        elif key == "ctrl v":
            self.message_view.toggle_view()
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
        self.main.loop.screen.stop()
        import ipdb; ipdb.set_trace()
        self.main.loop.screen.start()
        #self.set_focus_path(['body',0,0])

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
        self.set_focus_path(['body',1,0])

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
        self.set_focus_path(['body',1,1])

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
