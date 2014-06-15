import sys
import urwid
from IPython import embed_kernel as embed_ipython_kernel
from pmc.providers.test import TestProvider
from pmc.providers.imap import IMAPProvider
from pmc.views.email import EmailView

class LoginView(urwid.Frame):

    def __init__(self, main):
        self.main = main
        self.set_up_login_fields()
        self.set_up_login_layout()
        footer = urwid.Text('')
        super(LoginView, self).__init__(self.body, footer=footer)

    def set_up_login_fields(self):
        self.server = urwid.Edit('', 'mail.tangentlabs.co.uk')
        self.username = urwid.Edit('', 'david.dyball@tangentlabs.co.uk')
        self.password = urwid.Edit('', mask='*')

    def set_up_login_layout(self):
        login_button = urwid.Button('Login', on_press=self.do_login)
        label_widgets = [urwid.Text('Server Name:', align="right"),
                         urwid.Text('Username:', align="right"),
                         urwid.Text('Password:', align="right")]
        labels = urwid.Pile(widget_list=label_widgets)
        login_widgets = [self.server, self.username, self.password,
                         login_button]
        login_fields = urwid.Pile(widget_list=login_widgets)
        layout_columns = urwid.Columns(
            widget_list=[labels, login_fields], dividechars=1)
        self.body = urwid.Filler(layout_columns)

    def do_login(self, button):
        self.set_status('Logging In....')
        if self.validate_login_fields():
            self.provider = IMAPProvider()
            (result, msg) = self.provider.login(self.server.edit_text,
                                                self.username.edit_text,
                                                self.password.edit_text)
            if result:
                self.main.push_view(EmailView(self.main,self.provider))
            else:
                self.set_status('ERROR: %s' % msg)
                del(self.provider)
        else:
            self.set_status('Invalid Form')

    def validate_login_fields(self):
        if self.server.edit_text in (None, ''):
            self.set_status('ERROR: Server Name is Required')
            self.body.focus_item = self.server
        elif self.username.edit_text in (None,''):
            self.set_status('ERROR: Username is Required')
            self.dialog.focus_item = self.username
        elif self.password in (None,''):
            self.set_status('ERROR: Password is Required')
            self.dialog.focus_item = self.password
        return True

    def set_status(self, message):
        self.footer.set_text(message)
