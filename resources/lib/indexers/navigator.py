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
import html

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
addonFanart = xbmcaddon.Addon().getAddonInfo('fanart')

import platform
import xml.etree.ElementTree as ET

os_info = platform.platform()
kodi_version = xbmc.getInfoLabel('System.BuildVersion')

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(current_directory)))
addon_xml_path = os.path.join(parent_directory, "addon.xml")

tree = ET.parse(addon_xml_path)
root = tree.getroot()
version = root.attrib.get("version")

xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info}', xbmc.LOGINFO)

base_url = 'https://jobbmintatv.org'

headers = {
    'authority': 'jobbmintatv.org',
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
        self.searchFileName = os.path.join(self.base_path, "search.history")

    def root(self):
        self.addDirectoryItem("Filmek", "only_movies", '', 'DefaultFolder.png')
        self.addDirectoryItem("Sorozatok", "only_series", '', 'DefaultFolder.png')
        self.addDirectoryItem("Film Kategóriák", "movie_categories", '', 'DefaultFolder.png')
        self.addDirectoryItem("Sorozat Kategóriák", "series_categories", '', 'DefaultFolder.png')
        self.addDirectoryItem("Film & Sorozat Kategóriák", "all_categories", '', 'DefaultFolder.png')
        self.addDirectoryItem("Keresés", "search", '', 'DefaultFolder.png')
        self.endDirectory()
        
    def getAllCategories(self):
        page = requests.get(f"{base_url}/mind/1/1//", headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        categories = soup.select('a[href^="//jobbmintatv.org/mind/1/1/"]:not(.aktiv)')
        
        for category in categories:
            category_name = category.text.strip()
            category_url = 'https:' + category['href']
            category_num =  re.findall(r'.*/(.*)', category_url)[0].strip()

            xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | getAllCategories | category_url | {category_url}', xbmc.LOGINFO)

            self.addDirectoryItem(f"{category_name}", f'items&url={category_url}', '', 'DefaultFolder.png')
        
        self.endDirectory('movies')        

    def getMovieCategories(self):
        page = requests.get(f"{base_url}/filmek/1/1//", headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        categories = soup.select('a[href^="//jobbmintatv.org/filmek/1/1/"]:not(.aktiv)')
        
        for category in categories:
            category_name = category.text.strip()
            category_url = 'https:' + category['href']
            category_num =  re.findall(r'.*/(.*)', category_url)[0].strip()

            xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | getMovieCategories | category_url | {category_url}', xbmc.LOGINFO)

            self.addDirectoryItem(f"{category_name}", f'movie_items&url={category_url}', '', 'DefaultFolder.png')
        
        self.endDirectory('movies')

    def getSeriesCategories(self):
        page = requests.get(f"{base_url}/sorozatok/1/1//", headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        categories = soup.select('a[href^="//jobbmintatv.org/sorozatok/1/1/"]:not(.aktiv)')
        
        for category in categories:
            category_name = category.text.strip()
            category_url = 'https:' + category['href']
            category_num =  re.findall(r'.*/(.*)', category_url)[0].strip()

            xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | getSeriesCategories | category_url | {category_url}', xbmc.LOGINFO)

            self.addDirectoryItem(f"{category_name}", f'series_items&url={category_url}', '', 'DefaultFolder.png')
        
        self.endDirectory('series')        

    def getItems(self, url):

        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        anchors = soup.find_all('a', class_='kocka')
        
        for anchor in anchors:
            try:
                card_link = anchor['href']
                if not re.match(r'https?://', card_link):
                    card_link = 'https:' + card_link                
                
                html_soup_2 = requests.get(card_link, headers=headers)
                
                soup_2 = BeautifulSoup(html_soup_2.text, 'html.parser')
                
                season_links = []
                evadoks = soup_2.find_all('a', class_='evadoks')
                htt = 'https://jobbmintatv.org'
                for evadok in evadoks:
                    season_number = evadok.text.strip()
                    season_link = urllib.parse.urljoin(htt, evadok['href'])
                    season_links.append({"evad": season_link})
                
                type = 'Sorozat'
                
                add_to = 'extract_series'
                
                veletlen_resz_element = soup_2.find('a', class_='evad_link_vezerlo', string='Véletlen rész')
                veletlen_resz = urllib.parse.urljoin(htt, veletlen_resz_element['href']) if veletlen_resz_element else ''
                
                sid_element = soup_2.find('a', class_='evad_link_vezerlo info rand', string='Véletlen rész').find_next('a', {'sid': True})
                sid = sid_element['sid'] if sid_element and 'sid' in sid_element.attrs else ''
                
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
                imdb = imdb_rating_match[0] if imdb_rating_match else ''
                img_url = urllib.parse.urljoin(htt, sorozat_borito_element.img['src']) if sorozat_borito_element and sorozat_borito_element.img else ''
                content = tartalom_element.text.strip() if tartalom_element else ''
                
                hun_m = f'{hun_title} - {year}'

            except:
                
                card_link = anchor['href']
                if not re.match(r'https?://', card_link):
                    card_link = 'https:' + card_link                 
                
                type_str = 'Film'
                type = f'{type_str:^10}'
                
                add_to = 'extract_movie'
                
                img_src = anchor.find('img')['src']
                if not re.match(r'https?://', img_src):
                    img_url = 'https:' + img_src
                
                hun_title = anchor.find('span', class_='cimk').text
                
                imdb_match = re.search(r'\[imdb:(\d+(\.\d+)?)\]', anchor.find('span', class_='egyebekk').text)
                imdb = imdb_match.group(1) if imdb_match else None
                
                year_match = re.search(r'\d{4}', anchor.find('span', class_='egyebekk').text)
                year = year_match.group() if year_match else None
                
                hun_m = f'{hun_title} - {year}'
                
            self.addDirectoryItem(f'[B]| {type} | {hun_title} - {year} | [COLOR yellow]{imdb}[/COLOR][/B]', f'{add_to}&url={quote_plus(card_link)}&img_url={img_url}&hun_title={hun_title}&year={year}', img_url, 'DefaultMovies.png', isFolder=True, meta={'title': hun_m})

        try:
            next_page_anchor = soup.find('a', string='következő oldal')
            if next_page_anchor:
                next_page = next_page_anchor['href']
                htt = 'https:'
                next_page_url = htt + next_page
            
            self.addDirectoryItem('[I]Következő oldal[/I]', f'items&url={quote_plus(next_page_url)}', '', 'DefaultFolder.png')
        except (AttributeError, UnboundLocalError):
            xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | getItems | next_page_url | csak egy oldal található', xbmc.LOGINFO)
            
        self.endDirectory('movies')


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

            imdb_match = re.search(r'\[imdb:(\d+(\.\d+)?)\]', anchor.find('span', class_='egyebekk').text)
            imdb = imdb_match.group(1) if imdb_match else None
            
            year_match = re.search(r'\d{4}', anchor.find('span', class_='egyebekk').text)
            year = year_match.group() if year_match else None            
            
            hun_m = f'{hun_title} - {year}'
            
            self.addDirectoryItem(f'[B]{hun_title} - {year} | [COLOR yellow]{imdb}[/COLOR][/B]', f'extract_movie&url={card_link}&img_url={img_url}&hun_title={hun_title}&year={year}', img_url, 'DefaultMovies.png', isFolder=True, meta={'title': hun_m})

        try:
            next_page_anchor = soup.find('a', string='következő oldal')
            if next_page_anchor:
                next_page = next_page_anchor['href']
                htt = 'https:'
                next_page_url = htt + next_page
            
            self.addDirectoryItem('[I]Következő oldal[/I]', f'movie_items&url={quote_plus(next_page_url)}', '', 'DefaultFolder.png')
        except AttributeError:
            xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | getOnlyMovies | next_page_url | csak egy oldal található', xbmc.LOGINFO)
        
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

            imdb_match = re.search(r'\[imdb:(\d+(\.\d+)?)\]', anchor.find('span', class_='egyebekk').text)
            imdb = imdb_match.group(1) if imdb_match else None
            
            year_match = re.search(r'\d{4}', anchor.find('span', class_='egyebekk').text)
            year = year_match.group() if year_match else None            
            
            hun_m = f'{hun_title} - {year}'
            
            self.addDirectoryItem(f'[B]{hun_title} - {year} | [COLOR yellow]{imdb}[/COLOR][/B]', f'extract_series&url={quote_plus(card_link)}&img_url={img_url}&hun_title={hun_title}&year={year}', img_url, 'DefaultMovies.png', isFolder=True, meta={'title': hun_m})
            
        try:
            next_page_anchor = soup.find('a', string='következő oldal')
            if next_page_anchor:
                next_page = next_page_anchor['href']
                httx = 'https:'
                next_page_url = httx + next_page
            
            self.addDirectoryItem('[I]Következő oldal[/I]', f'series_items&url={quote_plus(next_page_url)}', '', 'DefaultFolder.png')
        except AttributeError:
            xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | getOnlySeries | next_page_url | csak egy oldal található', xbmc.LOGINFO)
        
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

            imdb_match = re.search(r'\[imdb:(\d+(\.\d+)?)\]', anchor.find('span', class_='egyebekk').text)
            imdb = imdb_match.group(1) if imdb_match else None
            
            year_match = re.search(r'\d{4}', anchor.find('span', class_='egyebekk').text)
            year = year_match.group() if year_match else None            
            
            hun_m = f'{hun_title} - {year}'
            
            self.addDirectoryItem(f'[B]{hun_title} - {year} | [COLOR yellow]{imdb}[/COLOR][/B]', f'extract_movie&url={card_link}&img_url={img_url}&hun_title={hun_title}&year={year}', img_url, 'DefaultMovies.png', isFolder=True, meta={'title': hun_m})
            
        try:
            next_page_anchor = soup.find('a', string='következő oldal')
            if next_page_anchor:
                next_page = next_page_anchor['href']
                htt = 'https:'
                next_page_url = htt + next_page
            
            self.addDirectoryItem('[I]Következő oldal[/I]', f'movie_items&url={quote_plus(next_page_url)}', '', 'DefaultFolder.png')
        except (AttributeError, UnboundLocalError):
            xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | getMovieItems | next_page_url | csak egy oldal található', xbmc.LOGINFO)
        
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

            imdb_match = re.search(r'\[imdb:(\d+(\.\d+)?)\]', anchor.find('span', class_='egyebekk').text)
            imdb = imdb_match.group(1) if imdb_match else None
            
            year_match = re.search(r'\d{4}', anchor.find('span', class_='egyebekk').text)
            year = year_match.group() if year_match else None            
            
            hun_m = f'{hun_title} - {year}'
            
            self.addDirectoryItem(f'[B]{hun_title} - {year} | [COLOR yellow]{imdb}[/COLOR][/B]', f'extract_series&url={quote_plus(card_link)}&img_url={img_url}&hun_title={hun_title}&year={year}', img_url, 'DefaultMovies.png', isFolder=True, meta={'title': hun_m})
        
        try:
            next_page_anchor = soup.find('a', string='következő oldal')
            if next_page_anchor:
                next_page = next_page_anchor['href']
                httx = 'https:'
                next_page_url = httx + next_page
            
            self.addDirectoryItem('[I]Következő oldal[/I]', f'series_items&url={quote_plus(next_page_url)}', '', 'DefaultFolder.png')
        except (AttributeError, UnboundLocalError):
            xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | getSeriesItems | next_page_url | csak egy oldal található', xbmc.LOGINFO)
        
        self.endDirectory('series')

    def extractMovie(self, url, img_url, hun_title, content, year):
        
        html_soup_2 = requests.get(url, headers=headers)
        
        xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | extractMovie | url | {url}', xbmc.LOGINFO)
        
        soup_2 = BeautifulSoup(html_soup_2.text, 'html.parser')

        xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | extractMovie | soup_2 | {soup_2}', xbmc.LOGINFO)
        
        hun_title = soup_2.select_one('#sorozat_adatlap_film h1').text
        
        xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | extractMovie | hun_title | {hun_title}', xbmc.LOGINFO)
        
        en_title_element = soup_2.select_one('#sorozat_adatlap_film h1:nth-of-type(2)')
        en_title = en_title_element.text if en_title_element else None
        year = soup_2.select_one('#adatlap_menu div:-soup-contains("Évjárat") b').text
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

    def extractSeries(self, url, img_url, hun_title, content, ep_title, year):
        html_soup_2 = requests.get(url, headers=headers)
        
        soup_2 = BeautifulSoup(html_soup_2.text, 'html.parser')

        season_links = []
        evadoks = soup_2.find_all('a', class_='evadoks')
        htt = 'https://jobbmintatv.org'
        for evadok in evadoks:
            season_number = evadok.text.strip()
            season_link = urllib.parse.urljoin(htt, evadok['href'])
            season_links.append({"evad": season_link})

        veletlen_resz_element = soup_2.find('a', class_='evad_link_vezerlo', string='Véletlen rész')
        veletlen_resz = urllib.parse.urljoin(htt, veletlen_resz_element['href']) if veletlen_resz_element else ''
        
        sid_element = soup_2.find('a', class_='evad_link_vezerlo info rand', string='Véletlen rész')
        
        if sid_element is not None:
            next_a_element = sid_element.find_next('a', {'sid': True})
            sid = next_a_element['sid'] if next_a_element and 'sid' in next_a_element.attrs else ''
        else:
            sid = ''
        
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
            
            html_source = requests.get('https://jobbmintatv.org/ajax.php', params=params, headers=headers)
            
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
        xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | extractEpisodes | url | {url}', xbmc.LOGINFO)
    
        html_soup_2 = requests.get(url, headers=headers)
        soup_2 = BeautifulSoup(html_soup_2.text, 'html.parser')

        iframe = soup_2.find('iframe')

        if iframe:
            iframe_src = iframe.get('src')
            xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | extractEpisodes | iframe_src | {iframe_src}', xbmc.LOGINFO)
            
            hun_ep = f'{ep_title} - {hun_title} - {year}'
            
            self.addDirectoryItem(f'[B]{ep_title} - {hun_title} - {year}[/B]', f'playmovie&url={quote_plus(iframe_src)}&img_url={img_url}&hun_title={hun_title}&content={content}&year={year}', img_url, 'DefaultMovies.png', isFolder=False, meta={'title': hun_ep, 'plot': content})
        
        self.endDirectory('series')

    def playMovie(self, url):
        try:
            direct_url = urlresolver.resolve(url)
            
            xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | playMovie | direct_url: {direct_url}', xbmc.LOGINFO)
            play_item = xbmcgui.ListItem(path=direct_url)
            xbmcplugin.setResolvedUrl(syshandle, True, listitem=play_item)
        except:
            xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | playMovie | name: No video sources found', xbmc.LOGINFO)
            notification = xbmcgui.Dialog()
            notification.notification("JobbMintATv", "Törölt tartalom", time=5000)

    def getSearches(self):
        self.addDirectoryItem('[COLOR lightgreen]Új keresés[/COLOR]', 'newsearch', '', 'DefaultFolder.png')
        try:
            file = open(self.searchFileName, "r")
            olditems = file.read().splitlines()
            file.close()
            items = list(set(olditems))
            items.sort(key=locale.strxfrm)
            if len(items) != len(olditems):
                file = open(self.searchFileName, "w")
                file.write("\n".join(items))
                file.close()
            for item in items:
                url_p = f"{base_url}/ajax.php?keres={item}"
                enc_url = quote_plus(url_p)

                html_soup_2 = requests.get(enc_url, headers=headers)
                html_soup_2.encoding = 'ISO-8859-2'
                
                httx = 'https:'
                soup = BeautifulSoup(html_soup_2.text, 'html.parser')
                
                for link in soup.find_all('a'):
                    title = link.find('div').text
                    href = link.get('href')
                    url = urllib.parse.urljoin(httx, href)
                    
                    xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | getSearches | title | {title}', xbmc.LOGINFO)
                    xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | getSearches | title | {url}', xbmc.LOGINFO)
                

                    self.addDirectoryItem(title, f'items&url={quote_plus(url)}', '', 'DefaultFolder.png')
                    #self.getItems(url)                    

            if len(items) > 0:
                self.addDirectoryItem('[COLOR red]Keresési előzmények törlése[/COLOR]', 'deletesearchhistory', '', 'DefaultFolder.png')
        except:
            pass
        self.endDirectory()

    def deleteSearchHistory(self):
        if os.path.exists(self.searchFileName):
            os.remove(self.searchFileName)

    def doSearch(self):
        search_text = self.getSearchText()
        if search_text != '':
            if not os.path.exists(self.base_path):
                os.mkdir(self.base_path)
            file = open(self.searchFileName, "a")
            file.write(f"{search_text}\n")
            file.close()
            url_k = f"{base_url}/ajax.php?keres={search_text}"
            #enc_url = quote_plus(url_k)
            
            html_soup_2 = requests.get(url_k, headers=headers)
            html_soup_2.encoding = 'ISO-8859-2'

            httx = 'https:'
            soup = BeautifulSoup(html_soup_2.text, 'html.parser')
            
            for link in soup.find_all('a'):
                title = link.find('div').text
                href = link.get('href')
                url = urllib.parse.urljoin(httx, href)
                
                xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | doSearch | title | {title}', xbmc.LOGINFO)
                xbmc.log(f'JobbMintATv | v{version} | Kodi: {kodi_version[:5]}| OS: {os_info} | doSearch | url | {url}', xbmc.LOGINFO)
                
                
                self.addDirectoryItem(title, f'items&url={quote_plus(url)}', '', 'DefaultFolder.png')
                self.getItems(url)

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