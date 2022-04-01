You may think to yourself: aren't you hindering yourself by writing a massive Python script to use Jinja2 templating?

Probably. But I just copy and pasted my code from my own website and it works just fine.

The procedure for this code base is to run this code on Trillian or your own computer, copy `public/` into lug.mtu.edu's `/var/ww/default/`. Until I tear out Zaphod's heart and update its lost soul, we have to do this. 

# Run
1. `python3 build.py`
2. `bash mbox.sh`

`public/` is the https://lug.mtu.edu/ website.

# Explanation

python3 does 3 things, (1) copies `raw/` to `public_html/`, generates the files from the `content/` folder, and copies over `static/` into `public_html/`. `raw/` is used for any content I've scraped using the [webarchive scraper](https://github.com/lug-mtu/archivers/blob/master/wayback2html.py). It's honestly not used too much anymore since I was also using it for the archived meeting minutes, but I can now use a [pdf2md.py](https://github.com/lug-mtu/archivers/blob/master/pdf2md.py) script instead.

mhonarc is the way that I generate `https://lug.mtu.edu/archive/mail/threads.html`. The .mrc file I found is mostly the default .mrc, except I added a `FileOrder` parameter so it removes any of the `X-header-*` stuff. I try making sure the emails I send are either text-only or reduce most of garbage headers that are for mixed-content emails. For example, click on the three dots on any google calendar invite and look at that email. That is so garbage. By comparison, right click on one of my emails, and I make mine text-friendly.

In case someone sends an email to the lug-l mailing list, I don't want this shit to show up, so I force the headers to only show

```text
Date: Wed, 02 Mar 2022 14:12:14 +0000
Subject: Invitation: Workshop: Introduction to Revision Control Systems
  @ Tue 2022-04-05 9am - 11am (EDT)
From: [redacted name] <[redacted email]>
To: [redacted name] <[redacted email]>
```

mhonarc is genuinely a good app, and if you want to add more emails to the archive, simply copy-paste your mbox to the in directory. In the generator.sh file, it's `mail/in/`.

You need to execute `mbox.sh` second because `build.py` deletes `public/` to remove any unnecessary files.

## Requirement:

Pygments is used to generate syntax for the codeblocks.

## content/

Contains the markdown files and all the website.

## public/

The HTML output. This will be generated.

## static/

Static files such as pictures or css.

## raw/

Raw files that get directly copied into `public/` such as HTML files or an autoindex'd output.

Inside `raw/` there is a subfolder, `archive/pdfs/` which contains all the pdfs of all the old presentations.

The `403.gif`, `403.html`, and `404.html` files are located here.

## mail/

`mail/` is the working directory and [mhonarc](https://www.mhonarc.org/). 

Put in all the mail archives to `/mail/in/`. 

You can add multiple archives in `/mail/in/`.

## templates/

Jinja2 templates.

