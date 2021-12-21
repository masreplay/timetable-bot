from app.view import *


def main():
    # matlab -38
    # classroom_schedule("-38")
    # class_schedule("*22")
    # ولاء *58
    teacher_schedule("*24")
    # print("\n".join([f"{teacher.short}, {teacher.id}" for teacher in get_teachers()]))


if __name__ == '__main__':
    main()
