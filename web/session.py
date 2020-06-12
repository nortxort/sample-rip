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

import aiohttp
from aiohttp_proxy import ProxyConnector

log = logging.getLogger(__name__)


class Session(object):
    """
    Session class maintaining cookies across requests.
    """
    session = None
    connector = None

    @classmethod
    def create(cls, proxy: str = None):
        """
        Create a new aiohttp.ClientSession object

        TODO: Test if using detach, will release the proxy in use?

        :param proxy: If set, all session requests will use this proxy.
        :return: A aiohttp.ClientSession object.
        """

        if proxy is not None:
            cls.connector = ProxyConnector.from_url(proxy)

        cls.session = aiohttp.ClientSession(connector=cls.connector)
        log.debug(f'creating session: {cls.session}, connector: {cls.connector}, proxy: {proxy}')

        return cls.session

    @classmethod
    async def close(cls):
        """
        Close the session object.
        """
        if cls.session is not None:
            log.debug(f'closing session.')

        await cls.session.close()

    @classmethod
    def detach(cls):
        # https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession.detach
        if cls.session is not None:
            cls.session.detach()

    @classmethod
    def delete(cls):
        """
        Delete the session object.
        """
        cls.session = None
        log.debug('deleting WebSession.session.')

    @classmethod
    def cookie_jar(cls):
        """
        All the raw cookies for the session.

        :return: A aiohttp.cookiejar.CookieJar class, or None.
        :rtype: CookieJar | None
        """
        if cls.session is not None:
            return cls.session.cookie_jar

        return None

    @classmethod
    def cookies(cls, domain: str = None, name: str = None):
        """
        Checks if a cookie exists within the session cookies.

        If no cookie name is given(None), all cookies for the
        given domain will be returned(if any exists).

        :param domain: The domain for which the cookie(s) belongs.
        :param name: The name of the cookie.
        :return: bool(False) if no cookie(s) was found, else a Morsel object.
        """
        if cls.session is not None and domain is not None:

            domain_cookies = cls.cookie_jar().filter_cookies(domain)

            if name is None:
                if len(domain_cookies) == 0:
                    return False

                return domain_cookies

            cookie = domain_cookies.get(name)
            if cookie is not None:
                return cookie.value

        return False
