<div style="width: 100px; height: 100px; position: absolute; right: 10px; top: 10px">
<img src="assets/logo.svg" alt="FSI Logo" align="right">
</div>

# protokoll2nextcloud

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/Florian-Katerndahl/protokoll2nextcloud?label=version)

This package is used internally by the [FSI Geographie](https://fsigeographiefuberlin.wordpress.com/) of the FU Berlin to automatically upload any 
protocols of our plena to Nextcloud. The goal, however, is to keep this package as general as possible so that any E-Mail attachment can be converted to PDF 
and uploaded to Nextcloud folder.

This repo/package replaces an older implementation whose archived repo can be found [here](https://github.com/Florian-Katerndahl/Mails2FuBox).

## Installation

This package depends on `poetry`, `pandoc` and `lualatex`. Please install them before continuing. On Ubuntu, the steps are as following:

1. `curl -sSL https://install.python-poetry.org | python3 -`
2. `sudo apt update && sudo apt install -y pandoc texlive texlive-latex-extra`

Adjust your system's `PATH` variables accordingly.

Afterwards, you can clone the repository and use poetry to install the package. Should you choose to install from the release binaries: This was never 
tested but *should* work in some form or another.

```bash
git clone https://github.com/Florian-Katerndahl/protokoll2nextcloud.git
cd protokoll2nextcloud
poetry install
```

## Usage

Run the script manually or set up a cronjob via `crontab -e` (**needs absolute paths to interpreter and script**):

```bash
poetry run python application/main.py -h
usage: main.py [-h] --imap IMAP --user USER --nc-user NEXTCLOUD_USER --password IMAP_PASSWD --sender SENDER_ADDRESS --subject SUBJECT
               --nc-password NEXTCLOUD_APP_PASSWD --nc-url NEXTCLOUD_WEBDAV_URL --nc-dest NEXTCLOUD_DESTINATION_FOLDER
               [--max-age MAX_AGE]

options:
  -h, --help            show this help message and exit
  --imap IMAP           Hostname of the IMAP server.
  --user USER           Username to use when logging in to the IMAP server and Nextcloud instance.
  --nc-user NEXTCLOUD_USER
                        Username to use when logging in to Nextcloud, should from the IMAP server.
  --password IMAP_PASSWD
                        Password to use when logging in to the IMAP server.
  --sender SENDER_ADDRESS
                        E-Mail address to search for when querying mails.
  --subject SUBJECT     Mail subject to search for, currently allows for five typos.
  --nc-password NEXTCLOUD_APP_PASSWD
                        App password to use when logging into your Nextcloud instance.
  --nc-url NEXTCLOUD_WEBDAV_URL
                        Nextcloud Web-DAV url used for file upload. Must include trailing slash.
  --nc-dest NEXTCLOUD_DESTINATION_FOLDER
                        Path inside your Nextcloud instance. Must include trailing slash.
  --max-age MAX_AGE     Oldest delivery date which is still processed. Don't specify or set to zero to process all
                        messages which match the above given options.
```

```bash
# cronjob every 12th hour from monday thru friday
0 */12 * * 1-5 <path/to/python/interpreter> </path/to/main/script> <argument list>
```
