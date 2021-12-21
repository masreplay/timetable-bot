import json
import uuid
from typing import List, Dict, Set

import requests
import urllib3
from bs4 import BeautifulSoup as BSHTML

from app.const import *
from app.scrappers.email_extract import get_emails


def main():
    # http = urllib3.PoolManager()
    # for i in range(100):
    #     url = 'https://cs.uotechnology.edu.iq/index.php/s/cv/1258-bashar-saadoon-mahdi'
    #     http.request('GET', url)
    extract_department_teachers("ae")


def translate_list(untranslated: List[str], source: str = "en", target: str = "ar") -> List[str]:
    translations = requests.get(translation_key, params={
        "q": untranslated,
        "source": source,
        "target": target,
    }).json()["data"]["translations"]
    return [t["translatedText"] for t in translations]


def extract_department_teachers(department_abbr: str):
    _base_department_url = f'https://{department_abbr}.uotechnology.edu.iq'
    base_department_url = _base_department_url + '/'

    teachers_url = f'{base_department_url}index.php/s/cv'

    print("Connecting...")
    http = urllib3.PoolManager()
    response = http.request('GET', teachers_url)
    soup = BSHTML(response.data, "html.parser")

    # get teachers urls, image and en_name
    print("Getting teachers urls, image and en_name...")
    names = []
    teachers_urls = []
    teachers = []

    for link in soup.findAll('a'):
        href = link['href']
        if "/index.php/s/cv/" in href and "#itemCommentsAnchor" not in href:
            teacher_url = _base_department_url + link.get("href")

            # Prevent any duplication
            if teacher_url not in teachers_urls:
                image = link.find("img")
                teacher_name = image["alt"]

                teachers_urls.append(teacher_url)
                names.append(teacher_name)

                teacher = {
                    "id": uuid.uuid4().__str__(),
                    "ar_name": "",
                    "en_name": teacher_name,
                    "image": _base_department_url + image["src"],
                    "stage_id": [""],
                    "email": "",
                    "uot_url": teacher_url,
                    "role_id": ""
                }
                teachers.append(teacher)

    # translate en_name to ar_name
    print("Translating teachers name...")
    print(names)
    t_name: List[str] = translate_list(names)

    for (i, teacher) in enumerate(teachers):
        ar_name = t_name[i]
        teachers[i]["ar_name"] = ar_name

    # Get teacher role
    print("Getting teacher role...")
    roles = []
    roles_objects: List[Dict[str, str]] = []
    for (i, link) in enumerate(teachers_urls):

        response = http.request('GET', link)
        soup = BSHTML(response.data, "html.parser")
        if len(soup.findAll("span", {"style": "font-size: 12pt; color: #000000;"})) != 0:
            role_tag = soup.findAll("span", {"style": "font-size: 12pt; color: #000000;"})
            role_tag = role_tag[-1].text.title().rstrip()
        else:
            role_tag = soup.findAll("span", {"style": "font-size: 12pt;color: #000000;"})
            role_tag = role_tag[-1].text.title().rstrip()

        role = role_tag if len(role_tag) < 25 else "#"
        role_id: str
        if role not in roles:
            role_id = uuid.uuid4().__str__()
            roles_objects.append(
                {
                    "id": role_id,
                    "en_name": role
                }
            )
            roles.append(role)
            print(role)
        else:
            # get the id of the role if it's in roles
            role_id = [value for value in roles_objects if value["en_name"] == role][0]["id"]
            print(f"Copy {role}")
        teachers[i]["role_id"] = role_id

    print("Translating roles...")
    translation = translate_list(roles)
    for (i, ar_name) in enumerate(translation):
        roles_objects[i]["ar_name"] = ar_name
        roles_objects[i]["en_name"] = roles[i]

    # extract teacher email by his url
    print("Extracting emails...")
    teachers_emails = get_emails(teachers_urls)
    for (i, email) in enumerate(teachers_emails):
        teachers[i]["email"] = email

    # write roles json
    print("Writing roles json...")
    with open(f'{department_abbr}_roles.json', 'w', encoding='utf-8') as outfile:
        json.dump({"results": roles_objects}, outfile, ensure_ascii=False, indent=2)

    # write teacher json
    print("Writing teacher json...")
    with open(f'{department_abbr}_teachers.json', 'w', encoding='utf-8') as outfile:
        json.dump({"results": teachers}, outfile, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
