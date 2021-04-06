from bs4 import BeautifulSoup as BSHTML
import urllib3

http = urllib3.PoolManager()
url = 'https://uotcs.edupage.org/timetable/'

response = http.request('GET', url)
soup = BSHTML(response.data, "html.parser")
gs = soup.findAll('g')

for i in range(len(gs)):
    g = gs[i]
    print((g['alt']))
