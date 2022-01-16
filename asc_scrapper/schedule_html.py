from pydantic.color import Color

from asc_scrapper.crud import *
from asc_scrapper.schemas import *
from colors.color_utils import decide_text_color, reduce_color_lightness, cprint


def schedule_html(*, periods: list[Period], days: list[Day], cards: Schedule, title: str,
                  is_dark: bool):
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
        h2 {{
           display:inline;
           margin-top:40px;
           text-align:center;
        }}
        thead {{
            display: table-header-group;
            vertical-align: middle;
            border-color: inherit;
            border-collapse: separate;
        }}

        th {{
            color: black;
        }}

        tr {{
            display: table-row;
            vertical-align: inherit;
            border-color: inherit;
        }}

        th,
        td {{
            white-space:pre-wrap;
            height: {row_height}%;
            word-wrap:break-word;
            text-align: middle;
            vertical-align: middle;
            border-left: 1px solid #ddd;
        }}

        td {{
            border-top: 1px solid #ddd;
            text-align: center;
        }}
        
        p {{
            font-family: verdana;
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
    <div style="background-color: {"#202b36" if is_dark else "white"}; padding: 1%;">
        <h1 style="color: white; text-align: center;">{title}</h1>
        <table>
            <thead>
                <colgroup>
                    <col span="{len(periods) + 1}" width="{col_width}%">
                </colgroup>
                <tr>
                    <th></th>
                    {"".join([f'<th style="color: #ffffff">{period.time}</th>' for period in periods])}
                </tr>
            </thead>
            <tbody>{generate_table(days=days, periods=periods, cards=cards)}</tbody>
        </table>
    </div>
</body>

</html>"""


def generate_table(days: list[Day], periods: list[Period], cards: Schedule, is_dark: bool = True):
    card_tags = ""
    on_background_color = "#ffffff" if is_dark else "#000000"
    crud = AscCRUD.from_file(file_name="../asc_scrapper/asc_schedule.json")
    for day in days:
        if day.short in ["X", "E"]:
            continue
        _day = day.vals[0]
        row = []
        for period in periods:
            card: Card = crud.get_card(day=_day, period=period.period, cards=cards)
            if card:
                lesson = crud.get_item(id=card.lessonid, type=Lesson)
                teacher = crud.get_item(id=lesson.teacher_id, type=Teacher)
                color = teacher.color
                color = reduce_color_lightness(Color(color), 0.75)
                font_color = decide_text_color(color)
                row.append(
                    f'<td '
                    f'style="background-color: {color}; color: {font_color}">'
                    f'{card_into_table(card=card, lesson=lesson, teacher=teacher, color=color, crud=crud)}</td>'
                )
            else:
                row.append(f"<td></td>")
        card_tags += f'<tr><td style="color: {on_background_color}"><h2>{day.short}</h2></td>{"".join(row)}</tr>'
        row.clear()

    return card_tags


def card_into_table(*, card: Card, lesson: Lesson, teacher: Teacher, color: Color, crud):
    subject_name = crud.get_item(id=lesson.subjectid, type=Subject).short
    classroom = crud.get_item(id=lesson.classroom_id, type=Classroom)
    tags = [f"<p>{subject_name}</p>"]
    if teacher:
        tags.append(f"<p>{teacher.short}</p>")

    if classroom and len(lesson.classroomidss) > 0:
        tags.append(f"<p>{classroom.name}</p>")
    cprint(f"{subject_name} , {teacher.short if teacher else ''} , {classroom}", bg_color=color)
    return "".join(tags)
