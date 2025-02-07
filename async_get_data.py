import asyncio
import os

import aiohttp
import aiofiles
from lxml import html
from datetime import datetime

from constants import TEMPLATE_HTML, HOT_FILE, Url

async def fetch_data(url, session):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Referer": "https://tophub.today/"
    }
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            response.encoding = 'utf-8'
            tree = html.fromstring(await response.text())
            rows = tree.xpath('//div[@class="cc-dc"][1]//table[@class="table"]//tr')

            table_rows = ""
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
                table_rows += f"""
                <tr>
                    <td>{index}</td>
                    <td><img src="{Url.url_favicon_icon(url)}"> {title_with_link}</td>
                    <td>{hot_level}</td>
                </tr>"""

            return table_rows
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return ""


async def get_data():
    async with aiohttp.ClientSession() as session:
        table1_rows, table2_rows = await asyncio.gather(
            fetch_data(Url.WeiBo.value, session),
            fetch_data(Url.Zhihu.value, session)
        )

        async with aiofiles.open(TEMPLATE_HTML, "r", encoding="utf-8") as template_file:
            html_template = await template_file.read()

        html_content = html_template.replace("{{table1_rows}}", table1_rows)
        html_content = html_content.replace("{{table2_rows}}", table2_rows)
        create_datetime = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        html_content = html_content.replace("{{create_datetime}}", create_datetime)

        async with aiofiles.open(HOT_FILE, "w", encoding="utf-8") as file:
            await file.write(html_content)

        print(f"write html content to {HOT_FILE}")
