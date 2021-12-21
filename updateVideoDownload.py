import math
import os
import re

from pytube import YouTube

V_EXT = '.mp4'
A_EXT = '.mp3'
EXT = ''
file_name = ''
file_size = 0
progress = 0
DOWNLOAD_LOCATION = 'Downloads\\Youtube\\'


# on_progress_callback takes 3 parameters.
def progress_check(chunk, file_handle, bytes_remaining=None):
    # Gets the percentage of the file that has been downloaded.
    global file_size, progress
    # progress = (100 * (file_size - bytes_remaining)) / file_size
    # print("{:00.0f}% downloaded".format(progress))
    # Gets the percentage of the file that has been downloaded.
    percent = (100 * (file_size - bytes_remaining)) / file_size
    progress = percent
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


def sanitize_filename(name):
    global file_name
    file_name = re.sub("[^A-Za-z0-9]+", " ", name)
    file_name = re.sub('^\s+', "", file_name)
    file_name = re.sub("$\s+", "", file_name)
    file_name = file_name.strip()
    return file_name


# Grabs the file path for Download
def default_file_location():
    global DOWNLOAD_LOCATION
    home = os.path.expanduser('~')
    download_path = os.path.join(home, DOWNLOAD_LOCATION)
    return download_path


def start():
    # Input
    url, mode, file_location = get_input_values(url_text="Please enter your Youtube URL: ")
    print("Accessing YouTube URL...")
    video_file = download_youtube_video(url=url, mode=mode, file_location=file_location)


def download_youtube_video(url: str, mode: int, file_location: str = default_file_location()):
    global EXT, V_EXT, A_EXT, file_size, file_name
    try:
        # Searches for the video and sets up the callback to run the progress indicator.
        video = YouTube(url, on_progress_callback=progress_check)

        # Set the file extension based on the download mode
        EXT = V_EXT if mode == 1 else A_EXT

        # Get video or audio file based on the download mode
        if mode == 1:
            video_type = video.streams.filter(type='video').get_highest_resolution()
        else:
            video_type = video.streams.filter(type='audio').get_audio_only()

        # Gets the title of the video
        file_name = sanitize_filename(video.title)

        # Prepares the file for download
        print("Fetching: {} ...".format(file_name))
        file_size = video_type.filesize
        # Starts the download process

        video_type.download(output_path=file_location, filename=file_name + EXT, skip_existing=True)
        print(("Video" if mode == 1 else "Audio") + " successfully downloaded at {}".format(
            file_location + file_name + EXT))

        return file_location + file_name + EXT
    except:
        print("ERROR: Check your connection or URL!")


def get_input_values(url_text: str, mode_text: str = "0: Audio [Default]\n1: Video\nPlease select an option:"):
    url = input(url_text)
    mode = input(mode_text)
    file_location = input("Enter file location: [Default: {}]:".format(default_file_location()))

    if mode == '':
        mode = 0
    if file_location == '':
        file_location = default_file_location()

    return url, int(mode), file_location


if __name__ == "__main__":
    start()
