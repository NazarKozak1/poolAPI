from pydantic import BaseModel, Field
from typing import Optional
from datetime import time
from enum import IntEnum
from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import time
from asgiref.sync import sync_to_async
from django.db.models import ObjectDoesNotExist
from poolAPI.models import SettingsAux2Model, PoolSetting

router = APIRouter(
    prefix="/settings-aux2",
    tags=['Aux2 settings']
)


class Aux2NameEnum(IntEnum):
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

class Aux2Schema(BaseModel):
    pool_setting: Optional[int] = Field(default=None)
    aux2_regulation: bool
    aux2_activate: bool
    aux2_name: Aux2NameEnum
    aux2_flow: bool
    aux2_on_deck_closed: bool
    aux2_schedule: bool
    aux2_start_time: time
    aux2_stop_time: time
    aux2_monday: bool
    aux2_tuesday: bool
    aux2_wednesday: bool
    aux2_thursday: bool
    aux2_friday: bool
    aux2_saturday: bool
    aux2_sunday: bool

    class Config:
        use_enum_values = True
        from_attributes = True


@router.post("/", response_model=Aux2Schema)
async def create_settings_aux2(data: Aux2Schema):
    poolsetting_instance = None
    if data.pool_setting is not None:
        try:
            poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=data.pool_setting)
        except ObjectDoesNotExist:
            raise HTTPException(status_code=404, detail="PoolSetting not found")

    new_setting = SettingsAux2Model(
        poolsetting=poolsetting_instance,
        aux2_regulation=data.aux2_regulation,
        aux2_activate=data.aux2_activate,
        aux2_name=data.aux2_name,
        aux2_flow=data.aux2_flow,
        aux2_on_deck_closed=data.aux2_on_deck_closed,
        aux2_schedule=data.aux2_schedule,
        aux2_start_time=data.aux2_start_time,
        aux2_stop_time=data.aux2_stop_time,
        aux2_monday=data.aux2_monday,
        aux2_tuesday=data.aux2_tuesday,
        aux2_wednesday=data.aux2_wednesday,
        aux2_thursday=data.aux2_thursday,
        aux2_friday=data.aux2_friday,
        aux2_saturday=data.aux2_saturday,
        aux2_sunday=data.aux2_sunday
    )

    await sync_to_async(new_setting.save)()

    return new_setting


@router.get("/settings-aux2/{poolsetting_id}", response_model=Aux2Schema)
async def get_settings_aux2(poolsetting_id: int):
    try:
        poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=poolsetting_id)
        settings_aux2_instance = await sync_to_async(SettingsAux2Model.objects.get)(poolsetting=poolsetting_instance)
        return settings_aux2_instance
    except PoolSetting.DoesNotExist:
        raise HTTPException(status_code=404, detail="PoolSetting not found")
    except SettingsAux2Model.DoesNotExist:
        raise HTTPException(status_code=404, detail="SettingsAux2Model not found")