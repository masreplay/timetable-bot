from crud import *


def classroom_schedule(classroom_id: str):
    classroom = get_classroom(classroom_id)
    if classroom:
        return get_classroom_schedule(classroom_id)


def class_schedule(class_id: str):
    _class = get_class(class_id)

    if _class:
        return get_class_schedule(class_id)


def teacher_schedule(teacher_id: str):
    teacher = get_teacher(teacher_id)

    if teacher:
        return get_teacher_schedule(teacher_id)
