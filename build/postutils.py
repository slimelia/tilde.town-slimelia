#!/usr/bin/env python3
"""Assorted utilities relating to fetching, parsing and styling
Slimeblogger posts.
"""

from pathlib import Path
from operator import itemgetter
from markdown import markdown
from blog_attributes import BlogAttributes


def blog_post_dict(filename, title, author, date, body):
    """Return a standard Slimeblogger blog post dict."""
    return {
        "filename": filename,
        "title": title.lower(),
        "author": author,
        "date": f"{date:%Y-%m-%d}",
        "true_date": date,
        "body": body
    }


def get_post_dicts(post_path):
    """Fetch Markdown files from directory, store in a dict,
    then append to a list. Returns list of dicts.
    """
    directory = Path(post_path)
    post_list = []
    for file in directory.iterdir():
        if file.suffix == ".md":
            with open(file.resolve(), 'r', encoding='utf-8') as doc:
                first_line = doc.readline()
                post_body = markdown(doc.read())
            attributes = BlogAttributes(first_line)
            filename = file.stem + ".html"
            post = blog_post_dict(filename, attributes.title,
                                  attributes.author, attributes.date,
                                  post_body)
            post_list.append(post)
    post_list.sort(key=itemgetter("true_date"), reverse=True)
    return post_list


def package_post(post):
    """Take blog post and return in dict format required for site template."""
    return {"post": post}
