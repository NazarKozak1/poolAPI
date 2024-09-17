from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import time
from poolAPI.models import SettingsPhModel, PoolSetting
from asgiref.sync import sync_to_async
from django.db.models import ObjectDoesNotExist

router = APIRouter(
    prefix="/settings-pH",
    tags=['pH settings']
)

class SettingsPhSchema(BaseModel):
    pool_setting: Optional[int] = Field(default=None)
    ph_value_target: float = Field(..., ge=4, le=9)
    ph_dosing_time: int = Field(..., ge=0, le=3600)
    ph_pausing_time: int = Field(..., ge=0, le=1440)
    ph_dosing_choice: int = Field(...)
    ph_overdose_alert: int = Field(..., ge=0, le=65)
    ph_hysteresis: float = Field(..., ge=0, le=1)


    class Config:
        from_attributes = True


@router.post("/", response_model=SettingsPhSchema)
async def create_settings_ph(data: SettingsPhSchema):

    poolsetting_instance = None
    if data.poolsetting is not None:
        try:
            poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=data.poolsetting)
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