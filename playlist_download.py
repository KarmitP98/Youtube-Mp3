import re
from datetime import datetime

import pytube as pt
from moviepy.editor import *
from pytube import Playlist


# class DownloadAndConvert(threading.Thread):
#     def __init__(self, id, playlist, name, download_mode):
#         threading.Thread.__init__(self)
#         self.playlist = playlist
#         self.name = name
#         self.id = id
#         self.download_mode = download_mode
#
#     def run(self) -> None:
#         files = []
#         index = 0
#         for url in self.playlist:
#             files.append(download_video(url, self.name, len(self.playlist), index, download_mode=self.download_mode))
#             index += 1
#
#         print(files)
#         index = 1
#         print("\n\nStarting Conversion")
#
#         for file in files:
#             print(file)
#             if file != "none":
#                 convert_video(file_name=file, play_list_name=self.name, count=len(files), index=index,
#                               download_mode=self.download_mode)
#                 index += 1
#
#     def stopThread(self, name):
#         name.exit()


def file_exists(file_name: str, path: str):
    if os.path.isfile(path + file_name):
        return True
    return False


def download_video(video_url: str, play_list_name: str, count: int, index: int, download_mode):
    path = "./Downloads/" + play_list_name + "/"
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
        if download_mode == "1":
            if file_exists(file_name + a_ext, path):
                download_file = False

        if download_mode == "2":
            if file_exists(file_name + v_ext, path):
                download_file = False

        if download_mode == "3":
            if file_exists(file_name + v_ext, path) and file_exists(file_name + a_ext, path):
                download_file = False

        if download_file:
            print("Downloading...")
            print(file_name + v_ext)
            print("Link: " + video_url)
            video.download(path, file_name + v_ext)
        else:
            print(file_name + " already exists!")
        print("*****----------------------------------*****")
        if file_name != "none":
            return file_name

    except Exception as e:
        print(e)


def convert_video(file_name, play_list_name: str, download_mode):
    path = "./Downloads/" + play_list_name + "/"
    v_ext = ".mp4"
    a_ext = ".mp3"
    if file_exists(file_name + v_ext, path):
        if not file_exists(file_name + a_ext, path):
            print("Converting " + file_name + " to Audio...")
            # Convert the video into an audio
            vid = VideoFileClip(os.path.join(path + file_name + v_ext))
            vid.audio.write_audiofile(os.path.join(path + file_name + a_ext))
            vid.close()
        else:
            print(file_name + " already exists!")
        print("*****----------------------------------*****")
        if download_mode == "1":
            os.remove(path + file_name + v_ext)


def download_playlist(playlist_url: str, download_mode: str):
    playlist = Playlist(playlist_url)

    # # this fixes the empty playlist.videos list
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    title = playlist.title

    files = []
    index = 0
    for url in playlist.video_urls:
        files.append(download_video(url, title, len(playlist), index, download_mode=download_mode))
        index += 1

    index = 1

    if download_mode != "2":
        print("\n\nStarting Conversion")
        for file in files:
            if file != "none":
                convert_video(file_name=file, play_list_name=title, download_mode=download_mode)


def start():
    download_playlist(playlist_url=input("Enter the Youtube Playlist URL: "),
                      download_mode=input(
                          "What do you want to download?\n(1) Audio Only\n(2) Video Only\n(3) Audio and Video\nPick "
                          "any option ["
                          "1/2/3]:"))


if __name__ == "__main__":
    start()
