from typing import Optional, List
from imaplib import IMAP4_SSL
import email
from email.message import EmailMessage
import regex
from datetime import datetime
import math


class MetaMail:
    def __init__(self, server: str, user: str, password: str):
        self.server: str = server
        self.user: str = user
        self.password: str = password
        self.connection: Optional[IMAP4_SSL] = None
        self.id: Optional[List[str]] = None

    def __del__(self):
        self.connection.close()
        self.connection.logout()

    @classmethod
    def fuzzy_match_subject(cls, mail_subject: str, subject_query: str, max_error: int):
        pattern: str = f"(\s{subject_query}\s){{e<={max_error}}}"
        match: regex.Match = regex.search(pattern, mail_subject, regex.IGNORECASE | regex.BESTMATCH)

        return True if match else False

    @classmethod
    def mail_to_old(cls, delivery_date_string: str, max_age_seconds: int):
        delivery_date: float = math.floor(datetime.timestamp(datetime.strptime(delivery_date_string, "%a, %d %b %Y %H:%M:%S %z")))
        unix_now: float = math.floor(datetime.timestamp(datetime.now()))

        return (unix_now - delivery_date) > max_age_seconds if max_age_seconds > 0 else False

    def connect(self):
        self.connection = IMAP4_SSL(self.server)
        err, _ = self.connection.login(self.user, self.password)
        if err != "OK":
            self.connection.close()
            exit(1)

        self.connection.select("INBOX", readonly=True)

    def query_sender(self, sender: str):
        typ, message_ids = self.connection.search('utf-8', f'(Header To "{sender}")')
        if typ == 'OK':
            self.id = message_ids[0].decode().split()
        else:
            raise ValueError

    def query_attachments(self, subject: str, max_age: int):
        # if message has attachment; return date send, bytearray and filename(?) -> actually not necessary, or?
        meta_dict = dict()
        for message_id in self.id:
            typ, data = self.connection.fetch(message_id, '(RFC822)')
            email_message = email.message_from_bytes(data[0][1], _class=EmailMessage)
            if not MetaMail.fuzzy_match_subject(email_message.get("Subject"), subject, 5):
                continue
            if MetaMail.mail_to_old(email_message.get("delivery-date") or email_message.get("Date"), max_age):
                continue
            for message_part in email_message.walk():
                if message_part.get_content_disposition() != "attachment":
                    continue
                elif (message_part.get_content_type() in ["text/plain", "text/markdown"] or
                        message_part.get_content_maintype() == "application" and
                        message_part.get_content_subtype() in ["pdf", "msword",
                                                               "vnd.oasis.opendocument.text",
                                                               "vnd.openxmlformats-officedocument.wordprocessingml.document"]
                ):
                    meta_dict.update({
                            message_id: {
                                #'subject': email_message.get('Subject'),
                                'date': email_message.get("delivery-date") or email_message.get("Date"),
                                'filename': message_part.get_filename(),
                                'subtype': message_part.get_content_subtype(),
                                'file-content': message_part.get_payload(decode=True)
                            }
                        })

        return meta_dict
