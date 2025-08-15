# datetime演示
from datetime import datetime, UTC

# 格式化datetime
now = datetime.now()
print(f"原始输出：{now}")
print(f"格式化输出：{now.strftime('%Y/%m/%d %H:%M:%S')}")

# utc时间
utc_now: datetime = datetime.now(UTC)
print(f"原始输出utc时间：{utc_now}")
print(f"utc时间的时间戳：{utc_now.timestamp()}")
print(f"当前时区时间的时间戳：{datetime.now().timestamp()}")

# 日期时间字符串转timestamp
datetime_str = "2025/03/18 10:14:09"
parsed_datetime = datetime.strptime(datetime_str, "%Y/%m/%d %H:%M:%S")
print(f"日期时间字符串[2025/03/18 10:14:09]转换为时间戳为：{parsed_datetime.timestamp()}")
