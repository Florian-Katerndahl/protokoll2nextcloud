import argparse
from protokoll2nextcloud.argument_class import ArgumentClass
from protokoll2nextcloud.mail import MetaMail
from protokoll2nextcloud.messages import Messages

parser = argparse.ArgumentParser()
parser.add_argument("--imap", required=True, dest="imap", type=str)
parser.add_argument("--user", required=True, dest="user", type=str)
parser.add_argument("--password", required=True, dest="imap_passwd", type=str)
parser.add_argument("--sender", required=True, dest="sender_address", type=str)
parser.add_argument("--subject", required=True, dest="subject", type=str)
parser.add_argument("--nc-password", required=True, dest="nextcloud_app_passwd", type=str)
parser.add_argument("--nc-url", required=True, dest="nextcloud_webdav_url", type=str)
parser.add_argument("--nc-dest", required=True, dest="nextcloud_destination_folder", type=str)
parser.add_argument("--max-age", required=False, dest="max_age", type=int, default=0)

args = ArgumentClass()
parser.parse_args(namespace=args)

mailer = MetaMail(server=args.get("imap"), user=args.get("user"), password=args.get("imap_passwd"))
mailer.connect()
mailer.query_sender(sender=args.get("sender_address"))
messages_to_process = mailer.query_attachments(subject=args.get("subject"), max_age=args.get("max_age"))

messages = Messages(messages_to_process)
messages.normalize_and_upload(args.get("user"), args.get("nextcloud_app_passwd"),
                              args.get("nextcloud_webdav_url"), args.get("nextcloud_destination_folder"))

del mailer
