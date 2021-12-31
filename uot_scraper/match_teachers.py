from asc_scrapper.asc_data import db
from uot_scraper.db import get_teachers

TeachersName = list[str]


def formate_asc_teachers():
    return db.get_teachers()


def formate_uot_teachers():
    return get_teachers()


if __name__ == '__main__':
    uot_teachers = formate_uot_teachers()
    asc_teachers = formate_asc_teachers()
    print(f"uot: {len(uot_teachers)}")
    print(f"schedule: {len(asc_teachers)}")
    c = 0
    new_asc = []
    new_uot = []

    teachers = []

    for uot_teacher in uot_teachers:
        for asc_teacher in asc_teachers:
            if asc_teacher.get_name is not None \
                    and uot_teacher.first_name == asc_teacher.first_name \
                    and uot_teacher.second_name == asc_teacher.second_name:
                new_asc.append(asc_teacher)
                new_uot.append(uot_teacher)
                teachers.append(
                    {
                        "id": uot_teacher.id,
                        "ar_name": uot_teacher.ar_name,
                        "en_name": uot_teacher.en_name,
                        "image": uot_teacher.image,
                        "email": uot_teacher.email,
                        "uot_url": uot_teacher.uot_url,
                        "role_id": uot_teacher.role_id,
                        "other_name": asc_teacher.get_name,
                        "color": asc_teacher.color,
                        "gender": asc_teacher.gender,
                    }
                )
                c += 1
                break

    print(len(new_asc))
    print("\n".join([f"{i + 1} {teacher}" for i, teacher in enumerate(teachers)]))
    print(len(new_uot))
    # new_uot = [teacher for teacher in teachers if teacher not in asc_teachers]

    print(f"equal: {c}")
