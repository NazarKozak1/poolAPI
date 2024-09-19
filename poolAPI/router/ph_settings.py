from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import time
from poolAPI.models import SettingsPhModel, PoolSetting
from asgiref.sync import sync_to_async
from django.db.models import ObjectDoesNotExist
from enum import Enum


router = APIRouter(
    prefix="/settings-pH",
    tags=['pH settings']
)

class PhDosingChoiceEnum(Enum):
    PH_PLUS = 0  # "pH+"
    PH_MINUS = 1  # "pH-"
    PH_BOTH = 2  # "pH+ & pH-"


class SettingsPhSchema(BaseModel):
    pool_setting: Optional[int] = Field(default=None)
    ph_value_target: float = Field(..., ge=4, le=9)
    ph_dosing_time: int = Field(..., ge=0, le=3600)
    ph_pausing_time: int = Field(..., ge=0, le=1440)
    ph_dosing_choice: PhDosingChoiceEnum = Field(...)
    ph_overdose_alert: int = Field(..., ge=0, le=65)
    ph_hysteresis: float = Field(..., ge=0, le=1)

    class Config:
        use_enum_values = True
        from_attributes = True

@router.post("/", response_model=SettingsPhSchema)
async def create_settings_ph(data: SettingsPhSchema):
    poolsetting_instance = None
    if data.pool_setting is not None:
        try:
            poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=data.pool_setting)
        except ObjectDoesNotExist:
            raise HTTPException(status_code=404, detail="PoolSetting not found")

    new_setting = SettingsPhModel(
        poolsetting=poolsetting_instance,
        ph_value_target=data.ph_value_target,
        ph_dosing_time=data.ph_dosing_time,
        ph_pausing_time=data.ph_pausing_time,
        ph_dosing_choice=data.ph_dosing_choice,
        ph_overdose_alert=data.ph_overdose_alert,
        ph_hysteresis=data.ph_hysteresis
    )

    await sync_to_async(new_setting.save)()

    return new_setting


@router.get("/settings-ph/{poolsetting_id}", response_model=SettingsPhSchema)
async def get_settings_ph(poolsetting_id: int):
    try:
        poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=poolsetting_id)

        settings_ph_instance = await sync_to_async(SettingsPhModel.objects.get)(poolsetting=poolsetting_instance)

        return settings_ph_instance
    except PoolSetting.DoesNotExist:
        raise HTTPException(status_code=404, detail="PoolSetting not found")
    except SettingsPhModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="SettingsPhModel not found")
