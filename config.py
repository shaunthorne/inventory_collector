import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def resolve_ttp_path() -> str:
    """
    Resolve path to TTP templates directory.
    Priority:
    1. Environment variable TTP_TEMPLATE_DIR
    2. Local 'ttp/' directory
    3. Fallback to ~/shared_packages/ttp
    """
    env_path = os.environ.get("TTP_TEMPLATE_DIR")
    if env_path and Path(env_path).is_dir():
        return env_path

    local_path = Path(__file__).parent / "ttp"
    if local_path.is_dir():
        return str(local_path)

    fallback_path = Path.home() / "shared_packages" / "ttp"
    if fallback_path.is_dir():
        return str(fallback_path)

    raise FileNotFoundError("TTP template path not found.")

TTP_TEMPLATE_DIR = resolve_ttp_path()

TTP_MODEL_SPECIFIC_TEMPLATES = {
    'dlink_os': {
        'show util ports': {
            'DGS-1210': 'show_util_ports_1210.ttp',
        }
    }
}



SNMP_COMMUNITY = os.getenv("SNMP_COMMUNITY", "public")
SNMP_VERSION = int(os.getenv("SNMP_VERSION", 2))

# sysDescr signature matching
PLATFORM_SIGNATURES: dict[str, list[str]] = {
    "dlink_os": ["des-", "dgs-"],
    "snr_nos": ["s29", "switch device"],
    "tplink_os": ["omada", "jetstream"],
    "orion_nos": ["a28f"],
    "bdcom_os": ['baud data'],
    "cdata_os": ['cdata']
}

# scrapli dict
SCRAPLI_AUTH = {
    "auth_username": os.getenv("SCRAPLI_USERNAME", "admin"),
    "auth_password": os.getenv("SCRAPLI_PASSWORD", "admin"),
    "auth_strict_key": False,
    "transport": os.getenv("SCRAPLI_TRANSPORT", "telnet"),
    "timeout_socket": int(os.getenv("SCRAPLI_TIMEOUT", 30)),
}

DEFAULT_BASE_FIELDS = [
    "model",
    "mac_address",
    "serial_number",
    "hardware_version",
    "boot_version",
    "firmware_version",
]

PLATFORM_COMMAND_MAP = {
    "dlink_os": {
        "base_commands": [
            {
                "command": "show switch",
                "fields": DEFAULT_BASE_FIELDS,
            },
        ]
    },
    "snr_nos": {
        "base_commands": [
            {
                "command": "show version",
                "fields": DEFAULT_BASE_FIELDS,
            },
        ]
    },
    "tplink_os": {
        "base_commands": [
            {
                "command": "show system-info",
                "fields": DEFAULT_BASE_FIELDS,
            },
        ]
    }
}
