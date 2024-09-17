from fastapi import APIRouter

router = APIRouter(
    tags=['test']
)

@router.get("/status")
async def status():
    return {"status": "FastAPI is working!"}