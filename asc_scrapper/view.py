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


def print_schedule(schedule: Schedule, title: str = "Schedule"):
    print(
        f"{title}",
        "\n".join(
            f"{card.id}, "
            f"{get_subject_by_lesson_id(card.lessonid).short}, "
            f"{get_teacher_by_lesson_id(card.lessonid).short}, "
            f"{get_class_by_lesson_id(card.lessonid).short}, "
            f"{get_period(card.period).time}, "
            f"{get_day(card.days).name}"
            for card in schedule
        ),
        sep="\n"
    )
