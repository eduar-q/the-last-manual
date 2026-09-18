# 🖥️ The Last Manual
> 🔎 **A lightweight Linux tool for system handover triage and state reconciliation.**

## 🧩 The Problem & How It Works

Cuando una persona deja de administrar un sistema Linux, otra puede tener que hacerse cargo sin conocer bien cómo está configurado. El sistema puede seguir funcionando, pero surgen preguntas sencillas:

- 🖥️ **¿Este es el equipo que esperaba recibir?**
- ⚙️ **¿Los servicios importantes siguen funcionando?**
- 📂 **¿Las rutas críticas están presentes?**
- 👤 **¿Qué usuarios tienen una shell interactiva?**
- 🔍 **¿Coincide lo documentado con lo que existe realmente?**

**The Last Manual** ofrece un punto de partida para responderlas comparando la documentación de `manual.yaml` (**KNOWN**) con el estado actual del sistema (**REAL**).

El script realiza localmente estas comprobaciones:
1. 🖥️ **Hostname:** Compara el hostname esperado con el real.
2. 📂 **Rutas críticas:** Verifica que las rutas documentadas existan.
3. ⚙️ **Servicios:** Comprueba su estado mediante `systemctl`.
4. 👤 **Usuarios:** Consulta `/etc/passwd` y `/etc/shells` para identificar usuarios con shell interactiva.

⚠️ **Una discrepancia no significa necesariamente que algo esté mal.** Solo indica que existe una diferencia que debe ser revisada. Puede deberse a un cambio legítimo, una migración o documentación desactualizada.

---

## 📖 The Manual

`manual.yaml` contiene el contexto conocido del sistema. Está diseñado para ser simple y **no debe contener información sensible ni secretos**.

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
▶️ Usage
Ejecuta el programa localmente en un sistema Linux:
python3 last_manual.py

🛡️ No realiza cambios en el sistema.
🧪 Example Output
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
  - Usuario: example-user (Shell: /bin/bash)

========================================
[RESULTADO] Handover limpio: 0 discrepancias. Estado KNOWN confirmado. [✔]
========================================

```
📁 Project Structure
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
 * last_manual.py: Utiliza únicamente Python 3 y herramientas nativas de Linux, sin librerías externas.
 * manual.yaml: Sirve como referencia del estado conocido del sistema.
 * examples/: Contiene ejemplos para documentar un sistema y entender el resultado.
⚠️ Limitations
The Last Manual es una herramienta pequeña de apoyo durante un handover.
No pretende:
 * 🔎 Descubrir absolutamente todo lo que existe en Linux.
 * 🧠 Determinar por qué existe un servicio o usuario.
 * 🛡️ Decidir si una configuración es segura o insegura.
 * 🔐 Reemplazar una auditoría formal de seguridad.
 * ⚙️ Realizar cambios en el sistema.
Su objetivo es más sencillo:
Reducir la incertidumbre inicial cuando alguien tiene que hacerse cargo de un sistema que no conoce.
💭 Why I Built It
Un sistema puede seguir funcionando aunque la persona que lo administraba ya no esté disponible. A veces existe documentación, pero está incompleta o desactualizada. Otras veces simplemente hay que recibir un sistema que otra persona conoce mucho mejor.
The Last Manual intenta responder una pregunta sencilla:
¿Lo que está documentado coincide con lo que realmente existe?
Si no coincide, la herramienta no intenta adivinar. 🔍 Señala la diferencia para que una persona pueda investigar, preguntar o actualizar la documentación.
📜 License
MIT License.
👨‍💻 Author
Eduar Q.
🎓 Computer Engineer
🛡️ Defensive Cybersecurity & Systems Infrastructure

