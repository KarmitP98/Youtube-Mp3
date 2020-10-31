from pytube import Playlist
import pytube as pt
from moviepy.editor import *
import re


def run(video_url):
    PATH = "C:/Users/karmi/Desktop/Youtube/"
    V_EXT = ".mp4"
    A_EXT = ".mp3"

    print(video_url)

    try:
        yt = pt.YouTube(video_url)
        # Set File-Name
        file_name = re.sub("\W+", " ", yt.title).title()
        # Get the first stream (Usually the lowest quality, we just care about the audio here so it is fine!)
        video = yt.streams.first()
        # Download it at this location
        video.download(PATH, file_name)

        # Convert the video into an audio
        vid = VideoFileClip(os.path.join(PATH + file_name + V_EXT))
        vid.audio.write_audiofile(os.path.join(PATH + file_name + A_EXT))
        vid.close()

        os.remove(PATH + file_name + V_EXT)

    except Exception as e:
        print(e)


def download(playlist_url):
    playlist = Playlist(playlist_url)
    # this fixes the empty playlist.videos list
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    for url in playlist.video_urls:
        run(url)


def start():
    download(input("Enter the Youtube Playlist URL: "))


if __name__ == "__main__":
    start()
