import json
import re
import requests
import sys

from bs4 import BeautifulSoup

date = input('Date (YYYY-MM-DD):')

url = 'http://phishtracks.com/shows/%s' % date
resp = requests.get(url)
html = resp.text
soup = BeautifulSoup(html, 'html.parser')
script = soup.find('script', text=re.compile('PTData'))

for line in script.text.split("\n"):
    line = line.strip()
    if line.startswith("PTData"):
        data = line
        break

data = re.sub('\n', '', data)
data = re.sub('PTData\s*=\s*', '', data, count=1)
data = re.sub(';.*', '', data, count=1)

js_data = json.loads(data)

m3u = ''
m3u += '#EXTM3U\n'

for show_set in js_data['sets']:
    for track in show_set['tracks']:
        m3u += '#EXTINF:%d,Phish - %s\n' % (track['duration']/1000, track['title'])
        m3u += track['file_url'] + '\n'

f = open('/mnt/playlists/phish_%s.m3u' % (date,), 'w')
f.write(m3u)
