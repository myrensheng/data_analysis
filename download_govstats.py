import os

import requests
from bs4 import BeautifulSoup

base_url = "http://www.stats.gov.cn/tjsj/pcsj/rkpc/6rp/"

html_url = "http://www.stats.gov.cn/tjsj/pcsj/rkpc/6rp/lefte.htm"


def spider():
    html = requests.get(html_url)
    html.encoding = "gb2312"
    soup = BeautifulSoup(html.text, 'lxml')
    a_soup = soup.find_all("a")
    for a in a_soup:
        href = a.get("href")
        if "excel" in href:
            result = requests.get(base_url + href)
            excel_name = os.path.join(os.getcwd(), "excels", a.text + ".xlsx")
            with open(excel_name, "wb") as f:
                f.write(result.content)
            print(a.text,"完成")
            # time.sleep(2)


if __name__ == '__main__':
    spider()
