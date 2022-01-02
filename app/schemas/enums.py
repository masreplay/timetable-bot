from enum import Enum


class UserScrapeFrom(str, Enum):
    # https://cs.uotechnology.edu.iq/index.php/s/cv/
    uot = "uot"
    # https://uotcs.edupage.org/timetable/
    asc = "asc"
    # both of them
    uot_asc = "uot_asc"


class UserType(str, Enum):
    employee = "employee"
    teacher = "teacher"

    # teacher and employee
    teacher_employee = "teacher_employee"

    student = "student"
    other = "other"


class UserGender(str, Enum):
    male = "male"
    female = "female"
