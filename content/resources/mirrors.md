---
title: Using mirrors
tags: index
template: index
---

### Using our LUG mirrors [not complete]

* Ubuntu
	* Edit `/etc/apt/sources.list` and replace all but the Security repos with `"http://mirrors.lug.mtu.edu/ubuntu/"`.

* Gentoo
	* Edit [`/etc/portage/make.conf`](https://wiki.gentoo.org/wiki//etc/portage/make.conf) and rewrite (or add) the [`GENTOO_MIRRORS`](https://wiki.gentoo.org/wiki/GENTOO_MIRRORS) variable with `GENTOO_MIRRORS="http://mirrors.lug.mtu.edu/gentoo/"`.
