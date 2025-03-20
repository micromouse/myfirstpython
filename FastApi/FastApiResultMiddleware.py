# FastApi api结果中间件
import json

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response

class FastApiResultMiddleware(BaseHTTPMiddleware):
    """
    FastAPI api结果中间件
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        发送请求
        :param request: 请求
        :param call_next: 下一个调用
        :return: 响应结果
        """
        try:
            # 处理请求并获得响应
            response = await call_next(request)
            return response
        except Exception as e:
            # 捕获所有异常并返回统一格式的错误响应
            return JSONResponse(
                status_code=500,
                content={
                    "code": 500,
                    "data": {},
                    "message": str(e)  # 异常消息
                }
            )
