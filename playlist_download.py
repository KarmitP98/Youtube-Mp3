import re

import pytube as pt
from moviepy.editor import *
from pytube import Playlist


def download_video(video_url: str, play_list_name: str):
    PATH = "C:/Users/karmi/Desktop/Youtube/" + play_list_name + "/"
    V_EXT = ".mp4"

    try:
        yt = pt.YouTube(video_url)
        # Set File-Name
        file_name = re.sub("\W+", " ", yt.title).title()
        print("Downloading...")
        print(file_name + V_EXT)
        # Get the first stream (Usually the lowest quality, we just care about the audio here so it is fine!)
        video = yt.streams.first()
        # Download it at this location
        video.download(PATH, file_name)
        return file_name

    except Exception as e:
        print(e)


def convert_video(file_name, play_list_name: str):
    PATH = "C:/Users/karmi/Desktop/Youtube/" + play_list_name + "/"
    V_EXT = ".mp4"
    A_EXT = ".mp3"

    print("Converting " + file_name + " to Audio...")
    # Convert the video into an audio
    vid = VideoFileClip(os.path.join(PATH + file_name + V_EXT))
    vid.audio.write_audiofile(os.path.join(PATH + file_name + A_EXT))
    vid.close()
    os.remove(PATH + file_name + V_EXT)


def download(playlist_url: str, play_list_name: str):
    playlist = Playlist(playlist_url)
    # this fixes the empty playlist.videos list
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    files = []

    for url in playlist.video_urls:
        files.append(download_video(url, play_list_name))

    print(files)

    for file in files:
        convert_video(file_name=file, play_list_name=play_list_name)


def start():
    download(playlist_url=input("Enter the Youtube Playlist URL: "), play_list_name=input("Enter the playlist Name: "))


if __name__ == "__main__":
    start()
