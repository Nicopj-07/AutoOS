"""
====================================================================
AUTOOS - SISTEMA OPERATIVO PARA VEHÍCULO INTELIGENTE
Módulo: ui_components.py
Responsable: Componentes Visuales de Alta Fidelidad para Cockpit
====================================================================
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, List

def aplicar_estilos_cockpit():
    """Aplica hojas de estilo personalizadas con estética de Cabina Inteligente"""
    st.markdown("""
        <style>
        /* Tipografía y fondo vehicular */
        .main {
            background-color: #0d1117;
        }
        
        /* Tarjetas de métricas automotrices */
        .auto-card {
            background: linear-gradient(135deg, #161b22 0%, #1f2937 100%);
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            transition: transform 0.2s ease;
        }
        .auto-card:hover {
            border-color: #38bdf8;
            transform: translateY(-2px);
        }
        
        /* Semáforo vehicular */
        .semaforo-banner {
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 20px;
            color: #ffffff;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 4px 16px rgba(0,0,0,0.5);
        }
        .semaforo-verde {
            background: linear-gradient(90deg, #065f46 0%, #047857 100%);
            border-left: 8px solid #10b981;
        }
        .semaforo-amarillo {
            background: linear-gradient(90deg, #78350f 0%, #b45309 100%);
            border-left: 8px solid #f59e0b;
        }
        .semaforo-rojo {
            background: linear-gradient(90deg, #7f1d1d 0%, #b91c1c 100%);
            border-left: 8px solid #ef4444;
            animation: pulse-red 2s infinite;
        }
        
        @keyframes pulse-red {
            0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
            70% { box-shadow: 0 0 0 14px rgba(239, 68, 68, 0); }
            100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
        }
        
        /* Badges de estado de dispositivos */
        .badge-operativo { background-color: #064e3b; color: #34d399; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: bold; border: 1px solid #059669; }
        .badge-degradado { background-color: #451a03; color: #fbbf24; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: bold; border: 1px solid #d97706; }
        .badge-falla { background-color: #450a0a; color: #f87171; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: bold; border: 1px solid #dc2626; }
        .badge-desconectado { background-color: #1f2937; color: #9ca3af; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: bold; border: 1px solid #4b5563; }
        
        /* Pasos del ciclo de 5 fases */
        .fase-step {
            border-left: 4px solid #38bdf8;
            padding: 10px 14px;
            margin-bottom: 10px;
            background: #111827;
            border-radius: 0 8px 8px 0;
        }
        </style>
    """, unsafe_allow_html=True)


def render_banner_semaforo(semaforo_data: Dict[str, Any]):
    """Renderiza el semáforo vehicular de estado general en el encabezado"""
    color = semaforo_data["color"]
    css_class = f"semaforo-{color.lower()}"
    
    st.markdown(f"""
        <div class="semaforo-banner {css_class}">
            <div>
                <span style="font-size: 24px; margin-right: 12px;">{semaforo_data['icono']}</span>
                <span style="font-size: 20px; font-weight: 700; letter-spacing: 0.5px;">{semaforo_data['titulo']}</span>
                <div style="font-size: 13px; opacity: 0.9; margin-top: 4px;">{semaforo_data['mensaje']}</div>
            </div>
            <div style="text-align: right; min-width: 160px;">
                <div style="font-size: 12px; text-transform: uppercase; opacity: 0.8;">Batería BMS: <b>{semaforo_data['bateria_soc']}%</b></div>
                <div style="font-size: 12px; text-transform: uppercase; opacity: 0.8;">Eventos Críticos: <b>{semaforo_data['eventos_criticos_count']}</b></div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def crear_gauge_bateria(soc_pct: float, temp_c: float) -> go.Figure:
    """Genera medidor tipo tacómetro para el estado de carga de la batería"""
    color_bar = "#10b981" if soc_pct > 25 else ("#f59e0b" if soc_pct > 12 else "#ef4444")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=soc_pct,
        number={'suffix': "%", 'font': {'size': 26, 'color': '#ffffff'}},
        title={'text': f"Batería HV (Temp: {temp_c}°C)", 'font': {'size': 14, 'color': '#94a3b8'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
            'bar': {'color': color_bar, 'thickness': 0.3},
            'bgcolor': "#1e293b",
            'borderwidth': 1,
            'bordercolor': "#334155",
            'steps': [
                {'range': [0, 12], 'color': 'rgba(239, 68, 68, 0.2)'},
                {'range': [12, 25], 'color': 'rgba(245, 158, 11, 0.2)'},
                {'range': [25, 100], 'color': 'rgba(16, 185, 129, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 3},
                'thickness': 0.75,
                'value': 10
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=15, r=15, t=30, b=15),
        height=170
    )
    return fig


def crear_gauge_circular(valor: float, titulo: str, unidad: str = "%", max_val: float = 100.0, color_hex: str = "#38bdf8") -> go.Figure:
    """Genera medidor circular estilizado para CPU y Memoria"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=valor,
        number={'suffix': unidad, 'font': {'size': 24, 'color': '#ffffff'}},
        title={'text': titulo, 'font': {'size': 13, 'color': '#94a3b8'}},
        gauge={
            'axis': {'range': [0, max_val], 'tickcolor': "#475569"},
            'bar': {'color': color_hex, 'thickness': 0.28},
            'bgcolor': "#1e293b",
            'borderwidth': 1,
            'bordercolor': "#334155"
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=15, r=15, t=30, b=15),
        height=160
    )
    return fig


def render_tarjeta_dispositivo(dev: Dict[str, Any]):
    """Renderiza tarjeta individual para un periférico o sensor de AutoOS"""
    badge_map = {
        "operativo": ('<span class="badge-operativo">OPERATIVO</span>', "#10b981"),
        "degradado": ('<span class="badge-degradado">DEGRADADO</span>', "#f59e0b"),
        "falla": ('<span class="badge-falla">FALLA</span>', "#ef4444"),
        "desconectado": ('<span class="badge-desconectado">DESCONECTADO</span>', "#6b7280")
    }
    badge_html, color = badge_map.get(dev["estado"], ('<span class="badge-operativo">OPERATIVO</span>', "#10b981"))
    
    critico_color = "#ef4444" if dev["nivel_critico"] == "critico" else ("#f59e0b" if dev["nivel_critico"] == "esencial" else "#38bdf8")
    
    st.markdown(f"""
        <div class="auto-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-weight: 700; color: #f1f5f9; font-size: 15px;">{dev['nombre']}</span>
                {badge_html}
            </div>
            <div style="font-size: 12px; color: #94a3b8; margin-bottom: 6px;">
                <code>{dev['codigo']}</code> &bull; Bus: <b>{dev['puerto_bus']}</b> &bull; Sub: {dev['sub_sistema']}
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px;">
                <span>Salud: <b style="color: {color};">{dev['salud_porcentaje']}%</b></span>
                <span style="color: {critico_color}; text-transform: uppercase; font-weight: 600; font-size: 11px;">Nivel: {dev['nivel_critico']}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
