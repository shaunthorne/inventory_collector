from pydantic import BaseModel
from typing import Optional, List, Dict, Union

class InventoryModel(BaseModel):
    platform: str
    ip_address: str

    model: Optional[str] = None
    mac_address: Optional[str] = None
    serial_number: Optional[str] = None

    hardware_version: Optional[str] = None
    boot_version: Optional[str] = None
    firmware_version: Optional[str] = None