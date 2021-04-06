import requests
from bs4 import BeautifulSoup as BSHTML
import urllib3
import re
from extract_emails import EmailExtractor
from extract_emails.browsers import ChromeBrowser
from schemas import Teacher

http = urllib3.PoolManager()
url = 'https://cs.uotechnology.edu.iq/index.php/s/cv'

response = http.request('GET', url)
soup = BSHTML(response.data, "html.parser")
# images = [image for image in soup.findAll('img') if "/media/k2/items/cache/" in image['src']]
links = []

for i in soup.findAll('a'):
    if "/index.php/s/cv/" in i['href']:
        try:
            links.append(("https://cs.uotechnology.edu.iq" + i['href'], i['title']))
        except KeyError:
            pass

for i in range(len(links)):
    # image = images[i]
    link = links[i][0]
    # print(image['alt'])
    # print(link)
    with ChromeBrowser() as browser:
        email_extractor = EmailExtractor(link, browser, depth=2)
        emails = email_extractor.get_emails()

    for email in emails:
        if "uotechnology" in email.email:
            print(email.email)
    # print("https://cs.uotechnology.edu.iq" + image['src'])
    # r = requests.post('http://localhost:8000/v1/teacher',
    #                   json={
    #                       "gmail": f"{i}@gmail.com",
    #                       "name": (image['alt']),
    #                       "is_supervisor": False,
    #                       "job_degree": " ",
    #                       "image_url": "https://cs.uotechnology.edu.iq" + image['src']
    #                   },
    #                   headers={'access_token_key': '04537657ECB14221BD97253277998A0C'})
    # print(r.json())
    # teacher = Teacher(**r.json())
    # w = requests.post('http://localhost:8000/v1/link', params={"item_id": teacher.id, "item_type": "teacher"},
    #                   json={
    #                       "name": "0",
    #                       "url": link,
    #                       "is_public": True},
    #                   headers={'access_token_key': '04537657ECB14221BD97253277998A0C'})
    # print(r.status_code)
    # print(w.status_code)
