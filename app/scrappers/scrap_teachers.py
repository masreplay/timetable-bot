import json
import uuid
from typing import List, Dict, Set

import requests
import urllib3
from bs4 import BeautifulSoup as BSHTML

from app.const import *


def translate_list(untranslated: List[str], source: str = "en", target: str = "ar") -> List[str]:
    translations: List[Dict[str, str]] = requests.get(translation_key, params={
        "q": untranslated,
        "source": source,
        "target": target,
    }).json()["data"]["translations"]
    return [t["translatedText"] for t in translations]


def main():
    base_department_url = 'https://cs.uotechnology.edu.iq/'
    _base_department_url = 'https://cs.uotechnology.edu.iq'

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
                    "gmail": "",
                    "uot_url": teacher_url,
                    "role_id": ""
                }
                teachers.append(teacher)

    # translate en_name to ar_name
    print("Translating teachers name...")
    t_name: List[str] = translate_list(names)

    for (i, teacher) in enumerate(teachers):
        ar_name = t_name[i]
        teachers[i]["ar_name"] = ar_name

    # Get teacher role
    print("Getting teacher role")
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
        if role not in roles:
            role_id = uuid.uuid4().__str__()
            roles_objects.append(
                {
                    "id": role_id,
                }
            )
            teachers[i]["role_id"] = role_id

            roles.append(role)
            print(role)

    translation = translate_list(roles)
    for (i, ar_name) in enumerate(translation):
        roles_objects[i]["ar_name"] = ar_name
        roles_objects[i]["en_name"] = roles[i]

    with open('roles.json', 'w', encoding='utf-8') as outfile:
        json.dump({"results": roles_objects}, outfile, ensure_ascii=False, indent=2)

    # write teacher json
    print("Writing teacher json...")
    with open('teachers.json', 'w', encoding='utf-8') as outfile:
        json.dump({"results": teachers}, outfile, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
