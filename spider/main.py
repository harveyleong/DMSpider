from .dmzj import Comic, Chapter
from .exceptions import DMException


def download_comic(url, path=None):
    """Downloads a comic."""

    try:
        comic = Comic(url)
        comic.download(path)
    except DMException as e:
        print(e)


def download_chapter(url, path=None):
    """Downloads a chapter."""

    try:
        chapter = Chapter(url)
        chapter.download(path)
    except DMException as e:
        print(e)


def download(urls, is_comic, path=None):
    """Downloads all comics or chapters."""

    function = download_comic if is_comic else download_chapter
    for url in urls:
        function(url, path)
    print("Done.")

