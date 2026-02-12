import os

def get_files_in_directory(directory):
    filenames = []
    for directory, subdirectories, files in os.walk(directory):
        for file in files:
            filenames.append(os.path.join(directory, file))
    return filenames