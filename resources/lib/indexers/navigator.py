# -*- coding: utf-8 -*-

'''
    JobbMintATv Addon
    Copyright (C) 2023 heg, vargalex

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

import os, sys, re, xbmc, xbmcgui, xbmcplugin, xbmcaddon, locale, base64
from bs4 import BeautifulSoup
import requests
import urllib.parse
import resolveurl as urlresolver
from resources.lib.modules.utils import py2_decode, py2_encode
from resources.lib.modules import xmltodict
import html

from urllib.parse import urljoin, urlparse, parse_qs
import struct
import random
import string

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
addonFanart = xbmcaddon.Addon().getAddonInfo('fanart')

version = xbmcaddon.Addon().getAddonInfo('version')
kodi_version = xbmc.getInfoLabel('System.BuildVersion')
base_log_info = f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}'

xbmc.log(f'{base_log_info}', xbmc.LOGINFO)

base_url = 'https://jobbmintatv.pro'

headers = {
    'authority': 'jobbmintatv.pro',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}

if sys.version_info[0] == 3:
    from xbmcvfs import translatePath
    from urllib.parse import urlparse, quote_plus
else:
    from xbmc import translatePath
    from urlparse import urlparse
    from urllib import quote_plus

class navigator:
    def __init__(self):
        try:
            locale.setlocale(locale.LC_ALL, "hu_HU.UTF-8")
        except:
            try:
                locale.setlocale(locale.LC_ALL, "")
            except:
                pass
        self.base_path = py2_decode(translatePath(xbmcaddon.Addon().getAddonInfo('profile')))

    def root(self):
        self.addDirectoryItem("Filmek", "only_movies", '', 'DefaultFolder.png')
        self.addDirectoryItem("Sorozatok", "only_series", '', 'DefaultFolder.png')
        self.addDirectoryItem("Film Kategóriák", "movie_categories", '', 'DefaultFolder.png')
        self.addDirectoryItem("Sorozat Kategóriák", "series_categories", '', 'DefaultFolder.png')
        self.addDirectoryItem("Keresés", "newsearch", '', 'DefaultFolder.png')
        self.endDirectory()

    def getMovieCategories(self):
        jsonData = {
          "categorys": [
            {
              "genre": "vígjáték",
              "url": "https://jobbmintatv.pro/filmek/1/1/vigjatek"
            },
            {
              "genre": "anime",
              "url": "https://jobbmintatv.pro/filmek/1/1/anime"
            },
            {
              "genre": "akció",
              "url": "https://jobbmintatv.pro/filmek/1/1/akcio"
            },
            {
              "genre": "romantikus",
              "url": "https://jobbmintatv.pro/filmek/1/1/romantikus"
            },
            {
              "genre": "kaland",
              "url": "https://jobbmintatv.pro/filmek/1/1/kaland"
            },
            {
              "genre": "animáció",
              "url": "https://jobbmintatv.pro/filmek/1/1/animacio"
            },
            {
              "genre": "thriller",
              "url": "https://jobbmintatv.pro/filmek/1/1/thriller"
            },
            {
              "genre": "családi",
              "url": "https://jobbmintatv.pro/filmek/1/1/csaladi"
            },
            {
              "genre": "bűnügyi",
              "url": "https://jobbmintatv.pro/filmek/1/1/bunugyi"
            },
            {
              "genre": "rövidfilm",
              "url": "https://jobbmintatv.pro/filmek/1/1/rovidfilm"
            },
            {
              "genre": "musical",
              "url": "https://jobbmintatv.pro/filmek/1/1/musical"
            },
            {
              "genre": "sci-fi",
              "url": "https://jobbmintatv.pro/filmek/1/1/sci-fi"
            },
            {
              "genre": "valóságshow",
              "url": "https://jobbmintatv.pro/filmek/1/1/valosagshow"
            },
            {
              "genre": "fantasy",
              "url": "https://jobbmintatv.pro/filmek/1/1/fantasy"
            },
            {
              "genre": "misztikus",
              "url": "https://jobbmintatv.pro/filmek/1/1/misztikus"
            },
            {
              "genre": "háborús",
              "url": "https://jobbmintatv.pro/filmek/1/1/haborus"
            },
            {
              "genre": "western",
              "url": "https://jobbmintatv.pro/filmek/1/1/western"
            },
            {
              "genre": "horror",
              "url": "https://jobbmintatv.pro/filmek/1/1/horror"
            },
            {
              "genre": "történelmi",
              "url": "https://jobbmintatv.pro/filmek/1/1/tortenelni"
            },
            {
              "genre": "sport",
              "url": "https://jobbmintatv.pro/filmek/1/1/sport"
            },
            {
              "genre": "zene",
              "url": "https://jobbmintatv.pro/filmek/1/1/zene"
            },
            {
              "genre": "dráma",
              "url": "https://jobbmintatv.pro/filmek/1/1/drama"
            },
            {
              "genre": "életrajz",
              "url": "https://jobbmintatv.pro/filmek/1/1/eletrajzi"
            },
            {
              "genre": "dokumentum",
              "url": "https://jobbmintatv.pro/filmek/1/1/dokumentum"
            },
            {
              "genre": "karácsonyi",
              "url": "https://jobbmintatv.pro/filmek/1/1/karacsonyi"
            },
            {
              "genre": "török",
              "url": "https://jobbmintatv.pro/filmek/1/1/torok"
            },
            {
              "genre": "feliratos",
              "url": "https://jobbmintatv.pro/filmek/1/1/feliratos"
            }
		  ]
        }
        
        for movie in jsonData['categorys']:
            category_name = movie['genre']
            category_url = movie['url']

            self.addDirectoryItem(f"{category_name}", f'movie_items&url={category_url}', '', 'DefaultFolder.png')
        
        self.endDirectory('movies')

    def getSeriesCategories(self):
        jsonData = {
          "categorys": [
            {
              "genre": "vígjáték",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/vigjatek"
            },
            {
              "genre": "anime",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/anime"
            },
            {
              "genre": "akció",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/akcio"
            },
            {
              "genre": "romantikus",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/romantikus"
            },
            {
              "genre": "kaland",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/kaland"
            },
            {
              "genre": "animáció",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/animacio"
            },
            {
              "genre": "thriller",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/thriller"
            },
            {
              "genre": "családi",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/csaladi"
            },
            {
              "genre": "bűnügyi",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/bunugyi"
            },
            {
              "genre": "rövidfilm",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/rovidfilm"
            },
            {
              "genre": "musical",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/musical"
            },
            {
              "genre": "sci-fi",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/sci-fi"
            },
            {
              "genre": "valóságshow",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/valosagshow"
            },
            {
              "genre": "fantasy",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/fantasy"
            },
            {
              "genre": "misztikus",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/misztikus"
            },
            {
              "genre": "háborús",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/haborus"
            },
            {
              "genre": "western",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/western"
            },
            {
              "genre": "horror",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/horror"
            },
            {
              "genre": "történelmi",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/tortenelni"
            },
            {
              "genre": "sport",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/sport"
            },
            {
              "genre": "zene",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/zene"
            },
            {
              "genre": "dráma",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/drama"
            },
            {
              "genre": "életrajz",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/eletrajzi"
            },
            {
              "genre": "dokumentum",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/dokumentum"
            },
            {
              "genre": "karácsonyi",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/karacsonyi"
            },
            {
              "genre": "török",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/torok"
            },
            {
              "genre": "feliratos",
              "url": "https://jobbmintatv.pro/sorozatok/1/1/feliratos"
            }
		  ]
        }
        
        for movie in jsonData['categorys']:
            category_name = movie['genre']
            category_url = movie['url']

            self.addDirectoryItem(f"{category_name}", f'series_items&url={category_url}', '', 'DefaultFolder.png')
        
        self.endDirectory('series')

    def getOnlyMovies(self):
        page = requests.get(f"{base_url}/filmek/1/1//", headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        anchors = soup.find_all('a', class_='kocka')
        
        for anchor in anchors:
            card_link = anchor['href']
            if not re.match(r'https?://', card_link):
                card_link = 'https:' + card_link
        
            img_src = anchor.find('img')['src']
            if not re.match(r'https?://', img_src):
                img_url = 'https:' + img_src
        
            hun_title = anchor.find('span', class_='cimk').text
        
            details = anchor.find_next_sibling('span', class_='egyebekk').text
        
            imdb_match = re.search(r'\[imdb:(\d+(\.\d+)?)\]', details)
            imdb = imdb_match.group(1) if imdb_match else None
        
            year_match = re.search(r'\d{4}', details)
            year = year_match.group() if year_match else None
        
            hun_m = f'{hun_title} - {year}'
            
            self.addDirectoryItem(f'[B]{hun_title} - {year} | [COLOR yellow]{imdb}[/COLOR][/B]', f'extract_movie&url={card_link}&img_url={img_url}&hun_title={hun_title}&year={year}', img_url, 'DefaultMovies.png', isFolder=True, meta={'title': hun_m})

        try:
            next_page_anchor = soup.find('a', string='következő oldal')
            if next_page_anchor:
                next_page = next_page_anchor['href']
                
                next_page_url = 'https:' + next_page
            
            self.addDirectoryItem('[I]Következő oldal[/I]', f'movie_items&url={quote_plus(next_page_url)}', '', 'DefaultFolder.png')
        except AttributeError:
            xbmc.log(f'{base_log_info}| getOnlyMovies | next_page_url | csak egy oldal található', xbmc.LOGINFO)
        
        self.endDirectory('movies')

    def getOnlySeries(self):
        page = requests.get(f"{base_url}/sorozatok/1/1//", headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        anchors = soup.find_all('a', class_='kocka')
        
        for anchor in anchors:
            card_link = anchor['href']
            if not re.match(r'https?://', card_link):
                card_link = 'https:' + card_link
        
            img_src = anchor.find('img')['src']
            if not re.match(r'https?://', img_src):
                img_url = 'https:' + img_src
        
            hun_title = anchor.find('span', class_='cimk').text
        
            details = anchor.find_next_sibling('span', class_='egyebekk').text
        
            imdb_match = re.search(r'\[imdb:(\d+(\.\d+)?)\]', details)
            imdb = imdb_match.group(1) if imdb_match else None
        
            year_match = re.search(r'\d{4}', details)
            year = year_match.group() if year_match else None
        
            hun_m = f'{hun_title} - {year}'
            
            self.addDirectoryItem(f'[B]{hun_title} - {year} | [COLOR yellow]{imdb}[/COLOR][/B]', f'extract_series&url={quote_plus(card_link)}&img_url={img_url}&hun_title={hun_title}&year={year}', img_url, 'DefaultMovies.png', isFolder=True, meta={'title': hun_m})
            
        try:
            next_page_anchor = soup.find('a', string='következő oldal')
            if next_page_anchor:
                next_page = next_page_anchor['href']
                
                next_page_url = 'https:' + next_page
            
            self.addDirectoryItem('[I]Következő oldal[/I]', f'series_items&url={quote_plus(next_page_url)}', '', 'DefaultFolder.png')
        except AttributeError:
            xbmc.log(f'{base_log_info}| getOnlySeries | next_page_url | csak egy oldal található', xbmc.LOGINFO)
        
        self.endDirectory('movies')      

    def getMovieItems(self, url, img_url, hun_title, content, year):
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        anchors = soup.find_all('a', class_='kocka')
        
        for anchor in anchors:
            card_link = anchor['href']
            if not re.match(r'https?://', card_link):
                card_link = 'https:' + card_link
        
            img_src = anchor.find('img')['src']
            if not re.match(r'https?://', img_src):
                img_url = 'https:' + img_src
        
            hun_title = anchor.find('span', class_='cimk').text
        
            details = anchor.find_next_sibling('span', class_='egyebekk').text
        
            imdb_match = re.search(r'\[imdb:(\d+(\.\d+)?)\]', details)
            imdb = imdb_match.group(1) if imdb_match else None
        
            year_match = re.search(r'\d{4}', details)
            year = year_match.group() if year_match else None
        
            hun_m = f'{hun_title} - {year}'
            
            self.addDirectoryItem(f'[B]{hun_title} - {year} | [COLOR yellow]{imdb}[/COLOR][/B]', f'extract_movie&url={card_link}&img_url={img_url}&hun_title={hun_title}&year={year}', img_url, 'DefaultMovies.png', isFolder=True, meta={'title': hun_m})
            
        try:
            next_page_anchor = soup.find('a', string='következő oldal')
            if next_page_anchor:
                next_page = next_page_anchor['href']
                
                next_page_url = 'https:' + next_page
            
            self.addDirectoryItem('[I]Következő oldal[/I]', f'movie_items&url={quote_plus(next_page_url)}', '', 'DefaultFolder.png')
        except (AttributeError, UnboundLocalError):
            xbmc.log(f'{base_log_info}| getMovieItems | next_page_url | csak egy oldal található', xbmc.LOGINFO)
        
        self.endDirectory('movies')

    def getSeriesItems(self, url, img_url, hun_title, year):
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        anchors = soup.find_all('a', class_='kocka')
        
        for anchor in anchors:
            card_link = anchor['href']
            if not re.match(r'https?://', card_link):
                card_link = 'https:' + card_link
        
            img_src = anchor.find('img')['src']
            if not re.match(r'https?://', img_src):
                img_url = 'https:' + img_src
        
            hun_title = anchor.find('span', class_='cimk').text
        
            details = anchor.find_next_sibling('span', class_='egyebekk').text
        
            imdb_match = re.search(r'\[imdb:(\d+(\.\d+)?)\]', details)
            imdb = imdb_match.group(1) if imdb_match else None
        
            year_match = re.search(r'\d{4}', details)
            year = year_match.group() if year_match else None
        
            hun_m = f'{hun_title} - {year}'
            
            self.addDirectoryItem(f'[B]{hun_title} - {year} | [COLOR yellow]{imdb}[/COLOR][/B]', f'extract_series&url={quote_plus(card_link)}&img_url={img_url}&hun_title={hun_title}&year={year}', img_url, 'DefaultMovies.png', isFolder=True, meta={'title': hun_m})
        
        try:
            next_page_anchor = soup.find('a', string='következő oldal')
            if next_page_anchor:
                next_page = next_page_anchor['href']
                next_page_url = 'https:' + next_page
            
            self.addDirectoryItem('[I]Következő oldal[/I]', f'series_items&url={quote_plus(next_page_url)}', '', 'DefaultFolder.png')
        except (AttributeError, UnboundLocalError):
            xbmc.log(f'{base_log_info}| getSeriesItems | next_page_url | csak egy oldal található', xbmc.LOGINFO)
        
        self.endDirectory('series')

    def extractMovie(self, url, img_url, hun_title, content, year):
        
        try:
            html_soup_2 = requests.get(url, headers=headers)
            
            soup_2 = BeautifulSoup(html_soup_2.text, 'html.parser')
            
            hun_title = soup_2.select_one('#sorozat_adatlap_film h1').text
            
            en_title_element = soup_2.select_one('#sorozat_adatlap_film h1:nth-of-type(2)')
            en_title = en_title_element.text if en_title_element else None
            imdb = soup_2.select_one('#adatlap_menu div:-soup-contains("IMDb") a').text
            content = soup_2.select_one('#sorozat_adatlap_film p').text
            img_url = soup_2.select_one('#sorozat_borito_film img')['src']
            video_src = soup_2.select_one('#video iframe')['src']
            
            if not re.match(r'https?://', img_url):
                img_url = 'https:' + img_url
            
            if not re.match(r'https?://', video_src):
                video_src = 'https:' + video_src
            
            hun_m = f'{hun_title} - {year}'
            
            self.addDirectoryItem(f'[B]{hun_title} - {year} | [COLOR yellow]{imdb}[/COLOR][/B]', f'playmovie&url={quote_plus(video_src)}&img_url={img_url}&hun_title={hun_title}&content={content}&year={year}', img_url, 'DefaultMovies.png', isFolder=False, meta={'title': hun_m, 'plot': content})
            
            self.endDirectory('movies')
        except:
            self.extractSeries(url, None, None, None, None, None)            

    def extractSeries(self, url, img_url, hun_title, content, ep_title, year):
        html_soup_2 = requests.get(url, headers=headers)
        
        soup_2 = BeautifulSoup(html_soup_2.text, 'html.parser')

        season_links = []
        evadoks = soup_2.find_all('a', class_='evadoks')
        htt = 'https://jobbmintatv.pro'
        for evadok in evadoks:
            season_number = evadok.text.strip()
            season_link = urllib.parse.urljoin(htt, evadok['href'])
            season_links.append({"evad": season_link})

        sid = re.findall(r'sid=\"(.*?)\"', str(soup_2))[0].strip()
        
        evad_nums = [int(evadok.text.strip()) for evadok in soup_2.find_all('a', class_='evadoks')]

        hun_title_element = soup_2.find('h1')
        en_title_element = soup_2.find('h1', style="color:#777;font-size:16px;margin:0 0 5 2;")
        sorozat_borito_element = soup_2.find('div', id='sorozat_borito')
        tartalom_element = soup_2.find('p')

        hun_title = hun_title_element.text.strip() if hun_title_element else ''
        en_title = en_title_element.text.strip() if en_title_element else ''
        evjarat_match = re.findall(r'Évjárat:.*?>(.*?)<', str(soup_2))
        year = evjarat_match[0] if evjarat_match else ''
        imdb_rating_match = re.findall(r'IMDb:.*?>.*?(\d.*?)</a>', str(soup_2))
        imdb_rating = imdb_rating_match[0] if imdb_rating_match else ''
        img_url = urllib.parse.urljoin(htt, sorozat_borito_element.img['src']) if sorozat_borito_element and sorozat_borito_element.img else ''
        content = tartalom_element.text.strip() if tartalom_element else ''

        for evad_stuffs in evad_nums:
            extr_evad_nums = evad_stuffs             

            params = {
                'sid': sid,
                'evad': int(extr_evad_nums),
                'evadnez': '1',
            }
            
            html_source = requests.get('https://jobbmintatv.pro/ajax.php', params=params, headers=headers)
            
            soup_xx = BeautifulSoup(html_source.text, 'html.parser')
            
            resz_elements = soup_xx.find_all('a', class_='reszek')
            
            for resz in resz_elements:
                resz_number = int(resz.text)
                resz_link = 'https:' + resz['href']
                ep_title = f'S{extr_evad_nums:02d}E{resz_number:02d}'
                
                hun_ep = f'{ep_title} - {hun_title} - {year}'
            
                self.addDirectoryItem(f'[B]{ep_title} - {hun_title} - {year}[/B]', f'extract_episodes&url={resz_link}&img_url={img_url}&hun_title={hun_title}&content={content}&ep_title={ep_title}&year={year}', img_url, 'DefaultMovies.png', isFolder=True, meta={'title': hun_ep, 'plot': content})
        
        self.endDirectory('series')

    def extractEpisodes(self, url, img_url, hun_title, content, ep_title, year):
    
        html_soup_2 = requests.get(url, headers=headers)
        soup_2 = BeautifulSoup(html_soup_2.text, 'html.parser')

        iframe = soup_2.find('iframe')

        if iframe:
            iframe_src = iframe.get('src')
            xbmc.log(f'{base_log_info}| extractEpisodes | iframe_src | {iframe_src}', xbmc.LOGINFO)
            
            hun_ep = f'{ep_title} - {hun_title} - {year}'
            
            self.addDirectoryItem(f'[B]{ep_title} - {hun_title} - {year}[/B]', f'playmovie&url={quote_plus(iframe_src)}&img_url={img_url}&hun_title={hun_title}&content={content}&year={year}', img_url, 'DefaultMovies.png', isFolder=False, meta={'title': hun_ep, 'plot': content})
        
        self.endDirectory('series')

    def playMovie(self, url):
        if re.search('.*videa.*', url):
            
            STATIC_SECRET = 'xHb0ZvME5q8CBcoQi6AngerDu3FGO9fkUlwPmLVY_RTzj2hJIS4NasXWKy1td7p'
            
            def rc4(cipher_text, key):
                def compat_ord(c):
                    return c if isinstance(c, int) else ord(c)
            
                res = b''
            
                key_len = len(key)
                S = list(range(256))
            
                j = 0
                for i in range(256):
                    j = (j + S[i] + ord(key[i % key_len])) % 256
                    S[i], S[j] = S[j], S[i]
            
                i = 0
                j = 0
                for m in range(len(cipher_text)):
                    i = (i + 1) % 256
                    j = (j + S[i]) % 256
                    S[i], S[j] = S[j], S[i]
                    k = S[(S[i] + S[j]) % 256]
                    res += struct.pack('B', k ^ compat_ord(cipher_text[m]))
            
                if sys.version_info[0] == 3:
                    return res.decode()
                else:
                    return res
            
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            }
            
            session = requests.Session()
            response = session.get(url, cookies={"session_adult": "1"})
            
            video_page = response.text
            
            if '/player' in url:
                player_url = url
                player_page = video_page
            else:
                player_url = re.search(r'<iframe.*?src="(/player\?[^"]+)"', video_page).group(1)
                player_url = urljoin(url, player_url)
                response = session.get(player_url)
                player_page = response.text
            
            nonce = re.search(r'_xt\s*=\s*"([^"]+)"', player_page).group(1)
            
            l = nonce[:32]
            s = nonce[32:]
            result = ''
            for i in range(0, 32):
                result += s[i - (STATIC_SECRET.index(l[i]) - 31)]
            
            query = parse_qs(urlparse(player_url).query)
            
            random_seed = ''
            for i in range(8):
                random_seed += random.choice(string.ascii_letters + string.digits)
            
            _s = random_seed
            _t = result[:16]
            if 'f' in query or 'v' in query:
                _param = f'f={query["f"][0]}' if 'f' in query else f'v={query["v"][0]}'
            response = session.get(f'https://videa.hu/player/xml?platform=desktop&{_param}&_s={_s}&_t={_t}')
            
            videaXml = response.text
            if not videaXml.startswith('<?xml'):
                key = result[16:] + random_seed + response.headers['x-videa-xs']
                videaXml = rc4(base64.b64decode(videaXml), key)            
            
            try:        
                videaData = xmltodict.parse(videaXml)

                sources = videaData["videa_video"]["video_sources"]["video_source"]
                if isinstance(sources, list):
                    sorted_sources = sorted(sources, key=lambda x: int(x["@width"]), reverse=True)
                else:
                    sorted_sources = [sources]

                selected_source = sorted_sources[0]
                s_format = selected_source["@name"]
                s_url = selected_source["#text"]
                s_exp = selected_source["@exp"]

                hash_key = "hash_value_" + s_format
                hash_x_key = videaData["videa_video"]["hash_values"][hash_key]
                video_url = f'https:{s_url}?md5={hash_x_key}&expires={s_exp}'
                
                xbmc.log(f'{base_log_info}| playMovie | video_url: {video_url}', xbmc.LOGINFO)

                play_item = xbmcgui.ListItem(path=video_url)

                try:
                    subtitles = videaData["videa_video"]["subtitles"]["subtitle"]
                    subtitle_urls = []
            
                    if isinstance(subtitles, list):
                        for subtitle in subtitles:
                            subtitle_url = 'https:' + subtitle["@src"]
                            subtitle_urls.append(subtitle_url)
                    else:
                        subtitle_url = 'https:' + subtitles["@src"]
                        subtitle_urls.append(subtitle_url)

                    play_item.setSubtitles(subtitle_urls)
                    xbmc.log(f'{base_log_info}| playMovie | subtitles: {subtitle_urls}', xbmc.LOGINFO)
                except KeyError:
                    xbmc.log(f'{base_log_info}| playMovie | No subtitles found', xbmc.LOGINFO)

                xbmcplugin.setResolvedUrl(syshandle, True, listitem=play_item)
                
            except Exception as e:
                xbmc.log(f'{base_log_info}| playMovie | Error: {str(e)}', xbmc.LOGINFO)
                notification = xbmcgui.Dialog()
                notification.notification("filmy.hu", "Törölt tartalom", time=5000)            
            ###
        
        else:
            try:
                direct_url = urlresolver.resolve(url)
                
                xbmc.log(f'{base_log_info}| playMovie (else) | direct_url: {direct_url}', xbmc.LOGINFO)
                play_item = xbmcgui.ListItem(path=direct_url)
                xbmcplugin.setResolvedUrl(syshandle, True, listitem=play_item)
            except:
                xbmc.log(f'{base_log_info}| playMovie | name: No video sources found', xbmc.LOGINFO)
                notification = xbmcgui.Dialog()
                notification.notification("JobbMintATv", "Törölt tartalom", time=5000)

    def doSearch(self, url):
        search_text = self.getSearchText()

        def custom_encode(text):
            replacements = {
                'á': '%E1',
                'é': '%E9',
                'í': '%ED',
                'ó': '%F3',
                'ö': '%F6',
                'ő': '%F5',
                'ú': '%FA',
                'ü': '%FC',
                'ű': '%FB',
                'ô': '%F4',
                'õ': '%F5',
                'û': '%FB',
                'ũ': '%F5'
            }
            encoded_text = ''
            for char in text:
                if char == ' ':
                    encoded_text += '%20'
                elif char in replacements:
                    encoded_text += replacements[char]
                else:
                    encoded_text += char
            return encoded_text

        encoded_search_text = custom_encode(search_text)
        url_k = f"{base_url}/ajax.php?keres={encoded_search_text}"
        
        html_soup_2 = requests.get(url_k, headers=headers)
        html_soup_2.encoding = 'ISO-8859-2'

        httx = 'https:'
        soup = BeautifulSoup(html_soup_2.text, 'html.parser')
        
        for link in soup.find_all('a'):
            div = link.find('div')
            if div is not None:
                title = div.text
                href = link.get('href')
                url_x = urllib.parse.urljoin(httx, href)
                self.addDirectoryItem(title, f'extract_movie&url={quote_plus(url_x)}', '', 'DefaultFolder.png')

        self.endDirectory()

    def getSearchText(self):
        search_text = ''
        keyb = xbmc.Keyboard('', u'Add meg a keresend\xF5 film c\xEDm\xE9t')
        keyb.doModal()
        if keyb.isConfirmed():
            search_text = keyb.getText()
        return search_text

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True, Fanart=None, meta=None, banner=None):
        url = f'{sysaddon}?action={query}' if isAction else query
        if thumb == '':
            thumb = icon
        cm = []
        if queue:
            cm.append((queueMenu, f'RunPlugin({sysaddon}?action=queueItem)'))
        if not context is None:
            cm.append((context[0].encode('utf-8'), f'RunPlugin({sysaddon}?action={context[1]})'))
        item = xbmcgui.ListItem(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb, 'poster': thumb, 'banner': banner})
        if Fanart is None:
            Fanart = addonFanart
        item.setProperty('Fanart_Image', Fanart)
        if not isFolder:
            item.setProperty('IsPlayable', 'true')
        if not meta is None:
            item.setInfo(type='Video', infoLabels=meta)
        xbmcplugin.addDirectoryItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def endDirectory(self, type='addons'):
        xbmcplugin.setContent(syshandle, type)
        xbmcplugin.endOfDirectory(syshandle, cacheToDisc=True)