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


class SamplePack:
    """
    Class representing a sample pack.
    """
    def __init__(self, url: str, title: str):
        self._url = url
        self._title = title

    @property
    def url(self) -> str:
        """
        The url of the sample pack.
        """
        return self._url

    @property
    def title(self) -> str:
        """
        The title of the sample pack.
        """
        return self._title

    @property
    def file_name(self) -> str:
        """
        The name of the sample pack(zip file name)
        """
        return self._url.split('/')[-1]

    @property
    def size(self) -> str:
        """
        The size of the sample pack in MB.

        Some packs does not have a MB size that can
        be parsed, in that case N/A will be returned.
        """
        if '\'' in self._title:
            self._title = self._title.replace('\'', '')

        if 'MB)' in self._title:
            return self._title.split('(')[1].split(')')[0]

        return 'N/A'
