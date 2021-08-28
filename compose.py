#!/usr/bin/env python3
#encoding=utf8

"""
This module use fd-find to find out latest modified post, and fix the space problem.
"""

import os
import subprocess
import datetime
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
layout:     post
title:      "{title}"
subtitle:   ""
date:       {datetime.datetime.now():%Y-%m-%d}
author:     "spin6lock"
catalog:    true
tags:
- tag
---
"""
    filepath = os.path.join("_posts", post_filename) 
    with open(filepath, "w") as fh:
        fh.write(front_matter)
    EDITOR = os.environ.get("EDITOR", "vim")
    subprocess.call([EDITOR, filepath])

def git_commit_push():
    subprocess.call(["git", "add", "_posts/*.md"]) 
    subprocess.call(["git", "commit", "-v"]) 
    subprocess.call(["git", "push"])

def main():
    title = handle_args()
    prepare_file(title)
    subprocess.call(["fd", ".", "_posts/", "--changed-within=5min", "-x", "python3", "_post_add_space/main.py"]) 
    git_commit_push()

if __name__ == "__main__":
    main()
