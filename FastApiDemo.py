# FastAPI 简单有应用
import uvicorn
from fastapi import FastAPI

from FastApi.FastApiResultMiddleware import FastApiResultMiddleware
from FastApi.RouterRegistrar import RouterRegistrar

app = FastAPI()

# noinspection PyTypeChecker
# 添加统一Api结果中间件
app.add_middleware(FastApiResultMiddleware)

# 动态注册路由
RouterRegistrar(app, "FastApi").registerRouters()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
