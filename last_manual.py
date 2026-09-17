#!/usr/bin/env python3
import platform, os

print("=== THE LAST MANUAL ===")

# 1. Cargar datos del manual.yaml de forma directa
exp_host, paths = "", []
if os.path.exists("manual.yaml"):
    with open("manual.yaml", encoding="utf-8") as f:
        for line in f:
            if "expected_hostname:" in line:
                exp_host = line.split(":")[1].strip().strip('"\'')
            elif line.startswith("- path:"):
                paths.append(line.split(":")[1].strip().strip('"\''))

# 2. Reconciliación de Hostname
real_host = platform.node()
match = "✔" if real_host == exp_host else "!"
print(f"\n[🔍] Hostname: Real ({real_host}) vs Esperado ({exp_host}) [{match}]")

# 3. Auditoría de Rutas Críticas
print("\n[📂] Rutas Críticas:")
for p in paths:
    status = "✔" if os.path.exists(p) else "!"
    print(f"  [{status}] {p}")

# 4. Auditoría rápida de Usuarios (con shell interactiva)
print("\n[👤] Usuarios del Sistema:")
with open("/etc/passwd") as f:
    for line in f:
        parts = line.strip().split(":")
        if len(parts) >= 7 and "sh" in parts[6]:
            print(f"  - {parts[0]} ({parts[6]})")
