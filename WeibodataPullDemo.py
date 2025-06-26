import os.path
from operator import indexOf
from time import strftime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime, time
from typing import Any
import requests
import json
import time
import sys

def selenium_login_and_get_cookies():
    """
    使用selenium登录微博并获取cookies
    :return: 微博cookies
    """
    """使用 Selenium 登录微博并提取 cookies"""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service("c:/windows/chromedriver.exe"), options=chrome_options)

    # 手动扫码/账号登录
    driver.get("https://weibo.com/")
    input("请登录微博后按回车继续...")
    time.sleep(5)

    # 获得cookies并保存至cookies.json文件
    # Python字典推导式（dict comprehension）语法：
    # {key_expr: value_expr for item in iterable}
    # 遍历iterable，对每个 item，计算 key 和 value，然后组成一个新的字典。
    cookies = {c["name"]: c["value"] for c in driver.get_cookies()}
    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
        print("cookies已保存至cookies.json")

    driver.quit()
    return cookies

def load_cookies() -> dict | None:
    """
    从cookies.json中载入cookies
    :return: cookies
    """
    # cookies.json文件不存在
    if not os.path.exists("cookies.json"):
        return None

    # 从cookies.json文件中加载cookies
    with open("cookies.json", "r", encoding="utf-8") as f:
        cookies = json.load(f)
        return cookies

def fetch_comments(mid: str, max_id: int, total_counter: int, cookies: dict) -> (int, int):
    """
    取得微博下帖子评论
    :param mid: 帖子mid
    :param max_id: 下一页id
    :param total_counter: 总记录数
    :param cookies: 登录用户cookies
    :return: (max_id,total_counter)
    """
    """使用 requests 抓取指定微博的评论"""
    current_page = f"&max_id={max_id}" if max_id > 0 else ""
    url = f"https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id={mid}&is_show_bulletin=2&is_mix=0&count=20{current_page}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": f"https://weibo.com/2806170583/{mid}",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code != 200:
        print("请求失败，状态码：", response.status_code)
        return 0, total_counter

    data: dict[str, Any] = response.json()
    if data["ok"] == -100:
        print("用户未登录，请重新登录")
        return -1, total_counter
    comments = data.get("data", [])
    print(f"共获取 {len(comments)} 条评论：")
    if not comments:
        print("当前页未返回任何评论，可能需要翻页")
        return 0, total_counter
    else:
        try:
            for i, c in enumerate(comments):
                created_ftime = (datetime
                                 .strptime(c["created_at"], "%a %b %d %H:%M:%S %z %Y")
                                 .strftime("%Y/%m/%d %H:%M:%S"))
                if "👌" in c["text_raw"]:
                    print(f"当前评论[{c['text_raw']}]包含表情符号OK")
                print(f"{total_counter + i + 1}. {created_ftime}{c['user']['screen_name']}: {c['text_raw']}")
            total_counter += len(comments)
        except Exception as e:
            print(f"获取评论时发生异常：{e}")

        return data["max_id"], total_counter

# ---------- 主程序入口 ----------
if __name__ == "__main__":
    # 第一步：登录并获取 cookie
    cookies = load_cookies()
    if cookies is None:
        cookies = selenium_login_and_get_cookies()

    # 第二步：抓取微博评论（mid 是微博 ID，不是链接中的 UID）
    weibo_mid = "PxpqkDWRS"  # 替换成你想抓的微博 MID
    max_id = 0
    total_counter = 0
    while True:
        max_id, total_counter = fetch_comments(weibo_mid, max_id, total_counter, cookies)
        if max_id == 0:
            break
        elif max_id == -1:
            if os.path.exists("cookies.json"):
                os.remove("cookies.json")
            break

    print("按回车键退出")
    input()
    sys.exit(0)
