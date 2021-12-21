import io
import os
import zipfile

from flask import send_file

from playlist import download_playlist
from video import download_youtube_video


# Check if variable is a list
def is_list(variable):
	return isinstance(variable, list)


# Write the data to the file
def write_to_file(data, file_name, mode: str = 'a'):
	file = open(file_name, mode)
	if is_list(data):
		file.writelines(data)
	else:
		file.writelines([data])
	file.close()


# Delete files from the location
def delete_files(files):
	if files:
		for file in files:
			os.remove(file)


# Returned zipped files
def zip_files(files):
	if files:
		data = io.BytesIO()
		with zipfile.ZipFile(data, mode = 'w') as z:
			for file in files:
				z.write(file)
		data.seek(0)
		return data


def get_zipped(url: str, mode: int, file_location: str, url_type: str = 'file'):
	if url_type == 'file':
		files = download_youtube_video(url = url, mode = mode, file_location = file_location)
	else:
		files = download_playlist(playlist_url = url, mode = mode, file_location = file_location)
	zip_file = zip_files(files)
	delete_files(files)
	return send_file(zip_file, attachment_filename = 'download.zip', as_attachment = True)
