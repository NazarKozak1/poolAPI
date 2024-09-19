from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from django.core.exceptions import ValidationError
from asgiref.sync import sync_to_async
from django.db.models import ObjectDoesNotExist
from poolAPI.models import SettingsGeneralModel, PoolSetting
from enum import Enum

router = APIRouter(
    prefix="/settings-general",
    tags=['General settings']
)

class OffContactEnum(Enum):
    OFF = 0
    NO = 1
    NC = 2

class AlarmEnum(Enum):
    NO = 0
    NC = 1

class PumpVolumeEnum(Enum):
    L15 = 0  # "1.5 l/h"
    L3 = 1   # "3 l/h"

class LanguageEnum(Enum):
    NEDERLANDS = 0
    ENGLISH = 1
    DEUTSCH = 2
    FRANCAIS = 3

class SettingsGeneralSchema(BaseModel):
    poolsetting_id: int = Field(...)
    general_pause: bool = Field(...)
    general_flow_alarm: bool = Field(...)
    general_offcontact: OffContactEnum = Field(...)
    general_alarm: AlarmEnum = Field(...)
    general_ph_rx_pump_volume: PumpVolumeEnum = Field(...)
    general_boot_delay: int = Field(..., ge=0, le=999)
    general_standby_time: int = Field(..., ge=0, le=999)
    general_language: LanguageEnum = Field(...)

    class Config:
        use_enum_values = True
        from_attributes = True

@router.post("/", response_model=SettingsGeneralSchema)
async def create_settings_general(data: SettingsGeneralSchema):
    poolsetting_instance = None
    if data.poolsetting_id is not None:
        try:
            poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=data.poolsetting_id)
        except ObjectDoesNotExist:
            raise HTTPException(status_code=404, detail="PoolSetting not found")

    new_setting = SettingsGeneralModel(
        poolsetting=poolsetting_instance,
        general_pause=data.general_pause,
        general_flow_alarm=data.general_flow_alarm,
        general_offcontact=data.general_offcontact,
        general_alarm=data.general_alarm,
        general_ph_rx_pump_volume=data.general_ph_rx_pump_volume,
        general_boot_delay=data.general_boot_delay,
        general_standby_time=data.general_standby_time,
        general_language=data.general_language
    )

    try:
        await sync_to_async(new_setting.save)()
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return new_setting

@router.get("/{poolsetting_id}", response_model=SettingsGeneralSchema)
async def get_settings_general(poolsetting_id: int):
    try:
        poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=poolsetting_id)
        settings_general_instance = await sync_to_async(SettingsGeneralModel.objects.get)(poolsetting=poolsetting_instance)
        return settings_general_instance
    except PoolSetting.DoesNotExist:
        raise HTTPException(status_code=404, detail="PoolSetting not found")
    except SettingsGeneralModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="SettingsGeneralModel not found")