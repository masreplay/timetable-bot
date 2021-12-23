import shutil

import requests

from app.view import *

schedule: Schedule = teacher_schedule("*15")


def body(periods: list[Period], days: list[Day], cards: Schedule):
    col_width = 100 / (len(periods) + 1)
    row_height = 100 / (len(days) + 1)
    style = f"""<style>
        table {{
            border: 1px solid #ddd;
            border-collapse: separate;
            border-left: 0;
            border-radius: 10px;
            border-spacing: 0px;
            width: 100%;
            height: 100%;
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
            height: {row_height}%;
            vertical-align: inherit;
            border-color: inherit;
        }}

        th,
        td {{
            white-space:pre-wrap;
            word-wrap:break-word;
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
    </style>"""
    return f"""<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    {style}
</head>

<body>
    <div style="background-color: white; padding: 1%;">
        <table>
            <thead>
                <colgroup>
                    <col span="4" width="{col_width}%">
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


def generate_tab(days: list[Day], periods: list[Period], cards: Schedule):
    card_tags = ""
    for day in days:
        _day = day.vals[0]
        row = []
        for period in periods:
            card = get_card(day=_day, period=period.period, cards=cards)
            if card:
                row.append(
                    f'<td '
                    f'style="background-color: {get_teacher_by_lesson_id(card.lessonid).color}">'
                    f'{card_into_table(card)}</td>'
                )
            else:
                row.append(f"<td></td>")
        card_tags += f"<tr><td>{day.short}</td>{''.join(row)}</tr>"
        row.clear()

    return card_tags


def card_into_table(card: Card):
    card_data = \
        f"{get_subject_by_lesson_id(card.lessonid).short}\n" \
        f"{get_teacher_by_lesson_id(card.lessonid).short}\n" \
        f"{get_class_by_lesson_id(card.lessonid).short}\n"
    if len(card.classroomids) > 0:
        card_data += f"{get_classroom(card.classroomids[0]).short}"
    return card_data


def main():
    url = 'http://localhost:3000/image'
    periods = get_periods()
    days = get_days()
    data = body(periods=periods, days=days, cards=schedule)

    response = requests.get(url, data={"html": data}, stream=True)

    with open("table.g.html", "w", encoding="utf-8") as file:
        file.write(data)

    with open('table.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)


def main1():
    url = 'http://localhost:3000/image'

    print_schedule(schedule)
    with open("table.g.html", "r", encoding="utf-8") as file:
        response = requests.get(url, data={"html": file.read()}, stream=True)
    with open('table.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)


if __name__ == '__main__':
    main()
    # main1()

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
