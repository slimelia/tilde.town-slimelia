#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch posts from email address in ACCOUNT_USERNAME environment
variable, generate files, then send to server."""

import sys
import os
import imaplib
import quopri
from collections.abc import Generator
from email import message_from_bytes
from email.message import Message
from pathlib import Path
from dotenv import load_dotenv
import paramiko
import generate_pages


def fetch_mail() -> list:
    """Fetch posts from email address"""
    usr: str = os.getenv("ACCOUNT_USERNAME", "")
    pwd: str = os.getenv("ACCOUNT_PASSWORD", "")
    svr: str = os.getenv("IMAP_SERVER", "")
    sender: str = os.getenv("SENDER", "")
    imap_server: imaplib.IMAP4_SSL = imaplib.IMAP4_SSL(svr)
    imap_server.login(usr, pwd)
    imap_server.select()
    data: list
    _, data = imap_server.search(None, "UNSEEN")
    posts: list = []
    for num in data[0].split():
        msg: list
        _, msg = imap_server.fetch(num, "RFC822")
        if isinstance(msg, list):
            decoded_msg: bytes = quopri.decode(msg[0][1])
            this_email: Message = message_from_bytes(decoded_msg)
            if sender in this_email.get("From", ""):
                posts.append((this_email.get("Subject", ""),
                              this_email.get_payload()))
    imap_server.close()
    imap_server.logout()
    return posts


def write_md_files(posts: list) -> None:
    """Create Markdown post files in posts directory"""
    for post in posts:
        with open(f"posts/{post[0]}.md", "w", encoding="utf-8") as f:
            f.write(post[1])


def upload_to_server() -> None:
    """Upload via SFTP to destination"""
    key_file: str = os.getenv("SSH_ID_PATH", "")
    hostname: str = os.getenv("SSH_HOSTNAME", "")
    username: str = os.getenv("USERNAME", "")
    ssh_client: paramiko.SSHClient = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.connect(hostname, key_filename=key_file, username=username)
    sftp: paramiko.SFTPClient = ssh_client.open_sftp()
    pub_html = Path("../public_html/")
    index_files: Generator[Path] = (f for f in pub_html.iterdir()
                                    if not f.is_dir())
    for file in index_files:
        dest_path = '/'.join(file.parts[1:])
        sftp.put(file, dest_path)
    pages_html = Path("../public_html/pages/")
    page_files: Generator[Path] = (f for f in pages_html.iterdir()
                                   if not f.is_dir())
    for file in page_files:
        dest_path = '/'.join(file.parts[1:])
        sftp.put(file, dest_path)
    sftp.close()
    ssh_client.close()


def main() -> int:
    """Fetch posts from email address in ACCOUNT_USERNAME environment
    variable, generate files, then send to server."""
    load_dotenv(".env")
    posts = fetch_mail()
    write_md_files(posts)
    generate_pages.main()
    upload_to_server()
    return 0


if __name__ == '__main__':
    sys.exit(main())
