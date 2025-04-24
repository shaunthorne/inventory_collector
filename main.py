import argparse
from get_inventory import get_inventory

def main():
    parser = argparse.ArgumentParser(description="Collect inventory from a network device")
    parser.add_argument("--ip", required=True, help="Device IP address")
    parser.add_argument("--platform", required=False, help="Platform name (e.g. dlink_os)")
    parser.add_argument("--return-cn", action="store_true", help="Return connection object (debug mode)")
    args = parser.parse_args()

    inventory, err_or_cn = get_inventory(
        ip=args.ip,
        platform=args.platform,
        return_cn=args.return_cn
    )

    if inventory:
        print(inventory.model_dump_json(indent=2))
        pass
    else:
        print(f"ERROR: {err_or_cn}")

if __name__ == "__main__":
    main()
