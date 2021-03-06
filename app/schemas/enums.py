from enum import Enum


class UserScrapeFrom(str, Enum):
    # https://cs.uotechnology.edu.iq/index.php/s/cv/
    uot = "uot"
    # https://uotcs.edupage.org/timetable/
    asc = "asc"
    # both of them
    uot_asc = "uot_asc"


class StaffType(str, Enum):
    employee = "employee"
    teacher = "teacher"


class UserType(str, Enum):
    employee = "employee"
    teacher = "teacher"
    student = "student"
    other = "other"


class UserGender(str, Enum):
    male = "male"
    female = "female"


class CollageShifts(str, Enum):
    morning = "morning"
    evening = "evening"
    both = "both"


class RoomType(str, Enum):
    classroom = "classroom"
    employee = "employee"
    other = "other"


class Environment(str, Enum):
    development = "development"
    production = "production"
