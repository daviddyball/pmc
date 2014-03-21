from IPython import embed_kernel as embed_ipython_kernel
import datetime
import re
import urwid

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

    def get_user_input(self, caption='Input: ', edit_text='', callback=None):
        """
        Get user input and return result to "callback" for handling

        :param caption: Text to set in Edit.caption for this widget
        :type caption: str

        :param callback: Function to return the input text to for handling
        :type callback: func
        """
        if callback is None:
            self.set_caption('ERROR: No Callback Specified')
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
