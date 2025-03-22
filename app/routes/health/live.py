from fastapi import APIRouter, Response

router = APIRouter(tags=["health"])


@router.get("")
async def health_check():
    return Response(status_code=200)
