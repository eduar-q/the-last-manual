🔎 **A lightweight Linux tool for system handover triage and state reconciliation.**

## 🧩 The Problem & How It Works

Cuando una persona deja de administrar un sistema Linux, otra persona puede tener que hacerse cargo de él sin conocer bien cómo está configurado. El sistema puede seguir funcionando, pero surgen preguntas clave: 

- **¿Este es el equipo que esperaba recibir?**
- ¿Los servicios importantes siguen funcionando?
- ¿Las rutas críticas están presentes?
- ¿Qué usuarios tienen una shell interactiva?
- ¿Hay alguna diferencia entre lo que está documentado y lo que existe realmente?

**The Last Manual** ofrece un punto de partida rápido y seguro para responder esas preguntas mediante una reconciliación directa entre la documentación declarada (`manual.yaml` / **KNOWN**) y el estado operativo real del sistema (**UNKNOWN**). 

El script realiza de forma local las siguientes comprobaciones:
1. **Reconciliación de Hostname**: Compara el nombre esperado con el real (`platform.node()`).
2. **Auditoría de Rutas Críticas**: Verifica la existencia física de los archivos declarados.
3. **Auditoría de Servicios**: Comprueba el estado activo mediante `systemctl is-active`.
4. **Inventario de Usuarios**: Consulta `/etc/passwd` y valida contra las shells interactivas permitidas en `/etc/shells`.

⚠️ **Nota sobre discrepancias**: Una alerta no significa necesariamente que algo esté mal. Simplemente señala una diferencia entre la documentación y la realidad para que sea investigada (actualización, migración o documentación desactualizada).

## 📖 The Manual (`manual.yaml`)

El archivo de configuración contiene el contexto conocido del sistema. Está diseñado para ser simple, legible y **sin información sensible o secretos** (sin contraseñas, claves privadas ni tokens).

```yaml
system_metadata:
  expected_hostname: "linux-lab"

known_components:
  services:
    - name: "ssh"
      description: "Secure Shell remote access daemon"
      critical: true
    - name: "NetworkManager"
      description: "Network interface management"
      critical: true

  critical_paths:
    - path: "/etc/passwd"
      purpose: "System user database"
    - path: "/etc/ssh/sshd_config"
      purpose: "SSH security configuration"

```

## ▶️ Uso Rápido y Ejemplo de Salida

El programa debe ejecutarse localmente en un sistema Linux. **No realiza ningún cambio en el sistema.**

```bash
python3 last_manual.py

```

Un resultado exitoso se ve así:

```text
=== THE LAST MANUAL ===
[*] Iniciando reconciliación de estado (KNOWN vs UNKNOWN)...

[🔍] Reconciliación de Hostname:
  - Documentado (KNOWN): linux-lab
  - Real (UNKNOWN):      linux-lab
  [✔] Estado: CONFORME (KNOWN)

[📂] Auditoría de Rutas Críticas:
  - /etc/passwd -> Presente (KNOWN)
  - /etc/ssh/sshd_config -> Presente (KNOWN)

[⚙️] Auditoría de Servicios del Sistema:
  - ssh -> Activo (KNOWN)
  - NetworkManager -> Activo (KNOWN)

[👤] Auditoría de Usuarios con Shell Interactiva:
  - Usuario: root (Shell: /bin/bash)
  - Usuario: raude (Shell: /bin/bash)

========================================
[RESULTADO] Handover limpio: 0 discrepancias. Estado KNOWN confirmado. [✔]
========================================

```

## 📁 Estructura del Proyecto, Tecnologías y Licencia

```text
the-last-manual/
├── last_manual.py
├── manual.yaml
├── README.md
├── LICENSE
├── .gitignore
└── examples/
    ├── manual.example.yaml
    └── handover_report.example.md

```

El proyecto está compuesto por el script principal **`last_manual.py`** (stdlib-only, sin dependencias externas en Python 3), el archivo de contexto **`manual.yaml`** y el directorio **`examples/`** con plantillas de referencia.

*The Last Manual* es una herramienta de apoyo rápido para un proceso de *handover* basada en Linux, `/etc/passwd`, `/etc/shells` y `systemctl`. No pretende reemplazar auditorías formales de seguridad ni descubrir absolutamente todo en el sistema, sino acortar la curva de incertidumbre inicial.

Distribuido bajo la **Licencia MIT**.

---

**Autor:** Eduar Q.

🎓 *Computer Engineer*

🛡️ *Defensive Cybersecurity & Systems Infrastructure*
