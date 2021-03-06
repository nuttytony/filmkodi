# -*- coding: utf-8 -*-

'''
    FanFilm Add-on
    Copyright (C) 2016 mrknow

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,urllib,urlparse

from resources.lib.libraries import client
from resources.lib.libraries import control
from resources.lib.resolvers import realdebrid
from resources.lib.resolvers import premiumize

import urlresolver


def request(url):
    try:
        url =url.replace(" ", "")
        control.log("#RESOLVER#  my url 1 ************ %s " % url)

        if '</regex>' in url:
            import regex ; url = regex.resolve(url)

        rd = realdebrid.resolve(url)
        control.log("#RESOLVER#  my rd 2 ************ %s url: %s" % (rd,url))

        if not rd == None: return rd

        pz = premiumize.resolve(url)
        if not pz == None: return pz

        if url.startswith('rtmp'):
            if len(re.compile('\s*timeout=(\d*)').findall(url)) == 0: url += ' timeout=10'
            return url


        try:
            z=False
            hmf = urlresolver.HostedMediaFile(url,include_disabled=True, include_universal=False)
            if hmf:
                print 'yay! we can resolve this one'
                z = hmf.resolve()
            else:
                print 'sorry :( no resolvers available to handle this one.'

            control.log("!!!!!!!!! OK #urlresolver#  URL %s " % z)

            if z !=False : return z
        except Exception as e:
            control.log("!!!!!!!!! ERRR #urlresolver#  URL %s " % url)
            pass

        #u = client.shrink_host(url)
        u = urlparse.urlparse(url).netloc
        u = u.replace('www.', '').replace('embed.', '')
        u = u.lower()

        control.log("#RESOLVER#  URL TO MATCH url 3 ************ %s " % u)

        r = [i['class'] for i in info() if u in i['netloc']][0]
        r = __import__(r, globals(), locals(), [], -1)
        control.log("#RESOLVER#  my url 4 ************ %s " % r)

        r = r.resolve(url)
        #control.log("#RESOLVER#  my url 5 %s ************ %s " % (r,url))

        if r == None: return r

        elif type(r) == list: return r
        #elif not r.startswith('http'): return r

        try: h = dict(urlparse.parse_qsl(r.rsplit('|', 1)[1]))
        except: h = dict('')

        if not 'User-Agent' in h: h['User-Agent'] = client.agent()
        if not 'Referer' in h: h['Referer'] = url

        r = '%s|%s' % (r.split('|')[0], urllib.urlencode(h))
        control.log("#RESOLVER#  my url 6 %s ************ %s " % (r,url))

        return r
    except:
        return url


def info():
    return [{
        'class': '',
        'netloc': ['oboom.com', 'rapidgator.net', 'uploaded.net'],
        'host': ['Oboom', 'Rapidgator', 'Uploaded'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': True
    }, {
        'class': '_180upload',
        'netloc': ['180upload.com'],
        'host': ['180upload'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'allmyvideos',
        'netloc': ['allmyvideos.net'],
        'host': ['Allmyvideos'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'allvid',
        'netloc': ['allvid.ch'],
        'host': ['Allvid'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'bestreams',
        'netloc': ['bestreams.net'],
        'host': ['Bestreams'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'clicknupload',
        'netloc': ['clicknupload.com', 'clicknupload.link'],
        'host': ['Clicknupload'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'cloudtime',
        'netloc': ['cloudtime.to'],
        'host': ['Cloudtime'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'cloudyvideos',
        'netloc': ['cloudyvideos.com'],
        #'host': ['Cloudyvideos'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'cloudzilla',
        'netloc': ['cloudzilla.to'],
        'host': ['Cloudzilla'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'daclips',
        'netloc': ['daclips.in'],
        'host': ['Daclips'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'yadisk',
        'netloc': ['yadi.sk']
    }, {
        'class': 'dailymotion',
        'netloc': ['dailymotion.com']
    }, {
        'class': 'datemule',
        'netloc': ['datemule.com']
    }, {
        'class': 'divxpress',
        'netloc': ['divxpress.com'],
        'host': ['Divxpress'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'exashare',
        'netloc': ['exashare.com'],
        'host': ['Exashare'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'fastvideo',
        'netloc': ['fastvideo.in', 'faststream.in', 'rapidvideo.ws'],
        'host': ['Fastvideo', 'Faststream'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'filehoot',
        'netloc': ['filehoot.com'],
        'host': ['Filehoot'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'filenuke',
        'netloc': ['filenuke.com', 'sharesix.com'],
        'host': ['Filenuke', 'Sharesix'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'filmon',
        'netloc': ['filmon.com']
    }, {
        'class': 'filepup',
        'netloc': ['filepup.net']
    }, {
        'class': 'googledocs',
        'netloc': ['google.com']
    }, {
        'class': 'googledocs',
        'netloc': ['docs.google.com', 'drive.google.com']
    }, {
        'class': 'googlephotos',
        'netloc': ['photos.google.com']
    }, {
        'class': 'googlepicasa',
        'netloc': ['picasaweb.google.com']
    }, {
        'class': 'googleplus',
        'netloc': ['plus.google.com']
    }, {
        'class': 'gorillavid',
        'netloc': ['gorillavid.com', 'gorillavid.in'],
        'host': ['Gorillavid'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'grifthost',
        'netloc': ['grifthost.com'],
        #'host': ['Grifthost'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'hdcast',
        'netloc': ['hdcast.me']
    }, {
        'class': 'hugefiles',
        'netloc': ['hugefiles.net'],
        'host': ['Hugefiles'],
        'quality': 'Medium',
        'captcha': True,
        'a/c': False
    }, {
        'class': 'ipithos',
        'netloc': ['ipithos.to'],
        'host': ['Ipithos'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'ishared',
        'netloc': ['ishared.eu'],
        'host': ['iShared'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'kingfiles',
        'netloc': ['kingfiles.net'],
        'host': ['Kingfiles'],
        'quality': 'Medium',
        'captcha': True,
        'a/c': False
    }, {
        'class': 'letwatch',
        'netloc': ['letwatch.us'],
        'host': ['Letwatch'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'mailru',
        'netloc': ['mail.ru', 'my.mail.ru', 'videoapi.my.mail.ru', 'api.video.mail.ru']
    }, {
        'class': 'cloudmailru',
        'netloc': ['cloud.mail.ru']
    }, {
        'class': 'mightyupload',
        'netloc': ['mightyupload.com'],
        'host': ['Mightyupload'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'movdivx',
        'netloc': ['movdivx.com'],
        'host': ['Movdivx'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'movpod',
        'netloc': ['movpod.net', 'movpod.in'],
        'host': ['Movpod'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'movshare',
        'netloc': ['movshare.net'],
        'host': ['Movshare'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'mrfile',
        'netloc': ['mrfile.me'],
        'host': ['Mrfile'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'mybeststream',
        'netloc': ['mybeststream.xyz']
    }, {
        'class': 'nosvideo',
        'netloc': ['nosvideo.com'],
        #'host': ['Nosvideo'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'novamov',
        'netloc': ['novamov.com'],
        'host': ['Novamov'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'nowvideo',
        'netloc': ['nowvideo.eu', 'nowvideo.sx'],
        'host': ['Nowvideo'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'openload',
        'netloc': ['openload.io', 'openload.co'],
        'host': ['Openload'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'cda',
        'netloc': ['cda.pl', 'cda'],
        'host': ['CDA'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'p2pcast',
        'netloc': ['p2pcast.tv']
    }, {
        'class': 'primeshare',
        'netloc': ['primeshare.tv'],
        'host': ['Primeshare'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'promptfile',
        'netloc': ['promptfile.com'],
        'host': ['Promptfile'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'putstream',
        'netloc': ['putstream.com'],
        'host': ['Putstream'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'realvid',
        'netloc': ['realvid.net'],
        'host': ['Realvid'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'sawlive',
        'netloc': ['sawlive.tv']
    }, {
        'class': 'sharerepo',
        'netloc': ['sharerepo.com'],
        'host': ['Sharerepo'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'skyvids',
        'netloc': ['skyvids.net'],
        'host': ['Skyvids'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'speedvideo',
        'netloc': ['speedvideo.net']
    }, {
        'class': 'stagevu',
        'netloc': ['stagevu.com'],
        'host': ['StageVu'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'streamcloud',
        'netloc': ['streamcloud.eu'],
        'host': ['Streamcloud'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'streamin',
        'netloc': ['streamin.to'],
        'host': ['Streamin'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'thefile',
        'netloc': ['thefile.me'],
        'host': ['Thefile'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'thevideo',
        'netloc': ['thevideo.me'],
        'host': ['Thevideo'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'turbovideos',
        'netloc': ['turbovideos.net'],
        'host': ['Turbovideos'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'tusfiles',
        'netloc': ['tusfiles.net'],
        'host': ['Tusfiles'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'up2stream',
        'netloc': ['up2stream.com'],
        'host': ['Up2stream'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'uploadc',
        'netloc': ['uploadc.com', 'uploadc.ch', 'zalaa.com'],
        'host': ['Uploadc', 'Zalaa'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'uploadrocket',
        'netloc': ['uploadrocket.net'],
        'host': ['Uploadrocket'],
        'quality': 'Medium',
        'captcha': True,
        'a/c': False
    }, {
        'class': 'uptobox',
        'netloc': ['uptobox.com'],
        'host': ['Uptobox'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'v_vids',
        'netloc': ['v-vids.com'],
        'host': ['V-vids'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'vaughnlive',
        'netloc': ['vaughnlive.tv', 'breakers.tv', 'instagib.tv', 'vapers.tv']
    }, {
        'class': 'veehd',
        'netloc': ['veehd.com']
    }, {
        'class': 'veetle',
        'netloc': ['veetle.com']
    }, {
        'class': 'vidbull',
        'netloc': ['vidbull.com'],
        'host': ['Vidbull'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'videomega',
        'netloc': ['videomega.tv'],
        #'host': ['Videomega'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'videopremium',
        'netloc': ['videopremium.tv', 'videopremium.me']
    }, {
        'class': 'videoweed',
        'netloc': ['videoweed.es'],
        'host': ['Videoweed'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'vidlockers',
        'netloc': ['vidlockers.ag'],
        'host': ['Vidlockers'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'vidspot',
        'netloc': ['vidspot.net'],
        'host': ['Vidspot'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'vidto',
        'netloc': ['vidto.me'],
        'host': ['Vidto'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'vidzi',
        'netloc': ['vidzi.tv'],
        'host': ['Vidzi'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'vimeo',
        'netloc': ['vimeo.com']
    }, {
        'class': 'vk',
        'netloc': ['vk.com']
    }, {
        'class': 'vodlocker',
        'netloc': ['vodlocker.com'],
        'host': ['Vodlocker'],
        'quality': 'Low',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'xfileload',
        'netloc': ['xfileload.com'],
        'host': ['Xfileload'],
        'quality': 'Medium',
        'captcha': True,
        'a/c': False
    }, {
        'class': 'xvidstage',
        'netloc': ['xvidstage.com'],
        'host': ['Xvidstage'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'youtube',
        'netloc': ['youtube.com'],
        'host': ['Youtube'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'zettahost',
        'netloc': ['zettahost.tv'],
        'host': ['Zettahost'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'zstream',
        'netloc': ['zstream.to'],
        'host': ['zStream'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }, {
        'class': 'watch1080p',
        'netloc': ['watch1080p.com'],
        'host': ['watch1080p'],
        'quality': 'Medium',
        'captcha': False,
        'a/c': False
    }]


