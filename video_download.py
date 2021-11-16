import re

import pytube as pt
from moviepy.editor import *


def progress_Check(chunk=None, file_handle=None, remaining=None):
    # Gets the percentage of the file that has been downloaded.
    percent = (100 * (file_size - remaining)) / file_size
    if percent % 1 == 0:
        print("{:00.0f}% downloaded".format(percent))


def getFilePath():
    home = os.path.expanduser('~')
    download_path = os.path.join(home, 'Desktop\\Youtube\\')
    return download_path


def videoToAudio():
    global file_name
    print("Converting mp4 to mp3...")
    # Convert the video into an audio
    path = getFilePath()
    vid = VideoFileClip(os.path.join(path + file_name + V_EXT))
    vid.audio.write_audiofile(os.path.join(path + file_name + A_EXT))
    vid.close()
    print("Audio Successfully Converted!")
    os.remove(path + file_name + V_EXT)


def getVideoFromYoutube(video_url):
    global file_name, file_size
    try:
        yt = pt.YouTube(video_url)

        print("Video Title: " + yt.title)
        print("Video Author: " + yt.author)

        print("\nDownloading video...")

        # Set File-Name
        file_name = re.sub("\W+", " ", yt.title).title()

        video = pt.YouTube(video_url, on_progress_callback=progress_Check)

        video_type = video.streams.filter(progressive=True, file_extension="mp4").first()

        file_size = video_type.filesize

        video_type.download(getFilePath(), input("Do you also want to download the video?"))

    except Exception as e:
        print("Video not found!")

    videoToAudio()


def run():
    # PATH = "C:/Users/karmi/Desktop/Youtube/"

    video_url = input("Enter Youtube Vide URL: ")
    print(video_url)

    getVideoFromYoutube(video_url)


if __name__ == "__main__":
    while 1:
        run()

V_EXT = ".mp4"
A_EXT = ".mp3"
file_size = 0
file_name = ""
