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

    for uot_teacher in uot_teachers:
        for asc_teacher in asc_teachers:
            if asc_teacher.get_name is not None \
                    and uot_teacher.first_name == asc_teacher.first_name \
                    and uot_teacher.second_name == asc_teacher.second_name:
                new_asc.append(asc_teacher)
                new_uot.append(uot_teacher)
                c += 1
                break

    print(new_asc)
    print(new_uot)
    # new_uot = [teacher for teacher in teachers if teacher not in asc_teachers]

    print(f"equal: {c}")
