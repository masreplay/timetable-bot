import shutil

import requests

from app.crud import *
from app.view import *


# matlab -38
# classroom_schedule("-38")
# class_schedule("*22")
# ولاء *58
# teacher_schedule("*24")
# print("\n".join([f"{teacher.short}, {teacher.id}" for teacher in get_teachers()]))


def body(periods: list[Period], days: list[Day], cards: list[Card]):
    return f"""<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        table {{
            border: 1px solid #ddd;
            border-collapse: separate;
            border-left: 0;
            border-radius: 4px;
            border-spacing: 0px;
            width: 100%;
        }}

        thead {{
            display: table-header-group;
            vertical-align: middle;
            border-color: inherit;
            border-collapse: separate;
        }}

        th {{
            color: violet;
        }}
        
        tr {{
            display: table-row;
            vertical-align: inherit;
            border-color: inherit;
        }}

        th,
        td {{
            padding: 5px 4px 6px 4px;
            text-align: middle;
            vertical-align: middle;
            border-left: 1px solid #ddd;
        }}

        td {{
            border-top: 1px solid #ddd;
            text-align: center;
        }}

        thead:first-child tr:first-child th:first-child,
        tbody:first-child tr:first-child td:first-child {{
            border-radius: 4px 0 0 0;
        }}

        thead:last-child tr:last-child th:first-child,
        tbody:last-child tr:last-child td:first-child {{
            border-radius: 0 0 0 4px;
        }}
    </style>
</head>

<body>
    <div style="background-color: white ;">

        <table>
            <thead>
                <colgroup>
                    <colgroup>
                        <col span="4" width="{100 / len(periods)}%">
                    </colgroup>

                </colgroup>
                <tr>
                    <th></th>
                    {"".join([f"<th>{period.time}</th>" for period in periods])}
                </tr>
            </thead>
            <tbody>{generate_tab(days=days, periods=periods, cards=cards)}</tbody>
        </table>
    </div>
</body>

</html>"""


def generate_tab(days: list[Day], periods: list[Period], cards: list[Card]):
    card_tags = ""
    print(len(cards))
    for day in days:
        row = f"<tr><td>{day.name}</td>"
        for card in cards:
            if card.days == day.vals[0]:
                row += f"<td>{card_into_table(card)}</td>"
            else:
                row += "<td></td>"
        card_tags += row
    return card_tags


# class: software-fourth-
def class_schedule(class_id: str):
    _class = get_class(class_id)

    if _class:
        schedule = get_class_schedule(class_id)
        return sorted(schedule, key=lambda card: get_day(card.days).id)


def card_into_table(card: Card):
    return f"{get_subject_by_lesson_id(card.lessonid).short}, " \
           f"{get_teacher_by_lesson_id(card.lessonid).short}, " \
           f"{get_class_by_lesson_id(card.lessonid).short}, "


def main():
    class_schedule("*22")
    url = 'http://localhost:3000/image'
    data = body(get_periods(), get_days(), class_schedule("*21"))
    response = requests.get(url, data={"html": data}, stream=True)
    with open("table.g.html", "w", encoding="utf-8") as file:
        file.write(data)
    with open('table.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)


if __name__ == '__main__':
    main()

# print(
#             f"{_class.short}",
#             "\n".join(
#                 f"{card.id}, "
#                 f"{get_subject_by_lesson_id(card.lessonid).short}, "
#                 f"{get_teacher_by_lesson_id(card.lessonid).short}, "
#                 f"{get_class_by_lesson_id(card.lessonid).short}, "
#                 f"{get_period(card.period).time}, "
#                 f"{get_day(card.days).name}"
#                 for card in schedule_sort
#             ),
#             sep="\n"
#         )
