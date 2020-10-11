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

from utilities import chunk_list
from web import download_file

log = logging.getLogger(__name__)


class Downloader:
    """
    Class to download files.
    """
    def __init__(self, path, tasks_amount: int = 10, wait_time: int = 5):
        """
        Initialize the Downloader class.

        :param path: The path to the download directory.
        :param tasks_amount: The amount of tasks to run concurrently.
        :param wait_time: The wait time in seconds between concurrent tasks.
        """
        self._path = path
        self._tasks = tasks_amount
        self._wait = wait_time

    async def download(self, sample_packs: list) -> list:
        """
        Download SamplePacks concurrently.

        :param sample_packs: A list of SamplePack objects.
        :return: A list of strings containing the destination of files downloaded.
        """
        results = []

        log.debug('creating download tasks')

        sample_pack_chunks = chunk_list(sample_packs, self._tasks)
        for pack_chunk in sample_pack_chunks:

            tasks = []

            for chunk in pack_chunk:
                destination = self._path.joinpath(chunk.file_name)
                task = asyncio.create_task(self._download(chunk.url, destination))
                tasks.append(task)

            results = await asyncio.gather(*tasks)

            await asyncio.sleep(self._wait)

        return results

    @staticmethod
    async def _download(url: str, destination: str):
        # download file from url to the destination.
        return await download_file(url=url, destination=destination, rua=True, chunk_size=1024*4)
