from typing import Any

import requests

from CookiesGetter import CookiesGetter

class CommentsFetcher:
    """
    使用 requests 抓取微博指定帖子的全部评论
    """

    def __init__(self, user_id: str, page_size: int = 20):
        """
        初始化使使用 requests 抓取微博指定帖子的全部评论
        :param user_id: 用户Id
        """
        self.user_id = user_id
        self.page_size = page_size
        self.__cookiesGetter = CookiesGetter()

    def fetch_all_comments(self, m_id: str) -> list[dict[str, Any]]:
        """
        获取所有评论
        :param m_id: 帖子Id
        :return: 微博下所有评论集合
        """
        max_id: int = 0
        all_comments: list[dict[str, Any]] = []

        # 循环获取所有页评论
        while True:
            (comments, max_id) = self.fetch_paging_comments(m_id, max_id)
            if comments:
                all_comments.extend(comments)
            else:
                break

        return all_comments

    def fetch_paging_comments(self, m_id: str, max_id: int) -> tuple[list[dict[str, Any]], int]:
        """
        获取分页评论
        :param m_id: 帖子Id
        :param max_id: 当前页Id
        :return: (微博评论集合, 下一页Id)
        """
        url = ("https://weibo.com/ajax/statuses/buildComments?" +
               f"flow=0&is_reload=1&id={m_id}&is_show_bulletin=2&is_mix=0&count={self.page_size}" +
               (f"&max_id={max_id}" if max_id > 0 else ""))
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": f"https://weibo.com/{self.user_id}/{m_id}",
            "Accept": "application/json",
        }

        response = requests.get(url, headers=headers, cookies=self.__cookiesGetter.load_cookies())
        if response.status_code != 200:
            raise requests.HTTPError(f"Http请求异常,相应代码：{response.status_code}")
        response_data: dict[str, Any] = response.json()
        if response_data["ok"] == -100:
            self.__cookiesGetter.remove_cookies()
            raise PermissionError(f"用户未登录异常")

        # 返回当前页(评论集合,下一页Id)
        comments = response_data.get("data", [])
        if not isinstance(comments, list):
            raise ValueError("当前页没有任何评论，可能需要翻页")
        next_max_id = response_data.get("max_id", 0)
        return comments, next_max_id
