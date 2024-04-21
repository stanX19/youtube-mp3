# youtube-mp3

python script to download playlist from youtube as mp3.

`youtube-dl` didnt provide an option to properly retry on download failures. So I had to do it myself.

## setup

```commandline
py -m pip install -r requirements.txt
```

## usage

```commandline
py main.py
```

## example usage

```commandline
C:\Users\STANX19\Desktop>py main.py
Playlist url: https://youtube.com/playlist?list=OLAK5uy_lpuQ9v1KQMhRhSslD9SkWoi1rimC_mtTM&si=BqSYEIafKkBSerP0
70 songs found. Do you want to download all songs? [Y/n]
: y
Total progress:   6%|███▊                                                               | 4/70 [02:24<38:30, 35.00s/it]
ERROR: unable to download video data: HTTP Error 403: Forbidden
Exception thrown when attempting to run <function download_video at 0x000001BD853439D0>, attempt 0 of 10
Total progress:  69%|█████████████████████████████████████████████▎                    | 48/70 [31:48<12:56, 35.29s/it]
ERROR: unable to download video data: HTTP Error 403: Forbidden
Exception thrown when attempting to run <function download_video at 0x000001BD853439D0>, attempt 0 of 10
Total progress:  87%|█████████████████████████████████████████████████████████▌        | 61/70 [40:43<05:35, 37.28s/it]
Downloading [Handsome Pose Collection]:  27%|███████▉                      | 544023/2051225 [00:08<00:25, 58977.54it/s]```
