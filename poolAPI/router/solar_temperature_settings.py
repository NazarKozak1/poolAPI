from pydantic import BaseModel, Field
from typing import Optional
from fastapi import APIRouter, HTTPException
from asgiref.sync import sync_to_async
from poolAPI.models import SettingsTemperatureSolarModel, PoolSetting


class SettingsTemperatureSolarSchema(BaseModel):
    pool_setting: Optional[int] = Field(default=None)
    temperaturesolar_regulation: bool = Field(default=False)
    temperaturesolar_temperature_offset: float = Field(..., ge=0, le=999)
    temperaturesolar_pump_speed: int = Field(..., ge=0, le=4)
    temperaturesolar_sp_too_high: float = Field(..., ge=0, le=999)
    temperaturesolar_sp_high: float = Field(..., ge=0, le=999)

    class Config:
        from_attributes = True


router = APIRouter(
    prefix="/settings-solar-temperature",
    tags=['solar temperature settings']
)

@router.post("/", response_model=SettingsTemperatureSolarSchema)
async def create_settings_temperature_solar(data: SettingsTemperatureSolarSchema):
    poolsetting_instance = None
    if data.pool_setting is not None:
        try:
            poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=data.pool_setting)
        except PoolSetting.DoesNotExist:
            raise HTTPException(status_code=404, detail="PoolSetting not found")

    new_setting = SettingsTemperatureSolarModel(
        poolsetting=poolsetting_instance,
        temperaturesolar_regulation=data.temperaturesolar_regulation,
        temperaturesolar_temperature_offset=data.temperaturesolar_temperature_offset,
        temperaturesolar_pump_speed=data.temperaturesolar_pump_speed,
        temperaturesolar_sp_too_high=data.temperaturesolar_sp_too_high,
        temperaturesolar_sp_high=data.temperaturesolar_sp_high
    )

    await sync_to_async(new_setting.save)()

    return new_setting


@router.get("/settings-temperature-solar/{poolsetting_id}", response_model=SettingsTemperatureSolarSchema)
async def get_settings_temperature_solar(poolsetting_id: int):
    try:
        poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=poolsetting_id)

        settings_temperature_solar_instance = await sync_to_async(SettingsTemperatureSolarModel.objects.get)(
            poolsetting=poolsetting_instance)

        return settings_temperature_solar_instance
    except PoolSetting.DoesNotExist:
        raise HTTPException(status_code=404, detail="PoolSetting not found")
    except SettingsTemperatureSolarModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="SettingsTemperatureSolarModel not found")