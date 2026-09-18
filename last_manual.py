#!/usr/bin/env python3
import platform, os, subprocess

print("=== THE LAST MANUAL ===")
alerts = 0

# 1. Hostname
host = platform.node()
print(f"\n[🔍] Hostname: {host} [✔]")

# 2. Rutas Críticas
print("\n[📂] Rutas Críticas:")
for p in ["/etc/passwd", "/etc/ssh/sshd_config"]:
    ok = os.path.exists(p)
    print(f"  [{'✔' if ok else '!'}] {p}")
    if not ok: alerts += 1

# 3. Servicios (ssh y NetworkManager)
print("\n[⚙️] Servicios:")
for s in ["ssh", "NetworkManager"]:
    res = subprocess.run(["systemctl", "is-active", s], capture_output=True, text=True)
    state = res.stdout.strip()
    print(f"  [{'✔' if state == 'active' else '!'}] {s}: {state}")
    if state != "active": alerts += 1

# 4. Usuarios con shell
print("\n[👤] Usuarios:")
with open("/etc/passwd") as f:
    for line in f:
        parts = line.strip().split(":")
        if len(parts) >= 7 and "sh" in parts[6]:
            print(f"  - {parts[0]} ({parts[6]})")

# Resumen
print(f"\n[RESULTADO] Alertas detectadas: {alerts}")
