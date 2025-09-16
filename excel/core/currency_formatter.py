from decimal import Decimal, ROUND_HALF_UP
from numbers import Number

from num2words import num2words

class CurrencyFormatter:
    """
    货币格式化器
    """

    @staticmethod
    def format_currency_amount(amount: Number) -> str:
        """
        格式化金额为财务专用格式
        :param amount: Decimal, 金额
        :return: 金额财务专用格式内容
        """
        # 不是Decimal类型转换为Decimal类型
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))

        if amount == 0:
            return "**SAY US DOLLARS ZERO ONLY**"
        else:
            return f"**SAY US DOLLARS {CurrencyFormatter._money_to_english(amount)} ONLY**"

    @staticmethod
    def _money_to_english(amount: Decimal) -> str:
        """
        金额转英文金额
        :param amount: Decimal, 金额
        :return: 金额英文显示内容
        """
        # 四舍五入
        amount = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # 负数处理
        sign: str = ""
        if amount < 0:
            sign = "negative "
            amount = -amount

        # 拆分整数部分和小数部分
        integer_part = int(amount)
        decimal_part = int(round((amount * 100) % 100))

        # 转换整数部分和小数部分
        words = f"{sign} {num2words(integer_part, lang='en').replace('-', ' ')} dollars"
        if decimal_part > 0:
            words += f" and {num2words(decimal_part, lang='en')} cents"

        # 结果大写
        return words.upper()
