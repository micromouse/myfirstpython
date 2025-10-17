# 函数演示
def sum_nums(first: int, *others: int):
    """
    不定长参数求和
    :param first: 第一个数字
    :param others: 其余任意数字
    :return: 所有数字的总和
    """
    sum: int = first
    for num in others:
        sum += num
    return sum

total = 0

def calculate_total(num1: int, num2: int):
    """
    计算total值
    :param num1: 数字1
    :param num2: 数字2
    """
    # 这里创建了一个新的局部变量 total，不影响外部的 total
    total = num1 + num2
    print(f"calculate_total方法内的total={total}")

# 多个数字求和
print(f"1={sum_nums(1)}")
print(f"1+2+3={sum_nums(1, 2, 3)}")
print(f"1+2+3+4+5={sum_nums(1, 2, 3, 4, 5)}")

# 计算total
calculate_total(1, 2)
print(f"calculate_total方法外的total={total}")
