import os
from os import path, walk
import cv2

# В этом кортеже перечислены все расширения файлов которые нужно считать
# изображениями.
PICTURES_EXTENSIONS = (".jpeg", ".jpg", ".png", ".webp")


def get_pictures_more_x_pix(dir_path: str, x_pix: int = 1024) -> list:
    """
    Рекурсивно обходит все вложенные папки в dir_path, проверяет размер в
    пикселях для файлов с расширениями перечисленными в PICTURES_EXTENSIONS.
    Если у файла размер по оси x больше чем x_pix, то добавляем такой файл в
    список pic_paths_for_resize в виде кортежа, содержащего первым элементом
    абсолютный путь к файлу, а вторым элементом, размер файла в байтах.

    :param dir_path: str
    :param x_pix: int
    :return: list[tuple[str, int]]
    """
    pic_paths_for_resize = []
    for root, dirs, files in walk(dir_path):
        for file_name in files:
            if file_name.endswith(PICTURES_EXTENSIONS):
                file_path = path.join(root, file_name)
                picture_candidate = cv2.imread(file_path)
                if (picture_candidate is not None and
                        picture_candidate.shape[1] > x_pix):
                    pic_paths_for_resize.append(
                        (path.abspath(file_path), os.path.getsize(file_path)))
    return pic_paths_for_resize


def get_files_more_x_kb(dir_path: str, file_size_limit=200):
    """
    Рекурсивно обходит все вложенные папки в dir_path, проверяет размер файла
    для файлов с расширениями перечисленными в PICTURES_EXTENSIONS. Если размер
    больше чем file_size_limit, задается в килобайтах, то добавляем такой файл
    в список file_candidates_list в виде кортежа, содержащего первым элементом
    абсолютный путь к файлу, а вторым элементом, размер файла в байтах.
    
    :param dir_path: str
    :param file_size_limit: int
    :return: list[tuple[str, int]]
    """

    file_candidates_list = []
    for root, dirs, files in walk(dir_path):
        for file in files:
            if file.endswith(PICTURES_EXTENSIONS):
                file_path = path.join(root, file)
                file_size = os.path.getsize(file_path)
                if file_size > file_size_limit * 1024:
                    file_candidates_list.append(
                        (path.abspath(file_path), file_size))
    return file_candidates_list


def get_total_size_of_all_files(files_list: list) -> tuple:
    """
    Возвращает общий размер всех файлов в списке в мегабайтах и их количество.
    :param files_list: list[tuple[str, int]]
    :return: tuple[int, int]
    """
    t_size = 0
    for _, size in files_list:
        t_size += size
    t_size /= 1024 * 1024
    return t_size, len(files_list)


def resize_files(file_paths_list: list, desired_width: int = 1024) -> None:
    """
    Изменяет размер холста изображения до desired_width, высоту изменяет
    пропорционально (сохраняет пропорции). ВНИМАНИЕ, изменяет изображение на
    месте (перезаписывает исходники).

    :param file_paths_list: list[tuple[str, int]]
    :param desired_width: int
    :return: None
    """
    _, number_of_files_to_resize = get_total_size_of_all_files(file_paths_list)
    answer = input(f"WARNING!!! All {number_of_files_to_resize} files will "
                   f"overwritten. Are you sure? (yes/no)\n")
    if answer.lower() == "yes":
        for file_path, _ in file_paths_list:
            img = cv2.imread(file_path)
            aspect_ratio = img.shape[1] / img.shape[0]  # width/height
            desired_height = int(desired_width / aspect_ratio)
            new_size = (desired_width, desired_height)
            resized_img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
            cv2.imwrite(file_path, resized_img)
    else:
        print("Resizing is aborted")


def encode_files(file_paths_list: list, quality: int = 70) -> None:
    """
    Сжимает файлы с качеством quality. ВНИМАНИЕ, перезаписывает исходники.
    :param file_paths_list: list[tuple[str, int]]
    :param quality: int
    :return: None
    """
    answer = input("WARNING!!! All files will overwritten. Are you sure? "
                   "(yes/no)\n")
    if answer.lower() == 'yes':
        for file_path, _ in file_paths_list:
            img = cv2.imread(file_path)
            if img is not None:
                encode_param = [cv2.IMWRITE_JPEG_QUALITY, quality]
                result, imgencode = cv2.imencode(".jpg", img, encode_param)
                if result:
                    with open(file_path, "wb") as f:
                        f.write(imgencode)
    else:
        print("Encoding is aborted")


if __name__ == "__main__":
    print("start resizing")
    files_list = get_pictures_more_x_pix(r"test", 1024)
    resize_files(files_list)
    print(files_list)
    files_list = get_files_more_x_kb(r"test", 20)
    print(files_list)

    # resize_files(files_list)
    # print("start encoding")
    # files_list = get_files_more_x_KB(r"W:\goods_photos")
    # encode_files(files_list)

