import re

from pytube import Playlist

from IO import write_to_file
from video import get_input_values, download_youtube_video


# Download the playlist
def download_playlist(playlist_url: str, mode: int, file_location: str):
    # Fetch playlist
    playlist = Playlist(playlist_url)

    # This fixes the empty playlist.videos list
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    # Fetch playlist Title
    title = playlist.title

    file_location = file_location + title + "\\"

    files = []
    count = 1
    total = len(playlist.video_urls)

    for url in playlist.video_urls:
        print("Downloading {} of {} for Playlist: {}...".format(count, total, title))
        files.append(download_youtube_video(url=url, mode=mode, file_location=file_location))
        count += 1

    print("Completed downloading the playlist.\n")
    # Return all the files
    return files


# Start the application
def start():
    url, mode, file_location = get_input_values(
        url_text="Press (Enter) to refresh saved playlists or enter a new Playlist URL: ")
    if url == '':
        f = open("playlists.txt", "r")
        lines = f.readlines()
        for line in lines:
            download_playlist(playlist_url=line.split(' ')[0], mode=int(line.split(' ')[1]),
                              file_location=file_location)
        f.close()
    else:
        # Download the playlist
        download_playlist(playlist_url=url, mode=mode, file_location=file_location)

        # Add the new playlist to file for future downloads
        write_to_file(data=url + ' ' + str(mode), file_name="playlists.txt", mode="a")


if __name__ == "__main__":
    start()
