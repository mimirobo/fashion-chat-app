from fastapi import APIRouter

router = APIRouter()


@router.get("", tags=["health"])
async def check_health():
    return {"status": "OK"}
