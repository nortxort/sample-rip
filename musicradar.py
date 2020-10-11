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

from bs4 import BeautifulSoup
from web import get
from utilities import chunk_list
from samplepack import SamplePack


log = logging.getLogger(__name__)


class MusicRadarError(Exception):
    pass


class NoSamplePagesError(MusicRadarError):
    pass


class MusicRadarParser:
    """
    MusicRadar sample pack parser.
    """
    _main_url = 'https://www.musicradar.com/news/tech/' \
                'free-music-samples-download-loops-hits-and-multis-627820'

    _sample_pages_urls = []
    _sample_packs = []
    _page_errors = 0

    def __init__(self, tasks_amount: int = 10, wait_time: int = 5):
        """
        Initialize the MusicRadar parser.

        :param tasks_amount: The amount of tasks to run concurrently.
        :param wait_time: The wait time in seconds between concurrent tasks.
        """
        self._tasks = tasks_amount
        self._wait = wait_time

    @property
    def sample_pages(self) -> list:
        """
        List containing parsed sample page urls.
        """
        return self._sample_pages_urls

    @property
    def sample_packs(self) -> list:
        """
        A list of SamplePack objects.
        """
        return self._sample_packs

    @property
    def errors(self) -> int:
        """
        Error count from parsing sample pack urls.
        """
        return self._page_errors

    async def gather_urls(self):
        """
        Parse the sample page urls.
        """
        log.info('starting url parsing')

        response = await get(self._main_url)
        if response is not None:

            soup = BeautifulSoup(await response.text(), 'html.parser')
            body = soup.find(attrs={'id': 'article-body'})

            p_tags = body.find_all('p')
            if len(p_tags) > 6:

                for p in p_tags[6:-1]:

                    p_a_tag = p.a
                    if hasattr(p_a_tag, 'text'):
                        log.debug(f'parsed url: {p_a_tag["href"]}')
                        self._sample_pages_urls.append(p_a_tag['href'])

    async def gather_sample_urls(self):
        """
        Parse sample pack urls concurrently.
        """
        if len(self._sample_pages_urls) == 0:
            raise NoSamplePagesError(f'No sample urls parsed, {len(self._sample_pages_urls)}')
        else:
            log.info('parsing sample pages')

            url_chunks = chunk_list(self._sample_pages_urls, self._tasks)

            for i, chunk in enumerate(url_chunks):

                tasks = []
                for url in chunk:
                    task = asyncio.create_task(get(url, rua=True))
                    tasks.append(task)

                pages = await asyncio.gather(*tasks)
                await self._parse_sample_pack_url(pages)

                if i + 1 == len(url_chunks):
                    break

                log.debug(f'waiting for {self._wait} seconds')
                await asyncio.sleep(self._wait)

    async def _parse_sample_pack_url(self, pages: list):
        # parse sample pack url
        log.info('parsing sample pack urls')

        for page in pages:

            if page is not None and page.status == 200:

                soup = BeautifulSoup(await page.text(), 'html.parser')
                text_copy_class = soup.find(attrs={'class': 'text-copy bodyCopy auto'})

                if text_copy_class is not None:
                    p_tags = text_copy_class.find_all('p')

                    for p in p_tags:
                        p_a_tag = p.a
                        if p_a_tag is not None:

                            if p_a_tag['href'].endswith('.zip'):
                                sample_pack_url = p_a_tag['href']
                                sample_pack_title = p_a_tag.text

                                debug = f'sample pack url: {sample_pack_url}, title: {sample_pack_title}'
                                log.debug(debug)

                                sample = SamplePack(sample_pack_url, sample_pack_title)
                                self._sample_packs.append(sample)
            else:
                self._page_errors += 1
