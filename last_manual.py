#!/usr/bin/env python3
import platform

def get_system_identity():
    """Recopila la información básica del sistema operativo."""
    system_info = {
        "hostname": platform.node(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
    }
    
    try:
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    system_info["os_name"] = line.split("=")[1].strip().strip('"')
                    break
    except FileNotFoundError:
        system_info["os_name"] = platform.platform()
        
    return system_info

if __name__ == "__main__":
    print("=== THE LAST MANUAL: System Handover Triage ===")
    info = get_system_identity()
    for key, value in info.items():
        print(f"  {key.capitalize():<12}: {value}")
