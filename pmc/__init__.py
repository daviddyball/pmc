from IPython import embed_kernel as embed_ipython_kernel
import urwid
from pmc.views.email import EmailView
from pmc.views.login import LoginView
from pmc.providers.test import TestProvider

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

        self.stack = []

        if 'debug' in kwargs:
            if kwargs['debug']:
                self.stack.append(EmailView(self,TestProvider()))
                #embed_ipython_kernel(self)
            else:
                self.stack.append(LoginView(self))
        else:
            self.stack.append(LoginView(self))

        self.loop = urwid.MainLoop(self.stack[-1],self.palette,
                                   unhandled_input=self.unhandled_input)

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
