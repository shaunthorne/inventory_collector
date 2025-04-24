from scrapli import Scrapli
from scrapli.exceptions import (
    ScrapliAuthenticationFailed,
    ScrapliConnectionNotOpened,
    ScrapliConnectionError,
    ScrapliTimeout,
)
from scrapli.logging import enable_basic_logging
from inventory.models import InventoryModel
from inventory.base import CollectorBase
from typing import Optional, Tuple, Union, Type
from easysnmp import Session
from config import SNMP_COMMUNITY, SNMP_VERSION, SCRAPLI_AUTH, PLATFORM_SIGNATURES

# Supported collectors
from inventory.generic import GenericCollector

# enable_basic_logging('scrapli.log', level='DEBUG')

PLATFORM_MAP = {
    "dlink_os": GenericCollector,
    "tplink_os": GenericCollector,
    "snr_nos": GenericCollector,
}


def get_sysdescr(ip: str, community: str = "public", version: int = 2, timeout: int = 2) -> Optional[str]:
    try:
        session = Session(hostname=ip, community=SNMP_COMMUNITY, version=SNMP_VERSION, timeout=timeout)
        return session.get(".1.3.6.1.2.1.1.1.0").value
    except Exception:
        return None


def detect_platform(sysdescr: str) -> Optional[str]:
    sysdescr = sysdescr.lower()
    for platform, sigs in PLATFORM_SIGNATURES.items():
        if any(sig in sysdescr for sig in sigs):
            return platform
    return None


def get_inventory(
    ip: str,
    platform: Optional[str] = None,
    return_cn: bool = False,
    check_snmp: bool = True
) -> Tuple[Optional[InventoryModel], Union[str, None]]:
    if check_snmp:
        sysdescr = get_sysdescr(ip)
        if not sysdescr:
            return None, "no snmp"
        detected = detect_platform(sysdescr)
        if not detected:
            return None, f"unsupported platform: {sysdescr[:50]}"
        platform = detected

    if not platform:
        return None, "platform not specified"

    collector_class = PLATFORM_MAP.get(platform)
    if not collector_class:
        return None, f"unsupported platform: {platform}"

    try:
        cn = Scrapli(host=ip, platform=platform, **SCRAPLI_AUTH)
        cn.open()
        collector = collector_class(cn, ip, platform)
        inventory = collector.collect_inventory()
        if return_cn:
            return inventory, cn
        else:
            cn.close()
            return inventory, None

    except ScrapliAuthenticationFailed:
        return None, "auth failed"
    except ScrapliConnectionNotOpened:
        return None, "connection not opened"
    except ScrapliConnectionError:
        return None, "connection error"
    except ScrapliTimeout:
        return None, "connection timed out"
    except BrokenPipeError:
        return None, "communication channel failure"
    except Exception as e:
        return None, str(e).strip()
