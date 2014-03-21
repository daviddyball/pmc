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
        pass
