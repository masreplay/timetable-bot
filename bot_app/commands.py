from enum import Enum


class Commands(str, Enum):
    start = "start"
    schedule = "schedule"
    cancel = "cancel"
    test = "test"
