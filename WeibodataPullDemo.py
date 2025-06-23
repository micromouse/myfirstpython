from time import strftime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime, time
import requests
import json
import time
import sys

def get_cookies_dict(cookies_list):
    """将 selenium cookies 转换为 requests 可用的 dict 格式"""
    return {cookie['name']: cookie['value'] for cookie in cookies_list}

def selenium_login_and_get_cookies():
    """使用 Selenium 登录微博并提取 cookies"""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service("c:/windows/chromedriver.exe"), options=chrome_options)

    driver.get("https://weibo.com/")
    input("请登录微博后按回车继续...")  # 手动扫码/账号登录
    time.sleep(5)

    cookies = driver.get_cookies()
    driver.quit()
    return get_cookies_dict(cookies)

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
    next_page = f"&max_id={max_id}" if max_id > 0 else ""
    url = f"https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id={mid}&is_show_bulletin=2&is_mix=0&count=20{next_page}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": f"https://weibo.com/2806170583/{mid}",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code != 200:
        print("请求失败，状态码：", response.status_code)
        return 0, total_counter

    data = response.json()
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
                print(f"{total_counter + i + 1}. {created_ftime}{c['user']['screen_name']}: {c['text_raw']}")
            total_counter += len(comments)
        except Exception as e:
            print(f"获取评论时发生异常：{e}")

        return data["max_id"], total_counter

# ---------- 主程序入口 ----------
if __name__ == "__main__":
    # 第一步：登录并获取 cookie
    cookies = selenium_login_and_get_cookies()

    # 第二步：抓取微博评论（mid 是微博 ID，不是链接中的 UID）
    weibo_mid = "PxpqkDWRS"  # 替换成你想抓的微博 MID
    max_id = 0
    total_counter = 0
    while True:
        max_id, total_counter = fetch_comments(weibo_mid, max_id, total_counter, cookies)
        if max_id == 0:
            break

    print("按回车键退出")
    input()
    sys.exit(0)
