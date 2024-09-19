from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async
from datetime import datetime
from poolAPI.models import RealTimeMeasurement, PoolSetting


router = APIRouter(
    prefix="/real-time-measurement",
    tags=['real time measurement']
)

class RealTimeMeasurementSchema(BaseModel):
    poolsetting_id: int
    water_temperature: float
    ambient_temperature: float
    solar_temperature: float
    filterpump_current: float
    ph_actual: float
    rx_actual: float
    tds_ppm: int
    pollution_degree_ppm: int
    conductivity: float
    clm_ppm: float
    empty_tank: bool
    imx_temperature: float
    main_temperature: float
    date_time: datetime
    error: int

    class Config:
        orm_mode = True

@router.post("/", response_model=RealTimeMeasurementSchema)
async def create_real_time_measurement(data: RealTimeMeasurementSchema):
    try:
        poolsetting_instance = await sync_to_async(PoolSetting.objects.get)(id=data.poolsetting_id)
    except ObjectDoesNotExist:
        raise HTTPException(status_code=404, detail="PoolSetting not found")

    new_measurement = RealTimeMeasurement(
        poolsetting=poolsetting_instance,
        water_temperature=data.water_temperature,
        ambient_temperature=data.ambient_temperature,
        solar_temperature=data.solar_temperature,
        filterpump_current=data.filterpump_current,
        ph_actual=data.ph_actual,
        rx_actual=data.rx_actual,
        tds_ppm=data.tds_ppm,
        pollution_degree_ppm=data.pollution_degree_ppm,
        conductivity=data.conductivity,
        clm_ppm=data.clm_ppm,
        empty_tank=data.empty_tank,
        imx_temperature=data.imx_temperature,
        main_temperature=data.main_temperature,
        date_time=data.date_time,
        error=data.error
    )

    await sync_to_async(new_measurement.save)()

    return new_measurement


@router.get("/{poolsetting_id}", response_model=RealTimeMeasurementSchema)
async def get_real_time_measurement(poolsetting_id: int):
    try:
        measurement = await sync_to_async(RealTimeMeasurement.objects.get)(poolsetting_id=poolsetting_id)
    except ObjectDoesNotExist:
        raise HTTPException(status_code=404, detail="RealTimeMeasurement not found")

    return measurement