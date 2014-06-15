"""Base Mail Provider Class for PMC"""
import abc

class BaseProvider(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def list_folders(self):
        """
        List all folders in the remote backend

        :returns: list of strings
        """
        pass

    @abc.abstractmethod
    def list_messages_in_folder(self, folder):
        """
        List all messages in a specific backend folder

        :param folder: The folder to be queried

        :returns: list of message UID's by default
        """
        pass

    @abc.abstractmethod
    def get_folder_status(self, folder):
        """
        Return information about a given folder
        e.g. Unread, Total or Deleted Messages

        :param folder: The folder to be queried
        """
        pass

    @abc.abstractmethod
    def get_message(self, folder, uid):
        """
        Return a dict object for a given message

        :param folder: Folder containing the given message
            Some backends allow duplicate message IDs
            Fitler these using the specified folder

        :param uid: The ID of the message to be fetched

        :returns: Message Dict

            Message Dict Format
                - uid: Message UID
                - flags: List of Message flags
                - email: RFC822 encoded raw email message
        """
        pass

    @abc.abstractmethod
    def get_message_headers(self, folder, uid):
        """
        Return a dict of key,val headers for the given message id.

        :param folder: Folder containing the given message
        :param uid: Message ID to fetch headers for

        :returns: List object containing key/vals for each
            header
        """
        pass
