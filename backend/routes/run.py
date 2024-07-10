from fastapi import APIRouter
from fastapi import status


run = APIRouter()


@run.get("/")
async def check_app_status():
    return{
        "status_code": status.HTTP_200_OK,
        "detail": "App is running"
    }