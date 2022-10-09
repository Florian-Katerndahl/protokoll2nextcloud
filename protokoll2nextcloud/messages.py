from dataclasses import dataclass
from typing import Dict, Union
from datetime import datetime
import pandoc
import requests


@dataclass
class Messages:
    messages: Dict[str, Dict[str, Union[str, bytes]]]

    @classmethod
    def parse_delivery_date(cls):
        pass

    def normalize_and_upload(self, user: str, password: str, nc_webdav_url: str, nc_destination_path: str):
        for _, message_value in self.messages.items():
            delivery_date: datetime = datetime.strptime(message_value.get("date"), "%a, %d %b %Y %H:%M:%S %z")
            if message_value.get("subtype") != "pdf":
                trick_pandoc_extensions = message_value.get("filename").split(".")[-1]
                raw_attachment = message_value.get("file-content")
                converted_attachment = pandoc.read(raw_attachment, format=trick_pandoc_extensions if trick_pandoc_extensions != "txt" else "t2t")
                file_to_upload = pandoc.write(converted_attachment, format="pdf", options=["--pdf-engine=lualatex"])
            else:
                file_to_upload = message_value.get("file-content")

            with requests.session() as s:
                s.auth = (user, password)
                s.put(nc_webdav_url + nc_destination_path + "Protokoll vom " + datetime.strftime(delivery_date, "%d.%m.%Y") + ".pdf",
                      files={"file": file_to_upload})
