from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

default_router = APIRouter()


@default_router.get('/')
async def helloworld():
    return JSONResponse(content={'hello': 'world'}, status_code=status.HTTP_200_OK)
