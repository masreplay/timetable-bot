import requests
from bs4 import BeautifulSoup as BSHTML
import urllib3

from app.schemas import Teacher

api_key = '04537657ECB14221BD97253277998A0C'
key_header = {'access_token_key': api_key}
local_host = "http://localhost:8000/v1/"
host_url = "https://csuot.herokuapp.com/v1/"
base_url = local_host

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

teachers_gmail = ['110074@uotechnology.edu.iq', '110053@uotechnology.edu.iq', '110018@uotechnology.edu.iq',
                  '110004@uotechnology.edu.iq', '110026@uotechnology.edu.iq', 'ayad.r.abbas@uotechnology.edu.iq',
                  '110016@uotechnology.edu.iq', '110136@uotechnology.edu.iq', '110050@uotechnology.edu.iq',
                  'haimaa.h.shaker@uotechnology.edu.iq', '110009@uotechnology.edu.iq', '110017@uotechnology.edu.iq',
                  '110120@uotechnology.edu.iq', '110014@uotechnology.edu.iq', '110005@uotechnology.edu.iq',
                  '110034@uotechnology.edu.iq', 'saif.b.neamah@uotechnology.edu.iq', '110104@uotechnology.edu.iq',
                  '10861@uotechnology.edu.iq', '70200@uotechnology.edu.iq', '110020@uotechnology.edu.iq',
                  '10035@uotechnology.edu.iq', '110030@uotechnology.edu.iq', '110008@uotechnology.edu.iq',
                  '40265@uotechnology.edu.iq', '110078@uotechnology.edu.iq', '110113@uotechnology.edu.iq',
                  '10029@uotechnology.edu.iq', '110135@uotechnology.edu.iq', '110132@uotechnology.edu.iq',
                  '110022@uotechnology.edu.iq', '110124@uotechnology.edu.iq', '110121@uotechnology.edu.iq',
                  '110033@uotechnology.edu.iq', '10872@uotechnology.edu.iq', '10010@uotechnology.edu.iq',
                  '10860@uotechnology.edu.iq', '110039@uotechnology.edu.iq', '110077@uotechnology.edu.iq',
                  '110048@uotechnology.edu.iq', '110096@uotechnology.edu.iq', '110037@uotechnology.edu.iq',
                  'adiq@uotechnology.edu.iq', '110134@uotechnology.edu.iq', '110043@uotechnology.edu.iq',
                  '110131@uotechnology.edu.iq', '10886@uotechnology.edu.iq', '110027@uotechnology.edu.iq',
                  '110032@uotechnology.edu.iq', '110051@uotechnology.edu.iq', '110044@uotechnology.edu.iq',
                  '110102@uotechnology.edu.iq', '110105@uotechnology.edu.iq', '110056@uotechnology.edu.iq',
                  '110036@uotechnology.edu.iq', '110038@uotechnology.edu.iq', '110023@uotechnology.edu.iq',
                  '110015@uotechnology.edu.iq', '110029@uotechnology.edu.iq', '110024@uotechnology.edu.iq',
                  '110068@uotechnology.edu.iq', '110072@uotechnology.edu.iq', '110110@uotechnology.edu.iq',
                  '110119@uotechnology.edu.iq', '110019@uotechnology.edu.iq', '110040@uotechnology.edu.iq',
                  '110137@uotechnology.edu.iq', '110028@uotechnology.edu.iq', '110046@uotechnology.edu.iq',
                  '110108@uotechnology.edu.iq']

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
