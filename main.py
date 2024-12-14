# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2024 Nortxort

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import logging
import asyncio
import time

from file_handler import FileHandler
from musicradar import MusicRadarParser
from downloader import Downloader
from web import Session

# version 2.0.0

# the max amount of sample packs to process.
# setting this to 0 will download all packs.
MAX_SAMPLE_PACKS = 5

# amounts of simultaneously parsers.
PARSER_WORKERS = 3

# max size of the parser queue.
# https://docs.python.org/3/library/asyncio-queue.html#asyncio.Queue
PARSER_QUEUE_MAX_SIZE = 0

# amount of simultaneously downloads.
DOWNLOAD_WORKERS = 20

# max size of the download queue.
DOWNLOAD_QUEUE_MAX_SIZE = 150

# Debug
DEBUG = True

log = logging.getLogger(__name__)


def set_logger():

    fmt = ('%(asctime)s,%(msecs)03d:%(levelname)s:'
           'L%(lineno)d:%(filename)s:'
           '%(name)s.%(funcName)s(): %(message)s')

    logging.basicConfig(
        format=fmt,
        datefmt='%d/%m/%Y %H:%M:%S',
        level=logging.DEBUG
    )


if DEBUG:
    set_logger()


async def run(path: str):
    old_samples = []

    fh = FileHandler(path)

    if not fh.is_valid_path():
        print(f'path {path} does not exists. Creating..')
        fh.create_dir()
        if not fh.is_dir():
            print(f'Failed to create directory at {fh.path}, quitting.')
            return
        else:
            print(f'Successfully created directory at {fh.path}')

    if not fh.is_dir():
        print(f'{fh.path} is not a directory, quitting.')
        return

    if not fh.was_dir_created:
        old_samples = fh.iter_root_dir()
        print(f'Found {len(old_samples)} sample packs at {fh.path}')

    print('Starting parser..')

    parser = MusicRadarParser(PARSER_QUEUE_MAX_SIZE, MAX_SAMPLE_PACKS)
    sample_packs = await parser.start(workers=PARSER_WORKERS)

    print(f'parsed {len(sample_packs)} sample packs urls')

    downloads = []

    if len(old_samples) > 0:
        print('\nComparing files.')
        downloads, ignored = fh.compare(parser.sample_packs, old_samples)
        print(f'ignored {len(ignored)} sample packs already on local system.')
    else:
        downloads.extend(parser.sample_packs)

    if len(downloads) == 0:
        print('There is nothing to download.')
    else:
        input(f'Press enter to start downloading {len(downloads)} sample packs.')

        dl = Downloader(fh.path, downloads, DOWNLOAD_QUEUE_MAX_SIZE)
        print(f'\nStarting downloader, this might take a while...')

        start = time.time()

        results = await dl.start(workers=DOWNLOAD_WORKERS)
        if len(results) == 0:
            print('Nothing was downloaded.')
        else:
            for downloaded_file in results:
                print(f'Downloaded: {downloaded_file}')

            t = time.strftime('%H:%M:%S', time.gmtime(time.time() - start))
            print(f'\nDownloaded {len(downloads)} sample packs in {t}.')

    await Session.close()


def main():
    path = input('\nEnter root path [default=\'./samples\']: ') or './samples'

    asyncio.run(run(path))


if __name__ == '__main__':
    main()
