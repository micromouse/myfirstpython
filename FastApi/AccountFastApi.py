from uuid import UUID

from fastapi import APIRouter

from FastApi.FastApiBase import FastApiBase

class AccountFastApi(FastApiBase):
    """
    账户FastApi
    """
    router = APIRouter()

    @staticmethod
    @router.get("/getAccount")
    def getAccount(accountId: UUID):
        """
        由账户Id获得账户信息
        :return:
        """
        return FastApiBase._response({"AccountId": accountId})
