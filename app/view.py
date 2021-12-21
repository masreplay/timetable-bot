from crud import *


def classroom_schedule(classroom_id: str):
    classroom = get_classroom(classroom_id)
    schedule = get_classroom_schedule(classroom_id)

    sorted_schedule = sorted(schedule, key=lambda card: get_day(card.days).id)
    print(
        f"{classroom.name}",
        "\n".join(
            f"{card.id}, "
            f"{get_subject_by_lesson_id(card.lessonid).short}, "
            f"{get_teacher_by_lesson_id(card.lessonid).short}, "
            f"{get_class_by_lesson_id(card.lessonid).short}, "
            f"{get_period(card.period).time}, "
            f"{get_day(card.days).name}"
            for card in sorted_schedule
        ),
        sep="\n"
    )


def class_schedule(class_id: str):
    _class = get_class(class_id)

    if _class:
        schedule = get_class_schedule(class_id)
        schedule_sort = sorted(schedule, key=lambda card: get_day(card.days).id)
        print(
            f"{_class.short}",
            "\n".join(
                f"{card.id}, "
                f"{get_subject_by_lesson_id(card.lessonid).short}, "
                f"{get_teacher_by_lesson_id(card.lessonid).short}, "
                f"{get_class_by_lesson_id(card.lessonid).short}, "
                f"{get_period(card.period).time}, "
                f"{get_day(card.days).name}"
                for card in schedule_sort
            ),
            sep="\n"
        )


def teacher_schedule(teacher_id: str):
    teacher = get_teacher(teacher_id)

    if teacher:
        schedule = get_teacher_schedule(teacher_id)
        schedule_sort = sorted(schedule, key=lambda card: get_day(card.days).id)
        print(
            f"{teacher.short}",
            "\n".join(
                f"{card.id}, "
                f"{get_subject_by_lesson_id(card.lessonid).short}, "
                f"{get_teacher_by_lesson_id(card.lessonid).short}, "
                f"{get_class_by_lesson_id(card.lessonid).short}, "
                f"{get_period(card.period).time}, "
                f"{get_day(card.days).name}"
                for card in schedule_sort
            ),
            sep="\n"
        )
