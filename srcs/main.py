import logging
import random

import easygui
import my_progressbar
import user_input
import utils
import yt_dlp as youtube_dl
from tqdm import tqdm
from wininhibit import WindowsInhibitor
from decorators import retry, anti_sleep


class UrlData:
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url

    def __repr__(self):
        return f"UrlData(title={self.title}, url={self.url})"


def get_playlist_urls(playlist_url: str) -> list[UrlData]:
    ydl_opts = {
        'quiet': True,  # Suppress console output
        'extract_flat': True,  # Extract only URLs, no metadata
        'logger': logging.Logger("quiet", 60)
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(playlist_url, download=False)
        except youtube_dl.utils.DownloadError:
            print(f"Error: Invalid url")
            return []

        if "entries" in result:
            return [UrlData(entry['title'], entry['url']) for entry in result['entries']]
        elif "webpage_url" in result and "title" in result:
            return [UrlData(result['title'], result['webpage_url'])]
        else:
            print(list(result))
            return []


@retry(10, youtube_dl.DownloadError)
def download_video(url: str, output_dir: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': output_dir + '/%(title)s.%(ext)s',
        'audio_format': 'mp3',
        'extract_audio': True,
        'quiet': True,  # Suppress console output
        'extract_flat': True,  # Extract only URLs, no metadata
        'progress_hooks': [my_progressbar.my_hook],
        'logger': logging.Logger("quiet", level=60)
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


@anti_sleep
def download_playlist_videos(playlist_urls_data: list[UrlData], download_indexes: list[int], output_dir: str):
    failed: list[tuple[int, str, Exception]] = []

    for idx in tqdm(download_indexes, "Total progress"):
        data = playlist_urls_data[idx]
        try:
            download_video(data.url, output_dir)
        except youtube_dl.DownloadError as exc:
            failed.append((idx, data.title, exc))

    # for aesthetics
    my_progressbar.close_bar()
    print()
    if failed:
        print("During download, some error occurred. The following songs were skipped")
    for fail_data in failed:
        idx, title, exc = fail_data
        print(f"  {title[:80]:<80} [{idx}]; {exc}")


def get_args():
    playlist_url = ""
    playlist_urls: list[UrlData] = []
    while not playlist_urls:
        while not playlist_url:
            playlist_url = input("Playlist url: ")
        playlist_urls = get_playlist_urls(playlist_url)
    download_indexes = user_input.get_songs_to_download(len(playlist_urls))
    if not download_indexes:
        return None
    output_dir = easygui.diropenbox("Choose Download Location", default=utils.get_windows_downloads_path())
    if not output_dir:
        return None
    print("""Playlist url: {}\nTotal songs: {}\nDownloading songs: {}\nOutput dir: {}""".format(
        playlist_url,
        len(playlist_urls),
        len(download_indexes),
        output_dir
    ))
    return playlist_urls, download_indexes, output_dir


def run():
    args = get_args()

    if args:
        urls, indexes, output_dir = args
        download_playlist_videos(urls, indexes, output_dir)
        print("Completed")
    else:
        print("Cancelled")


def main():
    running = True
    while running:
        try:
            run()
        except KeyboardInterrupt:
            print("Cancelled", end='')
            if utils.get_confirmation("exit?") is True:
                running = False
        except BaseException as exc:
            print(exc)
            input("press enter to continue")


if __name__ == '__main__':
    main()
