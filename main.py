#!/usr/bin/env python3
#coding=utf-8

import time
import random
import requests
import os
from bs4 import BeautifulSoup

headers = {
    "accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding":
    "gzip, deflate, br",
    "accept-language":
    "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control":
    "max-age=0",
    "cookie":
    "UM_distinctid=16ff13fa8882a9-04cab7e1736859-39637b0f-13c680-16ff13fa8896ea; ors__user_login=YQKE8sA5jNRuuvZlA7iKKTiyHaamSP7v9vQlW5cK6WUIZGMNv0NxyIP3djLi%2FWkGyS4PaXqFGhV4JKApnjKAdgn%2Fb7u%2F2N9BFw42WjZVDzSeXH22bSRhLrpf7L02ky8DgaM8GRxNMbEamTjEQzTdkw%3D%3D; CNZZDATA1273638993=1742481213-1580300481-https%253A%252F%252Fwww.google.com%252F%7C1580687960; _ga=GA1.2.2112721461.1581489987; user_id=eyJfcmFpbHMiOnsibWVzc2FnZSI6ImJuVnNiQT09IiwiZXhwIjpudWxsLCJwdXIiOiJjb29raWUudXNlcl9pZCJ9fQ%3D%3D--7be7692be2b183cb596182cc0f259343111372bc; _gid=GA1.2.603236007.1581936869; Hm_lvt_928280caf87c86e98e74eefae01ebae4=1580687961,1581489987,1581656498,1581936870; _homeland_session=zFR7ANR%2F63AGXyVx7EkNv%2B9oiTH7MF%2B6I4ZlGz9ePaELEyiwHCiTC7Z53z1yXqL3KSLcqOT5gr0IvPWoDUxrZOVsEVjfBrZWe%2FilbQwPCtGwzfUYMfek%2Feb1Q2VCT5%2FI6Aw%2Fwna877iD8U22nIVM3Jdu0gzkbfcFg%2FSqEAFqK%2BCBc9VQtFrM%2Bp%2Fwr1UTE%2FjCFqhkzBZUQytWIVLAf4MlhDlBG1U4CfkJBw06MVfdIaSDlRsIq6lIxK%2FcaSR0CeZsW7ncOmK4qkJuIFetoZ6MxDt3Zd4QGwRSOK3WSuvrhYIUbH5h9MpqnRCW7f7ShAA%3D--KPKAGXpL2TTUnq5j--JG0eaejmEw2pIFgwHMNpZg%3D%3D; Hm_lpvt_928280caf87c86e98e74eefae01ebae4=1581982190",
    "if-none-match":
    "W/\"42172c688376f0dc4bbe90ea8f809825\"",
    "sec-fetch-dest":
    "document",
    "sec-fetch-mode":
    "navigate",
    "sec-fetch-site":
    "same-origin",
    "sec-fetch-user":
    "?1",
    "upgrade-insecure-requests":
    "1",
    "user-agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36",
}


def download(url):
    resp = requests.get(url, headers=headers)
    return resp.content.decode('utf-8')


def save_error_id(id):
    with open('error.txt', 'a') as fp:
        fp.write('{0}\n'.format(id))


def save_id(id):
    with open('success.txt', 'w') as fp:
        fp.write('{0}\n'.format(id))


def is_great_page(content):
    return '本帖已被设为精华帖' in content


def extract_title(content):
    soup = BeautifulSoup(content, 'html.parser')
    title = soup.find('span', class_='title')
    title = title.get_text()
    return title


def save_to_data(title, url):
    with open('data/data.md', 'a') as fp:
        result = '[{0}]({1})\n'.format(title, url)
        fp.write(result)


def random_sleep():
    time.sleep(random.random() * 2)


def crawl(start, end):
    for i in range(start, end):
        url = 'https://gocn.vip/topics/{0}'.format(i)
        try:
            content = download(url)
        except Exception as e:
            print('download {} error'.format(url))
            save_error_id(i)
        else:
            save_id(i)
            if is_great_page(content):
                title = extract_title(content)
                save_to_data(title, url)
                print('find great page {0} {1}'.format(title, url))
            else:
                print('skip url {0}'.format(url))
        random_sleep()


def test():
    if not os.path.exists('a.html'):
        content = download('https://gocn.vip/topics/9779')
        with open('test.html', 'w') as fp:
            fp.write(content)

    with open('test.html', 'r') as fp:
        content = fp.read()
        print(extract_title(content))


def main():
    crawl(11, 9779)


if __name__ == '__main__':
    main()
