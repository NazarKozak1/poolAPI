from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from asgiref.sync import sync_to_async
from poolAPI.models import StatusModel, PoolSetting

router = APIRouter(
    prefix="/status",
    tags=['Status']
)

class StatusCreate(BaseModel):
    poolsetting_id: int
    cover: int
    cover_error: int
    filter: int
    temperature: int
    lighting: int
    waterheight: int
    aux1: int
    aux2: int
    aux3: int
    aux4: int
    ph: int
    rx: int
    clm: int
    t_water: int
    t_ambient: int
    t_solar: int
    level: int
    tds: int
    empty: int
    pump: int
    pumpspeed: int
    backwash: int
    flow: int
    datetime: datetime



@router.post("/status/", response_model=StatusCreate)
async def create_status(status: StatusCreate):
    poolsetting = await sync_to_async(PoolSetting.objects.get)(id=status.poolsetting_id)
    new_status = await sync_to_async(StatusModel.objects.create)(
        poolsetting=poolsetting,
        cover=status.cover,
        cover_error=status.cover_error,
        filter=status.filter,
        temperature=status.temperature,
        lighting=status.lighting,
        waterheight=status.waterheight,
        aux1=status.aux1,
        aux2=status.aux2,
        aux3=status.aux3,
        aux4=status.aux4,
        ph=status.ph,
        rx=status.rx,
        clm=status.clm,
        t_water=status.t_water,
        t_ambient=status.t_ambient,
        t_solar=status.t_solar,
        level=status.level,
        tds=status.tds,
        empty=status.empty,
        pump=status.pump,
        pumpspeed=status.pumpspeed,
        backwash=status.backwash,
        flow=status.flow,
        datetime=status.datetime
    )
    return new_status


from django.core.exceptions import ObjectDoesNotExist

@router.get("/status/{poolsetting_id}", response_model=StatusCreate)
async def get_status(poolsetting_id: int):
    try:
        status = await sync_to_async(StatusModel.objects.get)(poolsetting_id=poolsetting_id)
    except ObjectDoesNotExist:
        raise HTTPException(status_code=404, detail="StatusModel not found")

    return status