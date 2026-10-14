# AutoOS — Sistema Operativo para Vehículo Inteligente
### Proyecto Integrador de Sistemas Operativos
**Equipo:** AutoOS  
**Rol Desarrollado:** **Integrante 3 — Seguridad y Dispositivos** (con integración completa de Dashboard)

---

##  1. Visión General del Proyecto
**AutoOS** es un prototipo funcional de Sistema Operativo especializado para vehículos autónomos e inteligentes. El sistema gestiona sensores de conducción asistida (LiDAR, Cámaras ADAS, Radar), actuadores dinámicos *By-Wire* (Dirección y Frenado), gestión energética de batería (BMS), control de procesos concurrentes y una rigurosa arquitectura de ciberseguridad automotriz basada en **RBAC** y **Row Level Security (RLS)** en Supabase.

---

##  2. Estructura del Proyecto
```text
auto_os/
├── app.py                      # Punto de entrada principal del Dashboard en Streamlit
├── config.py                   # Configuración y conexión Supabase con fallback local resiliente
├── requirements.txt            # Dependencias para ejecución local y Streamlit Cloud
├── modules/
│   ├── auth_security.py        # [Int. 3] Autenticación, Roles, Permisos RBAC y Auditoría
│   ├── devices.py              # [Int. 3] Abstracción de Hardware, CAN-Bus e inyector de fallas
│   ├── telemetry_battery.py    # [Int. 3] Batería BMS, cálculo de salud y Semáforo vehicular
│   ├── incidents.py            # [Int. 3 / Fase 10] 3 Escenarios de falla con ciclo de 5 fases
│   ├── processes.py            # [Int. 1 & 3] Procesos vehiculares con control de permisos
│   ├── memory_storage.py       # [Int. 2] RAM simulada (16 GB), archivos base y logs
│   └── ui_components.py        # Componentes UI de tablero vehicular y tacómetros Plotly
├── sql/
│   ├── 01_schema.sql           # DDL de tablas: perfiles, roles, permisos, dispositivos, eventos
│   ├── 02_rls_policies.sql     # Políticas Row Level Security en PostgreSQL
│   └── 03_seed_data.sql        # Semillas: Roles, Permisos, Usuarios de prueba, Dispositivos
├── docs/
│   ├── DOCUMENTO_ARQUITECTURA_INT3.md # Documento técnico de respaldo completo
│   └── BITACORA_VIBE_CODING.md        # Bitácora de prompts, código, errores y correcciones
└── .streamlit/
    └── secrets.toml.example    # Plantilla de credenciales Supabase Cloud
```

---

##  3. Instrucciones de Ejecución

### Opción A: Ejecución Local Inmediata
El sistema incluye un motor local emulado en memoria que permite probar el 100% de la funcionalidad de inmediato, sin necesidad de conexión a internet o configuración previa de Supabase:

1. Abrir una terminal en la carpeta del proyecto:
   ```bash
   cd auto_os
   ```
2. Instalar dependencias si no las tienes:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar el Dashboard:
   ```bash
   streamlit run app.py
   ```
4. El navegador se abrirá automáticamente en `http://localhost:8501`.

---

### Opción B: Conexión con Supabase Cloud
Para conectar el proyecto a tu propia instancia de Supabase:
1. Crea un proyecto en [supabase.com](https://supabase.com).
2. Ve al **SQL Editor** de Supabase y ejecuta secuencialmente los 3 scripts ubicados en la carpeta `sql/`:
   - `01_schema.sql` (Crea las tablas, enums e índices).
   - `02_rls_policies.sql` (Habilita RLS y las funciones de seguridad).
   - `03_seed_data.sql` (Inserta roles, permisos, dispositivos y procesos iniciales).
3. Copia el archivo `.streamlit/secrets.toml.example` a `.streamlit/secrets.toml`.
4. Coloca tu **Project URL** y tu **anon public key**:
   ```toml
   SUPABASE_URL = "https://tu-proyecto.supabase.co"
   SUPABASE_KEY = "tu-anon-key-aqui"
   ```
5. Al reiniciar la aplicación, el banner de la barra lateral indicará: `🟢 Supabase Cloud: Conectado`.

---

##  4. Cómo Sustentar los Requisitos del Integrante 3 ante el Profesor

| Requisito Evaluado | Cómo Demostrarlo en el Dashboard |
| :--- | :--- |
| **Autenticación ≠ Autorización** | En la barra lateral, cambia el usuario a **Pasajero (Guest)**. Ve a la pestaña *Procesos y CPU* e intenta hacer clic en **Terminar Proceso** o crear uno nuevo. Verás la alerta roja emergente de **Acceso Denegado (403 Forbidden)**. Luego ve a *Seguridad y Roles* para mostrar la traza en la tabla de **Auditoría de Accesos**. |
| **Simulación de Fallo de Dispositivo** | En la pestaña *Dispositivos y Hardware*, selecciona el sensor `DEV_LIDAR_01`, elige **Inyectar Fallo** o **Desconectar del Bus** y presiona **Ejecutar Acción**. El semáforo general superior cambiará inmediatamente a **Amarillo** o **Rojo**. |
| **Aporte de Batería y Eventos Críticos** | Muestra en el Cockpit cómo el tacómetro de batería (BMS) y los eventos críticos determinan el color del **Semáforo General** (Verde / Amarillo / Rojo). En la pestaña *Batería y Energía* puedes mover el deslizador de SoC por debajo del 10% para ver la activación del modo crítico. |
| **Escenarios de Falla (Fase 10 - 5 Pasos)** | Ve a la pestaña *Escenarios de Falla* y ejecuta cualquiera de los 3 incidentes (Sensor defectuoso, Batería baja, Proceso crítico). El sistema desplegará de forma visible el ciclo de 5 fases: `1. Detectar` ➔ `2. Registrar` ➔ `3. Generar Alerta` ➔ `4. Priorizar Procesos` ➔ `5. Ejecutar una Respuesta`. |
| **Revisión de Código y Scheduler** | Abre la pestaña *Guía de Sustentación* donde se resumen las respuestas a las preguntas típicas de la rúbrica oficial (PDF pág. 19). |
