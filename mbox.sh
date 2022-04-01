#!/bin/bash

python3 build.py

[[ ! -d public/archive ]] && mkdir public/archive
[[ ! -d public/archive/mail ]] && mkdir public/archive/mail

mhonarc -rcfile mail/.mrc -spammode -noreverse -outdir public/archive/mail mail/in/*
