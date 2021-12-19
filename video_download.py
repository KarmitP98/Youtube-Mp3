import re

import pytube as pt
from moviepy.editor import *

V_EXT = ".mp4"
A_EXT = ".mp3"
file_size = 0
file_name = ""
progress = 0
DOWNLOAD_FOLDER = 'Downloads\\Youtube\\'


def progress_check(chunk=None, file_handle=None, remaining=None):
    # Gets the percentage of the file that has been downloaded.
    percent = (100 * (file_size - remaining)) / file_size
    global progress
    progress = percent
    if percent % 1 == 0:
        print("{:00.0f}% downloaded".format(percent))


def get_file_path():
    home = os.path.expanduser('~')
    global DOWNLOAD_FOLDER
    download_path = os.path.join(home, DOWNLOAD_FOLDER)
    return download_path


def video_to_audio():
    global file_name, V_EXT, A_EXT
    print("Converting mp4 to mp3...")
    # Convert the video into an audio
    path = get_file_path()
    vid = VideoFileClip(os.path.join(path + file_name + V_EXT))
    vid.audio.write_audiofile(os.path.join(path + file_name + A_EXT))
    vid.close()
    print("Audio Successfully Converted!")
    os.remove(path + file_name + V_EXT)


def get_video_from_youtube(video_url):
    global file_name, file_size, V_EXT
    try:
        yt = pt.YouTube(video_url)

        print("Video Title: " + yt.title)
        print("Video Author: " + yt.author)

        print("\nDownloading file to " + get_file_path())

        # Set File-Name
        file_name = re.sub("\W+", " ", yt.title).title()
        file_name = file_name.replace(" ", "-")

        video = pt.YouTube(video_url, on_progress_callback=progress_check)

        video_type = video.streams.filter(progressive=True, file_extension="mp4").first()

        file_size = video_type.filesize

        video_type.download(get_file_path())

    except Exception as e:
        print("Video not found!")

    video_to_audio()


def run():
    # PATH = "C:/Users/karmi/Desktop/Youtube/"

    video_url = input("Enter Youtube Vide URL: ")
    print(video_url)

    get_video_from_youtube(video_url)


if __name__ == "__main__":
    while 1:
        run()
