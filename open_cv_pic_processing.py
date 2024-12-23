import os
from os import path, walk
import cv2


def get_jpg_files_more_x_pix(dir_path: str, x: int = 1024) -> list:
    jpg_paths_for_resize = []
    for root, dirs, files in walk(dir_path):
        for file in files:
            if file.endswith('.jpg') or file.endswith(
                    '.jpeg') or file.endswith('.png'):
                file_path = path.join(root, file)
                jpg_file_candidate = cv2.imread(file_path)
                if jpg_file_candidate is not None and jpg_file_candidate.shape[
                    0] > x:
                    jpg_paths_for_resize.append(
                        (path.abspath(file_path), os.path.getsize(file_path)))
    return jpg_paths_for_resize


def get_files_more_x_KB(dir_path: str, x=200):
    file_candidates_list = []
    # print(dir_path)
    for root, dirs, files in walk(dir_path):
        for file in files:
            if file.endswith('.jpg') or file.endswith(
                    '.jpeg') or file.endswith('.png'):
                file_path = path.join(root, file)
                file_size = os.path.getsize(file_path)
                if file_size > x * 1024:
                    file_candidates_list.append(
                        (path.abspath(file_path), file_size))
    return file_candidates_list


def get_size_of_files_for_resize(files_list: list) -> tuple:
    t_size = 0
    # print(files_list)
    for _, size in files_list:
        t_size += size
    t_size /= 1024 * 1024
    return (t_size, len(files_list))


def resize_files(file_paths_list: list, desired_width: int = 1024) -> None:
    for file_path, _ in file_paths_list:
        img = cv2.imread(file_path)
        aspect_ratio = img.shape[1] / img.shape[0]  # width/height
        desired_height = int(desired_width / aspect_ratio)
        new_size = (desired_width, desired_height)
        resized_img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
        cv2.imwrite(file_path, resized_img)


def encode_files(file_paths_list: list, quality: int = 70) -> None:
    for file_path, _ in file_paths_list:
        img = cv2.imread(file_path)
        if img is not None:
            encode_param = [cv2.IMWRITE_JPEG_QUALITY, quality]
            result, imgencode = cv2.imencode(".jpg", img, encode_param)
            if result:
                with open(file_path, "wb") as f:
                    f.write(imgencode)


if __name__ == "__main__":
    # print("start resizing")
    # files_list = get_jpg_files_more_1024pix(r"W:\goods_photos")
    # print(get_size_of_files_for_resize(files_list))
    # resize_files(files_list)
    print("start encoding")
    files_list = get_files_more_x_KB(r"W:\goods_photos")
    encode_files(files_list)

