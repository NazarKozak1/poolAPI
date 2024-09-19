from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from poolAPI.models import SettingsTemperatureHeatingModel, PoolSetting
from enum import IntEnum


router = APIRouter(
    prefix="/settings-temperature-heating",
    tags=["Temperature Heating Settings"]
)



class PumpSpeedEnum(IntEnum):
    OFF = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    MAXIMUM = 4

class SettingsTemperatureHeatingSchema(BaseModel):
    poolsetting_id: int
    temperatureheating_regulation: bool
    temperatureheating_interval: int
    temperatureheating_priority: bool
    temperatureheating_cooling_period: int
    temperatureheating_pump_speed: PumpSpeedEnum
    temperature_frost_protection: bool

    class Config:
        orm_mode = True



@router.post("/", response_model=SettingsTemperatureHeatingSchema)
async def create_settings_temperature_heating(settings_data: SettingsTemperatureHeatingSchema):
    try:
        poolsetting = await sync_to_async(PoolSetting.objects.get)(id=settings_data.poolsetting_id)
    except ObjectDoesNotExist:
        raise HTTPException(status_code=404, detail="PoolSetting not found")

    new_setting = await sync_to_async(SettingsTemperatureHeatingModel.objects.create)(
        poolsetting=poolsetting,
        temperatureheating_regulation=settings_data.temperatureheating_regulation,
        temperatureheating_interval=settings_data.temperatureheating_interval,
        temperatureheating_priority=settings_data.temperatureheating_priority,
        temperatureheating_cooling_period=settings_data.temperatureheating_cooling_period,
        temperatureheating_pump_speed=settings_data.temperatureheating_pump_speed,
        temperature_frost_protection=settings_data.temperature_frost_protection
    )

    return new_setting



@router.get("/{poolsetting_id}", response_model=SettingsTemperatureHeatingSchema)
async def get_settings_temperature_heating(poolsetting_id: int):
    try:
        setting = await sync_to_async(SettingsTemperatureHeatingModel.objects.get)(poolsetting_id=poolsetting_id)
    except ObjectDoesNotExist:
        raise HTTPException(status_code=404, detail="SettingsTemperatureHeatingModel not found")

    return setting


