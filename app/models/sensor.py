from beanie import Document
from pydantic import Field
from datetime import datetime, timezone
from typing import Optional

class SensorData(Document):
  device_id: str = Field(..., description="Mac Address / ID unik dari ESP32")
  soil_adc: int = Field(..., description="Nilai mentah ADC dari sensor kelembapan tanah")
  moisture: float = Field(..., description="Persentase kelembapan tanah (%)")
  status: str = Field(..., description="Status kondisi tanah (misal: KERING, LEMBAB, BASAH)")
  ph_adc: int = Field(..., description="Nilai mentah ADC dari sensor pH")
  ph_voltage: float = Field(..., description="Tegangan output sensor pH (Volt)")
  ph: float = Field(..., description="Nilai pH tanah/air")
  temperature: float = Field(..., description="Suhu (°C)")
  created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

  class Settings:
    name = "sensor_data"  # Nama collection di MongoDB