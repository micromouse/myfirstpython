from typing import Optional

from pydantic import BaseModel, Field

from FastApi.FastApiBase import FastApiBase

class UserRequest(BaseModel):
    """
    用户请求模型
    """
    name: str = Field(..., description="用户姓名")
    age: int = Field(..., description="用户年龄", ge=18, le=60)
    address: Optional[str] = Field(None, description="用户地址(可选)")

class HomeFastApi(FastApiBase):
    """
    Home FastAPI
    """

    def __init__(self):
        """
        初始化Home FastAPI
        """
        super().__init__()
        self.router.add_api_route("/index", self.index, methods=["GET"])
        self.router.add_api_route("/addUser", self.addUser, methods=["POST"])

    def index(self):
        """
        index api
        :return: 结果
        """
        return self._response({"message": "welcome HomeFastApi"})

    def addUser(self, userRequest: UserRequest):
        """
        添加用户
        :param userRequest: 用户请求
        :return: 结果
        """
        print(f"已添加用户：{userRequest}")
        if userRequest.address is None:
            print("用户请求地址为None")
            raise Exception("用户请求地址不能为None")
        return self._response({"message": "added user"})
