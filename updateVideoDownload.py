import os
import re

from pytube import YouTube

V_EXT = '.mp4'
A_EXT = '.mp3'
file_name = ''
file_size = 0
progress = 0
DOWNLOAD_LOCATION = 'Downloads\\Youtube\\'


# on_progress_callback takes 4 parameters.
def progress_check(chunk, file_handle, bytes_remaining=None):
    # Gets the percentage of the file that has been downloaded.
    global file_size, progress
    progress = (100 * (file_size - bytes_remaining)) / file_size
    print("{:00.0f}% downloaded".format(progress))


def sanitize_filename(name):
    global file_name
    file_name = re.sub("[^A-Za-z0-9]+", " ", name)
    file_name = re.sub('^\s+', "", file_name)
    file_name = re.sub("$\s+", "", file_name)
    return file_name


# Grabs the file path for Download
def file_path():
    global DOWNLOAD_LOCATION
    home = os.path.expanduser('~')
    download_path = os.path.join(home, DOWNLOAD_LOCATION)
    return download_path


def start():
    global V_EXT, file_size
    print("Your video will be saved to: {}".format(file_path()))
    # Input
    yt_url = input("Copy and paste your YouTube URL here: ")
    print(yt_url)
    print("Accessing YouTube URL...")

    # Searches for the video and sets up the callback to run the progress indicator.
    try:
        video = YouTube(yt_url, on_progress_callback=progress_check)
    except:
        print("ERROR. Check your:\n  -connection\n  -url is a YouTube url\n\nTry again.")
        start()

    # Get the first video type - usually the best quality.
    video_type = video.streams.filter(type='video').get_highest_resolution()

    # Gets the title of the video
    title = video.title

    # Prepares the file for download
    print("Fetching: {} ...".format(title))
    file_size = video_type.filesize
    # Starts the download process
    try:
        video_type.download(output_path=file_path(), filename=sanitize_filename(title) + V_EXT, skip_existing=True,
                            max_retries=2, timeout=5000)
        print("Video successfully downloaded at {}".format(file_path() + file_name + V_EXT))
    except:
        print("Error downloading the video!\nPlease try again!")


if __name__ == "__main__":
    start()
