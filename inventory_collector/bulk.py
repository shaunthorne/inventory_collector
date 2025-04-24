from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Tuple, Union

from inventory_collector.get_inventory import get_inventory
from inventory_collector.inventory.models import InventoryModel

def collect_inventory_bulk(
    targets: List[Dict[str, str]],
    concurrency: int = 5
) -> Dict[str, Tuple[Optional[InventoryModel], Optional[Union[str, Exception]]]]:
    """
    Collect inventory from multiple devices concurrently.

    Args:
        targets: List of dictionaries like {"ip": "1.2.3.4", "platform": "dlink_os"}
        concurrency: Number of threads for parallel execution

    Returns:
        Dictionary of results per IP: {ip: (inventory or None, error or None)}
    """
    results = {}

    def worker(target):
        ip = target.get("ip")
        platform = target.get("platform", None)
        try:
            inventory, err_or_cn = get_inventory(ip=ip, platform=platform)
            return ip, (inventory, err_or_cn if inventory is None else None)
        except Exception as e:
            return ip, (None, str(e))

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        future_to_ip = {executor.submit(worker, t): t.get("ip") for t in targets}
        for future in as_completed(future_to_ip):
            ip, result = future.result()
            results[ip] = result

    return results
