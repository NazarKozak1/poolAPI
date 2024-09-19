from pydantic import BaseModel, Field
from typing import Optional
from fastapi import APIRouter, HTTPException
from asgiref.sync import sync_to_async
from poolAPI.models import SettingsDeckModel, PoolSetting

class SettingsDeckSchema(BaseModel):
    pool_setting: Optional[int] = Field(default=None)
    deck_open: bool = Field(default=False)
    deck_close: bool = Field(default=False)
    deck_stop: bool = Field(default=False)

    class Config:
        from_attributes = True


router = APIRouter(
    prefix="/settings-deck",
    tags=['deck settings']
)


@router.post("/", response_model=SettingsDeckSchema)
async def create_settings_deck(data: SettingsDeckSchema):
    poolsetting_instance = None
    if data.pool_setting is not None:
        try:
            poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=data.pool_setting)
        except PoolSetting.DoesNotExist:
            raise HTTPException(status_code=404, detail="PoolSetting not found")

    new_setting = SettingsDeckModel(
        poolsetting=poolsetting_instance,
        deck_open=data.deck_open,
        deck_close=data.deck_close,
        deck_stop=data.deck_stop
    )

    await sync_to_async(new_setting.save)()

    return new_setting


@router.get("/settings-deck/{poolsetting_id}", response_model=SettingsDeckSchema)
async def get_settings_deck(poolsetting_id: int):
    try:
        poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=poolsetting_id)

        settings_deck_instance = await sync_to_async(SettingsDeckModel.objects.get)(poolsetting=poolsetting_instance)

        return settings_deck_instance
    except PoolSetting.DoesNotExist:
        raise HTTPException(status_code=404, detail="PoolSetting not found")
    except SettingsDeckModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="SettingsDeckModel not found")