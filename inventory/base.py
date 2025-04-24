from abc import ABC, abstractmethod
from typing import Any
from pathlib import Path

from config import TTP_TEMPLATE_DIR, TTP_MODEL_SPECIFIC_TEMPLATES
from .models import InventoryModel

class CollectorBase(ABC):
    def __init__(self, cn: Any, ip: str, platform: str):
        self.cn = cn
        self.ip = ip
        self.platform = platform
        self.inventory = {
            "platform": platform,
            "ip_address": ip,
            "model": None,
            "mac_address": None,
            "serial_number": None,
            "hardware_version": None,
            "boot_version": None,
            "firmware_version": None,
        }

    @abstractmethod
    def collect_inventory(self) -> InventoryModel:
        pass

    def parse(self, command: str, timeout: int = 30) -> dict:
        """
        Run CLI command and parse output using TTP.
        """
        try:
            result = self.cn.send_command(command, timeout_ops=timeout)
            template_path = self.get_template_path(command)
            parsed = result.ttp_parse_output(template_path)
            
            return parsed[0][0] if parsed and parsed[0] else {}
        except Exception as e:
            print(str(e))
            return {}

    def get_template_path(self, command: str) -> str:
        """
        Select appropriate TTP template based on platform and model (if needed).
        """
        override = TTP_MODEL_SPECIFIC_TEMPLATES.get(self.platform, {}).get(command)
        model = self.inventory.get("model", "")

        if isinstance(override, dict):
            for keyword, template in override.items():
                if keyword.lower() in model.lower():
                    return str(Path(TTP_TEMPLATE_DIR) / self.platform / template)

        return str(Path(TTP_TEMPLATE_DIR) / self.platform / f"{command.replace(' ', '_')}.ttp")
