import requests
from lxml import html


def get_weibo_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Referer": "https://tophub.today/"
    }
    url = "https://tophub.today/n/KqndgxeLl9"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = 'utf-8'
        tree = html.fromstring(response.text)
        rows = tree.xpath('//div[@class="cc-dc"][1]//table[@class="table"]//tr')

        html_table = """<html>
<head>
    <meta charset="UTF-8">
    <title>微博热搜</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            font-size: 24px
        }
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            text-align: center;
        }
        td {
            font-size: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <h1>TopHub 热点数据</h1>
    <table>
        <thead>
            <tr>
                <th>序号</th>
                <th>标题</th>
                <th>热度</th>
            </tr>
        </thead>
        <tbody>"""

        for row in rows:
            index_element = row.xpath('./td[1]')
            index = index_element[0].text_content().strip().replace('.', '') if index_element else "N/A"

            title_element = row.xpath('./td[2]/a')
            if title_element:
                title = title_element[0].text_content().strip()
                url = title_element[0].get('href', '无链接')
                title_with_link = f'<a href="{url}">{title}</a>'
            else:
                title_with_link = "N/A"

            hot_level_element = row.xpath('./td[3]')
            hot_level = hot_level_element[0].text_content().strip() if hot_level_element else "N/A"

            html_table += f"""
            <tr>
                <td>{index}</td>
                <td>{title_with_link}</td>
                <td>{hot_level}</td>
            </tr>"""

        html_table += """
        </tbody>
    </table>
</body>
</html>"""

        with open("weibo.html", "w", encoding="utf-8") as file:
            file.write(html_table)

        print("HTML表格已生成并写入到weibo.html 文件中！")

    except requests.RequestException as e:
        print("请求失败：", e)
    except Exception as e:
        print("发生错误：", e)



