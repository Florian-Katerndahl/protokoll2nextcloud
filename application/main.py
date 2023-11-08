import argparse
from protokoll2nextcloud.argument_class import ArgumentClass
from protokoll2nextcloud.mail import MetaMail
from protokoll2nextcloud.messages import Messages

parser = argparse.ArgumentParser()
parser.add_argument("--imap", required=True, dest="imap", type=str, help="Hostname of the IMAP server.")
parser.add_argument("--user", required=True, dest="user", type=str, help="Username to use when logging in to the IMAP server and Nextcloud instance.")
parser.add_argument("--nc-user", required=False, dest="nextcloud_user", default="", type=str, help="Username to use when logging in to Nextcloud, should "
                                                                                                    " from the IMAP server")
parser.add_argument("--password", required=True, dest="imap_passwd", type=str, help="Password to use when logging in to the IMAP server.")
parser.add_argument("--sender", required=True, dest="sender_address", type=str, help="E-Mail address to search for when querying mails.")
parser.add_argument("--subject", required=True, dest="subject", type=str, help="Mail subject to search for, currently allows for five typos.")
parser.add_argument("--nc-password", required=True, dest="nextcloud_app_passwd", type=str, help="App password to use when logging into your Nextcloud "
                                                                                                "instance.")
parser.add_argument("--nc-url", required=True, dest="nextcloud_webdav_url", type=str, help="Nextcloud Web-DAV url used for file upload. Must include trailing "
                                                                                           "slash.")
parser.add_argument("--nc-dest", required=True, dest="nextcloud_destination_folder", type=str, help="Path inside your Nextcloud instance. Must include "
                                                                                                    "trailing slash.")
parser.add_argument("--max-age", required=False, dest="max_age", type=int, default=0, help="Oldest delivery date which is still processed. Don't specify or "
                                                                                           "set to zero to process all messages which match the above given "
                                                                                           "options.")

args = ArgumentClass()
parser.parse_args(namespace=args)

mailer = MetaMail(server=args.get("imap"), user=args.get("user"), password=args.get("imap_passwd"))
mailer.connect()
mailer.query_sender(sender=args.get("sender_address"))
messages_to_process = mailer.query_attachments(subject=args.get("subject"), max_age=args.get("max_age"))

messages = Messages(messages_to_process)
messages.normalize_and_upload(args.get("nextcloud_user") or args.get("user"), args.get("nextcloud_app_passwd"),
                              args.get("nextcloud_webdav_url"), args.get("nextcloud_destination_folder"))

del mailer
