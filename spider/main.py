import os
import zipfile

from .dmzj import Comic, Chapter
from .exceptions import DMException


def compress_folder(directory_path):
    """Compresses picture folder using .zip format."""

    def list_file(directory_path):
        paths = []
        for dir_path, dirnames, filenames in os.walk(directory_path):
            for filename in filenames:
                paths.append(os.path.join(dir_path, filename))
        length = len(directory_path)
        files = [(path, path[length:].strip('/')) for path in paths]
        return files

    zip_name = directory_path.strip('/').split('/')[-1] + ".zip"
    saved_path = '/' + '/'.join(directory_path.strip('/').split('/')[:-1])
    files = list_file(directory_path)
    with zipfile.ZipFile(
            os.path.join(saved_path, zip_name),
            "w",
            zipfile.ZIP_DEFLATED) as f:
        for file in files:
            f.write(file[0], file[1])


def download_comic(url, path=None):
    """Downloads a comic."""

    try:
        comic = Comic(url)
        comic.download(path)
    except DMException as e:
        print(e)
    return comic.saved_path


def download_chapter(url, path=None):
    """Downloads a chapter."""

    try:
        chapter = Chapter(url)
        chapter.download(path)
    except DMException as e:
        print(e)
    return chapter.saved_path


def download(urls, is_comic, path=None, zip=False):
    """Downloads all comics or chapters."""

    function = download_comic if is_comic else download_chapter
    for url in urls:
        saved_path = function(url, path)
        if zip:
            compress_folder(saved_path)
    print("Done.")

