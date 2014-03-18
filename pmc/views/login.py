from IPython import embed_kernel as embed_ipython_kernel
import urwid
import sys
from pmc.providers.test import TestProvider
from pmc.providers.imap import IMAPProvider

class LoginView(urwid.Frame):
    def __init__(self, main):
        self.main = main
        self.server = urwid.Edit('','mail.tangentlabs.co.uk')
        self.username = urwid.Edit('','david.dyball@tangentlabs.co.uk')
        self.password = urwid.Edit('',mask='*')
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
