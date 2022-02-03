<div align="center">
  <img src="./assets/logo.png" width="450" />

  [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/F1F7ABOVF)
</div>

# Saves Buddyfit videos for offline enjoyment

Why? During the COVID-19 lockdown, my ISP was kinda lame, as a result I had issue streaming LIVE classes and even replaying old ones, this way I could use them reliably at a later time and once finished the lesson **delete the file**.

## Disclaimer

Hopefully this doesn't break the end user agreement for Buddyfit. Since I'm simply saving the HLS stream to disk as if we were a browser, this does not abuse the streaming endpoints. However I take NO responsibility if some trainer with a bunch of muscles will knock on your door wanting to have a little chat with you.

___
Logo by *catalyst*

## Prereqs

- [**Python 3.8**][python]: Tested on 3.8. YOU ARE ON YOUR OWN.
- [**ffmpeg**][ffmpeg]: a recent version (year 2019 or above).
- [**chromium**][chromium]: whatever version you want.
- **chromedriver**: whatever version you want (match w/ chromium please).
- [**ffpb**][ffpb]: used to quickly display progress bar during download.


[ffmpeg]: https://www.ffmpeg.org/download.html
[python]: https://www.python.org/downloads/
[chromium]: https://www.chromium.org/getting-involved/download-chromium
[ffpb]: https://github.com/althonos/ffpb

## Before running
I'm expecting, in the same working directory, the following data:
- *keys*, file containing emailAddr and password of the account, one line each.
- *video_links*, file containing direct video links, one line each.

## Examples
```
$ cat keys
test@test.com
testPassword
$ cat video_links
https://domain/classes/replay/videoID1/live
https://domain/classes/replay/videoID2/live
```

## Usage

```
$ python3 buddyStream.py
```
All the videos will be stored in a *videos* folder in the same working directory.

## Supported Platforms
Tested on macOS 11.1, Ubuntu 20.04, Ubuntu 20.10, Alpine 3.13. (Should work no problemo on Windows as well)
