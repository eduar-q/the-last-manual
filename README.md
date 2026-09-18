# The Last Manual

> **System Handover Triage & State Reconciliation Tool**

> [!NOTE]  
> 🚧 **PROYECTO EN FASE DE CONSTRUCCIÓN (MVP)**: Herramienta minimalista y defensiva para auditorías rápidas de entrega de servidores (*handover*).

*The Last Manual* contrasta la realidad operativa del sistema operativo (**UNKNOWN**) frente a una fuente de verdad documentada (**KNOWN**), operando de forma estrictamente local, segura y sin dependencias externas complejas.

## ¿Qué audita?
1. **Reconciliación de Hostname**: Compara el nombre real del equipo contra el esperado en el manual.
2. **Rutas Críticas**: Valida la existencia de archivos esenciales del sistema.
3. **Servicios del Sistema**: Comprueba el estado activo (`systemctl`) de servicios clave como SSH y NetworkManager.
4. **Usuarios con Acceso**: Lista rápidamente los usuarios del sistema con shell interactiva.

## Estructura del Proyecto
- `last_manual.py`: Script principal de triage y auditoría.
- `manual.yaml`: Archivo de contexto con los componentes esperados.

## Uso Rápido
```bash
python3 last_manual.py
