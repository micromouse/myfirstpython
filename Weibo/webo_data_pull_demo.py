import sys
from datetime import datetime

from CommentsFetcher import CommentsFetcher

def main():
    """
    主方法
    :return: None
    """
    comments_fetcher = CommentsFetcher(user_id="2806170583")
    all_comments = comments_fetcher.fetch_all_comments(m_id="PxpqkDWRS")
    for index, comment in enumerate(all_comments):
        created_ftime = (datetime
                         .strptime(comment["created_at"], "%a %b %d %H:%M:%S %z %Y")
                         .strftime("%Y/%m/%d %H:%M:%S"))
        if "👌" in comment["text_raw"]:
            print(f"当前评论[{comment['text_raw']}]包含表情符号OK")
        print(f"{index + 1}. {created_ftime}{comment['user']['screen_name']}: {comment['text_raw']}")

# ---------- 主程序入口 ----------
if __name__ == "__main__":
    main()

    print("按回车键退出")
    input()
    sys.exit(0)
