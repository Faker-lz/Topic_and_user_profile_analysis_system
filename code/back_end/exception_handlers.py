"""
: 
@author: lingzhi
@time: 2021/7/19 17:21
"""
from exceptions import TokenException, NotExistException
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from models import RESTfulModel


def register_exception_handler(app: FastAPI):
    """
    app注册异常处理器
    """

    @app.exception_handler(TokenException)
    async def token_exc_handler(exc: TokenException):
        """
        处理Token认证错误
        :param exc:
        :return:
        """
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=RESTfulModel(code=-1,
                                 data=exc.msg).dict()
        )

    @app.exception_handler(NotExistException)
    async def not_exc_handler(request: Request, exc: NotExistException):
        """
        处理NotExistException
        :param request:
        :param exc:
        :return:
        """
        return JSONResponse(
            RESTfulModel(
                code=-1,
                data=exc.msg
            ).dict()
        )
