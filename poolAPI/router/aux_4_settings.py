from pydantic import BaseModel, Field
from typing import Optional
from datetime import time
from enum import IntEnum
from fastapi import APIRouter, HTTPException
from asgiref.sync import sync_to_async
from django.db.models import ObjectDoesNotExist
from poolAPI.models import SettingsAux4Model, PoolSetting

router = APIRouter(
    prefix="/settings-aux4",
    tags=['Aux4 settings']
)


class Aux4NameEnum(IntEnum):
    DESINFECTION_1 = 0
    DESINFECTION_2 = 1
    FOUNTAIN_1 = 2
    FOUNTAIN_2 = 3
    LIGHTING_1 = 4
    LIGHTING_2 = 5
    VALVE_1 = 6
    VALVE_2 = 7
    GARDEN_LIGHTING_1 = 8
    GARDEN_LIGHTING_2 = 9
    REVERSE_FLOW_MACHINE = 10
    DOMOTICA = 11
    GARDEN_FENCE = 12
    WINDOW_BLINDS = 13
    NONE = 14
    OTHER = 15

class Aux4Schema(BaseModel):
    pool_setting: Optional[int] = Field(default=None)
    aux4_regulation: bool
    aux4_activate: bool
    aux4_flow: bool
    aux4_schedule: bool
    aux4_start_time: time
    aux4_stop_time: time
    aux4_monday: bool
    aux4_tuesday: bool
    aux4_wednesday: bool
    aux4_thursday: bool
    aux4_friday: bool
    aux4_saturday: bool
    aux4_sunday: bool
    aux4_name: Aux4NameEnum
    aux4_on_deck_closed: bool

    class Config:
        use_enum_values = True
        from_attributes = True


@router.post("/", response_model=Aux4Schema)
async def create_settings_aux4(data: Aux4Schema):
    poolsetting_instance = None
    if data.pool_setting is not None:
        try:
            poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=data.pool_setting)
        except ObjectDoesNotExist:
            raise HTTPException(status_code=404, detail="PoolSetting not found")

    new_setting = SettingsAux4Model(
        poolsetting=poolsetting_instance,
        aux4_regulation=data.aux4_regulation,
        aux4_activate=data.aux4_activate,
        aux4_flow=data.aux4_flow,
        aux4_schedule=data.aux4_schedule,
        aux4_start_time=data.aux4_start_time,
        aux4_stop_time=data.aux4_stop_time,
        aux4_monday=data.aux4_monday,
        aux4_tuesday=data.aux4_tuesday,
        aux4_wednesday=data.aux4_wednesday,
        aux4_thursday=data.aux4_thursday,
        aux4_friday=data.aux4_friday,
        aux4_saturday=data.aux4_saturday,
        aux4_sunday=data.aux4_sunday,
        aux4_name=data.aux4_name,
        aux4_on_deck_closed=data.aux4_on_deck_closed
    )

    await sync_to_async(new_setting.save)()

    return new_setting


@router.get("/settings-aux4/{poolsetting_id}", response_model=Aux4Schema)
async def get_settings_aux4(poolsetting_id: int):
    try:
        poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=poolsetting_id)
        settings_aux4_instance = await sync_to_async(SettingsAux4Model.objects.get)(poolsetting=poolsetting_instance)
        return settings_aux4_instance
    except PoolSetting.DoesNotExist:
        raise HTTPException(status_code=404, detail="PoolSetting not found")
    except SettingsAux4Model.DoesNotExist:
        raise HTTPException(status_code=404, detail="SettingsAux4Model not found")