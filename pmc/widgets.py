from IPython import embed_kernel as embed_ipython_kernel
import datetime
import urwid

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

class SearchBox(urwid.Edit):
    """
    Search pane, context specific
    """
    def __init__(self, caption='', edit_text='',callback=None):
        self.callback = callback
        super(SearchBox,self).__init__(caption,edit_text)

    def set_edit_text(self, text):
        if text.endswith('\n'):
            if self.callback is not None:
                self.callback(text)
        else:
            super(SearchBox,self).set_edit_text(text)
