#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch posts from email address in ACCOUNT_USERNAME environment
variable, generate files, then send to server."""

import sys
import os
import imaplib
from email import message_from_bytes
from email.message import Message
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
            this_email: Message = message_from_bytes(msg[0][1])
            if sender in this_email.get("From", ""):
                posts.append((this_email.get("Subject", ""),
                              this_email.get_payload()))
    imap_server.close()
    imap_server.logout()
    return posts


def main():
    """Fetch posts from email address in ACCOUNT_USERNAME environment
    variable, generate files, then send to server."""
    load_dotenv(".env")
    posts = fetch_mail()
    for post in posts:
        with open(f"posts/{post[0]}.md", "w", encoding="utf-8") as f:
            f.write(post[1])
    generate_pages.main()
    ssh_client: paramiko.SSHClient = paramiko.SSHClient()
    key_file: str = os.getenv("SSH_ID_PATH", "")
    hostname: str = os.getenv("SSH_HOSTNAME", "")
    username: str = os.getenv("USERNAME", "")
    ssh_client.connect(hostname, key_filename=key_file, username=username)
    return 0


if __name__ == '__main__':
    sys.exit(main())
