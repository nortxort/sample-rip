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

from web import download_file

log = logging.getLogger(__name__)


class Downloader:
    """
    Class to download files.
    """
    def __init__(self, path, sample_packs: list, queue_size: int = 10):
        """
        Initialize the Downloader class.

        :param path: The path to the download directory.
        :param sample_packs: A list of SamplePack objects.
        """
        self._path = path
        self._sample_packs = sample_packs
        self._main_queue = asyncio.Queue(maxsize=queue_size)
        self._downloaded_files = []

    async def start(self, workers: int):
        # prepare workers to work on the queue
        consumers = [asyncio.create_task(self._queue_worker())
                     for _ in range(workers)]

        # start adding urls to the queue
        await self._create_download_queue()

        log.debug('calling queue.join()')
        # wait for all workers to be done
        await self._main_queue.join()

        log.debug('cancelling consumers')
        # cancel workers. they will still be in
        # a loop state, waiting for queue items
        for consumer in consumers:
            consumer.cancel()

        # return a list of downloaded file locations
        return self._downloaded_files

    async def _create_download_queue(self):
        for pack in self._sample_packs:
            log.debug(f'adding {pack.url} to download queue')
            await self._main_queue.put(pack)

    async def _queue_worker(self):

        while True:
            pack = await self._main_queue.get()
            log.debug(f'handling: {pack}')
            destination = self._path.joinpath(pack.file_name)
            downloaded_file = await self._download(pack.url, destination)
            self._downloaded_files.append(downloaded_file)
            self._main_queue.task_done()

    @staticmethod
    async def _download(url: str, destination: str):
        # download file from url to the destination.
        return await download_file(url=url,
                                   destination=destination,
                                   rua=True)
