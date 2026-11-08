#!/usr/bin/env python3
#encoding=utf8

"""Create a post, add spacing, then commit and push it."""

import os
import subprocess
import datetime
import sys
import argparse
import json

def handle_args():
    parser = argparse.ArgumentParser(description="Create a blog post interactively")
    parser.add_argument("title", nargs="?", help="the title of the new blogpost")
    args = parser.parse_args()
    title = (args.title or "").strip()
    while not title:
        title = input("文章标题：").strip()
    raw_tags = input("Tag（多个用逗号分隔，留空表示无标签）：")
    tags = [tag.strip() for tag in raw_tags.replace("，", ",").split(",") if tag.strip()]
    return title, tags

def prepare_file(title, tags):
    datestr = f"{datetime.datetime.now():%Y-%m-%d}"
    post_filename = ''.join([datestr, '-', title, '.md'])
    front_matter = f"""---
title:      {json.dumps(title, ensure_ascii=False)}
subtitle:   ""
date:       {datetime.datetime.now():%Y-%m-%d}
author:     "spin6lock"
catalog:    true
tags:       {json.dumps(tags, ensure_ascii=False)}
---
"""
    filepath = os.path.join("content", "blog", "post", post_filename)
    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write(front_matter)
    EDITOR = os.environ.get("EDITOR", "vim")
    subprocess.run([EDITOR, filepath], check=True)
    return filepath

def git_commit_push(filepath):
    subprocess.run(["git", "add", filepath], check=True)
    subprocess.run(["git", "commit", "-v"], check=True)
    subprocess.run(["git", "push"], check=True)

def main():
    title, tags = handle_args()
    filepath = prepare_file(title, tags)
    subprocess.run([sys.executable, "_post_add_space/main.py", filepath], check=True)
    git_commit_push(filepath)

if __name__ == "__main__":
    main()
