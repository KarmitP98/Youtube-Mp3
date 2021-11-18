import math
import re
from datetime import datetime

import pytube as pt
from moviepy.editor import *
from pytube import Playlist


# Get File Path
def get_file_path():
    home = os.path.expanduser('~')
    download_path = os.path.join(home, 'Downloads\\Youtube\\')
    return download_path


# Check if the file exists
def file_exists(file_name: str, path: str):
    if os.path.isfile(path + file_name):
        return True
    return False


# on_progress_callback takes 4 parameters.
def progress_check(chunk, file_handle, bytes_remaining=None):
    # Gets the percentage of the file that has been downloaded.
    percent = (100 * (file_size - bytes_remaining)) / file_size
    a1 = "[*--------------------] {:00.0f}% downloaded".format(percent)
    a2 = "[**-------------------] {:00.0f}% downloaded".format(percent)
    a3 = "[***------------------] {:00.0f}% downloaded".format(percent)
    a4 = "[****-----------------] {:00.0f}% downloaded".format(percent)
    a5 = "[*****----------------] {:00.0f}% downloaded".format(percent)
    a6 = "[******---------------] {:00.0f}% downloaded".format(percent)
    a7 = "[*******--------------] {:00.0f}% downloaded".format(percent)
    a8 = "[********-------------] {:00.0f}% downloaded".format(percent)
    a9 = "[*********------------] {:00.0f}% downloaded".format(percent)
    a10 = "[**********-----------] {:00.0f}% downloaded".format(percent)
    a11 = "[***********----------] {:00.0f}% downloaded".format(percent)
    a12 = "[************---------] {:00.0f}% downloaded".format(percent)
    a13 = "[*************--------] {:00.0f}% downloaded".format(percent)
    a14 = "[**************-------] {:00.0f}% downloaded".format(percent)
    a15 = "[***************------] {:00.0f}% downloaded".format(percent)
    a16 = "[****************-----] {:00.0f}% downloaded".format(percent)
    a17 = "[*****************----] {:00.0f}% downloaded".format(percent)
    a18 = "[******************---] {:00.0f}% downloaded".format(percent)
    a19 = "[*******************--] {:00.0f}% downloaded".format(percent)
    a20 = "[********************-] {:00.0f}% downloaded".format(percent)
    a21 = "[*********************] {:00.0f}% downloaded".format(percent)
    p_list = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21]
    print(p_list[math.floor(percent / 5)], end="\r")


# Download the video from Youtube and return the filename
def download_video(video_url: str, play_list_name: str, count: int, index: int, download_mode):
    path = get_file_path() + "\\" + play_list_name + "\\"
    v_ext = ".mp4"
    a_ext = ".mp3"

    try:
        yt = pt.YouTube(video_url, on_progress_callback=progress_check)
        # Set File-Name
        file_name = re.sub("[^A-Za-z0-9]+", " ", yt.title).title()
        file_name = re.sub('^\s+', "", file_name)
        file_name = re.sub("$\s+", "", file_name)
        if len(file_name) == 0:
            file_name = str(datetime.now())
        # Get the first stream (Usually the lowest quality, we just care about the audio here so it is fine!)
        video = yt.streams.get_audio_only() if download_mode == "1" else yt.streams.get_highest_resolution()
        download_file = True
        # Download it at this location
        if download_mode == "1":
            if file_exists(file_name + a_ext, path) or file_exists(file_name + v_ext, path):
                download_file = False

        if download_mode == "2" or download_mode == "3":
            if file_exists(file_name + v_ext, path):
                download_file = False

        if download_file:
            global file_size
            file_size = video.filesize
            print("Downloading...")
            print(file_name + (v_ext if download_mode != "1" else a_ext))
            print("Link: " + video_url)
            video.download(path, file_name + (v_ext if download_mode != "1" else a_ext))
            print("Download Complete!                                                                             ")
        else:
            print(file_name + " already exists!")
        print("*****----------------------------------*****")
        if file_name != "none":
            return file_name

    except Exception as e:
        print(e)


# Convert the video in the directory
def convert_video(file_name, play_list_name: str, download_mode):
    path = get_file_path() + "\\" + play_list_name + "\\"
    v_ext = ".mp4"
    a_ext = ".mp3"
    if file_exists(file_name + v_ext, path):
        if not file_exists(file_name + a_ext, path):
            print("Converting " + file_name + " to Audio...")
            # Convert the video into an audio
            vid = VideoFileClip(os.path.join(path + file_name + v_ext))
            vid.audio.write_audiofile(os.path.join(path + file_name + a_ext))
            vid.close()
            if download_mode == "1":
                os.remove(path + file_name + v_ext)
        else:
            print(file_name + " already exists!")
        print("*****----------------------------------*****")


# Download the playlist
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

    if download_mode == "3":
        print("\n\nStarting Conversion")
        for file in files:
            if file != "none":
                convert_video(file_name=file, play_list_name=title, download_mode=download_mode)


# Start the application
def start():
    refresh = input("Press (R) to refresh saved playlists or enter a new Playlist URL: ")
    if refresh == "r" or refresh == "R":
        f = open("playlists.txt", "r")
        lines = f.readlines()
        for line in lines:
            download_playlist(line.split(' ')[0], "1")
        f.close()
    else:
        playlist_url = refresh
        download_mode = input(
            "What do you want to download?\n(1) Audio Only\n(2) Video Only\n(3) Audio and "
            "Video\nPick "
            "any option ["
            "1/2/3]: ")

        download_playlist(playlist_url, download_mode)
        f = open("playlists.txt", "a")
        new_line = playlist_url + ' ' + download_mode
        f.write("\n" + new_line)
        f.close()


if __name__ == "__main__":
    start()

file_size = 0
