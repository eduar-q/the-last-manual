# The Last Manual

> **A small Linux tool for understanding a system when its administrator is no longer available.**

## The Problem

Cuando una persona deja de administrar un sistema Linux, otra persona puede tener que hacerse cargo de él sin conocer bien cómo está configurado.

El sistema puede seguir funcionando, pero pueden aparecer preguntas sencillas:

- ¿Este es el equipo que esperaba recibir?
- ¿Los servicios importantes siguen funcionando?
- ¿Las rutas importantes están presentes?
- ¿Qué usuarios tienen una shell interactiva?
- ¿Hay alguna diferencia entre lo que está documentado y lo que existe realmente?

**The Last Manual** intenta dar un punto de partida para responder esas preguntas.

La herramienta toma una pequeña documentación del sistema y la compara con información que puede comprobar directamente en el equipo.

La idea es sencilla:

> **Comparar lo que sabemos con lo que realmente existe.**

## How It Works

El proyecto utiliza `manual.yaml` como referencia de lo que se conoce del sistema.

El archivo puede indicar:

- el hostname esperado;
- los servicios que deberían estar funcionando;
- las rutas importantes que deberían existir.

`last_manual.py` lee esa información y la compara con el estado actual del sistema Linux.

El resultado muestra qué coincide con lo documentado y qué necesita revisión.

Una diferencia no significa necesariamente que algo esté mal.

Por ejemplo, si el hostname cambió, puede existir una razón válida para ello.

La herramienta solamente señala la diferencia para que una persona pueda investigarla.

## System Checks

### Hostname

Compara el hostname documentado en `manual.yaml` con el hostname real del equipo.

```text
[🔍] Reconciliación de Hostname:
  - Documentado (KNOWN): raude-OptiPlex-380
  - Real (UNKNOWN):      raude-OptiPlex-380
  [✔] Estado: CONFORME (KNOWN)

Si son diferentes, se marca como:

[!] Estado: DISCREPANCIA (REVIEW REQUIRED)

Critical Paths

Comprueba si las rutas definidas en manual.yaml existen realmente en el sistema.

Actualmente el ejemplo incluye:

/etc/passwd
/etc/ssh/sshd_config

Si una ruta no existe, se marca para revisión.

System Services

Comprueba el estado de los servicios definidos en manual.yaml utilizando systemctl.

Actualmente el ejemplo incluye:

ssh
NetworkManager

Un servicio activo se muestra como conforme.

Un servicio detenido, inexistente o que no pueda verificarse se marca para revisión.

Interactive Users

Consulta /etc/passwd y /etc/shells para mostrar los usuarios que tienen una shell considerada válida para interacción.

Esta sección funciona como un inventario rápido.

Actualmente no compara estos usuarios contra una lista documentada, por lo que encontrar un usuario aquí no significa que sea desconocido o incorrecto.

The Manual

El archivo manual.yaml contiene el contexto conocido del sistema.

Ejemplo:

system_metadata:
  expected_hostname: "raude-OptiPlex-380"

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

El archivo está pensado para contener información de contexto, no secretos.

No debería contener:

contraseñas;

claves privadas;

tokens;

credenciales;

información sensible innecesaria.


Project Structure

the-last-manual/
├── last_manual.py
├── manual.yaml
├── README.md
├── LICENSE
├── .gitignore
└── examples/
    ├── manual.example.yaml
    └── handover_report.example.md

last_manual.py

Script principal.

Lee el manual y consulta información directamente en el sistema Linux para realizar las comprobaciones.

manual.yaml

Contiene la información conocida del sistema que se utilizará como referencia.

examples/

Contiene ejemplos seguros para entender cómo documentar un sistema y cómo puede verse un reporte.

Usage

Desde el directorio del proyecto:

python3 last_manual.py

El programa debe ejecutarse en un sistema Linux.

No realiza cambios en el sistema.

Example Output

Un resultado puede verse así:

=== THE LAST MANUAL ===
[*] Iniciando reconciliación de estado (KNOWN vs UNKNOWN)...

[🔍] Reconciliación de Hostname:
  - Documentado (KNOWN): raude-OptiPlex-380
  - Real (UNKNOWN):      raude-OptiPlex-380
  [✔] Estado: CONFORME (KNOWN)

[📂] Auditoría de Rutas Críticas:
  [✔] /etc/passwd -> Presente (KNOWN)
  [✔] /etc/ssh/sshd_config -> Presente (KNOWN)

[⚙️] Auditoría de Servicios del Sistema:
  [✔] ssh -> Activo (KNOWN)
  [✔] NetworkManager -> Activo (KNOWN)

[👤] Auditoría de Usuarios con Shell Interactiva:
  - Usuario: eduar (Shell: /bin/bash)

========================================
[RESULTADO] Handover limpio: 0 discrepancias. Estado KNOWN confirmado. [✔]
========================================

Si alguna comprobación no coincide con lo documentado, el resultado indica que necesita revisión.

Review Required

Una discrepancia no significa automáticamente que exista un problema de seguridad.

Por ejemplo:

Documentado: linux-server-01
Real:        linux-server-02

Esto solamente indica que el sistema actual no coincide con la documentación.

Puede ser consecuencia de:

un cambio legítimo;

una actualización;

una migración;

documentación desactualizada;

una configuración que nunca fue documentada.


La herramienta no intenta decidir cuál de estas situaciones ocurrió.

Señala la diferencia y deja la investigación a la persona que recibe el sistema.

Limitations

The Last Manual es una herramienta pequeña de apoyo durante un handover.

No intenta:

descubrir absolutamente todo lo que existe en Linux;

determinar por qué existe un servicio o usuario;

decidir si una configuración es segura o insegura;

reemplazar una auditoría de seguridad;

reemplazar una documentación completa;

detectar por sí solo una intrusión;

realizar cambios en el sistema.


El formato de manual.yaml utilizado por el proyecto es deliberadamente sencillo y está pensado para la estructura utilizada por esta herramienta. No pretende ser un parser YAML completo.

El proyecto tampoco mantiene un historial de cambios. Si algo cambia entre dos ejecuciones, la herramienta no puede saber cuándo ocurrió el cambio.

Why I Built It

Un sistema puede seguir funcionando aunque la persona que lo administraba ya no esté disponible.

El problema no siempre es que falte un manual.

A veces existe documentación, pero está incompleta o desactualizada.

Otras veces simplemente hay que recibir un sistema que otra persona conoce mucho mejor que tú.

The Last Manual intenta reducir ese primer momento de incertidumbre:

¿Qué debería existir?
        ↓
¿Qué existe realmente?
        ↓
¿Coincide?
        ↓
Si no coincide:
investigar, preguntar o documentar

La herramienta no intenta adivinar.

Si encuentra una diferencia, no dice:

> "Esto está mal."



Dice:

> "Esto no coincide con lo que está documentado. Revísalo."



Ese es el propósito del proyecto.

Technologies

Python 3

Linux

systemctl

/etc/passwd

/etc/shells

archivos de configuración del sistema


No requiere librerías externas de Python.

License

MIT License.

Author

Eduar Q.

Computer Engineer
Defensive Cybersecurity & Systems Infrastructure
