import re

from pytube import Playlist

from IO import write_to_file
from updateVideoDownload import get_input_values, download_youtube_video


# on_progress_callback takes 4 parameters.
# def progress_check(chunk, file_handle, bytes_remaining=None):
#     # Gets the percentage of the file that has been downloaded.
#     percent = (100 * (file_size - bytes_remaining)) / file_size
#     a1 = "[*--------------------] {:00.0f}% downloaded".format(percent)
#     a2 = "[**-------------------] {:00.0f}% downloaded".format(percent)
#     a3 = "[***------------------] {:00.0f}% downloaded".format(percent)
#     a4 = "[****-----------------] {:00.0f}% downloaded".format(percent)
#     a5 = "[*****----------------] {:00.0f}% downloaded".format(percent)
#     a6 = "[******---------------] {:00.0f}% downloaded".format(percent)
#     a7 = "[*******--------------] {:00.0f}% downloaded".format(percent)
#     a8 = "[********-------------] {:00.0f}% downloaded".format(percent)
#     a9 = "[*********------------] {:00.0f}% downloaded".format(percent)
#     a10 = "[**********-----------] {:00.0f}% downloaded".format(percent)
#     a11 = "[***********----------] {:00.0f}% downloaded".format(percent)
#     a12 = "[************---------] {:00.0f}% downloaded".format(percent)
#     a13 = "[*************--------] {:00.0f}% downloaded".format(percent)
#     a14 = "[**************-------] {:00.0f}% downloaded".format(percent)
#     a15 = "[***************------] {:00.0f}% downloaded".format(percent)
#     a16 = "[****************-----] {:00.0f}% downloaded".format(percent)
#     a17 = "[*****************----] {:00.0f}% downloaded".format(percent)
#     a18 = "[******************---] {:00.0f}% downloaded".format(percent)
#     a19 = "[*******************--] {:00.0f}% downloaded".format(percent)
#     a20 = "[********************-] {:00.0f}% downloaded".format(percent)
#     a21 = "[*********************] {:00.0f}% downloaded".format(percent)
#     p_list = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21]
#     print(p_list[math.floor(percent / 5)], end="\r")


# Convert the video in the directory
# def convert_video(file_name, play_list_name: str, download_mode):
#     path = get_file_path() + "\\" + play_list_name + "\\"
#     v_ext = ".mp4"
#     a_ext = ".mp3"
#     if file_exists(file_name + v_ext, path):
#         if not file_exists(file_name + a_ext, path):
#             print("Converting " + file_name + " to Audio...")
#             # Convert the video into an audio
#             vid = VideoFileClip(os.path.join(path + file_name + v_ext))
#             vid.audio.write_audiofile(os.path.join(path + file_name + a_ext))
#             vid.close()
#             if download_mode == "1":
#                 os.remove(path + file_name + v_ext)
#         else:
#             print(file_name + " already exists!")
#         print("*****----------------------------------*****")


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
