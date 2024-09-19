from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import time
from poolAPI.models import SettingsLightingModel, PoolSetting
from asgiref.sync import sync_to_async
from django.db.models import ObjectDoesNotExist
from enum import Enum

router = APIRouter(
    prefix="/settings-lighting",
    tags=['lighting settings']
)

class LightingConfigurationEnum(int, Enum):
    SINGLE_COLOUR = 0
    ROTATING_RGB = 1
    STL_RGB = 2


class LightingColour(int, Enum):
    WHITE = 0
    RED = 1
    BLUE = 2
    GREEN = 3
    MAGENTA = 4
    CYAN = 5
    YELLOW = 6
    SEQ1 = 7
    SEQ2 = 8
    SEQ3 = 9
    SEQ4 = 10
    SEQ5 = 11
    DISCO1 = 12
    DISCO2 = 13

class SettingsLightingSchema(BaseModel):
    pool_setting: int
    lighting_regulation: bool
    lighting_active: bool
    lighting_schedule: bool
    lighting_start_time: time
    lighting_stop_time: time
    lighting_monday: bool
    lighting_tuesday: bool
    lighting_wednesday: bool
    lighting_thursday: bool
    lighting_friday: bool
    lighting_saturday: bool
    lighting_sunday: bool
    lighting_on_deck_closed: bool
    lighting_configuration: LightingConfigurationEnum
    lighting_colour_stl: LightingColour
    lighting_rgb_stl_time: int
    lighting_next_colour: bool

    class Config:
        from_attributes = True

@router.post("/", response_model=SettingsLightingSchema)
async def create_settings_lighting(data: SettingsLightingSchema):
    poolsetting = None
    if data.pool_setting is not None:
        try:
            poolsetting = await sync_to_async(PoolSetting.objects.get)(id=data.pool_setting)
        except ObjectDoesNotExist:
            raise HTTPException(status_code=404, detail="PoolSetting not found")

    new_setting = SettingsLightingModel(
        poolsetting=poolsetting,
        lighting_regulation=data.lighting_regulation,
        lighting_active=data.lighting_active,
        lighting_schedule=data.lighting_schedule,
        lighting_start_time=data.lighting_start_time,
        lighting_stop_time=data.lighting_stop_time,
        lighting_monday=data.lighting_monday,
        lighting_tuesday=data.lighting_tuesday,
        lighting_wednesday=data.lighting_wednesday,
        lighting_thursday=data.lighting_thursday,
        lighting_friday=data.lighting_friday,
        lighting_saturday=data.lighting_saturday,
        lighting_sunday=data.lighting_sunday,
        lighting_on_deck_closed=data.lighting_on_deck_closed,
        lighting_configuration=data.lighting_configuration,
        lighting_colour_stl=data.lighting_colour_stl,
        lighting_rgb_stl_time=data.lighting_rgb_stl_time,
        lighting_next_colour=data.lighting_next_colour
    )

    await sync_to_async(new_setting.save)()

    response_data = {
        "pool_setting": new_setting.poolsetting_id if new_setting.poolsetting else None,
        "lighting_regulation": new_setting.lighting_regulation,
        "lighting_active": new_setting.lighting_active,
        "lighting_schedule": new_setting.lighting_schedule,
        "lighting_start_time": new_setting.lighting_start_time,
        "lighting_stop_time": new_setting.lighting_stop_time,
        "lighting_monday": new_setting.lighting_monday,
        "lighting_tuesday": new_setting.lighting_tuesday,
        "lighting_wednesday": new_setting.lighting_wednesday,
        "lighting_thursday": new_setting.lighting_thursday,
        "lighting_friday": new_setting.lighting_friday,
        "lighting_saturday": new_setting.lighting_saturday,
        "lighting_sunday": new_setting.lighting_sunday,
        "lighting_on_deck_closed": new_setting.lighting_on_deck_closed,
        "lighting_configuration": new_setting.lighting_configuration,
        "lighting_colour_stl": new_setting.lighting_colour_stl,
        "lighting_rgb_stl_time": new_setting.lighting_rgb_stl_time,
        "lighting_next_colour": new_setting.lighting_next_colour
    }

    return response_data

    response_data = {
        "pool_number": new_setting.poolsetting.poolnumber if new_setting.poolsetting else None,
        "lighting_regulation": new_setting.lighting_regulation,
        "lighting_active": new_setting.lighting_active,
        "lighting_schedule": new_setting.lighting_schedule,
        "lighting_start_time": new_setting.lighting_start_time,
        "lighting_stop_time": new_setting.lighting_stop_time,
        "lighting_monday": new_setting.lighting_monday,
        "lighting_tuesday": new_setting.lighting_tuesday,
        "lighting_wednesday": new_setting.lighting_wednesday,
        "lighting_thursday": new_setting.lighting_thursday,
        "lighting_friday": new_setting.lighting_friday,
        "lighting_saturday": new_setting.lighting_saturday,
        "lighting_sunday": new_setting.lighting_sunday,
        "lighting_on_deck_closed": new_setting.lighting_on_deck_closed,
        "lighting_configuration": LightingConfigurationEnum(new_setting.lighting_configuration),
        "lighting_colour_stl": LightingColour(new_setting.lighting_colour_stl),
        "lighting_rgb_stl_time": new_setting.lighting_rgb_stl_time,
        "lighting_next_colour": new_setting.lighting_next_colour
    }

    return response_data


@router.get("/{settings_lighting_id}", response_model=SettingsLightingSchema)
async def get_settings_lighting(settings_lighting_id: int):
    try:
        setting = await sync_to_async(SettingsLightingModel.objects.get)(id=settings_lighting_id)
    except ObjectDoesNotExist:
        raise HTTPException(status_code=404, detail="SettingsLighting not found")

    response_data = {
        "pool_setting": setting.poolsetting_id,
        "lighting_regulation": setting.lighting_regulation,
        "lighting_active": setting.lighting_active,
        "lighting_schedule": setting.lighting_schedule,
        "lighting_start_time": setting.lighting_start_time,
        "lighting_stop_time": setting.lighting_stop_time,
        "lighting_monday": setting.lighting_monday,
        "lighting_tuesday": setting.lighting_tuesday,
        "lighting_wednesday": setting.lighting_wednesday,
        "lighting_thursday": setting.lighting_thursday,
        "lighting_friday": setting.lighting_friday,
        "lighting_saturday": setting.lighting_saturday,
        "lighting_sunday": setting.lighting_sunday,
        "lighting_on_deck_closed": setting.lighting_on_deck_closed,
        "lighting_configuration": setting.lighting_configuration,
        "lighting_colour_stl": setting.lighting_colour_stl,
        "lighting_rgb_stl_time": setting.lighting_rgb_stl_time,
        "lighting_next_colour": setting.lighting_next_colour
    }

    return response_data