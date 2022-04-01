---
title: git talk
date: 2021-10-28
tags: minutes,git
author: Steven Whitaker
template: minutes
---
# Technical Information

Git commands

git init, git status, git add, git rm, git diff, git clone, git commit

git branch

* Merge requests are not part of git, but rather gitlab and github

* Merge into master, and try not to commit directly into master.

* Try not to branch too many times. Branching into multiple branches is
confusing.

git remote server

---
In the remote server
---

* git init --bare

* cd hooks, echo "git --work-tree=/path/to/files --git-dir=/path/to/repo.git \
checkout" > post-receive

* chmod +x post-receive

---
On the local computer
---

* git init, git add, etc.

* git remote add <name> user@shell.lug.mtu.edu:/path/tp/repo.git

* git push <name> master

Customizing git profile

* git config --list

* git config --global <parameter> <value>

* File is also in ~/.gitconfig


Steven is writing this in post, so I actually have no idea what else we did.
We probably joked about arch and complained about people like usual.
Shell is super damn slow and I don't know why. Might be a connection issue.
