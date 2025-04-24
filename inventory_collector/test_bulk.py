from inventory_collector.bulk import collect_inventory_bulk

targets = [{"ip": f"192.168.249.{i}"} for i in range(9, 101)]
results = collect_inventory_bulk(targets, concurrency=10)

for ip, (inv, err) in results.items():
    if inv:
        print(f"[+] {ip}: {inv.model or 'OK'}")
    else:
        print(f"[!] {ip}: ERROR: {err}")
