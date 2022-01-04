from pydantic.color import Color

from app import schemas
from app.schemas.user import UserGender, UserScrapeFrom, UserType
from asc_scrapper.asc_data import db
from colors.color_utils import random_primary, colored_text
from uot_scraper.db import get_teachers

TeachersName = list[str]


def formate_asc_teachers():
    return db.get_teachers()


def formate_uot_teachers():
    return get_teachers()


def get_acs_uot_teachers():
    old_uot = formate_uot_teachers()
    old_asc = formate_asc_teachers()

    c = 0
    new_asc = []
    new_uot = []

    teachers = []

    for uot_teacher in old_uot:
        for asc_teacher in old_asc:
            if asc_teacher.get_name is not None \
                    and uot_teacher.first_name == asc_teacher.first_name \
                    and uot_teacher.second_name == asc_teacher.second_name:
                new_asc.append(asc_teacher)
                new_uot.append(uot_teacher)
                teachers.append(
                    schemas.UserCreate(
                        type=UserType.teacher,
                        name=uot_teacher.ar_name,
                        en_name=uot_teacher.en_name,
                        image=uot_teacher.image,
                        email=uot_teacher.email,
                        uot_url=uot_teacher.uot_url,
                        role_id=uot_teacher.role_id,
                        color=asc_teacher.color,
                        asc_job_title=asc_teacher.job_title,
                        asc_name=asc_teacher.get_name,
                        scrape_from=UserScrapeFrom.uot_asc,
                        gender=UserGender.male if asc_teacher.gender.lower() == "m" else UserGender.female,
                    )

                )
                c += 1
                break
    new_asc = [teacher for teacher in old_asc if teacher not in new_asc]
    for teacher in new_asc:
        teachers.append(
            schemas.UserCreate(
                type=UserType.teacher,
                name=teacher.get_name,
                en_name=None,
                image=None,
                email=None,
                uot_url=None,
                role_id=None,
                color=teacher.color,
                asc_job_title=teacher.job_title,
                asc_name=teacher.get_name,
                scrape_from=UserScrapeFrom.asc,
                gender=UserGender.male if teacher.gender.lower() == "m" else UserGender.female,
            )

        )
    new_uot = [teacher for teacher in old_uot if teacher not in new_uot]
    for teacher in new_uot:
        teachers.append(
            schemas.UserCreate(
                type=UserType.teacher,
                name=teacher.ar_name,
                en_name=teacher.en_name,
                image=teacher.image,
                email=teacher.email,
                uot_url=teacher.uot_url,
                role_id=teacher.role_id,
                color=random_primary(400).as_hex(),
                asc_job_title=None,
                asc_name=None,
                scrape_from=UserScrapeFrom.uot,
                gender=None,
            )

        )
    # remove nameless data
    teachers = [
        teacher for teacher in teachers
        if (teacher.en_name is not None and teacher.name is not None) or teacher.asc_name is not None
    ]
    return teachers


if __name__ == '__main__':
    print("\n".join(
        [f"{colored_text(i + 1, bg_color=Color(teacher.color))}{teacher.dict(),}" for i, teacher in
         enumerate(get_acs_uot_teachers())]
    ))
