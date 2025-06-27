import os
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class CookiesGetter:
    """
    微博Cookies获取器
    """

    def __init__(self, chromedriver: str = "c:/windows/chromedriver.exe"):
        """
        初始化微博Cookies获取器
        :param chromedriver: chromedriver.exe文件
        """
        self.chromedriver = chromedriver
        self.__cookies_file = "./cookies.json"

    def load_cookies(self) -> dict[str, str]:
        # cookies.json文件不存在,使用selenium登录微博并获取cookies
        if not os.path.exists(self.__cookies_file):
            cookies = self.__selenium_login_and_get_cookies()
            self.__save_cookies_to_file(cookies)

        # 从cookies.json文件中加载cookies
        with open(self.__cookies_file, "r", encoding="utf-8") as f:
            cookies = json.load(f)
            return cookies

    def __selenium_login_and_get_cookies(self) -> list[dict]:
        """
        使用selenium登录微博并获取cookies
        :return: 微博cookies
        """
        """使用 Selenium 登录微博并提取 cookies"""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        with webdriver.Chrome(service=Service(self.chromedriver), options=chrome_options) as driver:
            # 手动扫码/账号登录
            driver.get("https://weibo.com/")
            input("请登录微博后按回车继续...")
            time.sleep(5)
            return driver.get_cookies()

    def __save_cookies_to_file(self, cookies: list[dict]):
        # Python字典推导式（dict comprehension）语法：
        # {key_expr: value_expr for item in iterable}
        # 遍历iterable，对每个 item，计算 key 和 value，然后组成一个新的字典。
        cookies = {c["name"]: c["value"] for c in cookies}
        with open(self.__cookies_file, "w", encoding="utf-8") as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
            print("cookies已保存至cookies.json")
