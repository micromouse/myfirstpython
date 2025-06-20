"""
微博数据抓取演示
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# 打开微博
service = Service(executable_path="c:/windows/chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://weibo.com")

# 等你手动登录
input("登录后按 Enter 继续...")

# 访问具体微博页面，延时5秒
print("正在获取微博帖子：https://weibo.com/1499104401/PxnC4laEm")
driver.get("https://weibo.com/1499104401/PxnC4laEm")
time.sleep(5)

# 滚动加载评论
print("滚动浏览器加载评论")
for _ in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# 提取评论内容
print("获取评论内容")
comments = driver.find_elements(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/main/div[1]/div/div[2]/div[2]/div[3]/div/div[2]/div/div')
print(f"\n共获取 {len(comments)} 条评论：")
for i, c in enumerate(comments):
    print(f"{i + 1}. {c.text}")

print("完成评论获取，按 Enter 退出")
input()
driver.quit()
