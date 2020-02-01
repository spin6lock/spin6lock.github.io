#!/usr/bin/env python3
#encoding=utf8

"""
This module use fd-find to find out latest modified post, and fix the space problem.
"""

import subprocess

def main():
    subprocess.call(["fd", ".", "_posts/", "--changed-within=1day", "-x", "python3", "post_add_space/main.py"]) 
    subprocess.call(["git", "add", "_posts/*.md"]) 
    subprocess.call(["git", "commit", "-v"]) 
    subprocess.call(["git", "push"])

if __name__ == "__main__":
    main()
