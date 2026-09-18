#!/usr/bin/env python3
import platform, os, subprocess

print("=== THE LAST MANUAL ===")
print("[*] Iniciando reconciliación de estado (KNOWN vs UNKNOWN)...\n")

# 1. Leer manual.yaml de forma nativa y limpia
exp_host = ""
paths = []
services = []

if os.path.exists("manual.yaml"):
    current_section = ""
    with open("manual.yaml", encoding="utf-8") as f:
        for line in f:
            line_s = line.strip()
            if not line_s or line_s.startswith("#"):
                continue
            
            # Detectar secciones
            if "expected_hostname:" in line_s:
                exp_host = line_s.split(":")[1].strip().strip('"\'')
            elif "services:" in line_s:
                current_section = "services"
            elif "critical_paths:" in line_s:
                current_section = "critical_paths"
            
            # Extraer elementos según la sección
            if current_section == "services" and "- name:" in line_s:
                svc = line_s.split(":")[1].strip().strip('"\'')
                services.append(svc)
            elif current_section == "critical_paths" and "- path:" in line_s:
                p = line_s.split(":")[1].strip().strip('"\'')
                paths.append(p)
else:
    print("[!] Error crítico: No se encontró el archivo 'manual.yaml'.")
    exit(1)

alerts = 0

# 2. Reconciliación real de Hostname
real_host = platform.node()
print("[🔍] Reconciliación de Hostname:")
print(f"  - Documentado (KNOWN): {exp_host}")
print(f"  - Real (UNKNOWN):      {real_host}")
if real_host == exp_host:
    print("  [✔] Estado: CONFORME (KNOWN)\n")
else:
    print("  [!] Estado: DISCREPANCIA (REVIEW REQUIRED)\n")
    alerts += 1

# 3. Auditoría de Rutas Críticas basadas en manual.yaml
print("[📂] Auditoría de Rutas Críticas:")
for p in paths:
    if os.path.exists(p):
        print(f"  [✔] {p} -> Presente (KNOWN)")
    else:
        print(f"  [!] {p} -> No encontrada (REVIEW REQUIRED)")
        alerts += 1
print()

# 4. Auditoría de Servicios basada en manual.yaml
print("[⚙️] Auditoría de Servicios del Sistema:")
for s in services:
    try:
        res = subprocess.run(["systemctl", "is-active", s], capture_output=True, text=True, timeout=2)
        state = res.stdout.strip()
        if state == "active":
            print(f"  [✔] {s} -> Activo (KNOWN)")
        else:
            print(f"  [!] {s} -> Estado: {state} (REVIEW REQUIRED)")
            alerts += 1
    except Exception:
        print(f"  [!] {s} -> No se pudo verificar (REVIEW REQUIRED)")
        alerts += 1
print()

# 5. Auditoría robusta de Usuarios Interactivos usando /etc/shells
valid_shells = set()
if os.path.exists("/etc/shells"):
    with open("/etc/shells", encoding="utf-8") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith("#"):
                valid_shells.add(l)

print("[👤] Auditoría de Usuarios con Shell Interactiva:")
with open("/etc/passwd", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(":")
        if len(parts) >= 7 and parts[6] in valid_shells:
            print(f"  - Usuario: {parts[0]} (Shell: {parts[6]})")

# Resumen Final
print("\n" + "="*40)
if alerts == 0:
    print("[RESULTADO] Handover limpio: 0 discrepancias. Estado KNOWN confirmado. [✔]")
else:
    print(f"[RESULTADO] Atención: Se detectaron {alerts} discrepancias (REVIEW REQUIRED) [!]")
print("="*40)
