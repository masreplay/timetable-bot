import json
import uuid
from typing import List

import requests
import urllib3
from bs4 import BeautifulSoup as BSHTML

from settings import get_settings
from uot_scraper.email_extract import get_emails
from uot_scraper.schemas import UotTeacher, UotTeachers, UotRole, UotRoles


def main():
    extract_department_teachers("ae")


def translate_list(untranslated: List[str], source: str = "en", target: str = "ar") -> List[str]:
    translations = requests.get(get_settings().translation_key, params={
        "q": untranslated,
        "source": source,
        "target": target,
    }).json()["asc_data"]["translations"]
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
    teachers: UotTeachers = []

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

                teacher: UotTeacher = UotTeacher(
                    id=uuid.uuid4().__str__(),
                    ar_name=None,
                    en_name=teacher_name,
                    image=_base_department_url + image["src"],
                    stages_id=[],
                    email=None,
                    uot_url=teacher_url,
                    role_id=None
                )
                teachers.append(teacher)

    # translate en_name to ar_name
    print("Translating teachers name...")
    print(names)
    t_name: List[str] = translate_list(names)

    for (i, teacher) in enumerate(teachers):
        ar_name = t_name[i]
        teachers[i] = ar_name

    # Get teacher role
    print("Getting teacher role...")
    roles = []
    roles_objects: UotRoles = []
    for (i, link) in enumerate(teachers_urls):

        response = http.request('GET', link)
        soup = BSHTML(response.data, "html.parser")
        if len(soup.findAll("span", {"style": "font-size: 12pt; color: #000000;"})) != 0:
            role_tag = soup.findAll("span", {"style": "font-size: 12pt; color: #000000;"})
            role_tag = role_tag[-1].msg.title().rstrip()
        else:
            role_tag = soup.findAll("span", {"style": "font-size: 12pt;color: #000000;"})
            role_tag = role_tag[-1].msg.title().rstrip()

        role = role_tag if len(role_tag) < 25 else "#"
        role_id: str
        if role not in roles:
            role_id = uuid.uuid4().__str__()
            roles_objects.append(
                UotRole(
                    id=role_id,
                    en_name=role
                )
            )
            roles.append(role)
            print(role)
        else:
            # get the id of the role if it's in roles
            role_id = [value for value in roles_objects if value.en_name == role][0].id
            print(f"Copy {role}")
        teachers[i].role_id = role_id

    print("Translating roles...")
    translation = translate_list(roles)
    for (i, ar_name) in enumerate(translation):
        roles_objects[i].ar_name = ar_name
        roles_objects[i].en_name = roles[i]

    # extract teacher email by his url
    print("Extracting emails...")
    teachers_emails = get_emails(teachers_urls)
    for (i, email) in enumerate(teachers_emails):
        teachers[i].email = email

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