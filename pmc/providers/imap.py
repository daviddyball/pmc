from email import email
from imapclient import IMAPClient
import getpass
import os

class IMAPProvider(object):
    def login(self, server, username, password, use_ssl=False, **kwargs):
        try:
            self.server = IMAPClient(server, use_uid=True, ssl=use_ssl)
            self.server.login(username, password)
        except Exception as e:
            return (False, e.message)
        return (True, 'Login Successful')

    def list_folders(self):
        """
        Return a list of IMAP folders
        """
        server_folders = self.server.list_sub_folders()
        directory_tree = {}
        folders = []

        for flags,delimiter,folder in server_folders:
            folders.append(folder)
            folders = sorted(folders)

        return folders

    def get_messages_in_folder(self, folder):
        """
        Return a list of message dicts in *folder*.

        Message dict format:
            - uid
            - flags
            - email.email encoded RFC822 message
        """
        if folder in self.list_folders():
            self.server.select_folder(folder)
            message_ids = self.server.search(['NOT DELETED'])
            raw_messages = self.server.fetch(message_ids,['FLAGS','RFC822'])
            messages = []
            for uid in raw_messages.keys():
                try:
                    messages.append({'uid': uid,
                                     'folder': folder,
                                     'flags': raw_messages[uid]['FLAGS'],
                                     'email': email.message_from_string(
                                                raw_messages[uid]['RFC822'])
                                     })
                except:
                    pass
            return messages

        return []

    def get_folder_status(self, folder):
        """
        Return the read/unread message count of an IMAP folder
        """
        if folder in self.list_folders():
            select_info = self.server.select_folder(folder)
            total = select_info['EXISTS']
            unseen = int(select_info['UNSEEN'][0])
            return (total,unseen)
        return None

    def get_message(self, folder, uid):
        """
        Return a dict object for a given message in a given folder.

        Message dict format:
            - uid
            - flags
            - email.email encoded RFC822 message
        """
        if folder in self.list_folders():
            select_info = self.server.select_folder(folder)
            raw_message = self.server.fetch(uid,['FLAGS','RFC822'])[uid]
            return {'uid':uid,
                    'folder':folder,
                    'flags':raw_message['FLAGS'],
                    'email':email.message_from_string(raw_message['RFC822'])}
