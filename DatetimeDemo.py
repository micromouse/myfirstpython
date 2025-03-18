# datetime演示
from datetime import datetime

# 格式化datetime
now = datetime.now()
print(f"原始输出：{now}")
print(f"格式化输出：{now.strftime('%Y/%m/%d %H:%M:%S')}")

# 日期时间字符串转timestamp
datetime_str = "2025/03/18 10:14:09"
parsed_datetime = datetime.strptime(datetime_str, "%Y/%m/%d %H:%M:%S")
print(f"日期时间字符串[2025/03/18 10:14:09]转换为时间戳为：{parsed_datetime.timestamp()}")
