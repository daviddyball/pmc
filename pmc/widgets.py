from IPython import embed_kernel as embed_ipython_kernel
import datetime
import re
import urwid

class ViewPane(urwid.ListBox):
    def __init__(self, view, body):
        """
        :param view: A reference to the parent view
        :type view: instance(EmailView)
        """
        self.view = view
        self.show = True
        self.search_caption = 'Search: '
        super(ViewPane, self).__init__(body)

    def toggle_view(self):
        if self.show:
            self.show = False
        else:
            self.show = True

    def search(self, text):
        self.view.main.loop.screen.stop()
        import ipdb; ipdb.set_trace()
        self.view.main.loop.screen.start()
        pass


class FolderListBox(ViewPane):
    def __init__(self, view):
        """
        Widget to display a list of email folders

        :param view: A reference to the current view owning this widget
        :type view: an urwid.Widget

        :returns: instance of FolderListBox widget
        :type: urwid.Widget
        """
        self.view = view
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

    def search(self, text, case_sensitive=False):
        """
        Search through the self.contents list and set focus to the first item
        who's :param folder: attribute matches :param text:
        """
        items = list(enumerate(self.body))
        ordered = items[self.focus_position + 1:] + items[:self.focus_position]
        for index, item in ordered:
            if item.name.startswith(text):
                self.set_focus(index)
                self.view.set_status('Found')
                break
        else:
            self.view.set_status('No Match Found')
        

    def reverse_search(self, text, case_sensitive=False):
        """
        Reverse search self.contents looking for a FolderListItem
        who's :param folder: attribute matches :param text:.
        """
        self.contents


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
        
        self.display_label = re.sub('.+?/','  ',folder)
        self.name = folder.split('/')[-1]
        self.path = folder
        super(FolderListItem, self).__init__(self.display_label)
        urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(self.display_label, 2), None,
				'highlighted')

    def select(self):
        """
        Toggle the font settings for this folder item so it shows
        as selected (bold)
        """
        self.set_label(self.display_label)

    def deselect(self):
        """
        Toggle the font settings for this folder item so it shows
        as normal
        """
        self.set_label(('reversed',self.display_label))


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

class StatusBar(urwid.Edit):
    """
    Status display + Search pane (context aware)

    :param view: parent view (used to switch focus back when done)
    :type view: pmc.views.BaseView
    """
    def __init__(self, view, caption='',edit_text=''):
        self.view = view
        self.callback = None
        super(StatusBar,self).__init__(caption,edit_text)

    def get_user_input(self, caption='Input: ', edit_text='', callback = None):
        """
        Get user input and return result to "callback" for handling

        :param caption: Text to set in Edit.caption for this widget
        :type caption: str

        :param callback: Function to return the input text to for handling
        :type callback: func
        """
        if not callback:
            self.set_caption('No Callback Assigned to get_user_input')
            self.set_edit_text('')
            self.view.set_focus('body')
        else:
            self.callback = callback
            self.set_caption(caption)
            self.view.set_focus('footer')

    def keypress(self, size, key):
        """
        Override keypress to allow for cancelling an action with Esc
        """
        #self.view.main.loop.screen.stop()
        #import ipdb; ipdb.set_trace()
        #self.view.main.loop.screen.start()
        if key == "esc":
            self.set_edit_text('')
            self.set_caption('Cancelled')
            self.view.set_focus('body')
        elif key == "enter":
            callback = self.callback
            self.callback = None
            submit_text = self.edit_text
            self.set_edit_text('')
            self.set_caption(self.caption + submit_text )
            callback(submit_text)
            self.view.set_focus('body')
        else:
            super(StatusBar,self).keypress(size,key)

    def set_edit_text(self, text):
        if text.endswith('\n'):
            if self.callback is not None:
                self.callback(text)
        else:
            super(StatusBar,self).set_edit_text(text)
