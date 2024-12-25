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

from pathlib import Path


class FileHandler:
    """
    FileHandler class for various operation at the given path.
    """
    def __init__(self, path: str):
        """
        Initialize the FileHandler class.

        :param path: The work path.
        """
        self._path = Path(path)
        self._old_samples = []
        self._dir_created = False

    @property
    def path(self):
        """
        Returns the absolute path
        """
        return self._path.resolve()

    @property
    def was_dir_created(self) -> bool:
        """
        Check if a directory was created at the work path.

        :return: True if a directory was created, else False.
        """
        return self._dir_created

    def is_valid_path(self) -> bool:
        """
        Check if the path is valid.

        :return: True if valid, else False.
        """
        if self._path.exists():
            return True
        return False

    def is_dir(self) -> bool:
        """
        Check directory.

        :return: True if valid directory, else False.
        """
        if self._path.is_dir():
            return True
        return False

    def create_dir(self):
        """
        Create a directory.
        """
        self._path.mkdir()
        self._dir_created = True

    def iter_root_dir(self) -> list:
        """
        Iter the work path directory.
        """
        if self._path.is_dir():
            for d in self._path.iterdir():
                if d.is_file() and d.name.endswith('.zip'):
                    # *.zip files in this folder is sample packs
                    self._old_samples.append(d.name)
                if d.is_dir():
                    self._old_samples.append(d.name)

        return self._old_samples

    def compare(self, new_samples: list, old_samples: list) -> tuple:
        """
        Compare two lists.

        :param new_samples: list of SamplePack objects.
        :param old_samples: list of sample pack names.
        :return: tuple of list(a) not in old samples and list(b) in old samples.
        """
        to_download = []
        ignored = []

        if len(old_samples) == 0:
            to_download = new_samples
            return to_download, ignored

        for sample in new_samples:
            name = sample.file_name.replace('.zip', '')

            if name not in self._remove_extension(old_samples):  # check old samples for .zip
                to_download.append(sample)
            else:
                ignored.append(sample)

        return to_download, ignored

    @staticmethod
    def _remove_extension(sample_list: list) -> list:
        _ = []
        for s in sample_list:
            if s.endswith('.zip'):
                s = s.replace('.zip', '')
            _.append(s)

        return _
