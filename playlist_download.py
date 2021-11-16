import re
import threading
from datetime import datetime

import pytube as pt
from moviepy.editor import *
from pytube import Playlist


class DownloadAndConvert(threading.Thread):
    def __init__(self, id, playlist, name, audio_only):
        threading.Thread.__init__(self)
        self.playlist = playlist
        self.name = name
        self.id = id
        self.audio_only = audio_only

    def run(self) -> None:
        files = []
        index = 0
        for url in self.playlist:
            files.append(download_video(url, self.name, len(self.playlist), index, audio_only=self.audio_only))
            index += 1

        print(files)
        index = 1
        print("\n\nStarting Conversion")

        for file in files:
            print(file)
            if file != "none":
                convert_video(file_name=file, play_list_name=self.name, count=len(files), index=index,
                              audio_only=self.audio_only)
                index += 1

    def stopThread(self, name):
        name.exit()


def file_exists(file_name: str, path: str = 'C:/Users/karmit_patel/Desktop/Youtube/'):
    if os.path.isfile(path + file_name):
        return True
    return False


def download_video(video_url: str, play_list_name: str, count: int, index: int, audio_only):
    path = "C:/Users/karmit_patel/Desktop/Youtube/" + play_list_name + "/"
    v_ext = ".mp4"
    a_ext = ".mp3"

    try:
        yt = pt.YouTube(video_url)
        # Set File-Name
        file_name = re.sub("[^A-Za-z0-9]+", " ", yt.title).title()
        file_name = re.sub('^\s+', "", file_name)
        file_name = re.sub("$\s+", "", file_name)
        if len(file_name) == 0:
            file_name = str(datetime.now())
        # Get the first stream (Usually the lowest quality, we just care about the audio here so it is fine!)
        video = yt.streams.get_highest_resolution()
        download_file = True
        # Download it at this location
        if audio_only:
            if file_exists(file_name + a_ext, path):
                download_file = False
        else:
            if file_exists(file_name + v_ext, path):
                download_file = False

        if download_file:
            print("Downloading...")
            print(file_name + v_ext)
            print("Link: " + video_url)
            video.download(path, file_name + v_ext)
        else:
            print(file_name + " already exists!")
        if file_name != "none":
            return file_name

    except Exception as e:
        print(e)


def convert_video(file_name, play_list_name: str, count, index, audio_only):
    path = "C:/Users/karmit_patel/Desktop/Youtube/" + play_list_name + "/"
    v_ext = ".mp4"
    a_ext = ".mp3"
    if not file_exists(file_name + a_ext, path):
        print("Converting " + file_name + " to Audio...")
        # Convert the video into an audio
        vid = VideoFileClip(os.path.join(path + file_name + v_ext))
        vid.audio.write_audiofile(os.path.join(path + file_name + a_ext))
        vid.close()
        if audio_only:
            os.remove(path + file_name + v_ext)


def download(playlist_url: str, a: str):
    files = []
    index = 1
    audio_only = True if a == 1 else False

    playlist = Playlist(playlist_url)

    # # this fixes the empty playlist.videos list
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    middle = playlist.length // 2
    title = playlist.title

    urls = []

    for url in playlist.video_urls:
        urls.append(url)

    playlist_1 = urls[:middle]
    playlist_2 = urls[middle:]

    thread_1 = DownloadAndConvert(1, playlist_1, title, audio_only)
    thread_2 = DownloadAndConvert(2, playlist_2, title, audio_only)

    thread_1.start()
    thread_2.start()


def start():
    download(playlist_url=input("Enter the Youtube Playlist URL: "),
             a=input("What do you want to download?\n(1) Audio\n(2) Audio and Video\n:"))


if __name__ == "__main__":
    start()
