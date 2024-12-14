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

from bs4 import BeautifulSoup
from web import get
from samplepack import SamplePack


log = logging.getLogger(__name__)


class MusicRadarParser:
    """
    MusicRadar sample pack parser.
    """
    _main_url = ('https://www.musicradar.com/news/tech/'
                 'free-music-samples-royalty-free-loops-hits-and-multis-to-download-sampleradar')

    def __init__(self, queue_size: int = 0, packs_amount: int = 0):
        """
        Initialize the MusicRadar parser.

        :param queue_size: Sets the maxsize of the queue
        """
        self._main_queue = asyncio.Queue(maxsize=queue_size)
        self._packs_amount = packs_amount
        self._fail_queue = asyncio.Queue()
        self._sample_packs = []

    @property
    def sample_packs(self) -> list:
        """ A list of SamplePack objects. """
        return self._sample_packs

    async def start(self, workers: int) -> list:
        """
        Start the MusicRadar parser.

        This will get all the sample pack urls from
        the page(_main_url) containing links to sample
        packs (zip files)

        NOTE: The amount of workers should not be too high.
        since this could cause the server to not respond,
        resulting in timeouts

        :param workers: The amount of queue workers
        :return: A list of SamplePack objects
        """
        # prepare workers to work on the queue
        consumers = [asyncio.create_task(self._queue_worker(i))
                     for i in range(workers)]

        # start producing sample page urls
        await self._parse_sample_page_urls()

        # wait for all workers to be done
        await self._main_queue.join()

        # cancel workers. they will still be in
        # a loop state, waiting for queue items
        for consumer in consumers:
            consumer.cancel()

        # return a list of SamplePack objects
        return self._sample_packs

    async def _parse_sample_page_urls(self):

        log.info('starting url parsing')

        response = await get(self._main_url)
        if response is not None:

            soup = BeautifulSoup(await response.text(), 'html.parser')
            body = soup.find(attrs={'id': 'article-body'})

            p_tags = body.find_all('p')
            if len(p_tags) > 8:

                i = 0
                for p in p_tags[9:-1]:

                    if self._packs_amount > 0:
                        if i == self._packs_amount:
                            break

                    p_a_tag = p.a
                    if hasattr(p_a_tag, 'text'):
                        url = p_a_tag['href']
                        log.debug(f'parsed url: {url}')
                        if url.startswith('https://www.musicradar.com/'):
                            await self._main_queue.put(url)
                            i += 1

    async def _queue_worker(self, num: int):

        while True:
            url = await self._main_queue.get()
            log.debug(f'worker-{num}, handling: {url}')

            response = await get(url=url, rua=True, timeout=10)
            if response is not None:
                await self._parse_sample_pack_url(url, await response.text())
                self._main_queue.task_done()
            else:
                # TODO: implement something for the fail_queue
                await self._fail_queue.put(url)
                self._main_queue.task_done()

    async def _parse_sample_pack_url(self, url, response):

        soup = BeautifulSoup(response, 'html.parser')
        text_copy_class = soup.find(attrs={'class': 'text-copy bodyCopy auto'})

        if text_copy_class is not None:
            p_tags = text_copy_class.find_all('p')

            for p in p_tags:

                p_a_tag = p.a
                if p_a_tag is not None:

                    if p_a_tag['href'].endswith('.zip'):
                        pack_url = p_a_tag['href']
                        pack_title = p_a_tag.text

                        log.debug(f'sample pack url: {pack_url}, title: {pack_title}')

                        sample = SamplePack(url, pack_url, pack_title)
                        self._sample_packs.append(sample)
