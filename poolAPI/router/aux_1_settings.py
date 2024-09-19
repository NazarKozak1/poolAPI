from enum import IntEnum
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from asgiref.sync import sync_to_async
from django.db.models import ObjectDoesNotExist
from poolAPI.models import SettingsAux1Model, PoolSetting
from datetime import time

router = APIRouter(
    prefix="/settings-aux1",
    tags=['Aux1 settings']
)

class Aux1NameEnum(IntEnum):
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

class Aux1Schema(BaseModel):
    pool_setting: Optional[int] = Field(default=None)
    aux1_regulation: bool
    aux1_activate: bool
    aux1_name: Aux1NameEnum
    aux1_flow: bool
    aux1_on_deck_closed: bool
    aux1_schedule: bool
    aux1_start_time: time
    aux1_stop_time: time
    aux1_monday: bool
    aux1_tuesday: bool
    aux1_wednesday: bool
    aux1_thursday: bool
    aux1_friday: bool
    aux1_saturday: bool
    aux1_sunday: bool

    class Config:
        use_enum_values = True
        from_attributes = True

@router.post("/", response_model=Aux1Schema)
async def create_settings_aux1(data: Aux1Schema):
    poolsetting_instance = None
    if data.pool_setting is not None:
        try:
            poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=data.pool_setting)
        except ObjectDoesNotExist:
            raise HTTPException(status_code=404, detail="PoolSetting not found")

    new_setting = SettingsAux1Model(
        poolsetting=poolsetting_instance,
        aux1_regulation=data.aux1_regulation,
        aux1_activate=data.aux1_activate,
        aux1_name=data.aux1_name,
        aux1_flow=data.aux1_flow,
        aux1_on_deck_closed=data.aux1_on_deck_closed,
        aux1_schedule=data.aux1_schedule,
        aux1_start_time=data.aux1_start_time,
        aux1_stop_time=data.aux1_stop_time,
        aux1_monday=data.aux1_monday,
        aux1_tuesday=data.aux1_tuesday,
        aux1_wednesday=data.aux1_wednesday,
        aux1_thursday=data.aux1_thursday,
        aux1_friday=data.aux1_friday,
        aux1_saturday=data.aux1_saturday,
        aux1_sunday=data.aux1_sunday
    )

    await sync_to_async(new_setting.save)()

    return new_setting

@router.get("/settings-aux1/{poolsetting_id}", response_model=Aux1Schema)
async def get_settings_aux1(poolsetting_id: int):
    try:
        poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=poolsetting_id)

        settings_aux1_instance = await sync_to_async(SettingsAux1Model.objects.get)(poolsetting=poolsetting_instance)

        return settings_aux1_instance
    except PoolSetting.DoesNotExist:
        raise HTTPException(status_code=404, detail="PoolSetting not found")
    except SettingsAux1Model.DoesNotExist:
        raise HTTPException(status_code=404, detail="SettingsAux1Model not found")