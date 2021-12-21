import shutil

import requests


def main():
    url = 'http://localhost:3000/image'
    with open("table.html", "r", encoding="utf-8") as file:
        response = requests.get(url, data={"html": file.read()}, stream=True)
        with open('img.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)


if __name__ == '__main__':
    main()
