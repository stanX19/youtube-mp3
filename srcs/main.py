import logging

import easygui
import my_progressbar
import user_input
import utils
import yt_dlp as youtube_dl
from tqdm import tqdm
from wininhibit import WindowsInhibitor
from decorators import retry, anti_sleep


def get_playlist_urls(playlist_url: str) -> list[str]:
    ydl_opts = {
        'quiet': True,  # Suppress console output
        'extract_flat': True,  # Extract only URLs, no metadata
        'logger': logging.Logger("quiet", level=logging.CRITICAL)
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(playlist_url, download=False)
        except youtube_dl.utils.DownloadError:
            print(f"Error: Invalid url")
            return []

        if "entries" in result:
            return [entry['url'] for entry in result['entries']]
        elif "webpage_url" in result:
            return [result['webpage_url']]
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
        'progress_hooks': [my_progressbar.my_hook]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_playlist_videos(playlist_urls: list[str], download_indexes: list[int], output_dir: str):
    for idx in tqdm(download_indexes, "Total progress"):
        url = playlist_urls[idx]
        download_video(url, output_dir)


def get_args():
    playlist_url = ""
    playlist_urls = []
    while not playlist_urls:
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


@anti_sleep
def main():
    args = get_args()

    if args and utils.get_confirmation("Continue?"):
        download_playlist_videos(*args)
        print("Completed")
    else:
        print("Cancelled")


if __name__ == '__main__':
    running = True
    while running:
        try:
            main()
        except KeyboardInterrupt:
            print("Cancelled", end='')
            if utils.get_confirmation("exit?") is True:
                running = False

