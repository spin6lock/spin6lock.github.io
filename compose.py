#!/usr/bin/env python3
#encoding=utf8

"""Create a post, add spacing, then commit and push it."""

import os
import subprocess
import datetime
import sys
import argparse

def handle_args():
    parser = argparse.ArgumentParser(description="accept blog title as argument")
    parser.add_argument("title", help="the title of the new blogpost")
    args = parser.parse_args()
    return args.title

def prepare_file(title):
    datestr = f"{datetime.datetime.now():%Y-%m-%d}"
    post_filename = ''.join([datestr, '-', title, '.md'])
    front_matter = f"""---
title:      "{title}"
subtitle:   ""
date:       {datetime.datetime.now():%Y-%m-%d}
author:     "spin6lock"
catalog:    true
tags:
- tag
---
"""
    filepath = os.path.join("content", "blog", "post", post_filename)
    with open(filepath, "w") as fh:
        fh.write(front_matter)
    EDITOR = os.environ.get("EDITOR", "vim")
    subprocess.run([EDITOR, filepath], check=True)
    return filepath

def git_commit_push(filepath):
    subprocess.run(["git", "add", filepath], check=True)
    subprocess.run(["git", "commit", "-v"], check=True)
    subprocess.run(["git", "push"], check=True)

def main():
    title = handle_args()
    filepath = prepare_file(title)
    subprocess.run([sys.executable, "_post_add_space/main.py", filepath], check=True)
    git_commit_push(filepath)

if __name__ == "__main__":
    main()
