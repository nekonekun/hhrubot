from fastapi import APIRouter


default_router = APIRouter()


@default_router.get('/')
async def helloworld():
    return {'hello': 'world'}
