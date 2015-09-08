import json
import re
import requests
import sys

from bs4 import BeautifulSoup

date = input('Date (YYYY-MM-DD):')

r = requests.get('http://www.phishtracks.com/shows/%s' % (date,))
html = r.text
soup = BeautifulSoup(html, 'html.parser')
script = soup.find('script', text=re.compile('PTData'))

data = re.findall('PTData[\s\n]*=[\s\n]*\{[^;]+;', script.text)[0]

data = re.sub('\n', '', data)
data = re.sub('[^{]*', '', data, count=1)
data = re.sub(';.*', '', data, count=1)

js_data = json.loads(data)

m3u = ''
m3u += '#EXTM3U\n'

for show_set in js_data['sets']:
    for track in show_set['tracks']:
        m3u += '#EXTINF:%d, Phish: %s\n' % (track['duration']/1000, track['title'])
        m3u += track['file_url'] + '\n'

f = open('phish_%s.m3u' % (date,), 'w')
f.write(m3u)
