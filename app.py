import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, date, time

# ==============================================================================
# 1. CONFIGURACIÓN GENERAL Y ESTILO FUTURISTA (CYBER-AUTOMOTIVE UI)
# ==============================================================================
st.set_page_config(
    page_title="Cerrajería Automotriz Elías | Cotizador & Taller Oriente",
    page_icon="🔑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# CUADRO 1: MEMORIA GLOBAL DE VISITAS Y CLIENTES
# ==============================================================================
@st.cache_resource
def obtener_registro_global():
    return {"visitas": 140, "clientes": []}

registro_app = obtener_registro_global()

if "visita_contada" not in st.session_state:
    registro_app["visitas"] += 1
    st.session_state.visita_contada = True
    st.session_state.hora_entrada = datetime.now().strftime("%d/%m/%Y %I:%M %p")

st.markdown("""
<style>
    /* Fondo general y tipografía moderna */
    .stApp {
        background: radial-gradient(circle at top right, #111927 0%, #0B0F19 60%, #070A10 100%);
        color: #F3F4F6;
    }
    /* Animación suave para tarjetas y recibo */
    @keyframes aparecerSuave {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    /* Encabezado Hero Futurista */
    .hero-banner {
        background: linear-gradient(135deg, rgba(14, 30, 56, 0.95) 0%, rgba(28, 45, 74, 0.85) 50%, rgba(230, 126, 34, 0.25) 100%);
        border: 1px solid rgba(230, 126, 34, 0.45);
        border-radius: 18px;
        padding: 26px 30px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        animation: aparecerSuave 0.4s ease-out;
    }
    .hero-title {
        font-size: 34px;
        font-weight: 800;
        background: linear-gradient(90deg, #FFFFFF 0%, #38BDF8 50%, #F97316 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    .hero-subtitle {
        font-size: 16px;
        color: #CBD5E1;
        margin-bottom: 14px;
    }
    .badge-tech {
        display: inline-block;
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid #38BDF8;
        color: #38BDF8;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 6px;
    }
    .badge-orange {
        display: inline-block;
        background: rgba(249, 115, 22, 0.18);
        border: 1px solid #F97316;
        color: #FDBA74;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 6px;
    }
    /* Tarjetas Glassmorphism */
    .glass-card {
        background: rgba(30, 41, 59, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.35);
        animation: aparecerSuave 0.35s ease-out;
    }
    /* Recibo Desglosado */
    .receipt-box {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        border: 2px solid #F97316;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 12px 32px rgba(249, 115, 22, 0.18);
        animation: aparecerSuave 0.4s ease-out;
    }
    .receipt-header {
        border-bottom: 1px dashed #64748B;
        padding-bottom: 12px;
        margin-bottom: 14px;
    }
    .receipt-line {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        padding: 7px 0;
        border-bottom: 1px solid rgba(100, 116, 139, 0.2);
        font-size: 14.5px;
    }
    .receipt-total {
        display: flex;
        justify-content: space-between;
        padding-top: 14px;
        margin-top: 10px;
        border-top: 2px solid #38BDF8;
        font-size: 22px;
        font-weight: 800;
        color: #4ADE80;
    }
    /* Botones de Acción Redes Sociales */
    .btn-wa {
        display: block;
        width: 100%;
        text-align: center;
        background: linear-gradient(90deg, #16A34A 0%, #22C55E 100%);
        color: white !important;
        font-weight: 800;
        font-size: 17px;
        padding: 14px;
        border-radius: 12px;
        text-decoration: none;
        margin-top: 12px;
        box-shadow: 0 6px 20px rgba(34, 197, 94, 0.35);
    }
    .btn-mail {
        display: block;
        width: 100%;
        text-align: center;
        background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%);
        color: white !important;
        font-weight: 700;
        font-size: 15px;
        padding: 12px;
        border-radius: 12px;
        text-decoration: none;
        margin-top: 10px;
    }
    .social-btn {
        display: inline-block;
        width: 100%;
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        font-weight: 700;
        color: white !important;
        text-decoration: none;
        margin-bottom: 8px;
    }
    /* SOLUCIÓN MÓVIL: Evitar que se corten las letras y años en los Selectbox y Radio en teléfonos */
    div[data-baseweb="select"] > div {
        min-height: 48px !important;
        height: auto !important;
        padding-top: 4px !important;
        padding-bottom: 4px !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
        line-height: 1.35 !important;
    }
    ul[data-baseweb="menu"] li,
    div[role="listbox"] div[role="option"] {
        white-space: normal !important;
        word-wrap: break-word !important;
        line-height: 1.35 !important;
        padding-top: 8px !important;
        padding-bottom: 8px !important;
        height: auto !important;
    }
    div[role="radiogroup"] label {
        white-space: normal !important;
        line-height: 1.35 !important;
        margin-bottom: 6px !important;
    }
    @media (max-width: 768px) {
        .hero-title { font-size: 25px !important; }
        .hero-subtitle { font-size: 14px !important; }
        .hero-banner { padding: 18px !important; }
        .receipt-total { font-size: 18px !important; }
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. BASE DE DATOS AUTOMOTRIZ INTELIGENTE (12 MARCAS Y FILTRO POR TIPO DE LLAVE)
# ==============================================================================
CATALOGO_VEHICULOS = {
    "Toyota": {
        "Pick-up 22R / Hilux / Tercel / Corolla (1988-2002) [Sin Chip]": {
            "espada": "TR40 / TR47 Metálica", "chip": "No utiliza chip (100% Mecánico)", "frec": "N/A",
            "riesgo": "VERDE", "modo": "SIN_CHIP", "usa_chip": "NO (Llave Metálica Normal)"
        },
        "Hilux / Pick-up Tacoma (1998-2004)": {
            "espada": "TR47", "chip": "Sin Chip o Transponder 4C", "frec": "315 MHz",
            "riesgo": "VERDE", "modo": "CHIP_NORMAL", "usa_chip": "Algunas versiones US llevan Chip 4C"
        },
        "Corolla / RAV4 / Yaris / Matrix / 4Runner (2003-2010)": {
            "espada": "TR47", "chip": "Transponder ID 4D67", "frec": "315 MHz",
            "riesgo": "VERDE", "modo": "CHIP_NORMAL", "usa_chip": "SÍ (Chip Transponder 4D67)"
        },
        "Hilux / Hiace / Fortuner (2006-2015)": {
            "espada": "TR47", "chip": "Transponder 4D67 / Letra G (80 bits)", "frec": "433 MHz",
            "riesgo": "VERDE", "modo": "CHIP_ALTA", "usa_chip": "SÍ (Chip 4D67 o Letra G)"
        },
        "Corolla / RAV4 / Tacoma / Tundra / Yaris (2010-2014)": {
            "espada": "TR47 / TOY43", "chip": "Transponder Letra G (80 bits) / Smart 4D", "frec": "315 MHz",
            "riesgo": "VERDE", "modo": "MIXTO_SMART", "usa_chip": "SÍ (Chip Letra G o Smart Key)"
        },
        "Corolla / RAV4 / Tacoma / 4Runner (2014-2021)": {
            "espada": "TR47 / TOY48 Regata", "chip": "Chip Letra H (128 bits) / Smart Key 8A", "frec": "314.3 / 315 MHz",
            "riesgo": "VERDE", "modo": "MIXTO_SMART", "usa_chip": "SÍ (Chip H 128-bits o Presencia 8A)"
        },
        "Hilux / Fortuner / Prado (2016-2021)": {
            "espada": "TR47 / TOY48 Regata", "chip": "Chip Letra H (128 bits) / Smart Key 8A", "frec": "315 / 433 MHz",
            "riesgo": "AMARILLO", "modo": "MIXTO_SMART", "usa_chip": "SÍ (Chip H o Botón de Presencia)"
        },
        "Tacoma / Tundra / RAV4 / Corolla Cross (2022-2026)": {
            "espada": "TOY48 Alta Seguridad", "chip": "Sistema Presencia 8A-BA / 4A-BA", "frec": "315 / 433 MHz",
            "riesgo": "ROJO", "modo": "SOLO_SMART_MOD", "usa_chip": "SÍ (Sistema Inteligente de Última Generación)"
        },
    },
    "Honda": {
        "Civic / Accord / CR-V / Integra (1990-2000) [Sin Chip]": {
            "espada": "HON-31 Metálica", "chip": "No utiliza chip (Mecánico)", "frec": "N/A",
            "riesgo": "VERDE", "modo": "SIN_CHIP", "usa_chip": "NO (Llave Metálica Normal)"
        },
        "Civic / CR-V / Accord / Fit / Element / Pilot (2001-2013)": {
            "espada": "HON66 (Regata 4 Pistas)", "chip": "Transponder ID46", "frec": "313.8 / 433.92 MHz",
            "riesgo": "VERDE", "modo": "CHIP_ALTA", "usa_chip": "SÍ (Chip ID46 + Llave de Regata)"
        },
        "CR-V / Civic / HR-V / Fit / Pilot / Odyssey (2014-2021)": {
            "espada": "HON66 (Regata)", "chip": "Transponder G ID47 (Llave o Botón Smart)", "frec": "315 / 433 MHz",
            "riesgo": "AMARILLO", "modo": "MIXTO_SMART", "usa_chip": "SÍ (Chip Criptográfico ID47 / Smart Key)"
        },
        "Civic 11va Gen / CR-V / HR-V / Pilot (2022-2026)": {
            "espada": "HON66", "chip": "Smart Key ID47 / 4A CAN-FD", "frec": "433 MHz",
            "riesgo": "ROJO", "modo": "SOLO_SMART_MOD", "usa_chip": "SÍ (Smart Key con Protocolo Nuevo)"
        },
    },
    "Nissan": {
        "Pick-up D21 / Sentra B13-B14 / Tsuru (1990-2004) [Sin Chip]": {
            "espada": "DA34 Metálica", "chip": "No utiliza chip (Mecánico)", "frec": "N/A",
            "riesgo": "VERDE", "modo": "SIN_CHIP", "usa_chip": "NO (Llave 100% Metálica)"
        },
        "Frontier D22 / Sentra B15-B16 / Tiida / X-Trail / Pathfinder (2001-2012)": {
            "espada": "DA34 / NSN14", "chip": "Transponder ID46", "frec": "315 MHz",
            "riesgo": "VERDE", "modo": "CHIP_NORMAL", "usa_chip": "SÍ (Chip Transponder ID46)"
        },
        "Versa / March / Sentra B17 / NP300 Frontier / Juke / Kicks (2012-2019)": {
            "espada": "DA34 / NSN14", "chip": "ID46 / Hitag AES (Llave o Botón)", "frec": "315 / 433 MHz",
            "riesgo": "VERDE", "modo": "MIXTO_SMART", "usa_chip": "SÍ (Chip ID46/4A o Llave de Presencia)"
        },
        "Rogue T32 / Qashqai / Murano / Maxima Botón (2014-2020)": {
            "espada": "NSN14", "chip": "Smart Key 4A / ID46 (Módulo Delicado)", "frec": "433 MHz",
            "riesgo": "ROJO", "modo": "SOLO_SMART_MOD", "usa_chip": "SÍ (Requiere Revisión Previa de Módulo BCM)"
        },
        "Sentra B18 / Rogue T33 / Kicks / Frontier Nueva (2020-2026)": {
            "espada": "NSN14", "chip": "Smart Key 4A (PIN de 28 Dígitos)", "frec": "433 MHz",
            "riesgo": "ROJO", "modo": "SOLO_SMART_MOD", "usa_chip": "SÍ (Sistema con Módulo Gateway de Seguridad)"
        },
    },
    "Mazda": {
        "Pick-up B2000 / B2200 / 323 / Protegé (1988-1998) [Sin Chip]": {
            "espada": "MZ31 Metálica", "chip": "No utiliza chip (Mecánico)", "frec": "N/A",
            "riesgo": "VERDE", "modo": "SIN_CHIP", "usa_chip": "NO (Llave Metálica Sencilla)"
        },
        "Pick-up B2300 / B2500 / B3000 / BT-50 (1999-2014)": {
            "espada": "MZ31 / MZ27 / H76", "chip": "Transponder 4D63 (40/80 bits)", "frec": "315 / 433 MHz",
            "riesgo": "VERDE", "modo": "CHIP_NORMAL", "usa_chip": "SÍ (Chip 4D63)"
        },
        "Mazda 3 / Mazda 6 / CX-7 / CX-9 / Tribute (2004-2013)": {
            "espada": "MZ31 / MZ24R", "chip": "Transponder 4D63 80 bits", "frec": "315 MHz",
            "riesgo": "VERDE", "modo": "CHIP_NORMAL", "usa_chip": "SÍ (Chip 4D63 de 80 bits)"
        },
        "Mazda 3 / Mazda 2 / CX-5 / CX-3 / CX-9 SkyActiv (2014-2019)": {
            "espada": "MZ24R", "chip": "Smart Key ID49 (Encendido de Botón)", "frec": "315 MHz",
            "riesgo": "VERDE", "modo": "MIXTO_SMART", "usa_chip": "SÍ (Llave Inteligente de Presencia ID49)"
        },
        "Mazda CX-30 / Mazda 3 4ta Gen / CX-50 (2020-2026)": {
            "espada": "MZ24R", "chip": "Smart Key Nueva Generación 6A", "frec": "315 MHz",
            "riesgo": "ROJO", "modo": "SOLO_SMART_MOD", "usa_chip": "SÍ (Sistema de Presencia Encriptado 6A)"
        },
    },
    "Mitsubishi": {
        "Pick-up L200 / Montero / Lancer Antiguo (1990-2000) [Sin Chip]": {
            "espada": "MIT1 / MIT8 Metálica", "chip": "No utiliza chip (Mecánico)", "frec": "N/A",
            "riesgo": "VERDE", "modo": "SIN_CHIP", "usa_chip": "NO (Llave Metálica Normal)"
        },
        "L200 / Montero / Nativa / Lancer / Endeavor (2001-2015)": {
            "espada": "MIT1 / MIT3 / MIT8 / MIT11", "chip": "Transponder ID46", "frec": "315 / 433 MHz",
            "riesgo": "VERDE", "modo": "CHIP_NORMAL", "usa_chip": "SÍ (Chip Transponder ID46)"
        },
        "L200 Sportero / Outlander / ASX / Mirage / Montero Sport (2015-2021)": {
            "espada": "MIT17 / MIT6 / 003L", "chip": "ID46 / ID47 (Llave o Botón Start)", "frec": "315 / 433 MHz",
            "riesgo": "VERDE", "modo": "MIXTO_SMART", "usa_chip": "SÍ (Chip ID46/ID47 o Presencia)"
        },
        "Outlander Nueva Generación (2022-2026)": {
            "espada": "NSN14", "chip": "Smart Key 4A (Plataforma Moderna)", "frec": "433 MHz",
            "riesgo": "ROJO", "modo": "SOLO_SMART_MOD", "usa_chip": "SÍ (Sistema de Presencia de Seguridad Avanzada)"
        },
    },
    "Hyundai / Kia": {
        "Accent / Elantra / Rio / Sephia / Pick-up Porter Antiguo (1995-2005) [Sin Chip]": {
            "espada": "HYN6 / HY15 Metálica", "chip": "No utiliza chip (En versiones US/Latam)", "frec": "N/A",
            "riesgo": "VERDE", "modo": "SIN_CHIP", "usa_chip": "NO (En versión americana/local suele ser metálica)"
        },
        "Tucson / Santa Fe / Elantra / Accent / Sportage / Sorento / Rio / Soul / Forte (2006-2020)": {
            "espada": "HYN6 / HY15 / HY18 / KK12 / 050L", "chip": "ID46 / ID60 / 8A (Llave o Botón)", "frec": "315 / 433 MHz",
            "riesgo": "VERDE", "modo": "MIXTO_SMART", "usa_chip": "SÍ (Algunas versiones US 2011-2019 de llave giratoria no traen chip; las de agencia y botón SÍ)"
        },
        "Camiones H100 Porter / Microbús Starex H1 / Kia K2700 (2010-2021)": {
            "espada": "HYN6 / HY15", "chip": "Transponder ID46 / 4D60", "frec": "433 MHz",
            "riesgo": "AMARILLO", "modo": "CHIP_NORMAL", "usa_chip": "SÍ (Chip Inmovilizador Diesel)"
        },
        "Tucson NX4 / Sportage NQ5 / Creta / Seltos / K5 (2022-2026)": {
            "espada": "KK12 / HY18R Regata", "chip": "Smart Key 8A / 4A CAN-FD", "frec": "433 MHz",
            "riesgo": "ROJO", "modo": "SOLO_SMART_MOD", "usa_chip": "SÍ (Sistema CAN-FD de Nueva Generación)"
        },
    },
    "Ford": {
        "Ranger / F-150 / Explorer / Escape / Focus (1998-2012)": {
            "espada": "Ford 19 / H76", "chip": "Transponder 4D63 (40/80 bits)", "frec": "315 MHz",
            "riesgo": "VERDE", "modo": "CHIP_NORMAL", "usa_chip": "SÍ (Sistema PATS con Chip 4D63)"
        },
        "Focus / Fiesta / Escape / EcoSport / Ranger (2012-2015)": {
            "espada": "HU101 Regata Alta Seguridad", "chip": "Transponder 4D63 80 bits / ID49", "frec": "315 / 433 MHz",
            "riesgo": "VERDE", "modo": "CHIP_ALTA", "usa_chip": "SÍ (Llave de Regata HU101 con Chip)"
        },
        "F-150 / Explorer / Escape / Ranger / Edge (2015-2020)": {
            "espada": "HU101 Regata", "chip": "ID49 Hitag Pro (Navaja o Botón Smart)", "frec": "315 / 433 MHz",
            "riesgo": "AMARILLO", "modo": "MIXTO_SMART", "usa_chip": "SÍ (Chip Criptográfico ID49 o Smart Key)"
        },
        "F-150 / Bronco / Explorer / Ranger Nueva (2021-2026)": {
            "espada": "HU101", "chip": "ID49 Seguridad en Línea", "frec": "315 / 433 MHz",
            "riesgo": "ROJO", "modo": "SOLO_SMART_MOD", "usa_chip": "SÍ (Sistema Bloqueado por Servidor)"
        },
    },
    "Isuzu": {
        "Pick-up Faster / Pup / Camión NPR Antiguo (1988-2002) [Sin Chip]": {
            "espada": "X275 / B113 Metálica", "chip": "No utiliza chip (Mecánico)", "frec": "N/A",
            "riesgo": "VERDE", "modo": "SIN_CHIP", "usa_chip": "NO (Llave 100% Metálica)"
        },
        "Pick-up D-Max / Rodeo / Trooper / MU-X (2003-2019)": {
            "espada": "B111 / ISU5 / D-Max", "chip": "Transponder ID46 / 4D64", "frec": "433 MHz",
            "riesgo": "VERDE", "modo": "CHIP_NORMAL", "usa_chip": "SÍ (Chip ID46 + Opción Control Navaja)"
        },
        "Camiones NPR / NQR / ELF Mediano y Pesado (2003-2022)": {
            "espada": "X275 / ISU5", "chip": "Metálica o Transponder ID46", "frec": "N/A",
            "riesgo": "VERDE", "modo": "CHIP_NORMAL", "usa_chip": "Depende del año (Muchos son metálicos y otros ID46)"
        },
    },
    "Volkswagen": {
        "Jetta A4 (Clásico) / Golf / Beetle / Amarok / Saveiro / Gol (2000-2015)": {
            "espada": "HU66 Regata Alta Seguridad", "chip": "Megamos ID48", "frec": "315 / 434 MHz",
            "riesgo": "AMARILLO", "modo": "CHIP_ALTA", "usa_chip": "SÍ (Chip ID48 + Espada de Regata HU66)"
        },
        "Jetta MK6 / Tiguan / Passat / Amarok (2011-2018)": {
            "espada": "HU66 Regata", "chip": "ID48 Criptográfico (CS)", "frec": "315 / 434 MHz",
            "riesgo": "AMARILLO", "modo": "MIXTO_SMART", "usa_chip": "SÍ (Sistema Inmovilizador en Tablero)"
        },
        "Jetta MK7 / Tiguan / Taos / Teramont (2019-2026)": {
            "espada": "HU162T / HU66", "chip": "Plataforma MQB Digital", "frec": "434 MHz",
            "riesgo": "ROJO", "modo": "SOLO_SMART_MOD", "usa_chip": "SÍ (Plataforma MQB de Alta Seguridad)"
        },
    },
    "Jeep / Dodge / RAM": {
        "Jeep Wrangler / Cherokee / Dodge RAM / Dakota (1998-2007)": {
            "espada": "Y157 / Y159 / Chrysler", "chip": "Transponder ID64 / ID46", "frec": "315 MHz",
            "riesgo": "VERDE", "modo": "CHIP_NORMAL", "usa_chip": "SÍ (Llave Gris/Negra con Chip)"
        },
        "Grand Cherokee / Wrangler / Compass / Patriot / Journey / RAM (2008-2017)": {
            "espada": "Y159 / SIP22 / HU101", "chip": "ID46 (Llave Fobik o Botón)", "frec": "433 MHz",
            "riesgo": "VERDE", "modo": "MIXTO_SMART", "usa_chip": "SÍ (Control Fobik o Smart Key)"
        },
        "Jeep Renegade / Compass / Wrangler JL / RAM 1500 (2018-2026)": {
            "espada": "SIP22 / HU101", "chip": "Smart Key 4A (Con Módulo SGW)", "frec": "433 MHz",
            "riesgo": "ROJO", "modo": "SOLO_SMART_MOD", "usa_chip": "SÍ (Requiere Bypass de Seguridad SGW)"
        },
    },
    "Chevrolet / GM": {
        "Chevy / Aveo / Spark / Corsa / Pick-up S10 / Silverado (1998-2012)": {
            "espada": "GM-26V / B111 / DWO4R", "chip": "ID46 / ID48 (o Metálica en básicos)", "frec": "315 MHz",
            "riesgo": "VERDE", "modo": "CHIP_NORMAL", "usa_chip": "SÍ (Chip Transponder)"
        },
        "Cruze / Sonic / Trax / Equinox / Malibu / Colorado / Silverado (2011-2019)": {
            "espada": "HU100 Regata", "chip": "ID46 Extended (Navaja o Botón)", "frec": "315 / 433 MHz",
            "riesgo": "VERDE", "modo": "MIXTO_SMART", "usa_chip": "SÍ (Llave Navaja HU100 o Presencia)"
        },
        "Silverado / Tahoe / Tracker / Onix / Groove (2020-2026)": {
            "espada": "HU100", "chip": "Smart Key 4A CAN-FD", "frec": "433 MHz",
            "riesgo": "ROJO", "modo": "SOLO_SMART_MOD", "usa_chip": "SÍ (Protocolo CAN-FD)"
        },
    },
    "Suzuki": {
        "Samurai / Sidekick / Vitara / Swift / Alto Antiguo (1990-2004) [Sin Chip]": {
            "espada": "Suzuki Derecha / SUZ11", "chip": "No utiliza chip (Mecánico)", "frec": "N/A",
            "riesgo": "VERDE", "modo": "SIN_CHIP", "usa_chip": "NO (Llave Metálica Sencilla)"
        },
        "Grand Vitara / Swift / SX4 / Jimny / Celerio / Ertiga (2005-2022)": {
            "espada": "SUZ11 / HU133R", "chip": "ID46 / ID47 (Llave o Botón)", "frec": "315 / 433 MHz",
            "riesgo": "VERDE", "modo": "MIXTO_SMART", "usa_chip": "SÍ (Chip ID46/ID47 o Presencia)"
        },
    }
}

# ==============================================================================
# 3. MUNICIPIOS DE ORIENTE (KILÓMETROS IDA Y VUELTA DESDE SAN LUIS JILOTEPEQUE)
#    Nota interna: Ya están puestos al DOBLE (Ida y Vuelta) en la lista.
#    Si quieres ajustar el cobro general, cambia MULTIPLICADOR_COMBUSTIBLE.
# ==============================================================================
MULTIPLICADOR_COMBUSTIBLE = 1.0  # Con 1.0 cobra exacto el Ida y Vuelta de abajo; con 2.0 cobra el doble

DISTANCIAS_KM_ORIENTE = {
    "Jalapa": {
        "San Luis Jilotepeque (Sede Central - Casco Urbano)": 0,
        "San Pedro Pinula": 40,
        "San Manuel Chaparrón": 44,
        "Monjas": 76,
        "Jalapa (Cabecera)": 84,
        "San Carlos Alzatate": 124,
        "Mataquescuintla": 160
    },
    "Chiquimula": {
        "Ipala": 36,
        "Quezaltepeque": 68,
        "San Jacinto": 72,
        "San José La Arada": 76,
        "Chiquimula (Cabecera)": 88,
        "San Esteban": 96,
        "San Juan Ermita": 104,
        "Concepción Las Minas": 108,
        "Jocotán": 120,
        "Camotán": 124,
        "Esquipulas": 128,
        "Olopa": 136
    },
    "Jutiapa": {
        "Agua Blanca": 56,
        "Santa Catarina Mita": 76,
        "El Progreso": 100,
        "Asunción Mita": 108,
        "Jutiapa (Cabecera)": 128,
        "Atescatempa": 144,
        "Yupiltepeque": 152,
        "Zapotitlán": 160,
        "El Adelanto": 164,
        "Quesada": 164,
        "Jerez": 170,
        "San José Acatempa": 184,
        "Comapa": 192,
        "Jalpatagua": 200,
        "Conguaco": 220,
        "Moyuta": 230,
        "Pasaco": 260
    },
    "Zacapa": {
        "Estanzuela": 124,
        "Zacapa (Cabecera)": 136,
        "San Jorge": 144,
        "Río Hondo": 148,
        "Huité": 156,
        "Cabañas": 164,
        "Teculután": 168,
        "Usumatlán": 176,
        "San Diego": 180,
        "Gualán": 204,
        "La Unión": 216
    }
}

# ==============================================================================
# 4. BASE DE DATOS INTERNA DEL INVENTARIO 2027 (USO EXCLUSIVO TALLER)
# ==============================================================================
if "inv_2027" not in st.session_state:
    st.session_state.inv_2027 = pd.DataFrame([
        # RESIDENCIAL
        {"Categoría": "Residencial", "Marca": "Kwikset", "Producto": "Llave ND larga", "Stock_Inicial": 20, "Existencia": 20, "Usadas": 0, "Costo_Q": 5.0, "Precio_Q": 15.0},
        {"Categoría": "Residencial", "Marca": "Schlage", "Producto": "Llave SC1", "Stock_Inicial": 10, "Existencia": 10, "Usadas": 0, "Costo_Q": 5.0, "Precio_Q": 15.0},
        {"Categoría": "Residencial", "Marca": "Kwikset", "Producto": "Llave KW1 corta", "Stock_Inicial": 10, "Existencia": 10, "Usadas": 0, "Costo_Q": 5.0, "Precio_Q": 15.0},
        {"Categoría": "Residencial", "Marca": "Yale R8", "Producto": "Larga", "Stock_Inicial": 15, "Existencia": 12, "Usadas": 3, "Costo_Q": 5.0, "Precio_Q": 15.0},
        {"Categoría": "Residencial", "Marca": "Yale Y1", "Producto": "Corta", "Stock_Inicial": 35, "Existencia": 35, "Usadas": 0, "Costo_Q": 5.0, "Precio_Q": 15.0},
        {"Categoría": "Residencial", "Marca": "Alba", "Producto": "Y1 larga", "Stock_Inicial": 14, "Existencia": 14, "Usadas": 0, "Costo_Q": 5.0, "Precio_Q": 15.0},
        # CARRO / CAMIÓN METÁLICA
        {"Categoría": "Carro/Camión Metálica", "Marca": "Toyota", "Producto": "TR40 Metálica", "Stock_Inicial": 30, "Existencia": 24, "Usadas": 6, "Costo_Q": 15.0, "Precio_Q": 45.0},
        {"Categoría": "Carro/Camión Metálica", "Marca": "Toyota", "Producto": "TR47 Metálica", "Stock_Inicial": 15, "Existencia": 8, "Usadas": 7, "Costo_Q": 15.0, "Precio_Q": 45.0},
        {"Categoría": "Carro/Camión Metálica", "Marca": "Honda", "Producto": "Honda -31 Metálica", "Stock_Inicial": 15, "Existencia": 11, "Usadas": 4, "Costo_Q": 15.0, "Precio_Q": 45.0},
        {"Categoría": "Carro/Camión Metálica", "Marca": "Nissan", "Producto": "DA34 Metálica", "Stock_Inicial": 10, "Existencia": 7, "Usadas": 3, "Costo_Q": 15.0, "Precio_Q": 45.0},
        {"Categoría": "Carro/Camión Metálica", "Marca": "Freightliner", "Producto": "FRE-1 Camión", "Stock_Inicial": 10, "Existencia": 9, "Usadas": 1, "Costo_Q": 15.0, "Precio_Q": 45.0},
        {"Categoría": "Carro/Camión Metálica", "Marca": "Hino", "Producto": "X274 / HN3 Camión", "Stock_Inicial": 10, "Existencia": 10, "Usadas": 0, "Costo_Q": 15.0, "Precio_Q": 45.0},
        {"Categoría": "Carro/Camión Metálica", "Marca": "Isuzu", "Producto": "X275 / B113 Camión", "Stock_Inicial": 12, "Existencia": 10, "Usadas": 2, "Costo_Q": 15.0, "Precio_Q": 45.0},
        {"Categoría": "Carro/Camión Metálica", "Marca": "Kenworth", "Producto": "K1994 / B87 Camión", "Stock_Inicial": 5, "Existencia": 5, "Usadas": 0, "Costo_Q": 15.0, "Precio_Q": 45.0},
        # MOTO
        {"Categoría": "Moto", "Marca": "Honda", "Producto": "HD75 / 4I", "Stock_Inicial": 28, "Existencia": 15, "Usadas": 13, "Costo_Q": 15.0, "Precio_Q": 30.0},
        {"Categoría": "Moto", "Marca": "Honda", "Producto": "Navy 36-p1", "Stock_Inicial": 8, "Existencia": 3, "Usadas": 5, "Costo_Q": 15.0, "Precio_Q": 30.0},
        {"Categoría": "Moto", "Marca": "Suzuki", "Producto": "X179 / SUZ12", "Stock_Inicial": 30, "Existencia": 30, "Usadas": 0, "Costo_Q": 15.0, "Precio_Q": 30.0},
        {"Categoría": "Moto", "Marca": "Yamaha", "Producto": "YH48 NP / YAMA-19I", "Stock_Inicial": 10, "Existencia": 10, "Usadas": 0, "Costo_Q": 15.0, "Precio_Q": 30.0},
        {"Categoría": "Moto", "Marca": "Pulsar / Bajaj", "Producto": "4 BAJ-3P / Discover", "Stock_Inicial": 9, "Existencia": 9, "Usadas": 0, "Costo_Q": 15.0, "Precio_Q": 30.0},
        # LLAVES CON CHIP DEDICADAS
        {"Categoría": "Llaves con Chip", "Marca": "Toyota", "Producto": "TR47 TEXAS ID 4D67", "Stock_Inicial": 5, "Existencia": 5, "Usadas": 0, "Costo_Q": 60.0, "Precio_Q": 300.0},
        {"Categoría": "Llaves con Chip", "Marca": "Toyota", "Producto": "TR47 TEXAS ID 4D72 80 BITS G", "Stock_Inicial": 12, "Existencia": 12, "Usadas": 0, "Costo_Q": 60.0, "Precio_Q": 300.0},
        {"Categoría": "Llaves con Chip", "Marca": "Toyota", "Producto": "TR47 TEXAS ID 4D74 128 BITS H", "Stock_Inicial": 5, "Existencia": 5, "Usadas": 0, "Costo_Q": 60.0, "Precio_Q": 300.0},
        {"Categoría": "Llaves con Chip", "Marca": "Toyota", "Producto": "TR48 TEXAS ID 4D74 128 BITS H", "Stock_Inicial": 8, "Existencia": 8, "Usadas": 0, "Costo_Q": 60.0, "Precio_Q": 300.0},
        {"Categoría": "Llaves con Chip", "Marca": "Honda", "Producto": "HON66 HO01 ID46", "Stock_Inicial": 12, "Existencia": 12, "Usadas": 0, "Costo_Q": 60.0, "Precio_Q": 300.0},
        {"Categoría": "Llaves con Chip", "Marca": "Honda", "Producto": "HON66 HO01 ID47", "Stock_Inicial": 2, "Existencia": 2, "Usadas": 0, "Costo_Q": 60.0, "Precio_Q": 300.0},
        {"Categoría": "Llaves con Chip", "Marca": "Mitsubishi", "Producto": "MIT3 ID46 A", "Stock_Inicial": 7, "Existencia": 7, "Usadas": 0, "Costo_Q": 60.0, "Precio_Q": 300.0},
        {"Categoría": "Llaves con Chip", "Marca": "Nissan", "Producto": "DA34 ID46", "Stock_Inicial": 4, "Existencia": 4, "Usadas": 0, "Costo_Q": 60.0, "Precio_Q": 300.0},
        {"Categoría": "Llaves con Chip", "Marca": "Mazda", "Producto": "H76 TEXAS 4D63 80 BITS MZ02", "Stock_Inicial": 4, "Existencia": 4, "Usadas": 0, "Costo_Q": 60.0, "Precio_Q": 300.0},
        # LLAVES HUECAS
        {"Categoría": "Llaves Huecas", "Marca": "Toyota", "Producto": "TR47 Hueca", "Stock_Inicial": 28, "Existencia": 23, "Usadas": 5, "Costo_Q": 35.0, "Precio_Q": 175.0},
        {"Categoría": "Llaves Huecas", "Marca": "Honda", "Producto": "HON66 Hueca", "Stock_Inicial": 23, "Existencia": 19, "Usadas": 4, "Costo_Q": 35.0, "Precio_Q": 175.0},
        {"Categoría": "Llaves Huecas", "Marca": "Ford", "Producto": "HU101 Hueca", "Stock_Inicial": 7, "Existencia": 5, "Usadas": 2, "Costo_Q": 35.0, "Precio_Q": 175.0},
        {"Categoría": "Llaves Huecas", "Marca": "Isuzu", "Producto": "B111 Hueca", "Stock_Inicial": 3, "Existencia": 3, "Usadas": 0, "Costo_Q": 35.0, "Precio_Q": 175.0},
        # CHIPS Y PINES
        {"Categoría": "Chips y Pines", "Marca": "XHORSE", "Producto": "Super Chip XT27A", "Stock_Inicial": 104, "Existencia": 56, "Usadas": 48, "Costo_Q": 25.0, "Precio_Q": 100.0},
        {"Categoría": "Chips y Pines", "Marca": "XHORSE", "Producto": "Chip XT57B", "Stock_Inicial": 10, "Existencia": 10, "Usadas": 0, "Costo_Q": 25.0, "Precio_Q": 100.0},
        {"Categoría": "Chips y Pines", "Marca": "PINES", "Producto": "Pin de Acero Fijación Espada", "Stock_Inicial": 345, "Existencia": 345, "Usadas": 0, "Costo_Q": 5.0, "Precio_Q": 15.0},
        # CONTROLES
        {"Categoría": "Controles", "Marca": "XHORSE", "Producto": "PRESENCIA (NARANJA)", "Stock_Inicial": 15, "Existencia": 14, "Usadas": 1, "Costo_Q": 350.0, "Precio_Q": 1200.0},
        {"Categoría": "Controles", "Marca": "XHORSE", "Producto": "PRESENCIA XM38 TOYOTA", "Stock_Inicial": 11, "Existencia": 11, "Usadas": 0, "Costo_Q": 450.0, "Precio_Q": 1300.0},
        {"Categoría": "Controles", "Marca": "AUTEL", "Producto": "PRESENCIA ROJOS IKEY", "Stock_Inicial": 2, "Existencia": 2, "Usadas": 0, "Costo_Q": 450.0, "Precio_Q": 1200.0},
        {"Categoría": "Controles", "Marca": "XHORSE", "Producto": "WIRE (ROJO) Navaja 10 estilos", "Stock_Inicial": 32, "Existencia": 22, "Usadas": 10, "Costo_Q": 150.0, "Precio_Q": 650.0},
        {"Categoría": "Controles", "Marca": "XHORSE", "Producto": "WIRELESS (AZUL) 6 estilos", "Stock_Inicial": 15, "Existencia": 14, "Usadas": 1, "Costo_Q": 175.0, "Precio_Q": 650.0},
        {"Categoría": "Controles", "Marca": "XHORSE", "Producto": "SUPERMODEL (MORADO) 4 estilos", "Stock_Inicial": 9, "Existencia": 9, "Usadas": 0, "Costo_Q": 175.0, "Precio_Q": 650.0},
        {"Categoría": "Controles", "Marca": "KEYDIY", "Producto": "CELESTE 2 estilos", "Stock_Inicial": 20, "Existencia": 18, "Usadas": 2, "Costo_Q": 150.0, "Precio_Q": 650.0},
        {"Categoría": "Controles", "Marca": "KEYDIY", "Producto": "ROJOS KD", "Stock_Inicial": 9, "Existencia": 9, "Usadas": 0, "Costo_Q": 125.0, "Precio_Q": 650.0},
        {"Categoría": "Controles", "Marca": "Toyota OEM", "Producto": "Diamante 3B / 4B / Cuadrado", "Stock_Inicial": 20, "Existencia": 19, "Usadas": 1, "Costo_Q": 350.0, "Precio_Q": 650.0},
        {"Categoría": "Controles", "Marca": "Honda OEM", "Producto": "3B / 4B Espadín (313.8/315/434)", "Stock_Inicial": 11, "Existencia": 10, "Usadas": 1, "Costo_Q": 350.0, "Precio_Q": 600.0},
        # CARCASAS, BATERÍAS Y ESPADAS
        {"Categoría": "Carcasas", "Marca": "Honda / Toyota", "Producto": "Carcasa Control (3B / 4B / Diamante)", "Stock_Inicial": 32, "Existencia": 22, "Usadas": 10, "Costo_Q": 40.0, "Precio_Q": 200.0},
        {"Categoría": "Baterías", "Marca": "Litio", "Producto": "Batería Litio CR2032 / CR1616 / CR2025", "Stock_Inicial": 175, "Existencia": 132, "Usadas": 43, "Costo_Q": 10.0, "Precio_Q": 30.0},
        {"Categoría": "Espadas e Insertos", "Marca": "Multimarca", "Producto": "Espada / Inserto Virgen para Control o Smart Key", "Stock_Inicial": 315, "Existencia": 295, "Usadas": 20, "Costo_Q": 21.0, "Precio_Q": 80.0}
    ])

# ==============================================================================
# 5. ENCABEZADO HERO Y BARRA LATERAL CON SERVICIOS Y GOOGLE BUSINESS
# ==============================================================================
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🔑 CERRAJERÍA AUTOMOTRIZ ELÍAS</div>
    <div class="hero-subtitle">
        Laboratorio Móvil de Programación de Llaves con Chip, Controles de Presencia (Smart Key), Conversiones Tipo Navaja y Aperturas Sin Daño en <b>Jalapa, Chiquimula, Jutiapa y Zacapa</b>.
    </div>
    <span class="badge-tech">🔑 Programación de Chips y Controles</span>
    <span class="badge-tech">🗝️ Corte de Llaves de Alta Precisión</span>
    <span class="badge-tech">🚗 Apertura de Vehículos Sin Daño</span>
    <span class="badge-tech">🔪 Conversión a Control Tipo Navaja</span>
    <span class="badge-tech">🔋 Servicio de Jumper y Protección de Voltaje</span>
    <span class="badge-orange">📍 Servicio a Domicilio 24/7: +502 5191-6984</span>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# CUADRO 2: BIENVENIDA CON NOMBRE / ALIAS Y CONTADOR DE VISITAS
# ==============================================================================
if "alias_usuario" not in st.session_state:
    st.session_state.alias_usuario = ""

if st.session_state.alias_usuario == "":
    st.markdown('<div class="glass-card" style="max-width:540px; margin:auto; text-align:center;">', unsafe_allow_html=True)
    st.markdown("### 👋 ¡Bienvenido a Cerrajería Automotriz Elías!")
    st.write("Escribe tu **Nombre o Alias** para ingresar al Cotizador y Catálogo en línea:")
    alias_input = st.text_input("Tu Nombre o Alias:", max_chars=30, placeholder="Ej. Carlos / Taller El Progreso")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("🚀 Entrar al Cotizador", type="primary", use_container_width=True):
            if alias_input.strip() != "":
                st.session_state.alias_usuario = alias_input.strip()
                registro_app["clientes"].append({
                    "Fecha y Hora": st.session_state.hora_entrada,
                    "Nombre / Alias": st.session_state.alias_usuario,
                    "Teléfono": "En cotización",
                    "Vehículo / Consulta": "Ingresó al sistema"
                })
                st.rerun()
            else:
                st.warning("Escribe un nombre o alias corto, o toca 'Entrar como Invitado'.")
    with col_b2:
        if st.button("👀 Entrar como Invitado", use_container_width=True):
            st.session_state.alias_usuario = "Invitado"
            registro_app["clientes"].append({
                "Fecha y Hora": st.session_state.hora_entrada,
                "Nombre / Alias": "Invitado",
                "Teléfono": "En cotización",
                "Vehículo / Consulta": "Ingresó al sistema"
            })
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()
else:
    st.caption(f"👤 Conectado como: **{st.session_state.alias_usuario}** | 🔥 Visitas en línea: **{registro_app['visitas']}**")

with st.sidebar:
    st.markdown("### 🌐 Nuestras Redes Oficiales")
    st.caption("Síguenos, califícanos y escríbenos directo:")
    st.markdown('<a class="social-btn" style="background:#25D366;" href="https://wa.link/77nelo" target="_blank">💬 WhatsApp Directo (+502 5191-6984)</a>', unsafe_allow_html=True)
    st.markdown('<a class="social-btn" style="background:#EA4335; border:1px solid #FBBF24;" href="https://www.google.com/maps/search/?api=1&query=Cerrajeria+Automotriz+Elias" target="_blank">📍 Google Business / Maps (Cerrajería Elías)</a>', unsafe_allow_html=True)
    st.markdown('<a class="social-btn" style="background:#000000; border:1px solid #38BDF8;" href="https://www.tiktok.com/@cerrajeria_auto_elias" target="_blank">🎵 TikTok (@cerrajeria_auto_elias)</a>', unsafe_allow_html=True)
    st.markdown('<a class="social-btn" style="background:#1877F2;" href="https://www.facebook.com/search/top?q=Cerrajeria%20Automotriz%20Elias" target="_blank">📘 Facebook (Cerrajería Automotriz Elias)</a>', unsafe_allow_html=True)
    st.markdown('<a class="social-btn" style="background:linear-gradient(45deg,#F58529,#DD2A7B,#8134AF);" href="https://www.instagram.com/cerrajeria_auto_elias/" target="_blank">📸 Instagram (@cerrajeria_auto_elias)</a>', unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("### 🛠️ Nuestros Servicios")
    st.markdown("""
    * 🚗 **Apertura de vehículos** sin rayar pintura ni doblar puertas.
    * 🔑 **Duplicado y hechura desde cero** de llaves con chip y metálicas.
    * 📡 **Llaves de Presencia (Smart Key)** para encendido de botón.
    * 🔪 **Conversión a Control Navaja** retráctil moderno.
    * 🔄 **Cambio de combinación** y borrado electrónico de llaves robadas.
    * 🧩 **Cambio de carcasas rotas**, botones, espadines y baterías de litio.
    * 🔋 **Servicio de Jumper (Paso de corriente)**, diagnóstico electrónico y protección de voltaje.
    """)
    st.write("---")
    st.markdown("### 📍 Cobertura en Oriente")
    st.caption("Atendemos en taller y a domicilio en todos los municipios de:")
    st.markdown("**• Jalapa • Chiquimula • Jutiapa • Zacapa**")
    st.markdown("### 🚘 Marcas que Trabajamos")
    st.caption("Toyota • Honda • Nissan • Mazda • Mitsubishi • Hyundai • Kia • Ford • Isuzu • Volkswagen • Jeep • Dodge • RAM • Chevrolet • Suzuki • Motos y Camiones.")

# ==============================================================================
# 6. PESTAÑAS PRINCIPALES DE NAVEGACIÓN (4 PESTAÑAS)
# ==============================================================================
tab_cotizador, tab_catalogo, tab_buscador, tab_admin = st.tabs([
    "⚡ 1. Cotizador Inteligente & Agendar Cita",
    "🚘 2. Catálogo de Llaves & Biblioteca Interactiva",
    "🔍 3. ¿Mi Carro Usa Chip? (Consulta tu Vehículo)",
    "🔐 4. Panel de Taller & Inventario (Admin)"
])

# ==============================================================================
# PESTAÑA 1: COTIZADOR INTELIGENTE + FILTRO AUTOMÁTICO + TRASLADO INTERNO
# ==============================================================================
with tab_cotizador:
    st.subheader("🧮 Configura tu Vehículo, Revisa tu Desglose Exacto y Agenda tu Cita")
    st.write("Selecciona tu vehículo y el trabajo que necesitas. El sistema filtra automáticamente las opciones reales para tu modelo y detalla exactamente qué materiales y programación utilizaremos.")

    col_form, col_recibo = st.columns([1.18, 0.98], gap="large")

    with col_form:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Paso 1: ¿Qué deseas cotizar hoy?")
        tipo_bien = st.radio(
            "Categoría del Servicio:",
            ["🚗 Carro / Pick-up / Camioneta", "🏍️ Motocicleta / Cuatrimoto", "🚛 Camión Pesado (Hino/Isuzu/Freightliner)", "🏠 Casa / Chapa Residencial"],
            horizontal=True
        )

        desglose_items = []
        ficha_tecnica = {}
        alerta_tecnica = "VERDE"
        descripcion_vehiculo = ""

        # --- LÓGICA A: CARROS / PICK-UPS / CAMIONETAS ---
        if tipo_bien == "🚗 Carro / Pick-up / Camioneta":
            c1, c2 = st.columns([0.9, 2.3])
            with c1:
                marca_sel = st.selectbox("Marca:", list(CATALOGO_VEHICULOS.keys()))
            with c2:
                modelo_sel = st.selectbox("Modelo, Línea y Años:", list(CATALOGO_VEHICULOS[marca_sel].keys()))
            
            ficha_tecnica = CATALOGO_VEHICULOS[marca_sel][modelo_sel]
            alerta_tecnica = ficha_tecnica["riesgo"]
            modo_vehiculo = ficha_tecnica["modo"]
            espada_corta = ficha_tecnica["espada"].split()[0]
            descripcion_vehiculo = f"{marca_sel} — {modelo_sel}"

            st.info(f"🔧 **Ficha de tu Vehículo:** Espada `{ficha_tecnica['espada']}` | Sistema `{ficha_tecnica['chip']}` | Frecuencia `{ficha_tecnica['frec']}`")

            situaciones_disponibles = [
                "Tengo una llave que sí funciona y quiero SACAR COPIA (Duplicado)",
                "PERDÍ TODAS LAS LLAVES (El vehículo está sin llaves - Hacer desde cero)",
                "Me robaron o extravié una llave y quiero CAMBIAR COMBINACIÓN / BORRAR LLAVE ROBADA",
                "Solo necesito ABRIR mi vehículo (Dejé las llaves adentro)",
                "Mi control o llave falló (Cambio de Carcasa / Batería / Espada rota / Reprogramación)",
                "Necesito Servicio de Jumper (Paso de Corriente por Batería Descargada) o Diagnóstico"
            ]
            if modo_vehiculo in ["SIN_CHIP", "CHIP_NORMAL", "CHIP_ALTA", "MIXTO_SMART"]:
                situaciones_disponibles.insert(1, "Quiero MODERNIZAR mi llave actual a Control Tipo Navaja Retráctil")

            situacion_llave = st.selectbox("¿Cuál es tu situación actual?", situaciones_disponibles)

            # 1) DUPLICADO / SACAR COPIA (FILTRADO SEGÚN LA REALIDAD DEL CARRO)
            if "SACAR COPIA" in situacion_llave:
                if modo_vehiculo == "SIN_CHIP":
                    opciones_copia = [
                        "Llave 100% Metálica Normal (Este vehículo no requiere chip inmovilizador)"
                    ]
                elif modo_vehiculo == "CHIP_NORMAL":
                    opciones_copia = [
                        "Llave con Chip Estándar (Sin botones de control) — Económica y resistente",
                        "Control Tipo Navaja Retráctil con Botones + Chip Programado",
                        "Control con Espadín Estilo Original de Agencia + Chip Programado",
                        "Llave 100% Metálica Sencilla (Solo para abrir puertas o versión sin inmovilizador)"
                    ]
                elif modo_vehiculo == "CHIP_ALTA":
                    opciones_copia = [
                        "Llave con Chip de Alta Seguridad / Regata (Sin botones de control)",
                        "Control Tipo Navaja Retráctil con Botones + Chip de Alta Seguridad",
                        "Control con Espadín Estilo Original de Agencia + Chip Programado"
                    ]
                elif modo_vehiculo == "MIXTO_SMART":
                    if marca_sel == "Toyota":
                        opciones_copia = [
                            "Llave Inteligente de Presencia Toyota (Para encendido de botón Start/Stop)",
                            "Control Tipo Navaja Retráctil con Botones + Chip (Para versión de llave giratoria)",
                            "Control con Espadín Estilo Original + Chip (Para versión de llave giratoria)",
                            "Llave con Chip de Alta Seguridad (Sin botones de control)"
                        ]
                    else:
                        opciones_copia = [
                            "Llave Inteligente de Presencia (Para encendido de botón Start/Stop)",
                            "Control Tipo Navaja Retráctil con Botones + Chip (Para versión de llave giratoria)",
                            "Control con Espadín Estilo Original + Chip (Para versión de llave giratoria)",
                            "Llave con Chip de Alta Seguridad (Sin botones de control)"
                        ]
                else: # SOLO_SMART_MOD
                    if marca_sel == "Toyota":
                        opciones_copia = ["Llave Inteligente de Presencia Toyota (Para encendido de botón Start/Stop)"]
                    else:
                        opciones_copia = ["Llave Inteligente de Presencia Smart Key (Para encendido de botón Start/Stop)"]

                estilo_copia = st.selectbox("Elige el tipo de llave o control que necesitas:", opciones_copia)

                if "100% Metálica" in estilo_copia:
                    desglose_items = [
                        (f"Llave Metálica Automotriz Virgen (Perfil {espada_corta})", 35.0),
                        ("Tallado y Corte de Llave de Alta Precisión", 30.0)
                    ]
                elif "Chip Estándar" in estilo_copia:
                    desglose_items = [
                        (f"Llave Automotriz con Cabeza Plástica (Perfil {espada_corta})", 75.0),
                        (f"Chip Transponder Nuevo ({ficha_tecnica['chip']})", 95.0),
                        ("Tallado y Corte de Llave de Alta Precisión", 45.0),
                        ("Programación de Inmovilizador por Escáner + Protección de Voltaje", 85.0)
                    ]
                elif "Chip de Alta Seguridad" in estilo_copia:
                    desglose_items = [
                        (f"Llave de Alta Seguridad / Regata (Perfil {espada_corta})", 85.0),
                        (f"Chip Transponder Criptográfico ({ficha_tecnica['chip']})", 125.0),
                        ("Tallado Computarizado de Precisión en Pista Especial", 65.0),
                        ("Programación Electrónica de Inmovilizador + Protección de Voltaje", 100.0)
                    ]
                elif "Control Tipo Navaja" in estilo_copia:
                    desglose_items = [
                        (f"Módulo de Control Tipo Navaja Retráctil ({ficha_tecnica['frec']})", 260.0),
                        (f"Espada / Inserto Metálico ({espada_corta}) + Tallado de Alta Precisión", 85.0),
                        (f"Chip Transponder Programable Nuevo ({ficha_tecnica['chip']})", 110.0),
                        ("Pin de Acero de Fijación de Espada (Pasador)", 15.0),
                        ("Batería de Litio CR2032 Instalada y Comprobada", 30.0),
                        ("Configuración de Frecuencia y Programación en el Vehículo", 150.0)
                    ]
                elif "Estilo Original" in estilo_copia:
                    desglose_items = [
                        (f"Control con Espadín Estilo Original de Agencia ({ficha_tecnica['frec']})", 340.0),
                        (f"Chip Transponder Integrado ({ficha_tecnica['chip']}) + Batería de Litio", 90.0),
                        (f"Tallado y Corte de Llave de Alta Precisión ({espada_corta})", 70.0),
                        ("Sincronización de Control Remoto e Inmovilizador", 150.0)
                    ]
                elif "Presencia Toyota" in estilo_copia:
                    desglose_items = [
                        (f"Llave Inteligente de Presencia Toyota ({ficha_tecnica['frec']})", 760.0),
                        (f"Inserto Metálico de Emergencia ({espada_corta}) + Tallado de Precisión", 95.0),
                        ("Batería de Litio CR2032 Instalada y Comprobación de Frecuencia", 35.0),
                        ("Protección Electrónica de Voltaje de Batería", 70.0),
                        ("Programación de Sistema de Proximidad e Inmovilizador", 340.0)
                    ]
                else:
                    desglose_items = [
                        (f"Llave Inteligente de Presencia Smart Key ({ficha_tecnica['chip']})", 680.0),
                        (f"Inserto Metálico de Emergencia ({espada_corta}) + Tallado de Precisión", 95.0),
                        ("Batería de Litio CR2032 de Alto Rendimiento Instalada", 35.0),
                        ("Protección Electrónica de Voltaje de Batería", 70.0),
                        ("Programación de Proximidad e Inmovilizador en el Vehículo", 320.0)
                    ]

            # 2) MODERNIZAR A CONTROL NAVAJA REUTILIZANDO EL CHIP ACTUAL
            elif "MODERNIZAR" in situacion_llave:
                desglose_items = [
                    (f"Módulo de Control Tipo Navaja Retráctil ({ficha_tecnica['frec']})", 220.0),
                    (f"Espada / Inserto Metálico ({espada_corta}) + Tallado de Alta Precisión", 75.0),
                    ("Pin de Acero de Fijación + Traslado/Adaptación de tu Chip Actual", 35.0),
                    ("Batería de Litio CR2032 Nueva Instalada", 30.0),
                    ("Programación de Cierre Centralizado en el Vehículo", 65.0)
                ]

            # 3) PERDÍ TODAS LAS LLAVES (PREGUNTA SI ESTÁ ABIERTO O CERRADO + FILTRO DE LLAVE)
            elif "PERDÍ TODAS LAS LLAVES" in situacion_llave:
                estado_puertas_akl = st.radio(
                    "🚪 ¿Cómo se encuentra tu vehículo en este momento?",
                    [
                        "🔒 El vehículo está CERRADO (Necesito abrirlo sin daño + hacer la llave desde cero)",
                        "🔓 El vehículo ya está ABIERTO (Solo necesito lectura de combinación y hacer la llave)"
                    ]
                )
                carro_cerrado = "CERRADO" in estado_puertas_akl

                if modo_vehiculo == "SIN_CHIP":
                    opciones_akl = ["Hechura de Llave Metálica desde Cero (Vehículo sin chip inmovilizador)"]
                elif modo_vehiculo == "CHIP_NORMAL":
                    opciones_akl = [
                        "Hechura desde Cero de Llave con Chip Estándar (Sin botones)",
                        "Hechura desde Cero Entregando Control Tipo Navaja o Control Original con Chip"
                    ]
                elif modo_vehiculo == "CHIP_ALTA":
                    opciones_akl = [
                        "Hechura desde Cero de Llave con Chip de Alta Seguridad / Regata",
                        "Hechura desde Cero Entregando Control Tipo Navaja o Control Original con Chip"
                    ]
                elif modo_vehiculo == "MIXTO_SMART":
                    if marca_sel == "Toyota":
                        opciones_akl = [
                            "Hechura desde Cero de Llave de Presencia Toyota (Encendido de Botón Start/Stop)",
                            "Hechura desde Cero de Llave con Chip de Alta Seguridad (Encendido de Llave)",
                            "Hechura desde Cero Entregando Control Navaja o Control Original con Chip"
                        ]
                    else:
                        opciones_akl = [
                            "Hechura desde Cero de Llave de Presencia Smart Key (Encendido de Botón Start/Stop)",
                            "Hechura desde Cero de Llave con Chip (Encendido de Llave Giratoria)",
                            "Hechura desde Cero Entregando Control Navaja o Control Original con Chip"
                        ]
                else: # SOLO_SMART_MOD
                    if marca_sel == "Toyota":
                        opciones_akl = ["Hechura desde Cero de Llave de Presencia Toyota (Encendido de Botón Start/Stop)"]
                    else:
                        opciones_akl = ["Hechura desde Cero de Llave de Presencia Smart Key (Encendido de Botón Start/Stop)"]

                estilo_akl = st.selectbox("Selecciona qué llave o control necesitas que fabriquemos desde cero:", opciones_akl)

                if "Metálica desde Cero" in estilo_akl:
                    desglose_items = [
                        ("Apertura Sin Daño y Lectura Mecánica de Combinación de Chapa" if carro_cerrado else "Lectura Mecánica y Decodificación de Combinación de Chapa (Vehículo Abierto)", 150.0 if carro_cerrado else 100.0),
                        (f"Llave Metálica Virgen ({espada_corta}) + Tallado Exacto desde Cero", 150.0)
                    ]
                elif "Chip Estándar" in estilo_akl:
                    desglose_items = [
                        ("Apertura Técnica Sin Daño y Lectura de Alturas de Cerradura" if carro_cerrado else "Lectura de Alturas y Decodificación de Cerradura (Vehículo Abierto)", 180.0 if carro_cerrado else 100.0),
                        (f"Decodificación Mecánica y Tallado de Llave ({espada_corta}) desde Cero", 120.0),
                        (f"Llave Automotriz + Chip Transponder Nuevo ({ficha_tecnica['chip']})", 140.0),
                        ("Protección de Voltaje + Programación de Inmovilizador desde Cero", 260.0)
                    ]
                elif "Control Tipo Navaja" in estilo_akl or "Control Navaja" in estilo_akl:
                    desglose_items = [
                        ("Apertura Sin Daño y Lectura Mecánica de Cilindro" if carro_cerrado else "Lectura Mecánica y Decodificación de Cilindro (Vehículo Abierto)", 200.0 if carro_cerrado else 120.0),
                        (f"Control Tipo Navaja / Original ({ficha_tecnica['frec']}) + Inserto ({espada_corta}) Tallado", 410.0),
                        (f"Chip Transponder ({ficha_tecnica['chip']}) + Pin de Acero + Batería CR2032", 160.0),
                        ("Protección de Voltaje + Programación de Arranque y Control Remoto", 330.0)
                    ]
                elif "Presencia Toyota" in estilo_akl:
                    desglose_items = [
                        ("Apertura Profesional Sin Daño y Lectura de Cerradura" if carro_cerrado else "Lectura y Decodificación de Cerradura (Vehículo Abierto)", 250.0 if carro_cerrado else 150.0),
                        (f"Llave Inteligente de Presencia Toyota ({ficha_tecnica['frec']}) + Batería CR2032", 820.0),
                        (f"Inserto de Emergencia ({espada_corta}) Tallado por Código desde Cero", 130.0),
                        ("Conexión de Arnés de Módulo Inmovilizador (Sin Desoldar)", 380.0),
                        ("Protección de Voltaje + Programación de Smart Key desde Cero", 520.0)
                    ]
                elif "Presencia" in estilo_akl:
                    desglose_items = [
                        ("Apertura Profesional Sin Daño y Decodificación de Cerradura" if carro_cerrado else "Decodificación de Cerradura de Emergencia (Vehículo Abierto)", 250.0 if carro_cerrado else 150.0),
                        (f"Llave Inteligente de Presencia ({ficha_tecnica['chip']}) + Batería CR2032", 720.0),
                        (f"Inserto de Emergencia ({espada_corta}) Tallado por Código desde Cero", 130.0),
                        ("Protección de Voltaje + Programación de Inmovilizador desde Cero", 700.0)
                    ]
                else:
                    desglose_items = [
                        ("Apertura y Decodificación de Cilindro de Alta Seguridad" if carro_cerrado else "Decodificación de Cilindro de Alta Seguridad (Vehículo Abierto)", 240.0 if carro_cerrado else 140.0),
                        (f"Tallado de Precisión en Pista Especial ({espada_corta}) desde Cero", 150.0),
                        (f"Llave de Regata + Chip Criptográfico Nuevo ({ficha_tecnica['chip']})", 180.0),
                        ("Protección de Voltaje + Programación por Pérdida Total", 330.0)
                    ]

            # 4) ME ROBARON UNA LLAVE -> CAMBIO DE COMBINACIÓN + BORRADO ELECTRÓNICO + OPCIÓN DE SMART KEY / CONTROL
            elif "CAMBIAR COMBINACIÓN" in situacion_llave:
                estado_puertas_robo = st.radio(
                    "🚪 ¿Cómo se encuentra el vehículo actualmente?",
                    [
                        "🔓 El vehículo está ABIERTO (o tengo otra llave de respaldo en mano)",
                        "🔒 El vehículo está CERRADO (No tengo otra llave para abrirlo)"
                    ]
                )
                recargo_apertura_robo = 175.0 if "CERRADO" in estado_puertas_robo else 0.0

                if modo_vehiculo == "SOLO_SMART_MOD":
                    opciones_robo = [
                        "Cambio de Combinación de Chapa + Borrado Electrónico de Llave Robada + Llave de Presencia (Smart Key) Nueva",
                        "Solo Cambio de Combinación + Borrado Electrónico de Llave Robada (Conservando mi otra Smart Key actual)"
                    ]
                elif modo_vehiculo == "MIXTO_SMART":
                    opciones_robo = [
                        "Cambio de Combinación + Borrado Electrónico de Llave Robada + Llave de Presencia (Smart Key) Nueva",
                        "Cambio de Combinación + Borrado Electrónico de Llave Robada + Control Tipo Navaja / Original con Chip Nuevo",
                        "Cambio de Combinación + Borrado Electrónico de Llave Robada + Llave con Chip Sencilla Nueva",
                        "Solo Cambio de Combinación + Borrado Electrónico de Llave Robada (Conservando mi otra llave actual)"
                    ]
                elif modo_vehiculo in ["CHIP_NORMAL", "CHIP_ALTA"]:
                    opciones_robo = [
                        "Cambio de Combinación de Chapa y Switch + Borrado de Llave Robada + Control Tipo Navaja / Original con Chip",
                        "Cambio de Combinación de Chapa y Switch + Borrado de Llave Robada + Llave con Chip Nueva",
                        "Solo Cambio de Combinación + Borrado Electrónico de Llave Robada (Conservando mi otra llave actual)"
                    ]
                else: # SIN_CHIP
                    opciones_robo = [
                        "Cambio de Combinación de Chapa y Switch (Juego de Guardas Nuevas) + 2 Llaves Metálicas Nuevas"
                    ]

                paquete_robo = st.selectbox("¿Qué necesitas incluir para asegurar tu vehículo?", opciones_robo)

                if recargo_apertura_robo > 0:
                    desglose_items.append(("Apertura Técnica Profesional del Vehículo Sin Daño", recargo_apertura_robo))

                if "Llave de Presencia (Smart Key) Nueva" in paquete_robo:
                    precio_smart = 1150.0 if marca_sel == "Toyota" else 1050.0
                    desglose_items.extend([
                        ("Reconfiguración de Guardas de Cilindro de Puerta (La llave robada ya no girará)", 250.0),
                        ("Borrado Electrónico en Computadora de la Llave Robada (Desactivación Total)", 200.0),
                        (f"Llave Inteligente de Presencia Nueva ({ficha_tecnica['chip']} - {ficha_tecnica['frec']}) Programada", precio_smart),
                        (f"Inserto Metálico de Emergencia ({espada_corta}) Tallado a la Nueva Combinación", 100.0)
                    ])
                elif "Control Tipo Navaja" in paquete_robo:
                    desglose_items.extend([
                        ("Cambio de Combinación de Guardas en Chapa y Switch de Encendido", 280.0),
                        ("Borrado Electrónico en Inmovilizador de la Llave/Control Robado", 170.0),
                        (f"Control Tipo Navaja / Original ({ficha_tecnica['frec']}) + Chip ({ficha_tecnica['chip']}) Programado", 550.0),
                        (f"Espada Nueva ({espada_corta}) Tallada a la Nueva Combinación", 100.0)
                    ])
                elif "Llave con Chip" in paquete_robo:
                    desglose_items.extend([
                        ("Cambio de Combinación de Guardas en Chapa y Switch de Encendido", 280.0),
                        ("Borrado Electrónico en Inmovilizador de la Llave Robada", 150.0),
                        (f"Llave Nueva ({espada_corta}) + Chip ({ficha_tecnica['chip']}) Tallada y Programada", 320.0)
                    ])
                elif "Conservando mi otra" in paquete_robo:
                    desglose_items.extend([
                        ("Cambio de Combinación de Guardas en Cilindro/Switch (Anulación mecánica de llave robada)", 260.0),
                        ("Borrado Electrónico en Computadora de la Llave Robada + Reprogramación de tu Llave Actual", 220.0),
                        (f"Nuevo Espadín / Inserto ({espada_corta}) Tallado a la Nueva Combinación para tu llave actual", 120.0)
                    ])
                else:
                    desglose_items.extend([
                        ("Juego de Guardas Nuevas y Reconfiguración de Combinación de Chapa y Switch", 260.0),
                        (f"Juego de Llaves Metálicas Nuevas ({espada_corta}) Talladas a la Nueva Combinación", 140.0)
                    ])

            # 5) APERTURA DE VEHÍCULO
            elif "ABRIR" in situacion_llave:
                if any(k in ficha_tecnica["espada"] for k in ["Regata", "HON66", "HU101", "HU66", "TOY48"]):
                    desglose_items = [
                        (f"Apertura de Alta Precisión en Cerradura {espada_corta} (0% Daños)", 275.0)
                    ]
                else:
                    desglose_items = [
                        ("Apertura Técnica Profesional de Vehículo (Sin rayar pintura ni doblar puertas)", 175.0)
                    ]

            # 6) REPARACIÓN DE CONTROL / CARCASA / BATERÍA / REPROGRAMACIÓN
            elif "falló" in situacion_llave:
                sub_taller = st.selectbox(
                    "Selecciona el servicio de reparación:",
                    [
                        "Cambio de Carcasa Nueva + Tallado de Llave + Traslado de Placa y Chip (Q200)",
                        "Reemplazo solo de Espada / Inserto Metálico o Cabeza Quebrada (Q125)",
                        "Reprogramación / Sincronización de Control + Limpieza de Contactos (Q175)",
                        "Cambio de Batería de Litio de Alta Duración + Prueba de Frecuencia (Q35)"
                    ]
                )
                if "Carcasa" in sub_taller:
                    desglose_items = [
                        ("Carcasa Nueva de Alta Resistencia", 110.0),
                        (f"Tallado de Llave de Precisión ({espada_corta}) + Pin de Fijación", 55.0),
                        ("Traslado Cuidadoso de Placa Electrónica, Chip y Limpieza", 35.0)
                    ]
                elif "Espada" in sub_taller:
                    desglose_items = [
                        (f"Espada / Inserto Metálico ({espada_corta}) o Cabeza Nueva + Pin de Acero", 65.0),
                        ("Tallado de Precisión y Ajuste en el Control", 60.0)
                    ]
                elif "Reprogramación" in sub_taller:
                    desglose_items = [
                        ("Limpieza Electrónica de Placa y Contactos del Control", 45.0),
                        (f"Sincronización y Reprogramación de Control ({ficha_tecnica['frec']}) en el Vehículo", 130.0)
                    ]
                else:
                    desglose_items = [
                        ("Batería de Litio Nueva (CR2032 / CR1616 / CR2025 / CR2016 / CR1632)", 25.0),
                        ("Instalación y Comprobación de Señal de Radiofrecuencia", 10.0)
                    ]

            # 7) SERVICIO DE JUMPER (PASO DE CORRIENTE) O DIAGNÓSTICO
            else:
                sub_elec = st.radio(
                    "Selecciona la asistencia eléctrica requerida:",
                    [
                        "Servicio de Jumper (Paso de Corriente para Batería Descargada) + Prueba de Carga (Q100)",
                        "Diagnóstico Electrónico Multimarca por Escáner + Prueba de Batería y Alternador (Q150)"
                    ]
                )
                if "Jumper" in sub_elec:
                    desglose_items = [
                        ("Asistencia de Arranque Seguro con Equipo Jumper Portátil", 60.0),
                        ("Verificación de Voltaje de Batería y Carga del Alternador", 40.0)
                    ]
                else:
                    desglose_items = [
                        ("Escaneo Electrónico Completo de Módulos (Motor, ABS, Bolsas de Aire, Inmovilizador)", 100.0),
                        ("Prueba Digital de Estado de Vida de Batería y Alternador", 50.0)
                    ]

        # --- LÓGICA B: MOTOCICLETAS ---
        elif tipo_bien == "🏍️ Motocicleta / Cuatrimoto":
            marca_moto = st.selectbox("Marca de tu Moto:", ["Honda (HD75 / Navi / XR / Twister)", "Suzuki (SUZ12 / Gixxer / GN125)", "Yamaha (YM63 / YH48 / Fazer / Crux)", "Bajaj / Pulsar (Discover / NS200)", "Italika / Kymco / Kawasaki"])
            descripcion_vehiculo = f"Motocicleta {marca_moto}"
            serv_moto = st.radio("Servicio requerido para la moto:", [
                "Sacar copia de llave (Tengo muestra)",
                "Perdí todas las llaves de la moto (Hacer llave desde cero)",
                "Me robaron la llave (Cambio de combinación de switch + llave nueva)"
            ])
            if "copia" in serv_moto:
                precio_m = 45.0 if "Navi" in marca_moto else 35.0
                desglose_items = [
                    (f"Llave Virgen para {marca_moto}", 20.0),
                    ("Tallado de Precisión de Llave", precio_m - 20.0)
                ]
            elif "robaron" in serv_moto:
                desglose_items = [
                    ("Reconfiguración de Guardas de Switch y Tapón (La llave robada ya no girará)", 140.0),
                    (f"Juego de Llaves Nuevas para {marca_moto} Talladas a la Nueva Combinación", 110.0)
                ]
            else:
                desglose_items = [
                    ("Lectura Mecánica de Alturas de Switch y Tapón de Gasolina", 110.0),
                    (f"Llave Virgen para {marca_moto} + Tallado Exacto desde Cero", 90.0)
                ]

        # --- LÓGICA C: CAMIONES PESADOS ---
        elif tipo_bien == "🚛 Camión Pesado (Hino/Isuzu/Freightliner)":
            camion_sel = st.selectbox("Marca del Camión:", ["Freightliner (FRE-1)", "Hino Serie 300 / 500 (X274 / HN3)", "Isuzu NPR / NQR / ELF (X275 / B113)", "Kenworth (K1994 / B87)"])
            descripcion_vehiculo = f"Camión {camion_sel}"
            serv_camion = st.radio("Servicio para el camión:", ["Duplicado de llave metálica", "Hechura de llave desde cero (Pérdida total)", "Apertura de cabina sin daño"])
            if "Duplicado" in serv_camion:
                desglose_items = [
                    (f"Llave de Trabajo Pesado {camion_sel}", 45.0),
                    ("Tallado de Llave de Alta Precisión", 40.0)
                ]
            elif "cero" in serv_camion:
                desglose_items = [
                    ("Apertura y Lectura Mecánica de Cilindro de Camión", 180.0),
                    (f"Llave Virgen {camion_sel} + Tallado Exacto desde Cero", 120.0)
                ]
            else:
                desglose_items = [("Apertura Técnica de Cabina de Camión Sin Daño", 200.0)]

        # --- LÓGICA D: CASA / CHAPA RESIDENCIAL ---
        else:
            descripcion_vehiculo = "Servicio Residencial (Chapa de Casa)"
            serv_casa = st.radio(
                "Selecciona lo que necesitas:",
                [
                    "Duplicado de Llave de Casa (1 copia)",
                    "Promoción Dúo Residencial (2 copias de la misma llave)",
                    "Apertura de Puerta Residencial o Cambio de Combinación de Chapa"
                ]
            )
            if "Promoción" in serv_casa:
                desglose_items = [("2x Llaves Residenciales con Tallado de Precisión", 25.0)]
            elif "Apertura" in serv_casa:
                desglose_items = [("Servicio Técnico de Apertura / Cambio de Guardas de Chapa Residencial", 150.0)]
            else:
                desglose_items = [("1x Llave Residencial con Tallado de Precisión", 15.0)]

        st.write("---")
        st.markdown("#### Paso 2: Ubicación para Servicio a Domicilio y Datos de Cita")
        u1, u2 = st.columns(2)
        with u1:
            depto_sel = st.selectbox("Departamento:", list(DISTANCIAS_KM_ORIENTE.keys()))
        with u2:
            muni_sel = st.selectbox("Municipio Exacto:", list(DISTANCIAS_KM_ORIENTE[depto_sel].keys()))
        
        # Cálculo interno ida y vuelta desde San Luis Jilotepeque (oculto para el cliente)
        km_ida_vuelta = DISTANCIAS_KM_ORIENTE[depto_sel][muni_sel]
        costo_traslado = float(km_ida_vuelta * MULTIPLICADOR_COMBUSTIBLE)

        if costo_traslado > 0:
            desglose_items.append((f"Servicio de Unidad Móvil a Domicilio ({muni_sel}, {depto_sel})", costo_traslado))
        else:
            desglose_items.append((f"Atención Local en {muni_sel} (Sin recargo de traslado)", 0.0))

        direccion_exacta = st.text_input(
            "📍 Barrio, Aldea o Colonia y Punto de Referencia (Máx. 70 letras):",
            max_chars=70,
            placeholder="Ej. Barrio El Centro frente a Gasolinera / Aldea..."
        )
        
        f1, f2 = st.columns(2)
        with f1:
            fecha_cita = st.date_input("📅 Fecha deseada:", min_value=date.today(), value=date.today())
        with f2:
            hora_cita = st.time_input("⏰ Hora preferida:", value=time(10, 0))

        n1, n2 = st.columns(2)
        with n1:
            nombre_cliente = st.text_input(
                "👤 Tu Nombre (Máx. 35 letras):",
                value="" if st.session_state.alias_usuario == "Invitado" else st.session_state.alias_usuario,
                max_chars=35,
                placeholder="Ej. Carlos Morales"
            )
        with n2:
            tel_cliente = st.text_input(
                "📱 Tu Teléfono / WhatsApp (8 dígitos OBLIGATORIO):",
                max_chars=8,
                placeholder="Ej. 55443322"
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # --- COLUMNA DERECHA: RECIBO TRANSPARENTE + BLOQUEO HASTA QUE INGRESE 8 DÍGITOS ---
    with col_recibo:
        total_cotizacion = sum(monto for _, monto in desglose_items)
        fecha_str = fecha_cita.strftime("%d/%m/%Y")
        hora_str = hora_cita.strftime("%I:%M %p")
        tel_limpio = tel_cliente.strip().replace("-", "").replace(" ", "")
        telefono_valido = tel_limpio.isdigit() and len(tel_limpio) == 8

        # Actualizar los datos del visitante en la lista de la Pestaña 4 cuando escribe su teléfono o nombre
        if len(registro_app["clientes"]) > 0:
            registro_app["clientes"][-1]["Nombre / Alias"] = nombre_cliente if nombre_cliente else st.session_state.alias_usuario
            registro_app["clientes"][-1]["Teléfono"] = tel_limpio if telefono_valido else "Pendiente"
            registro_app["clientes"][-1]["Vehículo / Consulta"] = f"{descripcion_vehiculo} ({muni_sel}) - Q{total_cotizacion:,.2f}"

        if alerta_tecnica == "ROJO":
            st.error("⚠️ **NOTA TÉCNICA IMPORTANTE:** Este modelo reciente (2020-2026) cuenta con seguridad encriptada avanzada. Envíanos tu cotización por WhatsApp para verificar código de programación antes de llegar.")
        elif alerta_tecnica == "AMARILLO":
            st.warning("⚡ **PROTECCIÓN DE VOLTAJE INCLUIDA:** Tu cotización ya incluye estabilizador electrónico de batería durante toda la programación para cuidar los módulos de tu vehículo.")

        html_lineas = ""
        texto_lineas_wa = ""
        for concepto, valor in desglose_items:
            html_lineas += f'<div class="receipt-line"><span>🔹 {concepto}</span><b>Q {valor:,.2f}</b></div>'
            texto_lineas_wa += f"• {concepto}: Q{valor:,.2f}\n"

        resumen_ficha_html = ""
        resumen_ficha_wa = ""
        if ficha_tecnica:
            resumen_ficha_html = f"<br><b>Especificación Técnica:</b> Espada {ficha_tecnica['espada']} | {ficha_tecnica['chip']} | {ficha_tecnica['frec']}"
            resumen_ficha_wa = f"🔧 *Especificación:* Espada {ficha_tecnica['espada']} | {ficha_tecnica['chip']} | {ficha_tecnica['frec']}\n"

        st.markdown(f"""
        <div class="receipt-box">
            <div class="receipt-header">
                <h3 style="margin:0; color:#F97316;">🧾 COTIZACIÓN OFICIAL DESGLOSADA</h3>
                <p style="margin:4px 0 0 0; font-size:13px; color:#94A3B8;">
                    <b>Cerrajería Automotriz Elías</b> | Tel/WhatsApp: +502 5191-6984<br>
                    <b>Cliente:</b> {nombre_cliente if nombre_cliente else st.session_state.alias_usuario} | <b>Tel:</b> {tel_limpio if telefono_valido else '⚠️ Falta ingresar 8 dígitos'}<br>
                    <b>Vehículo/Bien:</b> {descripcion_vehiculo}{resumen_ficha_html}<br>
                    <b>Ubicación:</b> {muni_sel}, {depto_sel} ({direccion_exacta if direccion_exacta else 'Sin referencia'})<br>
                    <b>Cita solicitada:</b> {fecha_str} a las {hora_str}
                </p>
            </div>
            {html_lineas}
            <div class="receipt-total">
                <span>PRECIO FINAL TODO INCLUIDO:</span>
                <span>Q {total_cotizacion:,.2f}</span>
            </div>
            <p style="font-size:12px; color:#94A3B8; margin-top:10px; margin-bottom:0;">
                ✅ Incluye mano de obra profesional, tallado de precisión, materiales nuevos, servicio de unidad móvil y garantía.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if not telefono_valido:
            st.warning("🔒 **PASO OBLIGATORIO:** Ingresa tu número de teléfono de **8 dígitos** (sin guiones ni espacios) en la casilla **Tu Teléfono / WhatsApp** para activar los botones de envío y agendar tu cita.")
        else:
            mensaje_wa = (
                f"🔑 *NUEVA COTIZACIÓN Y CITA - CERRAJERÍA ELÍAS*\n\n"
                f"👤 *Cliente:* {nombre_cliente if nombre_cliente else st.session_state.alias_usuario}\n"
                f"📱 *Teléfono:* +502 {tel_limpio}\n"
                f"🚗 *Vehículo/Servicio:* {descripcion_vehiculo}\n"
                f"{resumen_ficha_wa}"
                f"📍 *Municipio:* {muni_sel}, {depto_sel}\n"
                f"🏠 *Referencia:* {direccion_exacta if direccion_exacta else 'Por confirmar ubicación GPS'}\n"
                f"📅 *Fecha y Hora:* {fecha_str} a las {hora_str}\n\n"
                f"📋 *DESGLOSE COMPLETO DEL SERVICIO:*\n"
                f"{texto_lineas_wa}\n"
                f"💰 *TOTAL FINAL A PAGAR: Q{total_cotizacion:,.2f}*\n\n"
                f"¿Me confirman disponibilidad para esta cita?"
            )
            wa_encoded = urllib.parse.quote(mensaje_wa)
            link_whatsapp = f"https://wa.me/50251916984?text={wa_encoded}"

            asunto_mail = urllib.parse.quote(f"Cita Cerrajería Elías: {descripcion_vehiculo} - Tel {tel_limpio}")
            link_mailto = f"mailto:cerrajeriaelias@gmail.com?subject={asunto_mail}&body={wa_encoded}"

            st.markdown(f'<a class="btn-wa" href="{link_whatsapp}" target="_blank">📲 ENVIAR COTIZACIÓN Y AGENDAR POR WHATSAPP</a>', unsafe_allow_html=True)
            st.markdown(f'<a class="btn-mail" href="{link_mailto}">📧 Enviar copia por Correo Electrónico</a>', unsafe_allow_html=True)

            st.download_button(
                label="📥 Descargar Comprobante de Cotización (.TXT)",
                data=mensaje_wa.encode("utf-8"),
                file_name=f"Cotizacion_Cerrajeria_Elias_{tel_limpio}.txt",
                mime="text/plain",
                use_container_width=True
            )

# ==============================================================================
# PESTAÑA 2: CATÁLOGO DE LLAVES & BIBLIOTECA INTERACTIVA
# ==============================================================================
with tab_catalogo:
    st.subheader("🚘 Guía de Llaves, Controles y Biblioteca Automotriz para Clientes")
    st.write("Conoce las diferencias entre cada tipo de llave automotriz y por qué los vehículos modernos utilizan chips y frecuencias de seguridad.")

    c_cat1, c_cat2, c_cat3, c_cat4 = st.columns(4)
    with c_cat1:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#38BDF8;">📡 1. Llave de Presencia (Smart Key)</h4>
            <p><b>¿Por qué elegirla?</b> Diseñada para vehículos con botón <b>Start/Stop</b>. Permite abrir las puertas y encender el motor llevando el control en el bolsillo gracias a sus antenas de proximidad.</p>
            <p>Incluye su llave metálica de emergencia oculta por si algún día se descarga la batería del carro.</p>
            <b>Duplicado: Q1,200 - Q1,300<br>Desde cero: Q1,800 - Q2,100</b>
        </div>
        """, unsafe_allow_html=True)
    with c_cat2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#F97316;">🔪 2. Control Tipo Navaja (Flip Key)</h4>
            <p><b>¿Por qué elegirla?</b> Si tu llave actual tiene la cabeza plástica quebrada o llevas el control colgando por separado, la llave tipo navaja guarda la espada metálica adentro del control con un botón retráctil.</p>
            <p>No rompe tus bolsas del pantalón, protege la lámina de encendido y moderniza tu vehículo.</p>
            <b>Modernización: Q425<br>Completa con chip: Q650</b>
        </div>
        """, unsafe_allow_html=True)
    with c_cat3:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#A855F7;">🕹️ 3. Control con Espadín Estilo Original</h4>
            <p><b>¿Por qué elegirlo?</b> Mantiene la estética clásica de fábrica de tu vehículo (como las llaves de 3 o 4 botones integrados en la cabeza de la llave).</p>
            <p>Integra en una sola pieza rígida el mando de cierre centralizado, el chip de encendido y la espada metálica.</p>
            <b>Duplicado completo: Q650<br>Cambio de carcasa: Q200</b>
        </div>
        """, unsafe_allow_html=True)
    with c_cat4:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#4ADE80;">🛡️ 4. Llave con Chip & Llave Metálica</h4>
            <p><b>¿Por qué elegirla?</b> Es la copia de respaldo ideal y más resistente al agua, golpes y trabajo pesado en el campo o comercio.</p>
            <p>Aun sin botones, lleva adentro el chip electrónico programado que autoriza a la computadora del motor a encender.</p>
            <b>Duplicado con Chip: Q300 - Q375<br>Metálica sin chip: Q35 - Q85</b>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("### 📚 Biblioteca Interactiva: ¿Cómo funciona la seguridad de tu llave?")
    exp1, exp2, exp3 = st.columns(3)
    with exp1:
        with st.expander("🧠 ¿Por qué una llave lleva Chip (Transponder)?", expanded=True):
            st.write("""
            Desde finales de los años 90, los fabricantes instalaron una antena alrededor del switch de encendido llamada **Inmovilizador**.
            
            Si cortas una llave solo de metal para un carro que lleva chip, la llave abrirá la puerta y girará el switch, **pero el motor no arrancará (o se apagará al instante)** porque la computadora no detecta el código electrónico del chip oculto dentro del cabezal de la llave.
            """)
    with exp2:
        with st.expander("🔐 ¿Qué tipos de Chips existen?", expanded=True):
            st.write("""
            * **Chips de Código Estándar (ID46, 4D63, 4D67, ID48):** Usados en la mayoría de vehículos entre 2000 y 2013.
            * **Chips Criptográficos de 80 y 128 bits (Letra G, Letra H, ID47, ID49):** Tienen encriptación avanzada contra robo en modelos 2011 en adelante.
            * **Sistemas de Proximidad Inteligente (8A, 4A, 6A):** Usados en llaves de botón *Start/Stop* que combinan arranque e inalámbrico en un solo procesador.
            """)
    with exp3:
        with st.expander("📻 ¿Qué son las Frecuencias (MHz) de un Control?", expanded=True):
            st.write("""
            Cada control remoto se comunica con el vehículo a través de una onda de radio específica según el país donde se fabricó el carro:
            * **313.8 MHz y 315 MHz:** Muy común en vehículos importados de Estados Unidos y Japón (Toyota, Honda, Mazda, Ford).
            * **433 MHz y 434 MHz:** Estándar frecuente en vehículos de agencia centroamericana, europeos y asiáticos recientes (Hilux, Hyundai, Kia, VW).
            """)

# ==============================================================================
# PESTAÑA 3: CONSULTA INTERACTIVA "¿MI CARRO USA CHIP?"
# ==============================================================================
with tab_buscador:
    st.subheader("🔍 Consulta Interactiva: ¿Tu Vehículo Ocupa Chip o es Llave Normal?")
    st.write("Selecciona la marca y el modelo de tu carro para descubrir al instante qué sistema utiliza, qué perfil de llave lleva y qué opciones se le pueden fabricar.")

    b1, b2 = st.columns(2)
    with b1:
        marca_busq = st.selectbox("1. Elige la Marca:", list(CATALOGO_VEHICULOS.keys()), key="busq_marca")
    with b2:
        modelo_busq = st.selectbox("2. Elige el Modelo y Años:", list(CATALOGO_VEHICULOS[marca_busq].keys()), key="busq_modelo")

    info_v = CATALOGO_VEHICULOS[marca_busq][modelo_busq]

    st.markdown(f"""
    <div class="glass-card" style="border-left: 6px solid #38BDF8;">
        <h3 style="margin-top:0; color:#38BDF8;">🚘 {marca_busq} — {modelo_busq}</h3>
        <p style="font-size:17px;"><b>¿Este vehículo ocupa Chip Inmovilizador?:</b> <span style="color:#4ADE80; font-weight:800;">{info_v['usa_chip']}</span></p>
        <ul>
            <li><b>Perfil de Llave / Espada Mecánica:</b> <code>{info_v['espada']}</code></li>
            <li><b>Tipo de Chip / Transponder:</b> <code>{info_v['chip']}</code></li>
            <li><b>Frecuencia de Control Remoto:</b> <code>{info_v['frec']}</code></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    if info_v["modo"] == "SIN_CHIP":
        st.success("✅ **Conclusión para tu vehículo:** Tu carro NO ocupa chip electrónico. Puedes sacarle duplicados con **Llave 100% Metálica (Q65)** de forma económica, o si perdiste todas las llaves te la fabricamos desde cero leyendo tu chapa por **Q300**.")
    elif info_v["modo"] in ["CHIP_NORMAL", "CHIP_ALTA"]:
        st.info("🔑 **Conclusión para tu vehículo:** Tu carro SÍ utiliza chip inmovilizador para poder arrancar. Puedes elegir entre una **Llave con Chip sencilla (Q300 - Q375)**, modernizarla a **Control Tipo Navaja (Q425 - Q650)** o pedir un **Control Estilo Original (Q650)**.")
    else:
        st.info("📡 **Conclusión para tu vehículo:** Esta generación cuenta con versiones de alta seguridad y/o **Encendido de Botón (Smart Key)**. Te recomendamos mantener siempre al menos 2 llaves programadas para evitar costos mayores por pérdida total.")

# ==============================================================================
# PESTAÑA 4: PANEL INTERNO DE TALLER E INVENTARIO 2027 (CÓDIGO EXCLUSIVO)
# ==============================================================================
with tab_admin:
    st.subheader("🔐 Panel Administrativo e Inventario (Uso Exclusivo del Taller)")
    pin_acceso = st.text_input("Ingresa el código de autorización del taller:", type="password")

    if pin_acceso == "6438":
        st.success("✅ Acceso autorizado. Panel de Control e Inventario 2027 desbloqueado.")
        
        df_actual = st.session_state.inv_2027
        valor_estanteria = (df_actual["Existencia"] * df_actual["Precio_Q"]).sum()
        costo_estanteria = (df_actual["Existencia"] * df_actual["Costo_Q"]).sum()
        ventas_acum = (df_actual["Usadas"] * df_actual["Precio_Q"]).sum()

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("📦 Piezas en Existencia", f"{int(df_actual['Existencia'].sum()):,}")
        m2.metric("💰 Valor Venta en Estantería", f"Q {valor_estanteria:,.2f}")
        m3.metric("🏦 Costo Real en Estantería", f"Q {costo_estanteria:,.2f}")
        m4.metric("💵 Ventas Registradas", f"Q {ventas_acum:,.2f}")

        st.markdown("#### ⚡ Descuento Rápido de Insumos (Modo Combo / Taller)")
        col_c1, col_c2 = st.columns([2, 1])
        with col_c1:
            insumos_usados = st.multiselect(
                "Selecciona TODOS los materiales que usaste en este trabajo (ej. Control + Espada + Pin + Chip):",
                df_actual["Producto"].tolist()
            )
        with col_c2:
            if st.button("🛠️ Descontar Materiales Seleccionados del Stock", type="primary"):
                if insumos_usados:
                    for item in insumos_usados:
                        idx = st.session_state.inv_2027[st.session_state.inv_2027["Producto"] == item].index[0]
                        if st.session_state.inv_2027.loc[idx, "Existencia"] > 0:
                            st.session_state.inv_2027.loc[idx, "Existencia"] -= 1
                            st.session_state.inv_2027.loc[idx, "Usadas"] += 1
                    st.toast("✅ Todos los materiales del combo fueron descontados.", icon="🔑")
                    st.rerun()
                else:
                    st.warning("Selecciona al menos un insumo.")

        st.markdown("#### 📊 Base de Datos Editable (`Inventario 2027 100 full`)")
        inv_editado = st.data_editor(
            st.session_state.inv_2027,
            use_container_width=True,
            num_rows="dynamic"
        )
        if st.button("💾 Guardar Cambios Manuales en Inventario"):
            st.session_state.inv_2027 = inv_editado
            st.success("Inventario actualizado.")

        # ======================================================================
        # CUADRO 3: BITÁCORA DE VISITAS Y USUARIOS EN PESTAÑA 4
        # ======================================================================
        st.write("---")
        st.markdown(f"#### 👥 Registro de Visitas (Total: {registro_app['visitas']} visitas)")
        if len(registro_app["clientes"]) > 0:
            st.dataframe(pd.DataFrame(registro_app["clientes"]), use_container_width=True)
        else:
            st.info("Aún no se han registrado visitantes hoy.")

    elif pin_acceso != "":
        st.error("❌ Código incorrecto.")
    else:
        st.info("🔒 Área restringida para administración interna de Cerrajería Automotriz Elías.")
