from IPython import embed_kernel as embed_ipython_kernel
import urwid
import sys
from pmc.widgets.folderlist import FolderList
from pmc.widgets.messagelist import MessageList
from pmc.widgets.messageview import MessageView
from pmc.widgets.statusbar import StatusBar

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


        self.folder_list = FolderList(self)
        self.message_list = MessageList(self)
        self.message_view = MessageView(self)
        self.columns = urwid.Columns([])
        self.message_pane = urwid.Pile([])
        self.status_bar = StatusBar(self,'','')
        self.footer= self.status_bar
        self.rebuild_view()
        super(EmailView, self).__init__(self.body,footer=self.footer)

    def keypress(self, size, key):
        """
        Handle Keypresses or pass to super.keypress()
        """
        if key == ":":
            self.start_command()
        #elif key == "v":
        #    self.focus_messageview()
        #    self.set_status('Message View Focused')
        #elif key == "f":
        #    self.focus_folderlist()
        #    self.set_status('Folder-List Focused')
        #elif key == "l":
        #    self.focus_messagelist()
        #    self.set_status('Message-List Focused')
        #
        #elif key == "ctrl up":
        #elif key == "ctrl down":
        #elif key == "ctrl left":
        #elif key == "ctrl right":
        elif key == "ctrl f":
            self.folder_list.toggle_view()
            self.rebuild_view()
            self.set_status('Folder-List Toggled (%s)' % self.folder_list.show)
        elif key == "ctrl l":
            self.message_list.toggle_view()
            self.rebuild_view()
            self.set_status('Message-List Toggled (%s)' % self.message_list.show)
        elif key == "ctrl v":
            self.message_view.toggle_view()
            self.rebuild_view()
            self.set_status('Message View Toggled (%s)' % self.message_view.show)
        elif key == "/":
            self.trigger_search()
        elif key == "?":
            self.trigger_search(reverse=True)
        else:
            return super(EmailView,self).keypress(size,key)

        self._invalidate()

    def focus_folderlist(self):
        """
        Set Focus to the FolderListBox Widget

        - Toggle Folder list if hidden
        - Set EmailView focus to body
        - Set LHS columns focus to Folder List
        """
        if not self.folder_list.show:
            self.folder_list.show = True
            self.rebuild_view()
        self.set_focus_path(['body',0,0])

    def focus_messagelist(self):
        """
        Set Focus to the MessageListBox Widget

        - Toggle Message list if hidden
        - Set EmailView focus to body
        - Set RHS columns focus to Message List
        """
        if not self.message_list.show:
            self.message_list.show = True
            self.rebuild_view()
        self.set_focus_path(['body',1,0])

    def focus_messageview(self):
        """
        Set Focus to the MessageViewBox Widget

        - Toggle Message view if hidden
        - Set EmailView focus to body
        - Set RHS columns focus to Message view
        """
        if not self.message_view.show:
            self.message_view.show = True
            self.rebuild_view()
        self.set_focus_path(['body',1,1])

    def set_status(self, message):
        """
        Update Status Bar Message

        :param message: (str) Message to display
        """
        self.footer.set_caption(message)

    def view_folder(self, folder):
        """
        Display contents of :param folder: in MessageListBox

        :param folder: Folder to display the contents of
        :type folder: str
        """
        self.message_list.get_messages(folder)
        self.focus_message_list()

    def view_message(self, message_id):
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
        if self.message_list.show:
            self.message_pane.contents.append((urwid.LineBox(self.message_list),
                                               self.message_pane.options('weight',1)))
        if self.message_view.show:
            self.message_pane.contents.append((urwid.LineBox(self.message_view),
                                               self.message_pane.options("weight",1)))
        self.columns.contents = []
        self.columns.contents.insert(0,(self.message_pane,
                                        self.columns.options("weight",2)))
        if self.folder_list.show:
            self.columns.contents.insert(0,(urwid.LineBox(self.folder_list),
                                         self.columns.options("weight",1)))
        self.body = self.columns

    def get_focused_widget(self):
        """
        Iterate across the focus path and return the in-focus
        widget
        """
        w = self.body
        for p in self.body.get_focus_path():
            if p != w.focus_position:
                w.focus_position = p
            if not issubclass(type(w.focus.base_widget), urwid.WidgetContainerMixin):
                break
            w = w.focus.base_widget
        return w

    def trigger_search(self, reverse=False):
        """
        Start a search operation by determining the in-focus widget and
        setting focus to self.status_bar (urwid.Edit), passing in the in-focus
        widgets "search" function.
        """
        # Retrieve the current in-focus widget 
        w = self.get_focused_widget()
        if reverse:
            if getattr(w,'reverse_search',None) is None:
                return
            callback = w.reverse_search
        else:
            if getattr(w,'search',None) is None:
                return
            callback = w.search

        self.status_bar.get_user_input(w.search_caption,'',
                                       callback)
            

    def start_command(self):
        """
        Toggle command mode, get input to pass to run_command()
        """
        key = self.status_bar.get_user_input('Command: ','',
                                             self.run_command)

    def run_command(self, command):
        """
        Run :param command:
        """
        self.set_status('({})'.format(command))
