---
title: sed
date: 2021-12-09
tags: minutes,minutes2021
author: Steven Whitaker
template: minutes
---

# [sed](http://www.gnu.org/software/sed/manual/sed.html)

This is a scriptable text editor. You can use `sed` to run `ed` commands on the input stream.

There are three points to `sed`:

* `sed` reads line-by-line.

* `sed` has a pattern buffer.

* `sed` has a hold buffer.

How `sed` works:

1. "Reads" the first line; it stores the first line into the `pattern` buffer.

2. Executes any commands that should be run on this line.

3. "Reads" the next line.

If you use the command `h`, this will push the pattern buffer into the hold buffer.

`g` does the opposite: it pushes the hold buffer into the pattern buffer.

## Usage

`sed [options] [script] [file]`

`options` found with `sed -h` or `sed --help`. There are not that many and you can read them all.

`script` is where all the magic or actual benefit to this program actually comes from.

`file` is any input stream. Can be a file name, or you can pipe data into it.

## Examples

### [Commands](http://www.gnu.org/software/sed/manual/sed.html#sed-commands-list)

`a` will append to a specific line, so: `seq 10 | sed '5ahello'` will append `hello` to the `5`th line.

`seq 10 | sed -n '!5p'`

Let's step through this command:

`seq 10 | sed '3{h;z;g}'` and what will happen when I execute this command? Absolutely nothing!

* `3` looks at the `3`rd line.

* `h` holds (stores) the data from the `3`rd line. (the `{` and `}` mean all commands use `3`).

* `z` zaps (deletes) the data from the `3`rd line.  (the `{` and `}` mean all commands use `3`).

* `g` replaces the `3`rd line with what is in `h`; which was the `3`rd line initially.

`h` is a single register and `g` writes this single register.

Let's say we want to swap lines `5` and `6`. Let's build up this command.

`seq 10 | sed '5{h;z;n;G}'`

We `h`old the 5th line in the buffer, `z`ap the 5th line, then go to the `n`ext line and print the hold buffer with `G`.

We've created a gap on the 5th line, though. We need to use some special flags to get this proper.

`seq 10 | sed -n '1,4p;5{h;z;n;G;p};7,$p'`

The `-n` flag removes automatic printing of the stream. Now, we need to `p`rint manually ourselves.

* `1,4p` just prints the beginning by ourselves. 

* `5{h;z;n;G;p}` is the same as before, but now we are `p`rinting manually.

* `7,$p` prints the rest of the file. We use `7` because `G` prints a new line and so the `6`th line is new.

At this point, you should start writing a file to save this for later:

`seq 10 | sed -n -f swap.sed`

Let's reverse a list, which is actually much easier:

`seq 10 | sed -n 'G;h;$p'`

Let's step through what happens in `sed` here. 

`sed` goes to the first line, and sees that `G` and `h` will be executed. 

* `G` will append whatever is on the hold buffer into the pattern buffer. There is nothing in the hold buffer right now, so it prints just a new line.

* `h` will store the pattern space 



### Regex substitutions

Say you only want lines that contain a word:

`sed -n '/text/p' file` -> Does not automatically print anything and uses regex to `p`rint only `text`. This is `grep`.

`echo sup | sed 's/p/d/'` -> `sed` will _(s)ubstitute_ the letter _p_ into _d_, so it will output `sud`.

`cat data.txt | sed 's/p/d/'` -> Same as the previous example, but using a different function to print the data.

`sed 's/p/d/' data.txt` -> the `data.txt` file is used as the `[file]` input into the `sed` function.

