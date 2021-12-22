import shutil

import requests

from app.crud import *


def body():
    f"""<html lang="en">

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
                        <col span="4" width="16.6%">
                    </colgroup>

                </colgroup>
                <tr>
                    <th></th>
                    {"".join([f"{period.time}" for period in get_periods()])}
                </tr>
                
            </thead>
            <tbody>
                <tr>
                    <td></td>
                    <td>رياضيات تيست تيستاية</td>
                    <td>رياضيات تيست تيستاية</td>
                    <td>رياضيات تيست تيستاية</td>
                    <td>رياضيات تيست تيستاية</td>
                    <td>رياضيات تيست تيستاية</td>
                </tr>
            </tbody>
        </table>
    </div>
</body>

</html>"""


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


def main():
    class_schedule("*22")
    url = 'http://localhost:3000/image'
    with open("table.html", "r", encoding="utf-8") as file:
        response = requests.get(url, data={"html": file.read()}, stream=True)
        with open('img.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)


if __name__ == '__main__':
    main()
