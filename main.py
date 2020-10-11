# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2020 Nortxort

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

# ------------- Configuration ----------------
# You could change these settings to speed up the overall process.
# But do bare in mind that setting SIMULTANEOUS_PARSER_TASKS
# and SIMULTANEOUS_DOWNLOADER_TASKS to high could lead to errors.

# The amount of simultaneous tasks for the parser.
SIMULTANEOUS_PARSER_TASKS = 40

# The wait time between parser tasks.
PARSER_WAIT_TIME = 5

# The amount of simultaneous downloader tasks.
SIMULTANEOUS_DOWNLOADER_TASKS = 20

# The wait time between download tasks.
DOWNLOADER_WAIT_TIME = 3
# --------------------------------------------

log = logging.getLogger(__name__)


def logger_setup():
    fmt = '%(asctime)s : %(levelname)s : %(filename)s : ' \
          '%(lineno)d : %(funcName)s() : %(name)s : %(message)s'

    logging.basicConfig(filename='debug.log', level=10, format=fmt)


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

    parser = MusicRadarParser(tasks_amount=SIMULTANEOUS_PARSER_TASKS,
                              wait_time=PARSER_WAIT_TIME)
    await parser.gather_urls()
    print(f'\n{len(parser.sample_pages)} urls parsed.')

    print(f'\nParsing sample pack urls...please wait.')
    await parser.gather_sample_urls()
    print(f'Found {len(parser.sample_packs)} sample packs on {len(parser.sample_pages)} pages.')

    if parser.errors > 0:
        print(f'{parser.errors} parser errors. Try adjusting the configuration.')

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

        dl = Downloader(fh.path, tasks_amount=SIMULTANEOUS_DOWNLOADER_TASKS,
                        wait_time=DOWNLOADER_WAIT_TIME)
        print(f'\nStarting downloader, this might take a while...')

        start = time.time()

        results = await dl.download(downloads)
        if len(results) == 0:
            print('Nothing was downloaded.')
        else:
            for download in results:
                print(f'Downloaded {download}')

            t = time.strftime('%H:%M:%S', time.gmtime(time.time() - start))
            print(f'\nDownloaded {len(downloads)} sample packs in {t}.')

    log.debug('cleaning up')
    await Session.close()
    await asyncio.sleep(2)


def main():
    path = input('\nEnter root path [default=\'./samples\']: ') or './samples'

    asyncio.run(run(path))


if __name__ == '__main__':
    logger_setup()
    main()
