from fastapi import APIRouter, HTTPException
from asgiref.sync import sync_to_async
from poolAPI.models import SettingsRxModel, PoolSetting
from pydantic import BaseModel, Field
from typing import Optional


router = APIRouter(
    prefix="/settings-rx",
    tags=['rx settings']
)

class SettingsRxSchema(BaseModel):
    pool_setting: Optional[int] = Field(default=None)
    rx_value_target: float = Field(..., ge=0, le=999)
    rx_value_target_ppm: float = Field(..., ge=0, le=5)
    rx_dosing_time: int = Field(..., ge=0, le=3600)
    rx_pausing_time: int = Field(..., ge=0, le=999)
    rx_overdose_alert: int = Field(..., ge=0, le=65)
    rx_min_water_temp: float = Field(..., ge=0.0, le=99)

    class Config:
        from_attributes = True


@router.post("/", response_model=SettingsRxSchema)
async def create_settings_rx(data: SettingsRxSchema):
    poolsetting_instance = None
    if data.pool_setting is not None:
        try:
            poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=data.pool_setting)
        except PoolSetting.DoesNotExist:
            raise HTTPException(status_code=404, detail="PoolSetting not found")

    new_setting = SettingsRxModel(
        poolsetting=poolsetting_instance,
        rx_value_target=data.rx_value_target,
        rx_value_target_ppm=data.rx_value_target_ppm,
        rx_dosing_time=data.rx_dosing_time,
        rx_pausing_time=data.rx_pausing_time,
        rx_overdose_alert=data.rx_overdose_alert,
        rx_min_water_temp=data.rx_min_water_temp
    )

    await sync_to_async(new_setting.save)()

    return new_setting


@router.get("/settings-rx/{poolsetting_id}", response_model=SettingsRxSchema)
async def get_settings_rx(poolsetting_id: int):
    try:
        poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=poolsetting_id)
        settings_rx_instance = await sync_to_async(SettingsRxModel.objects.get)(poolsetting=poolsetting_instance)

        return settings_rx_instance
    except PoolSetting.DoesNotExist:
        raise HTTPException(status_code=404, detail="PoolSetting not found")
    except SettingsRxModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="SettingsRxModel not found")