from pydantic import BaseModel, Field
from typing import Optional
from datetime import time
from fastapi import APIRouter, HTTPException
from asgiref.sync import sync_to_async
from poolAPI.models import SettingsFilterSchedule2Model, PoolSetting
from enum import IntEnum

class PumpSpeedEnum(IntEnum):
    OFF = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    MAXIMUM = 4


class SettingsFilterSchedule2Schema(BaseModel):
    pool_setting: Optional[int] = Field(default=None)
    filterschedule2_enabled: bool = Field(default=False)
    filterschedule2_start_time: time = Field(default=time(0, 0))
    filterschedule2_stop_time: time = Field(default=time(0, 0))
    filterschedule2_monday: bool = Field(default=False)
    filterschedule2_tuesday: bool = Field(default=False)
    filterschedule2_wednesday: bool = Field(default=False)
    filterschedule2_thursday: bool = Field(default=False)
    filterschedule2_friday: bool = Field(default=False)
    filterschedule2_saturday: bool = Field(default=False)
    filterschedule2_sunday: bool = Field(default=False)
    filterschedule2_pump_speed: PumpSpeedEnum = Field(default=PumpSpeedEnum.OFF)

    class Config:
        from_attributes = True


router = APIRouter(
    prefix="/settings-filter_settings_second",
    tags=['Settings Filter Schedule 2 settings']
)



@router.post("/", response_model=SettingsFilterSchedule2Schema)
async def create_settings_filter_schedule_2(data: SettingsFilterSchedule2Schema):
    poolsetting_instance = None
    if data.pool_setting is not None:
        try:
            poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=data.pool_setting)
        except PoolSetting.DoesNotExist:
            raise HTTPException(status_code=404, detail="PoolSetting not found")

    new_setting = SettingsFilterSchedule2Model(
        poolsetting=poolsetting_instance,
        filterschedule2_enabled=data.filterschedule2_enabled,
        filterschedule2_start_time=data.filterschedule2_start_time,
        filterschedule2_stop_time=data.filterschedule2_stop_time,
        filterschedule2_monday=data.filterschedule2_monday,
        filterschedule2_tuesday=data.filterschedule2_tuesday,
        filterschedule2_wednesday=data.filterschedule2_wednesday,
        filterschedule2_thursday=data.filterschedule2_thursday,
        filterschedule2_friday=data.filterschedule2_friday,
        filterschedule2_saturday=data.filterschedule2_saturday,
        filterschedule2_sunday=data.filterschedule2_sunday,
        filterschedule2_pump_speed=data.filterschedule2_pump_speed
    )

    await sync_to_async(new_setting.save)()

    return new_setting


@router.get("/settings-filter-schedule-2/{poolsetting_id}", response_model=SettingsFilterSchedule2Schema)
async def get_settings_filter_schedule_2(poolsetting_id: int):
    try:
        poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=poolsetting_id)

        settings_filter_schedule_2_instance = await sync_to_async(SettingsFilterSchedule2Model.objects.get)(
            poolsetting=poolsetting_instance)

        return settings_filter_schedule_2_instance
    except PoolSetting.DoesNotExist:
        raise HTTPException(status_code=404, detail="PoolSetting not found")
    except SettingsFilterSchedule2Model.DoesNotExist:
        raise HTTPException(status_code=404, detail="SettingsFilterSchedule2Model not found")
