from app import schemas
from bot_app.theme import ScheduleTheme


def schedule_template_html(*, schedule: schemas.ScheduleDetails, title: str, theme: ScheduleTheme):
    """
    Template body of schedule
    """
    col_width = 100 / (len(schedule.periods) + 1)
    row_height = 100 / (len(schedule.days) + 1)
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

        body, div, h1, h2, h3, h4, h5, h6, p, span {{
            font-family: {theme.font_name}!important;
            -webkit-user-select: none;
            -ms-user-select: none;
            user-select: none;
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
            color: {theme.on_background_color};
        }}

        tr {{
            display: table-row;
            vertical-align: inherit;
            border-color: inherit;
        }}

        th,
        td {{
            padding: 4px;
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
    <script src="https://ajax.googleapis.com/ajax/libs/webfont/1.6.26/webfont.js"></script>
        <script>
          WebFont.load({{
            google: {{
            families: ['{theme.font_name}']
            }}
          }});
        </script>
</head>

<body>
    <div style="background-color: {theme.background_color}; padding: 1%;">
        <h1 style="color: white; text-align: center;">{title}</h1>
        <table>
            <thead>
                <colgroup>
                    <col span="{len(schedule.periods) + 1}" width="{col_width}%">
                </colgroup>
                <tr>
                    <th></th>
                    {"".join([f'<th style="color: {theme.on_background_color}">{period.time}</th>' for period in schedule.periods])}
                </tr>
            </thead>
            <tbody>{generate_table(schedule=schedule, theme=theme)}</tbody>
        </table>
        <h3 style="color: white; text-align: right;">@ConstructorTeam</h1>
    </div>
</body>

</html>"""
