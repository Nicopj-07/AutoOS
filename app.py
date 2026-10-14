"""
====================================================================
AUTOOS - SISTEMA OPERATIVO PARA VEHÍCULO INTELIGENTE
Dashboard Principal de Control e Integración
Responsable Principal: Integrante 3 (Seguridad, Dispositivos y RLS)
====================================================================
"""

import streamlit as st
import pandas as pd
import datetime

# Configuración de página de Streamlit
st.set_page_config(
    page_title="AutoOS - Sistema Operativo Vehicular",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importar módulos del sistema
from config import get_db, get_supabase_client
from modules.auth_security import (
    obtener_usuario_actual, cambiar_usuario_activo, tiene_permiso,
    validar_accion, obtener_auditoria, obtener_matriz_permisos, ROLES_INFO
)
from modules.devices import (
    obtener_dispositivos, obtener_resumen_dispositivos,
    cambiar_estado_dispositivo, calibrar_dispositivo
)
from modules.telemetry_battery import (
    obtener_estado_bateria, calcular_semaforo_general,
    obtener_eventos_criticos_activos, actualizar_bateria
)
from modules.incidents import (
    ESCENARIOS_DISPONIBLES, ejecutar_escenario_falla, restablecer_sistema_a_normal
)
from modules.processes import (
    obtener_procesos, crear_proceso, cambiar_estado_proceso,
    finalizar_proceso, calcular_uso_cpu_total
)
from modules.memory_storage import (
    obtener_uso_memoria, obtener_sistema_archivos, obtener_logs_sistema
)
from modules.ui_components import (
    aplicar_estilos_cockpit, render_banner_semaforo,
    crear_gauge_bateria, crear_gauge_circular, render_tarjeta_dispositivo
)

# Aplicar temas visuales de cabina inteligente
aplicar_estilos_cockpit()

# Obtener usuario y estado del sistema
usuario_actual = obtener_usuario_actual()
semaforo = calcular_semaforo_general()
db = get_db()
bateria = obtener_estado_bateria()
resumen_dev = obtener_resumen_dispositivos()
cpu_total = calcular_uso_cpu_total()
memoria_info = obtener_uso_memoria()

# ====================================================================
# BARRA LATERAL (SIDEBAR): CONTROL DE SESIÓN Y CREDENCIALES
# ====================================================================
with st.sidebar:
    st.markdown("### 🚘 **AutoOS Cockpit v2.4**")
    st.caption("Sistema Operativo para Vehículo Inteligente")
    
    st.markdown("---")
    st.markdown("#### 👤 **Control de Usuario Activo (Int. 3)**")
    st.info("💡 *Usa este conmutador para demostrar en vivo el control de acceso y RBAC:*")
    
    # Selector de usuarios para prueba en vivo
    opciones_usuarios = {
        "usr_mecanico_01": "🔴 Carlos Vélez (Mecánico / Admin)",
        "usr_conductor_01": "🟢 Laura Gómez (Conductora / User)",
        "usr_pasajero_01": "🟡 Andrés Rivera (Pasajero / Guest)"
    }
    
    id_seleccionado = st.selectbox(
        "Autenticar como:",
        options=list(opciones_usuarios.keys()),
        format_func=lambda x: opciones_usuarios[x],
        index=list(opciones_usuarios.keys()).index(usuario_actual["id"]) if usuario_actual["id"] in opciones_usuarios else 1
    )
    
    if id_seleccionado != usuario_actual["id"]:
        cambiar_usuario_activo(id_seleccionado)
        st.rerun()
        
    rol_actual = usuario_actual.get("rol", "guest")
    info_rol = ROLES_INFO.get(rol_actual, {})
    
    st.markdown(f"""
        <div style="background-color: #1e293b; padding: 12px; border-radius: 8px; border-left: 4px solid #38bdf8; margin-top: 10px;">
            <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8;">Rol Asignado:</div>
            <div style="font-size: 15px; font-weight: bold; color: #f8fafc;">{info_rol.get('badge_color')} {info_rol.get('etiqueta')}</div>
            <div style="font-size: 11px; color: #cbd5e1; margin-top: 4px;">Privilegio Kernel: <b>Nivel {info_rol.get('nivel')}/10</b></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### ⚡ **Conectividad Backend**")
    cliente_sb = get_supabase_client()
    if cliente_sb:
        st.success("🟢 Supabase Cloud: Conectado")
    else:
        st.warning("🟠 Motor Local / Simulado Activo")
        st.caption("AutoOS opera con base de datos en memoria sincronizada y lista para conectar a Supabase.")
        
    st.markdown("---")
    st.markdown("#### 🛠️ **Acción Rápida de Respaldo**")
    if st.button("🔄 Restablecer Sistema a Normal", use_container_width=True):
        ok, msg = restablecer_sistema_a_normal(usuario_actual)
        if ok:
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)


# ====================================================================
# ENCABEZADO PRINCIPAL Y SEMÁFORO DE ESTADO GENERAL (Fila 10 de Plantilla)
# ====================================================================
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("🚗 AutoOS Dashboard")
    st.caption("Plataforma de Simulación del Sistema Operativo Vehicular & Control de Seguridad")
with col_head2:
    st.metric("Reloj de Sistema", datetime.datetime.now().strftime("%H:%M:%S"), delta="RTOS Synced")

# Renderizar el Semáforo General de AutoOS (Aporte Int. 3 e Int. 4)
render_banner_semaforo(semaforo)


# ====================================================================
# PESTAÑAS PRINCIPALES DEL DASHBOARD
# ====================================================================
tab_cockpit, tab_seguridad, tab_dispositivos, tab_bateria, tab_incidentes, tab_procesos, tab_memoria, tab_defensa = st.tabs([
    "🏎️ Cockpit General",
    "🛡️ Seguridad y Roles (Int. 3)",
    "📡 Dispositivos y Hardware (Int. 3)",
    "🔋 Batería y Energía (Int. 3)",
    "🚨 Escenarios de Falla (Fase 10)",
    "⚙️ Procesos y CPU (Int. 1)",
    "💾 Memoria y Archivos (Int. 2)",
    "🎓 Guía de Sustentación"
])


# --------------------------------------------------------------------
# 1. PESTAÑA: COCKPIT GENERAL
# --------------------------------------------------------------------
with tab_cockpit:
    st.subheader("📊 Indicadores de Telemetría en Tiempo Real")
    
    col_g1, col_g2, col_g3, col_g4 = st.columns(4)
    with col_g1:
        st.plotly_chart(crear_gauge_circular(cpu_total, "Uso Total de CPU", "%", 100.0, "#38bdf8"), use_container_width=True)
    with col_g2:
        st.plotly_chart(crear_gauge_circular(memoria_info["pct_usado"], "Uso de Memoria RAM", "%", 100.0, "#a855f7"), use_container_width=True)
    with col_g3:
        st.plotly_chart(crear_gauge_bateria(bateria["soc_pct"], bateria["temp_c"]), use_container_width=True)
    with col_g4:
        st.plotly_chart(crear_gauge_circular(resumen_dev["salud_promedio"], "Salud Dispositivos", "%", 100.0, "#10b981"), use_container_width=True)
        
    # Resumen rápido de subsistemas
    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.markdown(f"""
            <div class="auto-card">
                <h4>📡 Hardware y Periféricos</h4>
                <div>Total dispositivos: <b>{resumen_dev['total']}</b></div>
                <div style="color: #34d399;">Operativos: <b>{resumen_dev['operativos']}</b></div>
                <div style="color: #fbbf24;">Degradados: <b>{resumen_dev['degradados']}</b></div>
                <div style="color: #f87171;">Fallas / Desconectados: <b>{resumen_dev['fallas'] + resumen_dev['desconectados']}</b></div>
            </div>
        """, unsafe_allow_html=True)
    with col_res2:
        st.markdown(f"""
            <div class="auto-card">
                <h4>⚙️ Procesos Vehiculares</h4>
                <div>Procesos totales: <b>{len(db['procesos'])}</b></div>
                <div>Ejecutando: <b>{sum(1 for p in db['procesos'] if p['estado'] == 'ejecutando')}</b></div>
                <div>Procesos críticos (ASIL): <b>{sum(1 for p in db['procesos'] if p.get('critico'))}</b></div>
                <div>Carga total CPU: <b>{cpu_total}%</b></div>
            </div>
        """, unsafe_allow_html=True)
    with col_res3:
        st.markdown(f"""
            <div class="auto-card">
                <h4>🛡️ Seguridad y Control de Acceso</h4>
                <div>Usuario actual: <b>{usuario_actual['nombre_completo']}</b></div>
                <div>Rol: <b>{info_rol.get('etiqueta')}</b></div>
                <div>Intentos bloqueados hoy: <b>{sum(1 for a in db['auditoria'] if not a['autorizado'])}</b></div>
                <div>Políticas RLS activas: <b>100%</b></div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("#### 🚨 Registro de Alertas y Eventos Críticos Activos")
    eventos_criticos = obtener_eventos_criticos_activos()
    if eventos_criticos:
        for ev in eventos_criticos:
            st.error(f"🔴 **[{ev['severidad'].upper()}]** {ev['mensaje']} (Hora: {ev['creado_en']})")
    else:
        st.success("✅ No hay eventos críticos activos. El vehículo opera con normalidad.")


# --------------------------------------------------------------------
# 2. PESTAÑA: SEGURIDAD Y ROLES (INTEGRANTE 3)
# --------------------------------------------------------------------
with tab_seguridad:
    st.header("🛡️ Módulo de Seguridad y Control de Acceso")
    st.markdown("""
        **Responsable: Integrante 3**  
        *Concepto clave evaluado en el PDF:* **Autenticación ≠ Autorización**.  
        - **Autenticación:** Comprueba la identidad de la entidad (*¿Quién es?* Ejemplo: Mecánico, Conductor o Pasajero mediante Supabase Auth).  
        - **Autorización:** Comprueba si la entidad identificada tiene derecho a ejecutar una acción sobre un recurso específico (*¿Qué tiene permitido hacer?* Ejemplo: cambiar prioridades, apagar sensores o crear procesos).
    """)
    
    st.markdown("---")
    col_u1, col_u2 = st.columns([1, 2])
    with col_u1:
        st.subheader("Identidad del Usuario")
        st.write(f"**Nombre:** {usuario_actual['nombre_completo']}")
        st.write(f"**Correo:** `{usuario_actual['email']}`")
        st.write(f"**Rol:** {info_rol.get('badge_color')} {info_rol.get('etiqueta')}")
        st.write(f"**Nivel de Privilegio:** {info_rol.get('nivel')}/10")
        st.write(f"**Descripción del Rol:** {info_rol.get('descripcion')}")
        
    with col_u2:
        st.subheader("🧪 Simulador de Prueba de Autorización en Vivo")
        st.caption("Prueba interactiva para demostrar al docente cómo se bloquean accesos no permitidos:")
        
        permiso_a_probar = st.selectbox(
            "Selecciona una operación a probar:",
            options=[
                ("proceso.crear", "Crear un nuevo proceso vehicular"),
                ("proceso.finalizar", "Finalizar / Abortar un proceso"),
                ("dispositivo.calibrar", "Calibrar sensor LiDAR o Cámara ADAS"),
                ("dispositivo.desconectar", "Desconectar un actuador By-Wire"),
                ("seguridad.admin_usuarios", "Modificar roles y usuarios del vehículo"),
                ("telemetria.ver_bateria", "Consultar telemetría BMS")
            ],
            format_func=lambda x: f"{x[0]} - {x[1]}"
        )
        
        if st.button("Ejecutar Verificación de Autorización"):
            clave, desc = permiso_a_probar
            autorizado, motivo = validar_accion(usuario_actual, clave, recurso=f"recurso_test:{clave}")
            if autorizado:
                st.success(f"✅ **AUTORIZADO**: El rol '{usuario_actual['rol'].upper()}' tiene el permiso `{clave}`.")
            else:
                st.error(f"⛔ **DENEGADO (403 Forbidden)**: {motivo}")
                st.toast("Intento no autorizado registrado en auditoría y eventos de seguridad.", icon="🚫")
                
    st.markdown("---")
    st.subheader("📋 Matriz de Control de Acceso por Rol (RBAC)")
    matriz_df = pd.DataFrame(obtener_matriz_permisos())
    st.dataframe(matriz_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("📜 Registro de Auditoría de Accesos (Auditoria_Accesos)")
    st.caption("Demostración para la sustentación: cada intento queda registrado con su veredicto (Aprobado o Denegado).")
    auditoria_df = pd.DataFrame(obtener_auditoria(15))
    if not auditoria_df.empty:
        st.dataframe(
            auditoria_df[["hora", "usuario_email", "rol", "recurso", "accion", "autorizado", "motivo_rechazo"]],
            use_container_width=True,
            hide_index=True
        )


# --------------------------------------------------------------------
# 3. PESTAÑA: HARDWARE Y DISPOSITIVOS (INTEGRANTE 3)
# --------------------------------------------------------------------
with tab_dispositivos:
    st.header("📡 Abstracción de Hardware y Periféricos Vehiculares")
    st.markdown("""
        **Responsable: Integrante 3**  
        *Requisito de plantilla:* 'Entrega la lista de dispositivos con su estado'.  
        AutoOS administra sensores ADAS (Cámaras, LiDAR, Radares), actuadores By-Wire (Frenos, Dirección) y unidades electrónicas conectadas por redes automotrices CAN 2.0B y Automotive Ethernet.
    """)
    
    # Filtros
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filtro_estado = st.selectbox("Filtrar por Estado:", ["Todos", "Operativo", "Degradado", "Falla", "Desconectado"])
    with col_f2:
        filtro_bus = st.selectbox("Filtrar por Bus de Comunicación:", ["Todos", "CAN-Bus Principal", "CAN-Bus ADAS", "Automotive Ethernet", "LIN-Bus Confort"])
        
    dispositivos_filtrados = obtener_dispositivos(filtro_estado=filtro_estado, filtro_bus=filtro_bus)
    
    # Renderizar cuadrícula de tarjetas de dispositivos
    cols_tarjetas = st.columns(2)
    for idx, dev in enumerate(dispositivos_filtrados):
        with cols_tarjetas[idx % 2]:
            render_tarjeta_dispositivo(dev)
            
    st.markdown("---")
    st.subheader("🔧 Panel de Intervención de Dispositivos (Sustentación)")
    st.caption("Permite simular el comando del profesor: *'Simule un fallo de dispositivo'* o *'Provoque una desconexión'*.")
    
    col_act1, col_act2, col_act3 = st.columns([2, 1, 1])
    with col_act1:
        dev_codigo_seleccionado = st.selectbox(
            "Seleccionar dispositivo para operar:",
            options=[d["codigo"] for d in db["dispositivos"]],
            format_func=lambda x: f"{x} - {obtener_dispositivo(x)['nombre']}"
        )
    with col_act2:
        accion_hardware = st.selectbox(
            "Acción de Hardware:",
            options=["Inyectar Fallo", "Desconectar del Bus", "Calibrar / Restaurar"]
        )
    with col_act3:
        st.write("") # Espaciador
        st.write("")
        if st.button("Ejecutar Acción", use_container_width=True):
            if accion_hardware == "Inyectar Fallo":
                ok, msg = cambiar_estado_dispositivo(dev_codigo_seleccionado, "falla", usuario_actual, motivo="Inyección de fallo en laboratorio")
            elif accion_hardware == "Desconectar del Bus":
                ok, msg = cambiar_estado_dispositivo(dev_codigo_seleccionado, "desconectado", usuario_actual, motivo="Corte físico de línea CAN simulado")
            else:
                ok, msg = calibrar_dispositivo(dev_codigo_seleccionado, usuario_actual)
                
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)


# --------------------------------------------------------------------
# 4. PESTAÑA: BATERÍA Y ENERGÍA (INTEGRANTE 3)
# --------------------------------------------------------------------
with tab_bateria:
    st.header("🔋 Sistema de Gestión Térmica y Batería (BMS)")
    st.markdown("""
        **Responsable: Integrante 3**  
        *Requisito de plantilla:* 'Dashboard: estado general -> Aporta batería y eventos críticos'.  
        El módulo BMS supervisa el paquete LiFePO4 de 400V, calcula el estado de carga (SoC), temperatura de celdas y alimenta directamente la lógica del semáforo general del vehículo.
    """)
    
    col_bat1, col_bat2, col_bat3 = st.columns(3)
    with col_bat1:
        st.metric("Estado de Carga (SoC)", f"{bateria['soc_pct']}%", delta=bateria["modo_actual"])
    with col_bat2:
        st.metric("Voltaje del Paquete", f"{bateria['voltaje_v']} V", delta="398V Nominal")
    with col_bat3:
        st.metric("Temperatura de Celdas", f"{bateria['temp_c']} °C", delta="Máx tolerado: 55°C", delta_color="inverse")
        
    st.markdown("---")
    st.subheader("⚡ Simulador de Descarga y Estado de Batería")
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        nuevo_soc = st.slider("Ajustar Nivel de Carga (SoC %):", 0.0, 100.0, float(bateria["soc_pct"]))
    with col_s2:
        nueva_temp = st.slider("Ajustar Temperatura BMS (°C):", 15.0, 70.0, float(bateria["temp_c"]))
    with col_s3:
        st.write("")
        st.write("")
        if st.button("Actualizar Parámetros BMS", use_container_width=True):
            actualizar_bateria(nuevo_soc, nueva_temp)
            st.success("Parámetros de batería actualizados en el bus CAN.")
            st.rerun()


# --------------------------------------------------------------------
# 5. PESTAÑA: ESCENARIOS DE FALLA (FASE 10 - INTEGRANTE 3)
# --------------------------------------------------------------------
with tab_incidentes:
    st.header("🚨 Fase 10: Escenarios Críticos de Falla en AutoOS")
    st.markdown("""
        **Requisito riguroso del PDF (Página 12):**  
        *Cada equipo deberá implementar mínimo 3 escenarios críticos relacionados con su dispositivo.*  
        AutoOS implementa:  
        1. **Sensor defectuoso** (LiDAR frontal ADAS)  
        2. **Batería baja** (SoC crítico < 8% con advertencia térmica)  
        3. **Proceso crítico** (Fallo en actuador By-Wire de dirección)  

        **El sistema cumple las 5 fases obligatorias:**  
        `1. Detectar` ➡️ `2. Registrar` ➡️ `3. Generar alerta` ➡️ `4. Priorizar procesos` ➡️ `5. Ejecutar una respuesta`
    """)
    
    st.markdown("---")
    escenario_elegido = st.radio(
        "Selecciona el escenario crítico a ejecutar:",
        options=list(ESCENARIOS_DISPONIBLES.keys()),
        format_func=lambda x: f"{ESCENARIOS_DISPONIBLES[x]['icono']} {ESCENARIOS_DISPONIBLES[x]['titulo']}"
    )
    
    st.info(f"📌 **Descripción:** {ESCENARIOS_DISPONIBLES[escenario_elegido]['descripcion']}")
    
    if st.button("🚀 Disparar Escenario Crítico (Simular Incidente)", type="primary"):
        resultado = ejecutar_escenario_falla(escenario_elegido, usuario_actual)
        st.session_state["ultimo_escenario_resultado"] = resultado
        st.rerun()
        
    if "ultimo_escenario_resultado" in st.session_state:
        res = st.session_state["ultimo_escenario_resultado"]
        st.markdown(f"### 📋 Ejecución del Protocolo: *{res['titulo']}*")
        st.caption(f"Marca temporal: {res['hora_ejecucion']}")
        
        for paso in res["pasos"]:
            st.markdown(f"""
                <div class="fase-step">
                    <div style="font-weight: 700; color: #38bdf8; font-size: 14px;">{paso['fase']}</div>
                    <div style="color: #f1f5f9; font-size: 13px; margin-top: 3px;">{paso['accion']}</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.warning("⚠️ Nota cómo el semáforo superior, el estado de los dispositivos y las prioridades de los procesos se adaptaron automáticamente.")


# --------------------------------------------------------------------
# 6. PESTAÑA: PROCESOS Y CPU (INTEGRACIÓN CON INTEGRANTE 1)
# --------------------------------------------------------------------
with tab_procesos:
    st.header("⚙️ Gestión de Procesos Vehiculares y Scheduler")
    st.markdown("""
        **Integración:** Módulo de Procesos (Int. 1) + Control de Permisos RBAC (Int. 3).  
        *Requisitos de la imagen:*  
        - **Crear proceso:** 'Permiso necesario para crear' (Int. 3)  
        - **Cambiar estado (pausar/reanudar):** 'Valida que el rol pueda hacerlo' (Int. 3)  
        - **Finalizar proceso:** 'Valida que el rol pueda hacerlo' (Int. 3)
    """)
    
    # Formulario de creación de proceso
    with st.expander("➕ Iniciar Nuevo Proceso Vehicular (Crear)", expanded=False):
        col_cp1, col_cp2, col_cp3 = st.columns(3)
        with col_cp1:
            nombre_proc = st.text_input("Nombre del Proceso:", value="carplay_audio_stream")
            mem_proc = st.number_input("Memoria (MB):", min_value=16, max_value=2048, value=128, step=16)
        with col_cp2:
            prio_proc = st.slider("Prioridad (0 = Tiempo Real, 10 = Idle):", 0, 10, 5)
            cpu_proc = st.number_input("Consumo CPU Estimado (%):", min_value=0.5, max_value=50.0, value=3.5, step=0.5)
        with col_cp3:
            es_critico = st.checkbox("¿Es Proceso Crítico de Seguridad (ASIL)?", value=False)
            st.write("")
            if st.button("Crear Proceso"):
                ok, msg = crear_proceso(nombre_proc, prio_proc, cpu_proc, mem_proc, es_critico, usuario_actual)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
                    
    st.markdown("---")
    st.subheader("📋 Tabla de Procesos Activos en AutoOS")
    
    procesos_actuales = obtener_procesos()
    for p in procesos_actuales:
        col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns([2, 1, 1, 1, 2])
        with col_p1:
            critico_tag = "🔴 [ASIL-D]" if p.get("critico") else "⚪"
            st.write(f"**PID {p['pid']}**: `{p['nombre']}` {critico_tag}")
        with col_p2:
            st.write(f"Prioridad: **{p['prioridad']}**")
        with col_p3:
            st.write(f"CPU: **{p['cpu']}%**")
        with col_p4:
            st.write(f"Estado: `{p['estado']}`")
        with col_p5:
            # Botones de control con validación RBAC
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                nuevo_st = "bloqueado" if p["estado"] == "ejecutando" else "ejecutando"
                label_st = "⏸️ Pausar" if p["estado"] == "ejecutando" else "▶️ Reanudar"
                if st.button(label_st, key=f"btn_st_{p['pid']}"):
                    ok, msg = cambiar_estado_proceso(p["pid"], nuevo_st, usuario_actual)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            with c_btn2:
                if st.button("🛑 Terminar", key=f"btn_kill_{p['pid']}"):
                    ok, msg = finalizar_proceso(p["pid"], usuario_actual)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)


# --------------------------------------------------------------------
# 7. PESTAÑA: MEMORIA, ARCHIVOS Y LOGS (INTEGRACIÓN CON INTEGRANTE 2)
# --------------------------------------------------------------------
with tab_memoria:
    st.header("💾 Memoria, Sistema de Archivos y Registros (Logs)")
    st.markdown("""
        **Integración con Integrante 2**  
        *Requisitos de la matriz:*  
        - RAM total simulada (16 GB), bloques asignados y liberados  
        - Carpetas base vehiculares (`/config`, `/logs`, `/media`, `/maps`, `/telemetry`)  
        - Logs de sistema con niveles de severidad
    """)
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.subheader("Uso de Memoria RAM")
        st.write(f"Total: **{memoria_info['total_mb']} MB (16 GB)**")
        st.write(f"Usada por Kernel: **{memoria_info['kernel_mb']} MB**")
        st.write(f"Usada por Procesos: **{memoria_info['procesos_mb']} MB**")
        st.write(f"Memoria Libre: **{memoria_info['libre_mb']} MB**")
        st.progress(memoria_info["pct_usado"] / 100.0)
        
    with col_m2:
        st.subheader("Carpetas y Archivos Base del Vehículo")
        archivos_df = pd.DataFrame(obtener_sistema_archivos())
        st.dataframe(archivos_df[["ruta", "tipo", "tamano_kb", "permisos"]], hide_index=True)
        
    st.markdown("---")
    st.subheader("📜 Visor de Logs del Sistema (AutoOS Kernel Logs)")
    logs_data = obtener_logs_sistema(10)
    st.dataframe(pd.DataFrame(logs_data), hide_index=True, use_container_width=True)


# --------------------------------------------------------------------
# 8. PESTAÑA: GUÍA DE SUSTENTACIÓN Y DEFENSA
# --------------------------------------------------------------------
with tab_defensa:
    st.header("🎓 Preparación para la Sustentación y Preguntas del Docente")
    st.markdown("""
        Esta sección contiene las respuestas exactas y los pasos prácticos para responder a cada una de las preguntas indicadas en el **PDF (Página 19 - DEFENSA FINAL)** para el Integrante 3:
    """)
    
    with st.expander("❓ 1. 'Intente acceder a este recurso con un usuario sin permisos'", expanded=True):
        st.markdown("""
            **Cómo demostrarlo en la aplicación:**
            1. Ve a la barra lateral izquierda y cambia el usuario a **Andrés Rivera (Pasajero / Guest)**.
            2. Dirígete a la pestaña **'⚙️ Procesos y CPU'** e intenta hacer clic en **'🛑 Terminar'** en cualquier proceso o crear un proceso.
            3. Verás la alerta roja emergente de **Acceso Denegado (403 Forbidden)**.
            4. Luego ve a la pestaña **'🛡️ Seguridad y Roles'** y muéstrale al profesor la tabla de **Auditoría de Accesos**, donde el intento quedó registrado con fecha, hora, rol y motivo de rechazo.
            
            **Fundamento teórico a explicar:**
            > *"Profesor, demostramos el principio fundamental de que **Autenticación ≠ Autorización**. El pasajero está autenticado en Supabase con su identidad válida, pero la directiva RBAC y las políticas RLS le impiden ejecutar operaciones privilegiadas que comprometan el vehículo."*
        """)
        
    with st.expander("❓ 2. 'Simule un fallo de dispositivo'", expanded=True):
        st.markdown("""
            **Cómo demostrarlo en la aplicación:**
            1. En la pestaña **'📡 Dispositivos y Hardware'**, selecciona el sensor `DEV_LIDAR_01` o `DEV_ACT_STEER`.
            2. Selecciona la acción **'Inyectar Fallo'** o **'Desconectar del Bus'** y presiona **'Ejecutar Acción'**.
            3. Alternativamente, ve a la pestaña **'🚨 Escenarios de Falla'** y ejecuta el **Escenario 1** o **Escenario 3**.
            4. Muestra cómo el semáforo principal conmuta a **AMARILLO** o **ROJO**, el evento crítico se registra en la base de datos y el scheduler prioriza las tareas de emergencia.
            
            **Fundamento teórico a explicar:**
            > *"El sistema implementa detección de fallos por bus CAN / Automotive Ethernet con un ciclo de 5 fases: detección de anomalía, persistencia del evento, emisión de alerta al conductor, reasignación de prioridades en el scheduler y ejecución de la maniobra de contingencia Fail-Safe."*
        """)
        
    with st.expander("❓ 3. '¿Cómo se coordina la batería baja crítica con el sistema?'", expanded=True):
        st.markdown("""
            **Cómo responder:**
            > *"El módulo BMS aporta telemetría continua de SoC, voltaje y temperatura. Cuando el SoC cae por debajo del 10% o la temperatura de celdas supera los 55°C, el subsistema de energía emite una señal de interrupción al kernel. El scheduler suspende inmediatamente procesos de confort como el reproductor multimedia y el aire acondicionado, reservando la CPU y la energía exclusivamente para el control de tracción a baja velocidad (Modo Limp-Home) y el frenado regenerativo."*
        """)
        
    with st.expander("❓ 4. 'Explíqueme qué ocurre cuando dos procesos solicitan el mismo recurso'", expanded=True):
        st.markdown("""
            **Cómo responder:**
            > *"En AutoOS, los dispositivos de seguridad (como los actuadores de frenado y dirección) son recursos no compartibles en modo exclusivo. Se implementa control de concurrencia y herencia de prioridad (Priority Inheritance Protocol) para evitar inversión de prioridad. El proceso con mayor nivel ASIL (ej. frenado de emergencia) obtiene el candado (mutex) del actuador en el bus CAN, mientras que las solicitudes de confort quedan bloqueadas en una cola de espera con timeout."*
        """)
