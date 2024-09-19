from pydantic import BaseModel, Field
from typing import Optional
from datetime import time
from fastapi import APIRouter, HTTPException
from asgiref.sync import sync_to_async
from poolAPI.models import SettingsFilterSchedule3Model, PoolSetting
from enum import IntEnum


class PumpSpeedEnum(IntEnum):
    OFF = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    MAXIMUM = 4

class SettingsFilterSchedule3Schema(BaseModel):
    pool_setting: Optional[int] = Field(default=None)
    filterschedule3_enabled: bool = Field(default=False)
    filterschedule3_start_time: time = Field(default=time(0, 0))
    filterschedule3_stop_time: time = Field(default=time(0, 0))
    filterschedule3_monday: bool = Field(default=False)
    filterschedule3_tuesday: bool = Field(default=False)
    filterschedule3_wednesday: bool = Field(default=False)
    filterschedule3_thursday: bool = Field(default=False)
    filterschedule3_friday: bool = Field(default=False)
    filterschedule3_saturday: bool = Field(default=False)
    filterschedule3_sunday: bool = Field(default=False)
    filterschedule3_pump_speed: PumpSpeedEnum = Field(default=PumpSpeedEnum.OFF)

    class Config:
        from_attributes = True


router = APIRouter(
    prefix="/settings-filter_settings_three",
    tags=['Settings Filter Schedule 3 settings']
)


@router.post("/", response_model=SettingsFilterSchedule3Schema)
async def create_settings_filter_schedule_3(data: SettingsFilterSchedule3Schema):
    poolsetting_instance = None
    if data.pool_setting is not None:
        try:
            poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=data.pool_setting)
        except PoolSetting.DoesNotExist:
            raise HTTPException(status_code=404, detail="PoolSetting not found")

    new_setting = SettingsFilterSchedule3Model(
        poolsetting=poolsetting_instance,
        filterschedule3_enabled=data.filterschedule3_enabled,
        filterschedule3_start_time=data.filterschedule3_start_time,
        filterschedule3_stop_time=data.filterschedule3_stop_time,
        filterschedule3_monday=data.filterschedule3_monday,
        filterschedule3_tuesday=data.filterschedule3_tuesday,
        filterschedule3_wednesday=data.filterschedule3_wednesday,
        filterschedule3_thursday=data.filterschedule3_thursday,
        filterschedule3_friday=data.filterschedule3_friday,
        filterschedule3_saturday=data.filterschedule3_saturday,
        filterschedule3_sunday=data.filterschedule3_sunday,
        filterschedule3_pump_speed=data.filterschedule3_pump_speed
    )

    await sync_to_async(new_setting.save)()

    return new_setting


@router.get("/settings-filter-schedule-3/{poolsetting_id}", response_model=SettingsFilterSchedule3Schema)
async def get_settings_filter_schedule_3(poolsetting_id: int):
    try:
        poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=poolsetting_id)

        settings_filter_schedule_3_instance = await sync_to_async(SettingsFilterSchedule3Model.objects.get)(
            poolsetting=poolsetting_instance)

        return settings_filter_schedule_3_instance
    except PoolSetting.DoesNotExist:
        raise HTTPException(status_code=404, detail="PoolSetting not found")
    except SettingsFilterSchedule3Model.DoesNotExist:
        raise HTTPException(status_code=404, detail="SettingsFilterSchedule3Model not found")