# FastApi基类
from typing import Dict

from fastapi import APIRouter
from pydantic import BaseModel

class ResponseModel(BaseModel):
    """
    统一响应模型
    """
    code: int = 200
    message: str = "success"
    data: Dict

class FastApiBase:
    """
    FastApi基类
    """
    router: APIRouter

    def __init__(self):
        """
        初始化FastApi基类
        """
        self.router = APIRouter()

    @staticmethod
    def _response(data=None):
        """
        统一响应结果
        :param data: 内容
        :return: 统一响应结果
        """
        return ResponseModel(data=data)
