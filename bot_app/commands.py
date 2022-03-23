from enum import Enum


class Commands(str, Enum):
    start = "start"  # choose timetable
    timetable = "timetable"  # my timetable
    cancel = "cancel"  # cancel
    test = "test"  # test
