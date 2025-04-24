from .base import CollectorBase
from .models import InventoryModel
from inventory_collector.config import PLATFORM_COMMAND_MAP

class GenericCollector(CollectorBase):
    def __init__(self, cn, ip: str, platform: str):
        super().__init__(cn, ip, platform)
        self._parsed_cache: dict[str, object] = {}

    def collect_inventory(self) -> InventoryModel:
        command_cfg = PLATFORM_COMMAND_MAP[self.platform].get("base_commands", [])
        
        for entry in command_cfg:
            command = entry["command"]
            fields = entry.get("fields", [])
            target = entry.get("target")

            data = self.parse(command)
            self._parsed_cache[command] = data

            if target:
                self.inventory[target] = data
                continue

            if isinstance(data, dict):
                for key in fields:
                    self.inventory[key] = data.get(key)
            elif fields:
                raise ValueError(f"Command '{command}' returned non-dict, cannot extract fields")

        self.after_base_inventory()
        return InventoryModel(**self.inventory)

    def after_base_inventory(self) -> None:
        pass
