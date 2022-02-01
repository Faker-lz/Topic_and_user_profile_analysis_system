"""
:话题演变api
@author: lingzhi
* @date 2021/7/23 15:15
"""

from fastapi import APIRouter
from models.dto.restful_model import RESTfulModel

evolve_router = APIRouter(tags=['话题演变api'])

@evolve_router.get('/test')

def test():
    return RESTfulModel(code=0, data='success')

