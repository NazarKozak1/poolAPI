from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import time
from poolAPI.models import SettingsBackwashModel, PoolSetting
from asgiref.sync import sync_to_async
from django.db.models import ObjectDoesNotExist

router = APIRouter(
    prefix="/settings-backwash",
    tags=['Backwash settings']
)


class SettingsBackwashSchema(BaseModel):
    pool_setting: Optional[int]
    regulation: bool
    interval_period: bool
    pump_speed: int
    backwash_duration: int
    rinse_duration: int
    config_rinse: bool
    start: bool

    class Config:
        from_attributes = True


@router.post("/", response_model=SettingsBackwashSchema)
async def create_settings_backwash(data: SettingsBackwashSchema):
    poolsetting = None
    if data.pool_setting is not None:
        try:
            poolsetting = await sync_to_async(PoolSetting.objects.get)(id=data.pool_setting)
        except ObjectDoesNotExist:
            raise HTTPException(status_code=404, detail="PoolSetting not found")

    new_setting = SettingsBackwashModel(
        poolsetting=poolsetting,
        filterbackwash_regulation=data.regulation,
        filterbackwash_interval_period=data.interval_period,
        filterbackwash_pump_speed=data.pump_speed,
        filterbackwash_backwash_duration=data.backwash_duration,
        filterbackwash_rinse_duration=data.rinse_duration,
        filterbackwash_config_rinse=data.config_rinse,
        filterbackwash_start=data.start
    )

    await sync_to_async(new_setting.save)()

    response_data = {
        "pool_setting": new_setting.poolsetting_id,
        "regulation": new_setting.filterbackwash_regulation,
        "interval_period": new_setting.filterbackwash_interval_period,
        "pump_speed": new_setting.filterbackwash_pump_speed,
        "backwash_duration": new_setting.filterbackwash_backwash_duration,
        "rinse_duration": new_setting.filterbackwash_rinse_duration,
        "config_rinse": new_setting.filterbackwash_config_rinse,
        "start": new_setting.filterbackwash_start
    }

    return response_data


@router.get("/{id}", response_model=SettingsBackwashSchema)
async def get_settings_backwash(id: int):
    try:
        setting = await sync_to_async(SettingsBackwashModel.objects.get)(id=id)
    except ObjectDoesNotExist:
        raise HTTPException(status_code=404, detail="SettingsBackwashModel not found")

    response_data = {
        "pool_setting": setting.poolsetting_id,
        "regulation": setting.filterbackwash_regulation,
        "interval_period": setting.filterbackwash_interval_period,
        "pump_speed": setting.filterbackwash_pump_speed,
        "backwash_duration": setting.filterbackwash_backwash_duration,
        "rinse_duration": setting.filterbackwash_rinse_duration,
        "config_rinse": setting.filterbackwash_config_rinse,
        "start": setting.filterbackwash_start
    }

    return response_data