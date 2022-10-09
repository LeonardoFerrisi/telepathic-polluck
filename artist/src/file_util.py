import cv2
import os

from pathlib import Path

def make_dir(dir_name):
    output_directory_fullpath = os.path.join(str(Path.cwd()), dir_name)
    Path(output_directory_fullpath).mkdir(parents=True, exist_ok=True)
    return output_directory_fullpath

def save_numpy_image(data, filename, output_directory):
    output_directory_fullpath = make_dir(output_directory)

    print("\nSaving image to " + output_directory + ": " + filename)
    file_full_path = os.path.join(output_directory_fullpath, filename)

    cv2.imwrite(file_full_path, data, [int(cv2.IMWRITE_JPEG_QUALITY), 100])