# FastAPI 简单有应用
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

class UserRequest(BaseModel):
    """
    用户请求模型
    """
    name: str = Field(..., description="用户姓名")
    age: int = Field(..., description="用户年龄", ge=18, le=60)
    address: Optional[str] = Field(None, description="用户地址(可选)")

app = FastAPI()

@app.get("/index")
def index():
    """
    index api
    :return: 结果
    """
    return {"message": "Welcome FastAPI Nerds"}

@app.post("/addUser")
def addUser(userRequest: UserRequest):
    """
    添加用户
    :param userRequest: 用户请求
    :return: 结果
    """
    print(f"已添加用户：{userRequest}")
    if userRequest.address is None:
        print("用户请求地址为None")
    return {"message": "added user"}
