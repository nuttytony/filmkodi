'''
    urlresolver XBMC Addon
    Copyright (C) 2016 Gujal

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import re
from lib import jsunpack
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError


class FastplayResolver(UrlResolver):
    name = 'fastplay.sx'
    domains = ['fastplay.sx', 'fastplay.cc']
    pattern = '(?://|\.)(fastplay\.(?:sx|cc))/(?:flash-|embed-)?([0-9a-zA-Z]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        html = self.net.http_GET(web_url).content

        if '404 Not Found' in html:
            raise ResolverError('File Removed')

        if 'Video is processing' in html:
            raise ResolverError('File still being processed')

        packed = re.search('(eval\(function.*?)\s*</script>', html, re.DOTALL)
        if packed:
            js = jsunpack.unpack(packed.group(1))
        else:
            js = html

        link = re.search('sources[\d\D]+(http.*?)",label', js)
        if link:
            common.log_utils.log_debug('fastplay.sx Link Found: %s' % link.group(1))
            return link.group(1)

        raise ResolverError('Unable to find fastplay.sx video')

    def get_url(self, host, media_id):
        return 'http://%s/embed-%s.html' % (host, media_id)
