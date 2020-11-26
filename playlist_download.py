import re
from datetime import datetime

import pytube as pt
from moviepy.editor import *
from pytube import Playlist


def download_video(video_url: str, play_list_name: str, count: int, index: int):
    PATH = "C:/Users/karmi/Desktop/Youtube/" + play_list_name + "/"
    V_EXT = ".mp4"

    try:
        print(str(index) + " of " + str(count))
        print("Downloading...")
        print("Link: " + video_url)
        yt = pt.YouTube(video_url)
        # Set File-Name
        file_name = re.sub("[^A-Za-z0-9]+", " ", yt.title).title()
        file_name = re.sub("^\s+", "", file_name)
        file_name = re.sub("$\s+", "", file_name)
        if len(file_name) == 0:
            file_name = str(datetime.now())
        print(file_name + V_EXT)
        # Get the first stream (Usually the lowest quality, we just care about the audio here so it is fine!)
        video = yt.streams.first()
        # Download it at this location
        video.download(PATH, file_name)
        if file_name != "none":
            return file_name

    except Exception as e:
        print(e)


def convert_video(file_name, play_list_name: str, count, index):
    PATH = "C:/Users/karmi/Desktop/Youtube/" + play_list_name + "/"
    V_EXT = ".mp4"
    A_EXT = ".mp3"

    print(str(index) + " of " + str(count))
    print("Converting " + file_name + " to Audio...")
    # Convert the video into an audio
    vid = VideoFileClip(os.path.join(PATH + file_name + V_EXT))
    vid.audio.write_audiofile(os.path.join(PATH + file_name + A_EXT))
    vid.close()
    os.remove(PATH + file_name + V_EXT)


def download(playlist_url: str, play_list_name: str):
    files = []
    index = 1

    playlist = Playlist(playlist_url)

    # # this fixes the empty playlist.videos list
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    for url in playlist.video_urls:
        files.append(download_video(url, play_list_name, len(playlist.video_urls), index))
        index += 1

    print(files)
    index = 1
    print("\n\nStarting Conversion")

    for file in files:
        print(file)
        if file != "none":
            convert_video(file_name=file, play_list_name=play_list_name, count=len(files), index=index)
            index += 1


def start():
    while (1):
        download(playlist_url=input("Enter the Youtube Playlist URL: "),
                 play_list_name=input("Enter the playlist Name: "))


if __name__ == "__main__":
    start()
