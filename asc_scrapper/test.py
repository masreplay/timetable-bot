import json

from asc_scrapper import schemas

data_dir = "asc_data"
json_file = open(f"{data_dir}/asc_schedule.json", encoding="utf8")
data = json.load(json_file)

if __name__ == '__main__':
    asc_data: schemas.AscData = schemas.AscData.parse_obj(data)
    ignores = ["weeksdefs", "weeks", "termsdefs", "terms", "breaks", "studentsubjects", "students", "bells"]
    wanted = ["card", "day", "subject", "lesson", "period", "teacher", "class", "classroom", "building"]
    for column in asc_data.data:
        name = column.name
        if name not in ignores:
            file = open(f"{data_dir}/{name}.json", "w", encoding="utf8")
            json.dump(column.dict(), file, indent=2, ensure_ascii=False)
            file.close()
