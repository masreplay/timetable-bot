from data import db
from scrappers.db import get_teachers

TeachersName = list[str]


def formate_asc_teachers(asc_teachers=db.get_teachers()) -> TeachersName:
    teachers = []
    for teacher in asc_teachers:
        name = teacher.short.split(".")
        # remove where د.م.
        name = name[-1]
        if len(name) in [0, 1]:
            continue
        # remove where د م ا or empty spaces
        separated_name = name.split(" ")
        for part in separated_name:
            if len(part) in [0, 1]:
                separated_name.remove(part)
        teachers.append(" ".join(separated_name))
    return teachers


def formate_uot_teachers():
    teachers = get_teachers()
    print([teacher for teacher in get_teachers()])


if __name__ == '__main__':
    formate_asc_teachers()
