import email

class TestProvider(object):
    def login(self, server, username, password, use_ssl=False, **kwargs):
        return (True,'OK')

    def list_folders(self):
        return ['INBOX','INBOX/People','INBOX/Monitoring']

    def get_messages_in_folder(self, folder):
        return [ self.get_message(p,p) for p in range(20) ]

    def get_folder_status(self, folder):
        return (20,10)

    def get_message(self, folder, uid):
        return {'uid': 1,
                'folder': folder,
                'flags': ['UNSEEN'],
                'email': email.email.message_from_string('Date: 2014-01-01\nFrom:Test\nTo:David\nSubject: Meesage #{}\n\nTest'.format(folder))}
