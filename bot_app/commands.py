from enum import Enum


class Commands(str, Enum):
    start = "start"  # choose timetable
    timetable = "timetable"  # my timetable
    about = "about"  # about
    cancel = "cancel"  # cancel
