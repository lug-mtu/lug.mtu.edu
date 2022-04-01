---
title: FFmpeg
date: 2021-10-03
tags: minutes,ffmpeg
meeting-index: 0
author: Steven Whitaker
template: minutes
---
### Technical Information

We introduced one another and then Steven Whitaker went through the two commands on FFprobe and FFmpeg. Here are his notes:

```bash
# The process is to encode the movie in post-processing, then stream the movie afterwards.
# Encoding takes less than real-time, especially on a VPS with a small CPU.
# So, encode on a good computer, scp files over to server, and stream encoded movie with SRS.

### Encode a movie

# -i <file>       : input file
# -vcodec libx264 : I've found that libx264 works best with SRS.
# -vcodec copy    : I've had no issue with any audio codecs.
# -ar 44100       : I sometimes get issues with 48 kHz sample rates with SRS.
# -map 0:v:0      : Map the <file>'s first video stream "0:v" to the output stream.
#                   This only necessary if there's multiple video streams (typically not).
# -map 0:a:0      : Map the <file>'s first audio stream "0:a" to the output stream.
#                   Make sure you choose the wanted language.
#                   This is dependent on the creator, so please use `ffprobe` to see which
#                   audio dub is chosen.
# <out_file>      : Output of file. Choosing file type affects the ffmpeg encoding output!
ffmpeg -i in.mkv -vcodec libx264 -acodec copy -ar 44100 -map 0:v:0 -map 0:a:0 out.mp4

# Same as above, but with added subtitles
# -vf sbutitles=<file>:si=<num>
#
# Ensure the correct subtitle and subtitle codec is used.
# Use ffprobe <file> to see what subtitles are available. Once the proper subtitle
# is found, make sure you use bitmap -> bitmap encoding or text -> text encoding.
# I'd recommend just using -scodec copy.
ffmpeg -i in.mkv -vcodec libx264 -acodec copy -ar 44100 -scodec <sub_codec> \
-map 0:v:0 -map 0:a:0 -map 0:s:0 out.mp4

# Bitmap subtitles are different than text subtitles. This command maps the bitmap
# subtitle stream properly.
#
# The complex filter is used to overlay the subtitle stream over the video stream.
ffmpeg -i in.mkv -vcodec libx264 -acodec copy -ar 44100 -map 0:a:0 -map 0:v:0 \
-filter_complex "[0:v:0][0:s:0]overlay" out.mp4

### Stream a movie over SRS.

# You must have "-acodec copy -vcodec copy" to transfer the proper codecs, else SRS
# will attempt to encode in real time... and fail.
# Note that -vcodec seems to only work with libx264, please use `ffprobe` to
# see what type of video codec is used. You might not have to encode it!
# I've also found issues with the sample rate of the audio codec, if it's 48 kHz,
# so just use 44.1 kHz. This hasn't failed me.
ffmpeg -re -i out.mp4 -acodec copy -vcodec copy -f flv -y rtmp://localhost/live/livestream
```

### LUG Internal Updates

We are currently trying to get ourselves as an organization. We are in talks
with RSO to get ourselves to become an official student organization.

Attached is the current email:

```text
Steven,

Thank you for sending us your initial paperwork.  Do you have a Constitution & Bylaws already prepared that we can review or is that something you would like to discuss further?  Feel free to send it to us or let us know what help you need and then we can get a meeting set up!

Thanks,
Student Leadership & Involvement.

On Mon, Oct 4, 2021 at 10:04 AM Steven Whitaker <sjwhitak@mtu.edu> wrote:

> Hello,

> We would like to restart a previously dead organization. I figure it'd
> be easiest to say that our organization is a "new" organization, since
> this is probably easier on your side to do. I'm not sure of what you'd
> want, but attached is the student org registration form. Could we work
> out some meeting to figure out what is required to get this org back
> onto involvement link?
>
> Thank you,
> Steven Whitaker
```
