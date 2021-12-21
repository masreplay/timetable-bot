from typing import Type

from app import db
from schemas import *

Cards: Type = list[Card]


def get_classroom_schedule(classroom_id: str, cards: Cards = db.get_cards()) -> Cards:
    schedule = []
    for card in cards:
        classrooms: list = card.classroomids
        if len(classrooms) > 0 and classrooms[0] == classroom_id:
            schedule.append(card)

    return schedule


def get_class_schedule(class_id: str, cards: Cards = db.get_cards()) -> Cards:
    schedule = []
    for card in cards:
        _class = get_class_by_lesson_id(card.lessonid)
        if _class and _class.id == class_id:
            schedule.append(card)
    return schedule


def get_teacher_schedule(teacher_id: str, cards: Cards = db.get_cards()) -> Cards:
    schedule = []
    for card in cards:
        _class = get_teacher_by_lesson_id(card.lessonid)
        if _class and _class.id == teacher_id:
            schedule.append(card)
    return schedule


def get_classroom(classroom_id: str, classrooms=db.get_classrooms()) -> Classroom:
    for classroom in classrooms:
        if classroom.id == classroom_id:
            return classroom


def get_teacher(teacher_id: str, teachers=db.get_teachers()) -> Teacher:
    for teacher in teachers:
        if teacher.id == teacher_id:
            return teacher


def get_teachers() -> list[Teacher]:
    return db.get_teachers()


def get_subject_by_lesson_id(lesson_id: str) -> Subject:
    lesson = get_lesson(lesson_id)
    return get_subject(lesson.subjectid)


def get_class_by_lesson_id(lesson_id: str) -> Class:
    lesson = get_lesson(lesson_id)
    classes = lesson.classids
    if len(classes) > 0:
        return get_class(classes[0])


def get_teacher_by_lesson_id(lesson_id: str) -> Teacher:
    lesson = get_lesson(lesson_id)
    teachers = lesson.teacherids
    if len(teachers) > 0:
        return get_teacher(teachers[0])


def get_period(period_id: str, periods=db.get_periods()) -> Period:
    for period in periods:
        if period.id == period_id:
            return period


def get_day(day_id: str, days=db.get_days_def()) -> Day:
    for day in days:
        if day.vals[0] == day_id:
            return day


def get_subject(subject_id: str, subjects=db.get_subjects()) -> Subject:
    for subject in subjects:
        if subject.id == subject_id:
            return subject


def get_class(class_id: str, classes=db.get_classes()) -> Class:
    for _class in classes:
        if _class.id == class_id:
            return _class


def get_lesson(lesson_id: str, lessons=db.get_lessons()) -> Lesson:
    for lesson in lessons:
        if lesson.id == lesson_id:
            return lesson
