from dataclasses import dataclass, fields
from typing import List


@dataclass(init=False)
class ArgumentClass:
    imap: List[str]
    user: List[str]
    imap_passwd: List[str]
    sender_address: List[str]
    subject: List[str]
    nextcloud_app_passwd: List[str]
    nextcloud_webdav_url: List[str]
    nextcloud_destination_folder: List[str]
    max_age: int

    def __getitem__(self, item):
        for flub in fields(self):
            if flub.name == item:
                return self.__dict__[flub.name]

    def get(self, item):
        return self.__getitem__(item)

    def __str__(self):
        return f"""\
        My IMAP-Host is {self.imap}. User credentials are {self.user} with password {self.imap_passwd}.
        Querying mails from {self.sender_address} whose mails contain {self.subject} in the subject header and are not older than {self.max_age} seconds old.
        Logging in via Webdav to URL {self.nextcloud_webdav_url} using token {self.nextcloud_app_passwd}.
        Uploading converted files to {self.nextcloud_destination_folder}.
        """
