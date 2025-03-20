# FastAPI 简单有应用
import os

from fastapi import FastAPI
from FastApi.FastApiResultMiddleware import FastApiResultMiddleware
from FastApi.RouterRegistrar import RouterRegistrar

app = FastAPI()

# noinspection PyTypeChecker
# 添加统一Api结果中间件
app.add_middleware(FastApiResultMiddleware)

# 动态注册路由
apiDirectory = os.path.join(os.path.dirname(__file__), "FastApi")
RouterRegistrar(app, apiDirectory).registerRouters()
