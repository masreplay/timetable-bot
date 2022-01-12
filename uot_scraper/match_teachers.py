from pydantic import BaseModel

from app.schemas.user import UserGender, UserScrapeFrom
from asc_scrapper import schemas as asc_schemas
from asc_scrapper.crud import AscCRUD
from colors.color_utils import random_primary
from uot_scraper.db import get_teachers


class MergedTeacher(BaseModel):
    """
    Teacher's data from Acs and Uot combined
    """
    id: str
    name: str | None
    en_name: str | None
    image: str | None
    email: str | None
    uot_url: str | None
    role_id: str | None
    color: str
    asc_job_title: str | None
    asc_name: str | None
    scrape_from: UserScrapeFrom
    gender: UserGender | None


def combine_acs_uot_teachers(asc: AscCRUD) -> list[MergedTeacher]:
    """
    combine teacher's data from asc and uot
    :return: combined teachers data
    """
    old_uot = get_teachers()
    old_asc = asc.get_all(asc_schemas.Teacher)

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
                    MergedTeacher(
                        id=asc_teacher.id,
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
        if teacher.get_name is None:
            print(teacher)
        teachers.append(
            MergedTeacher(
                id=teacher.id,
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
            MergedTeacher(
                id=teacher.id,
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

# if __name__ == '__main__':
#     print("\n".join(
#         [f"{colored_text(i + 1, bg_color=Color(teacher.color))}{teacher.dict(),}" for i, teacher in
#          enumerate(get_acs_uot_teachers())]
#     ))
