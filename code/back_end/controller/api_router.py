
from fastapi import APIRouter
from . import(
    tag_test_controller,
    tag_controller,
    tag_retweet_controller,
    tag_evolve_controller,
    tag_comment_controller
)

api_router = APIRouter()

api_router.include_router(tag_test_controller.test_router, prefix='/test')
api_router.include_router(tag_controller.tag_router, prefix='/tag')
api_router.include_router(tag_retweet_controller.retweet, prefix='/tag/retweet')
api_router.include_router(tag_evolve_controller.evolve_router, prefix='/tag/evolve')
api_router.include_router(tag_comment_controller.comment_router, prefix='/tag/comment')
