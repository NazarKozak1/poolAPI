from pydantic import BaseModel, Field
from typing import Optional
from datetime import time
from fastapi import APIRouter, HTTPException
from asgiref.sync import sync_to_async
from poolAPI.models import SettingsFilterSchedule1Model, PoolSetting
from enum import IntEnum

class PumpSpeedEnum(IntEnum):
    OFF = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    MAXIMUM = 4

class SettingsFilterSchedule1Schema(BaseModel):
    pool_setting: Optional[int] = Field(default=None)
    filterschedule1_enabled: bool = Field(default=False)
    filterschedule1_start_time: time = Field(default=time(0, 0))  # Assuming default is midnight
    filterschedule1_stop_time: time = Field(default=time(0, 0))   # Assuming default is midnight
    filterschedule1_monday: bool = Field(default=False)
    filterschedule1_tuesday: bool = Field(default=False)
    filterschedule1_wednesday: bool = Field(default=False)
    filterschedule1_thursday: bool = Field(default=False)
    filterschedule1_friday: bool = Field(default=False)
    filterschedule1_saturday: bool = Field(default=False)
    filterschedule1_sunday: bool = Field(default=False)
    filterschedule1_pump_speed: PumpSpeedEnum = Field(default=PumpSpeedEnum.OFF)

    class Config:
        from_attributes = True


router = APIRouter(
    prefix="/settings-filter_settings_first",
    tags=['Settings Filter Schedule 1 settings']
)


@router.post("/", response_model=SettingsFilterSchedule1Schema)
async def create_settings_filter_schedule_1(data: SettingsFilterSchedule1Schema):
    poolsetting_instance = None
    if data.pool_setting is not None:
        try:
            poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=data.pool_setting)
        except PoolSetting.DoesNotExist:
            raise HTTPException(status_code=404, detail="PoolSetting not found")

    new_setting = SettingsFilterSchedule1Model(
        poolsetting=poolsetting_instance,
        filterschedule1_enabled=data.filterschedule1_enabled,
        filterschedule1_start_time=data.filterschedule1_start_time,
        filterschedule1_stop_time=data.filterschedule1_stop_time,
        filterschedule1_monday=data.filterschedule1_monday,
        filterschedule1_tuesday=data.filterschedule1_tuesday,
        filterschedule1_wednesday=data.filterschedule1_wednesday,
        filterschedule1_thursday=data.filterschedule1_thursday,
        filterschedule1_friday=data.filterschedule1_friday,
        filterschedule1_saturday=data.filterschedule1_saturday,
        filterschedule1_sunday=data.filterschedule1_sunday,
        filterschedule1_pump_speed=data.filterschedule1_pump_speed
    )

    await sync_to_async(new_setting.save)()

    return new_setting


@router.get("/settings-filter-schedule-1/{poolsetting_id}", response_model=SettingsFilterSchedule1Schema)
async def get_settings_filter_schedule_1(poolsetting_id: int):
    try:
        poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=poolsetting_id)

        settings_filter_schedule_1_instance = await sync_to_async(SettingsFilterSchedule1Model.objects.get)(
            poolsetting=poolsetting_instance)

        return settings_filter_schedule_1_instance
    except PoolSetting.DoesNotExist:
        raise HTTPException(status_code=404, detail="PoolSetting not found")
    except SettingsFilterSchedule1Model.DoesNotExist:
        raise HTTPException(status_code=404, detail="SettingsFilterSchedule1Model not found")