from pydantic import BaseModel, Field
from typing import Optional
from datetime import time
from enum import IntEnum
from fastapi import APIRouter, HTTPException
from asgiref.sync import sync_to_async
from django.db.models import ObjectDoesNotExist
from poolAPI.models import SettingsAux3Model, PoolSetting


router = APIRouter(
    prefix="/settings-aux3",
    tags=['Aux3 settings']
)


class Aux3NameEnum(IntEnum):
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

class Aux3Schema(BaseModel):
    pool_setting: Optional[int] = Field(default=None)
    aux3_regulation: bool
    aux3_activate: bool
    aux3_name: Aux3NameEnum
    aux3_flow: bool
    aux3_on_deck_closed: bool
    aux3_schedule: bool
    aux3_start_time: time
    aux3_stop_time: time
    aux3_monday: bool
    aux3_tuesday: bool
    aux3_wednesday: bool
    aux3_thursday: bool
    aux3_friday: bool
    aux3_saturday: bool
    aux3_sunday: bool

    class Config:
        use_enum_values = True
        from_attributes = True


@router.post("/", response_model=Aux3Schema)
async def create_settings_aux3(data: Aux3Schema):
    poolsetting_instance = None
    if data.pool_setting is not None:
        try:
            poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=data.pool_setting)
        except ObjectDoesNotExist:
            raise HTTPException(status_code=404, detail="PoolSetting not found")

    new_setting = SettingsAux3Model(
        poolsetting=poolsetting_instance,
        aux3_regulation=data.aux3_regulation,
        aux3_activate=data.aux3_activate,
        aux3_name=data.aux3_name,
        aux3_flow=data.aux3_flow,
        aux3_on_deck_closed=data.aux3_on_deck_closed,
        aux3_schedule=data.aux3_schedule,
        aux3_start_time=data.aux3_start_time,
        aux3_stop_time=data.aux3_stop_time,
        aux3_monday=data.aux3_monday,
        aux3_tuesday=data.aux3_tuesday,
        aux3_wednesday=data.aux3_wednesday,
        aux3_thursday=data.aux3_thursday,
        aux3_friday=data.aux3_friday,
        aux3_saturday=data.aux3_saturday,
        aux3_sunday=data.aux3_sunday
    )

    await sync_to_async(new_setting.save)()

    return new_setting


@router.get("/settings-aux3/{poolsetting_id}", response_model=Aux3Schema)
async def get_settings_aux3(poolsetting_id: int):
    try:
        poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=poolsetting_id)
        settings_aux3_instance = await sync_to_async(SettingsAux3Model.objects.get)(poolsetting=poolsetting_instance)
        return settings_aux3_instance
    except PoolSetting.DoesNotExist:
        raise HTTPException(status_code=404, detail="PoolSetting not found")
    except SettingsAux3Model.DoesNotExist:
        raise HTTPException(status_code=404, detail="SettingsAux3Model not found")