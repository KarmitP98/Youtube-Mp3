import io
import os
import zipfile


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

