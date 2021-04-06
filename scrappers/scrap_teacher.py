import os
from extract_emails import EmailExtractor
from extract_emails.browsers import ChromeBrowser

import requests
from bs4 import BeautifulSoup as BSHTML
import urllib3

from schemas import Teacher

api_key = '04537657ECB14221BD97253277998A0C'
key_header = {'access_token_key': api_key}
local_host = "http://localhost:8000/v1/"
host_url = "https://csuot.herokuapp.com/v1/"
base_url = host_url

http = urllib3.PoolManager()

url = 'https://cs.uotechnology.edu.iq/index.php/s/cv'

response = http.request('GET', url)
soup = BSHTML(response.data, "html.parser")

images = [image for image in soup.findAll('img') if "/media/k2/items/cache/" in image['src']]

links = []
for i in soup.findAll('a'):
    if "/index.php/s/cv/" in i['href']:
        try:
            links.append(("https://cs.uotechnology.edu.iq" + i['href'], i['title']))
        except KeyError:
            pass

teachers_gmail = []

for i in range(len(links)):
    image = images[i]
    link = links[i][0]
    gmail = teachers_gmail[i]

    print(image['alt'])
    print(gmail)
    print(link)
    print("https://cs.uotechnology.edu.iq" + image['src'])

    # extract gmail from page
    # with ChromeBrowser() as browser:
    #     email_extractor = EmailExtractor(link, browser, depth=2)
    #     emails = email_extractor.get_emails()
    # for email in emails:
    #     if "uotechnology" in email.email:
    #         print(email.email)

    create_teacher = requests.post(base_url + 'teacher',
                                   json={
                                       "gmail": gmail,
                                       "name": (image['alt']),
                                       "is_supervisor": False,
                                       "job_degree": "",
                                       "image_url": "https://cs.uotechnology.edu.iq" + image['src']
                                   },
                                   headers=key_header)
    print(create_teacher.json())
    if 300 > create_teacher.status_code > 200:
        teacher = Teacher(**create_teacher.json())

        create_teacher_link0 = requests.post(base_url + 'link',
                                             params={"item_id": teacher.id, "item_type": "teacher"},
                                             json={
                                                 "name": "0",
                                                 "url": link,
                                                 "is_public": True},
                                             headers=key_header)
        print(create_teacher_link0.status_code)
    print(create_teacher.status_code)

# turn teacher gmails to list
# os.chdir("./teachers_gmails")
# with open("cs_teacher_gmail.txt",'r') as file:
#     teachers_gmail = [teacher for teacher in file.read().split("\n")]
#     print(teachers_gmail)
