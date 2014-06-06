import datetime
import re
import urwid
from pmc.widgets.base import ViewPane

class FolderList(ViewPane):
    def __init__(self, view):
        """
        Widget to display a list of email folders

        :param view: A reference to the current view owning this widget
        :type view: an urwid.Widget

        :returns: instance of FolderList widget
        :type: urwid.Widget
        """
        self.view = view
        self.body = urwid.SimpleFocusListWalker([])
        super(FolderList,self).__init__(view, self.body)
        self.body = urwid.SimpleFocusListWalker(self.get_folders())
        self.search_caption = 'Search Folders: '

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
        Open a folders contents in FolderList
        
        :param folder: The button triggering this callback
        :type folder: pmc.FolderListItem
        """
        self.view.set_status('%s Opened' % folder.name)
        self.reset_selections()
        self.view.message_list.get_messages(folder)

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
        items = list(enumerate(self.body))
        ordered = reversed(items[self.focus_position + 1:] + items[:self.focus_position])
        for index, item in ordered:
            if item.name.startswith(text):
                self.set_focus(index)
                self.view.set_status('Found')
                break
        else:
            self.view.set_status('No Match Found')


class FolderListItem(urwid.Button):
    def  __init__(self, folder, callback):
        """
        Folder Item for display in FolderList

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
