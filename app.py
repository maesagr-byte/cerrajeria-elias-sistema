import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, date, time

# ==============================================================================
# 1. CONFIGURACIÓN GENERAL Y ESTILO FUTURISTA (CYBER-AUTOMOTIVE UI)
# ==============================================================================
st.set_page_config(
    page_title="Cerrajería Automotriz Elías | Cotizador & ERP Oriente",
    page_icon="🔑",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Fondo general y tipografía moderna */
    .stApp {
        background: radial-gradient(circle at top right, #111927 0%, #0B0F19 60%, #070A10 100%);
        color: #F3F4F6;
    }
    /* Encabezado Hero Futurista */
    .hero-banner {
        background: linear-gradient(135deg, rgba(14, 30, 56, 0.95) 0%, rgba(28, 45, 74, 0.85) 50%, rgba(230, 126, 34, 0.25) 100%);
        border: 1px solid rgba(230, 126, 34, 0.45);
        border-radius: 18px;
        padding: 26px 30px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
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
    }
    /* Tarjetas Glassmorphism */
    .glass-card {
        background: rgba(30, 41, 59, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.35);
    }
    /* Recibo Desglosado */
    .receipt-box {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        border: 2px solid #F97316;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 12px 32px rgba(249, 115, 22, 0.18);
    }
    .receipt-header {
        border-bottom: 1px dashed #64748B;
        padding-bottom: 12px;
        margin-bottom: 14px;
    }
    .receipt-line {
        display: flex;
        justify-content: space-between;
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
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. BASE DE DATOS AUTOMOTRIZ INTELIGENTE (ESPECIFICACIONES Y PROTOCOLOS)
# ==============================================================================
CATALOGO_VEHICULOS = {
    "Toyota": {
        "Hilux / Pick-up (1995-2005)": {"espada": "TR47 / TR40 Metálica", "chip": "Sin Chip / 4C", "frec": "N/A", "proto": "Mecánico / Clonación", "riesgo": "VERDE"},
        "Hilux (2006-2015)": {"espada": "TR47", "chip": "Texas 4D67 / Letra G (80 bits)", "frec": "433 MHz", "proto": "OBD2 Autel IM508S", "riesgo": "VERDE"},
        "Hilux (2016-2021)": {"espada": "TR47 / TOY48 Regata", "chip": "Chip H (128 bits) / Smart 8A", "frec": "315/433 MHz", "proto": "OBD2 / Arnés Smart 8A", "riesgo": "AMARILLO"},
        "Corolla / RAV4 / Yaris (2003-2010)": {"espada": "TR47", "chip": "Texas ID 4D67", "frec": "315 MHz (Diamante)", "proto": "OBD2 Autel IM508S", "riesgo": "VERDE"},
        "Corolla / RAV4 / Tacoma (2010-2014)": {"espada": "TR47", "chip": "Texas ID 4D72 Letra G (80 bits)", "frec": "315 MHz (GQ4-29T)", "proto": "OBD2 Autel IM508S", "riesgo": "VERDE"},
        "Corolla / RAV4 / Tacoma / 4Runner (2014-2021)": {"espada": "TR47 / TOY48 Short", "chip": "Chip H (128 bits) / Smart Key 8A (XM38)", "frec": "314.3 / 315 MHz", "proto": "OBD2 + Arnés 30/27 Pines (En AKL)", "riesgo": "VERDE"},
        "Tacoma / Tundra / RAV4 / Corolla Cross (2022-2026)": {"espada": "TOY48", "chip": "Smart Key 8A-BA / 4A-BA", "frec": "315 / 433 MHz", "proto": "Requiere Cable FP30 + PIN Servidor", "riesgo": "ROJO"},
    },
    "Honda": {
        "Civic / CR-V / Accord / Fit (2002-2013)": {"espada": "HON66 (HO01 Regata 4 Pistas)", "chip": "Philips ID46 (HO01)", "frec": "313.8 / 433.92 MHz", "proto": "OBD2 Autel IM508S + Noco Genius 10", "riesgo": "VERDE"},
        "CR-V / Civic / HR-V / Fit / Pilot (2014-2021)": {"espada": "HON66 (HO01)", "chip": "Hitag3 ID47 (G ID47)", "frec": "315 / 433 MHz", "proto": "OBD2 Autel IM508S (Voltaje Fijo 13.5V)", "riesgo": "VERDE"},
        "Civic 11va Gen / CR-V Nueva (2022-2026)": {"espada": "HON66", "chip": "ID47 / 4A CAN-FD", "frec": "433 MHz", "proto": "Protocolo CAN-FD (Solo Duplicado con Adaptador)", "riesgo": "ROJO"},
    },
    "Nissan": {
        "Pick-up D21 / D22 / Frontier / Sentra B15 (1998-2012)": {"espada": "DA34 / NSN14", "chip": "ID46 (o Metálica sin chip)", "frec": "315 MHz", "proto": "OBD2 Autel IM508S", "riesgo": "VERDE"},
        "Versa / Tiida / March / Sentra / NP300 Frontier (2012-2019)": {"espada": "DA34 / NSN14", "chip": "ID46 / Hitag AES (Llave o Navaja)", "frec": "315 / 433 MHz", "proto": "OBD2 Autel IM508S + Noco Genius 10", "riesgo": "VERDE"},
        "Rogue T32 / Qashqai / Murano Push-Button (2014-2020)": {"espada": "NSN14", "chip": "Smart Key 4A / ID46", "frec": "433 MHz", "proto": "PELIGRO BCM CALSONIC LISTA NEGRA", "riesgo": "ROJO"},
        "Sentra B18 / Rogue T33 / Kicks / Frontier (2020-2026)": {"espada": "NSN14", "chip": "Smart Key 4A (PIN 28 Dígitos)", "frec": "433 MHz", "proto": "Requiere Bypass SGW 40 Pines / APB131", "riesgo": "ROJO"},
    },
    "Mazda": {
        "Pick-up B2200 / B2300 / B2500 / BT-50 (1998-2014)": {"espada": "MZ31 / MZ27 / H76", "chip": "Texas 4D63 (40/80 bits)", "frec": "315 / 433 MHz", "proto": "OBD2 Autel IM508S", "riesgo": "VERDE"},
        "Mazda 3 / Mazda 6 / CX-7 / Tribute (2004-2013)": {"espada": "MZ31 / MZ24R", "chip": "Texas 4D63 80 bits", "frec": "315 MHz", "proto": "OBD2 Autel IM508S", "riesgo": "VERDE"},
        "Mazda 3 / CX-5 / CX-3 / CX-9 SkyActiv (2014-2019)": {"espada": "MZ24R (Inserto Smart)", "chip": "Smart Key ID49 (SKE13D-01)", "frec": "315 MHz", "proto": "OBD2 Autel IM508S / Xhorse Naranja", "riesgo": "VERDE"},
        "Mazda CX-30 / Mazda 3 4ta Gen / CX-50 (2020-2026)": {"espada": "MZ24R", "chip": "Smart Key 6A (BCKA)", "frec": "315 MHz", "proto": "Solo con Llave Original OEM + Incode", "riesgo": "ROJO"},
    },
    "Mitsubishi": {
        "L200 / Montero / Lancer / Nativa (2000-2015)": {"espada": "MIT1 / MIT3 / MIT8 / MIT11", "chip": "ID46 Mitsubishi (MIT3)", "frec": "315 / 433 MHz", "proto": "OBD2 Autel IM508S (PIN Automático)", "riesgo": "VERDE"},
        "L200 Sportero / Outlander / Mirage / Montero Sport (2015-2021)": {"espada": "MIT17 / MIT6 / 003L", "chip": "ID46 / ID47 KOS Smart", "frec": "315 / 433 MHz", "proto": "OBD2 Autel IM508S", "riesgo": "VERDE"},
        "Outlander 4ta Generación (2022-2026)": {"espada": "NSN14 (Plataforma Nissan)", "chip": "Smart Key 4A (BCM Nissan 28-digit)", "frec": "433 MHz", "proto": "Módulo Nissan T33 (No tocar sin cable 40 pines)", "riesgo": "ROJO"},
    },
    "Hyundai / Kia": {
        "Elantra / Accent / Tucson / Santa Fe / Rio / Sportage / Soul (2006-2020)": {"espada": "HYN6 / HY15 / HY18 / KK12 / 050L", "chip": "ID46 / ID60 / 8A", "frec": "315 / 433 MHz", "proto": "OBD2 Autel IM508S / Clonación XT27A", "riesgo": "VERDE"},
        "Camiones H100 Porter / Starex H1 / Kia K2700 (2010-2021)": {"espada": "HYN6 / HY15", "chip": "ID46 / 4D60", "frec": "433 MHz", "proto": "Clonación XT27A o PIN por VIN en AKL", "riesgo": "AMARILLO"},
        "Tucson NX4 / Sportage NQ5 / Creta / Seltos (2022-2026)": {"espada": "KK12 / HY18R", "chip": "Smart Key 8A / 4A CAN-FD", "frec": "433 MHz", "proto": "Requiere Adaptador CAN-FD + Código PIN por VIN", "riesgo": "ROJO"},
    },
    "Ford": {
        "Ranger / F-150 / Explorer / Escape / Focus (2000-2014)": {"espada": "H76 / Ford 19 / HU101 Regata", "chip": "Texas 4D63 (80 bits)", "frec": "315 MHz", "proto": "OBD2 Autel IM508S", "riesgo": "VERDE"},
        "F-150 / Escape / Explorer / Fiesta / EcoSport (2015-2020)": {"espada": "HU101 Regata Alta Seguridad", "chip": "ID49 Hitag Pro", "frec": "315 / 433 MHz", "proto": "OBD2 Autel IM508S + Noco 10 (Cuidado Alarma Activa)", "riesgo": "AMARILLO"},
        "F-150 / Bronco / Explorer / Ranger Nueva (2021-2026)": {"espada": "HU101", "chip": "ID49 CAN-FD (Servidor NASTF)", "frec": "315 / 433 MHz", "proto": "Bloqueo Servidor Ford FDRS Online", "riesgo": "ROJO"},
    },
    "Isuzu": {
        "Pick-up D-Max / Rodeo / Trooper (2000-2019)": {"espada": "B111 / ISU5 / X275 / D-Max", "chip": "ID46 / 4D64", "frec": "433 MHz", "proto": "OBD2 Autel IM508S / EEPROM XP400 Pro", "riesgo": "VERDE"},
        "Camiones NPR / NQR / ELF (2000-2022)": {"espada": "X275 / B113 / ISU5", "chip": "Metálica o ID46", "frec": "N/A", "proto": "Corte CNC Dolphin II + OBD2", "riesgo": "VERDE"},
    }
}

# Tarifas de Movilización / Traslado Departamental (Oriente de Guatemala)
ZONAS_ORIENTE = {
    "Chiquimula": {
        "Chiquimula Cabecera (En Taller o Casco Urbano)": 0.0,
        "San José La Arada / San Esteban": 75.0,
        "Ipala / Quezaltepeque / San Jacinto": 150.0,
        "Esquipulas / Jocotán / Camotán / Olopa": 225.0,
        "Concepción Las Minas / Frontera Agua Caliente": 300.0
    },
    "Jalapa": {
        "San Luis Jilotepeque (Casco Urbano)": 0.0,
        "San Pedro Pinula / San Manuel Chaparrón": 125.0,
        "Monjas / Jalapa Cabecera": 175.0,
        "San Carlos Alzatate / Mataquescuintla": 275.0
    },
    "Zacapa": {
        "Estanzuela / Río Hondo / Zacapa Cabecera": 225.0,
        "Teculután / Usumatlán / Cabañas / Huité": 275.0,
        "Gualán / La Unión": 350.0
    },
    "Jutiapa": {
        "Agua Blanca / Santa Catarina Mita / El Progreso": 225.0,
        "Asunción Mita / Jutiapa Cabecera / Yupiltepeque": 275.0,
        "Frontera San Cristóbal / Jalpatagua / Moyuta / Pedro de Alvarado": 400.0
    }
}

# ==============================================================================
# 3. BASE DE DATOS OFICIAL DEL INVENTARIO 2027 (SINCRONIZADA CON TU EXCEL)
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
        # LLAVES CON CHIP DEDICADAS (PRIORIDAD DE ROTACIÓN)
        {"Categoría": "Llaves con Chip", "Marca": "Toyota", "Producto": "TR47 TEXAS ID 4D67", "Stock_Inicial": 5, "Existencia": 5, "Usadas": 0, "Costo_Q": 60.0, "Precio_Q": 300.0},
        {"Categoría": "Llaves con Chip", "Marca": "Toyota", "Producto": "TR47 TEXAS ID 4D72 80 BITS G", "Stock_Inicial": 12, "Existencia": 12, "Usadas": 0, "Costo_Q": 60.0, "Precio_Q": 300.0},
        {"Categoría": "Llaves con Chip", "Marca": "Toyota", "Producto": "TR47 TEXAS ID 4D74 128 BITS H", "Stock_Inicial": 5, "Existencia": 5, "Usadas": 0, "Costo_Q": 60.0, "Precio_Q": 300.0},
        {"Categoría": "Llaves con Chip", "Marca": "Toyota", "Producto": "TR48 TEXAS ID 4D74 128 BITS H", "Stock_Inicial": 8, "Existencia": 8, "Usadas": 0, "Costo_Q": 60.0, "Precio_Q": 300.0},
        {"Categoría": "Llaves con Chip", "Marca": "Honda", "Producto": "HON66 HO01 ID46", "Stock_Inicial": 12, "Existencia": 12, "Usadas": 0, "Costo_Q": 60.0, "Precio_Q": 300.0},
        {"Categoría": "Llaves con Chip", "Marca": "Honda", "Producto": "HON66 HO01 ID47", "Stock_Inicial": 2, "Existencia": 2, "Usadas": 0, "Costo_Q": 60.0, "Precio_Q": 300.0},
        {"Categoría": "Llaves con Chip", "Marca": "Mitsubishi", "Producto": "MIT3 ID46 A", "Stock_Inicial": 7, "Existencia": 7, "Usadas": 0, "Costo_Q": 60.0, "Precio_Q": 300.0},
        {"Categoría": "Llaves con Chip", "Marca": "Nissan", "Producto": "DA34 ID46", "Stock_Inicial": 4, "Existencia": 4, "Usadas": 0, "Costo_Q": 60.0, "Precio_Q": 300.0},
        {"Categoría": "Llaves con Chip", "Marca": "Mazda", "Producto": "H76 TEXAS 4D63 80 BITS MZ02", "Stock_Inicial": 4, "Existencia": 4, "Usadas": 0, "Costo_Q": 60.0, "Precio_Q": 300.0},
        # LLAVES PARA CHIP HUECAS
        {"Categoría": "Llaves Huecas", "Marca": "Toyota", "Producto": "TR47 Hueca", "Stock_Inicial": 28, "Existencia": 23, "Usadas": 5, "Costo_Q": 35.0, "Precio_Q": 175.0},
        {"Categoría": "Llaves Huecas", "Marca": "Honda", "Producto": "HON66 Hueca", "Stock_Inicial": 23, "Existencia": 19, "Usadas": 4, "Costo_Q": 35.0, "Precio_Q": 175.0},
        {"Categoría": "Llaves Huecas", "Marca": "Ford", "Producto": "HU101 Hueca", "Stock_Inicial": 7, "Existencia": 5, "Usadas": 2, "Costo_Q": 35.0, "Precio_Q": 175.0},
        {"Categoría": "Llaves Huecas", "Marca": "Isuzu", "Producto": "B111 Hueca", "Stock_Inicial": 3, "Existencia": 3, "Usadas": 0, "Costo_Q": 35.0, "Precio_Q": 175.0},
        # CHIPS Y PINES
        {"Categoría": "Chips y Pines", "Marca": "XHORSE", "Producto": "Super Chip XT27A", "Stock_Inicial": 104, "Existencia": 56, "Usadas": 48, "Costo_Q": 25.0, "Precio_Q": 100.0},
        {"Categoría": "Chips y Pines", "Marca": "XHORSE", "Producto": "Chip XT57B", "Stock_Inicial": 10, "Existencia": 10, "Usadas": 0, "Costo_Q": 25.0, "Precio_Q": 100.0},
        {"Categoría": "Chips y Pines", "Marca": "PINES", "Producto": "Pin de Acero Fijación Espada", "Stock_Inicial": 345, "Existencia": 345, "Usadas": 0, "Costo_Q": 5.0, "Precio_Q": 15.0},
        # CONTROLES (PRESENCIA, NAVAJA Y OEM)
        {"Categoría": "Controles", "Marca": "XHORSE", "Producto": "PRESENCIA (NARANJA)", "Stock_Inicial": 15, "Existencia": 14, "Usadas": 1, "Costo_Q": 350.0, "Precio_Q": 1200.0},
        {"Categoría": "Controles", "Marca": "XHORSE", "Producto": "PRESENCIA XM38 TOYOTA", "Stock_Inicial": 11, "Existencia": 11, "Usadas": 0, "Costo_Q": 450.0, "Precio_Q": 1300.0},
        {"Categoría": "Controles", "Marca": "AUTEL", "Producto": "PRESENCIA ROJOS IKEY", "Stock_Inicial": 2, "Existencia": 2, "Usadas": 0, "Costo_Q": 450.0, "Precio_Q": 1200.0},
        {"Categoría": "Controles", "Marca": "XHORSE", "Producto": "WIRE (ROJO) Navaja 10 estilos", "Stock_Inicial": 32, "Existencia": 22, "Usadas": 10, "Costo_Q": 150.0, "Precio_Q": 650.0},
        {"Categoría": "Controles", "Marca": "XHORSE", "Producto": "WIRELESS (AZUL) 6 estilos", "Stock_Inicial": 15, "Existencia": 14, "Usadas": 1, "Costo_Q": 175.0, "Precio_Q": 650.0},
        {"Categoría": "Controles", "Marca": "XHORSE", "Producto": "SUPERMODEL (MORADO) 4 estilos", "Stock_Inicial": 9, "Existencia": 9, "Usadas": 0, "Costo_Q": 175.0, "Precio_Q": 650.0},
        {"Categoría": "Controles", "Marca": "KEYDIY", "Producto": "CELESTE 2 estilos", "Stock_Inicial": 20, "Existencia": 18, "Usadas": 2, "Costo_Q": 150.0, "Precio_Q": 650.0},
        {"Categoría": "Controles", "Marca": "KEYDIY", "Producto": "ROJOS KD", "Stock_Inicial": 9, "Existencia": 9, "Usadas": 0, "Costo_Q": 125.0, "Precio_Q": 650.0},
        {"Categoría": "Controles", "Marca": "XHORSE", "Producto": "GARAGE (ROJO) Portón", "Stock_Inicial": 21, "Existencia": 12, "Usadas": 9, "Costo_Q": 150.0, "Precio_Q": 450.0},
        {"Categoría": "Controles", "Marca": "Toyota OEM", "Producto": "Diamante 3B / 4B / Cuadrado", "Stock_Inicial": 20, "Existencia": 19, "Usadas": 1, "Costo_Q": 350.0, "Precio_Q": 650.0},
        {"Categoría": "Controles", "Marca": "Honda OEM", "Producto": "3B / 4B Espadín (313.8/315/434)", "Stock_Inicial": 11, "Existencia": 10, "Usadas": 1, "Costo_Q": 350.0, "Precio_Q": 600.0},
        # CARCASAS Y BATERÍAS
        {"Categoría": "Carcasas", "Marca": "Honda / Toyota", "Producto": "Carcasa Control (3B / 4B / Diamante)", "Stock_Inicial": 32, "Existencia": 22, "Usadas": 10, "Costo_Q": 40.0, "Precio_Q": 200.0},
        {"Categoría": "Baterías", "Marca": "KEYLESS / MAXELL", "Producto": "Batería Litio CR2032 / CR1616 / CR2025", "Stock_Inicial": 175, "Existencia": 132, "Usadas": 43, "Costo_Q": 10.0, "Precio_Q": 30.0},
        # ESPADAS E INSERTOS
        {"Categoría": "Espadas e Insertos", "Marca": "Multimarca", "Producto": "Espada / Inserto Virgen para Control o Smart Key", "Stock_Inicial": 315, "Existencia": 295, "Usadas": 20, "Costo_Q": 21.0, "Precio_Q": 80.0}
    ])

if "citas_registradas" not in st.session_state:
    st.session_state.citas_registradas = pd.DataFrame(columns=[
        "Fecha_Hora_Cita", "Cliente", "Teléfono", "Vehículo_Detalle",
        "Servicio", "Ubicación", "Total_Cotizado_Q"
    ])

# ==============================================================================
# 4. ENCABEZADO HERO Y BARRA LATERAL CON REDES SOCIALES OFICIALES
# ==============================================================================
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🔑 CERRAJERÍA AUTOMOTRIZ ELÍAS</div>
    <div class="hero-subtitle">
        Laboratorio Móvil de Programación de Llaves con Chip, Controles de Presencia (Smart Key), Conversiones Tipo Navaja y Aperturas Sin Daño en <b>Chiquimula, Jalapa, Zacapa y Jutiapa</b>.
    </div>
    <span class="badge-tech">⚡ Autel MaxiIM IM508S</span>
    <span class="badge-tech">🤖 Corte CNC Xhorse Dolphin II</span>
    <span class="badge-tech">📡 Xhorse Key Tool Max Pro</span>
    <span class="badge-tech">🔋 Protección Voltaje Noco Genius 10</span>
    <span class="badge-orange">📍 Servicio a Domicilio 24/7: +502 5191-6984</span>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🌐 Nuestras Redes Oficiales")
    st.caption("Conecta con nuestra comunidad de +5,500 seguidores en Oriente:")
    st.markdown('<a class="social-btn" style="background:#25D366;" href="https://wa.link/77nelo" target="_blank">💬 WhatsApp Directo (+502 5191-6984)</a>', unsafe_allow_html=True)
    st.markdown('<a class="social-btn" style="background:#000000; border:1px solid #38BDF8;" href="https://www.tiktok.com/@cerrajeria_auto_elias" target="_blank">🎵 TikTok (@cerrajeria_auto_elias)</a>', unsafe_allow_html=True)
    st.markdown('<a class="social-btn" style="background:#1877F2;" href="https://www.facebook.com/search/top?q=Cerrajeria%20Automotriz%20Elias" target="_blank">📘 Facebook (Cerrajería Automotriz Elias)</a>', unsafe_allow_html=True)
    st.markdown('<a class="social-btn" style="background:linear-gradient(45deg,#F58529,#DD2A7B,#8134AF);" href="https://www.instagram.com/cerrajeria_auto_elias/" target="_blank">📸 Instagram (@cerrajeria_auto_elias)</a>', unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("### 🏆 Alcancía Nuevo Programador")
    st.caption("Meta: Lonsdor K518 Pro + Cables 8A-BA / Nissan 40-Pin (Q12,500)")
    ventas_actuales = 28865.0
    progreso_meta = min(1.0, 4850.0 / 12500.0)
    st.progress(progreso_meta)
    st.info("💡 **Meta Operativa:** Rotar las 59 llaves con chip dedicadas en stock (Q17,700 disponibles).")

# ==============================================================================
# 5. PESTAÑAS PRINCIPALES DE NAVEGACIÓN
# ==============================================================================
tab_cotizador, tab_catalogo, tab_admin = st.tabs([
    "⚡ 1. Cotizador Inteligente & Agendar Cita (Clientes)",
    "🚘 2. Catálogo de Controles & Cobertura Oriente",
    "🔐 3. Panel de Taller, Inventario 2027 & Semáforo (Admin)"
])

# ==============================================================================
# PESTAÑA 1: COTIZADOR INTELIGENTE "HASTA LA HORMIGA" + AGENDADOR WHATSAPP/EMAIL
# ==============================================================================
with tab_cotizador:
    st.subheader("🧮 Configura tu Vehículo, Revisa tu Desglose Exacto y Agenda tu Cita")
    st.write("Selecciona tu vehículo y el tipo de trabajo. Nuestro sistema calcula **cada pieza, batería, pin, corte CNC y programación** con total transparencia.")

    col_form, col_recibo = st.columns([1.15, 1.0], gap="large")

    with col_form:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Paso 1: ¿Qué deseas cotizar hoy?")
        tipo_bien = st.radio(
            "Categoría del Servicio:",
            ["🚗 Carro / Pick-up / Camioneta", "🏍️ Motocicleta / Cuatrimoto", "🚛 Camión Pesado (Hino/Isuzu/Freightliner)", "🏠 Casa / Control de Portón Eléctrico"],
            horizontal=True
        )

        desglose_items = []
        ficha_tecnica = {}
        alerta_tecnica = "VERDE"
        descripcion_vehiculo = ""

        # --- LÓGICA A: CARROS / PICK-UPS / CAMIONETAS ---
        if tipo_bien == "🚗 Carro / Pick-up / Camioneta":
            c1, c2 = st.columns(2)
            with c1:
                marca_sel = st.selectbox("Marca del Vehículo:", list(CATALOGO_VEHICULOS.keys()))
            with c2:
                modelo_sel = st.selectbox("Modelo y Generación:", list(CATALOGO_VEHICULOS[marca_sel].keys()))
            
            ficha_tecnica = CATALOGO_VEHICULOS[marca_sel][modelo_sel]
            alerta_tecnica = ficha_tecnica["riesgo"]
            descripcion_vehiculo = f"{marca_sel} - {modelo_sel}"

            st.caption(f"🔧 **Ficha Detectada:** Espada `{ficha_tecnica['espada']}` | Transponder `{ficha_tecnica['chip']}` | Frecuencia `{ficha_tecnica['frec']}`")

            situacion_llave = st.selectbox(
                "¿Cuál es tu situación actual?",
                [
                    "Tengo una llave que sí arranca y quiero SACAR COPIA (Duplicado Preventivo)",
                    "Quiero MODERNIZAR mi llave actual a Control Tipo Navaja Retráctil",
                    "PERDÍ TODAS LAS LLAVES (El carro está cerrado/tirado - Hacer desde cero AKL)",
                    "Solo necesito ABRIR mi vehículo (Dejé las llaves adentro)",
                    "Mi control ya no da o se quebró (Cambio de Carcasa / Batería / Diagnóstico)"
                ]
            )

            if "SACAR COPIA" in situacion_llave:
                estilo_copia = st.selectbox(
                    "Elige el tipo de llave o control que deseas:",
                    [
                        "1. Llave con Chip Estándar (Sin botones de control) — Económica y resistente",
                        "2. Llave con Chip Alta Seguridad (Chip G / Chip H 128-bits / Honda ID47 / Regata)",
                        "3. Control Tipo Navaja Moderno (Xhorse Serie Roja/Azul/Morada o Keydiy Celeste) + Chip",
                        "4. Control Estilo Original de Agencia (Espadín Diamante Toyota / Honda 3B-4B / Nissan)",
                        "5. Llave Inteligente de Presencia (Smart Key Push-to-Start Xhorse Naranja)",
                        "6. Llave Inteligente de Presencia Toyota / Lexus (Xhorse XM38 / Autel Rojo)",
                        "7. Llave 100% Metálica Sencilla (Para pick-up o carro antiguo sin inmovilizador)"
                    ]
                )
                if estilo_copia.startswith("1."):
                    desglose_items = [
                        ("Llave Automotriz con Cabeza Plástica (Perfil " + ficha_tecnica["espada"].split()[0] + ")", 75.0),
                        ("Chip Transponder Dedicado en Stock (4D67 / ID46 / 4D63)", 95.0),
                        ("Corte Computarizado de Precisión CNC (Máquina Xhorse Dolphin II)", 45.0),
                        ("Programación Inmovilizador por OBD2 (Autel IM508S + Protección Voltaje)", 85.0)
                    ] # Total = Q300.00
                elif estilo_copia.startswith("2."):
                    desglose_items = [
                        ("Llave de Alta Seguridad / Regata (" + ficha_tecnica["espada"].split()[0] + ")", 85.0),
                        ("Chip Transponder Criptográfico (Letra G 80-bits / Letra H 128-bits / ID47)", 125.0),
                        ("Corte CNC de Alta Precisión en 2 o 4 Pistas (Dolphin II XP-005L)", 65.0),
                        ("Programación / Clonación con Servidor Xhorse Key Tool Max Pro / Autel", 100.0)
                    ] # Total = Q375.00
                elif estilo_copia.startswith("3."):
                    desglose_items = [
                        ("Control Universal Tipo Navaja Retráctil (Xhorse Rojo/Azul/Morado o KD Celeste)", 260.0),
                        ("Espada / Inserto Metálico Virgen + Corte CNC en Dolphin II (" + ficha_tecnica["espada"].split()[0] + ")", 85.0),
                        ("Super Chip Transponder Programable (Xhorse XT27A / Dedicado)", 110.0),
                        ("Pin de Acero de Fijación de Espada (Pasador de Seguridad)", 15.0),
                        ("Batería de Litio CR2032 Instalada y Comprobada", 30.0),
                        ("Generación de Frecuencia + Programación OBD2 (Autel IM508S + Noco 10)", 150.0)
                    ] # Total = Q650.00
                elif estilo_copia.startswith("4."):
                    desglose_items = [
                        ("Control con Espadín Estilo Original OEM (Toyota Diamante / Honda / Nissan)", 340.0),
                        ("Chip Transponder Integrado + Batería de Litio CR2016/CR1616", 90.0),
                        ("Corte Computarizado CNC en Máquina Xhorse Dolphin II", 70.0),
                        ("Sincronización de Control e Inmovilizador por OBD2 (Autel IM508S)", 150.0)
                    ] # Total = Q650.00
                elif estilo_copia.startswith("5."):
                    desglose_items = [
                        ("Smart Key de Proximidad (Xhorse Presencia Naranja Frecuencia Multi-Banda)", 680.0),
                        ("Inserto Metálico de Emergencia + Corte CNC en Dolphin II", 95.0),
                        ("Batería de Litio CR2032 de Alto Rendimiento Instalada", 35.0),
                        ("Respaldo de Batería Vehicular (Mantenedor Noco Genius 10 A)", 70.0),
                        ("Programación de Proximidad Keyless Go por OBD2 (Autel IM508S)", 320.0)
                    ] # Total = Q1,200.00
                elif estilo_copia.startswith("6."):
                    desglose_items = [
                        ("Smart Key Especial Toyota / Lexus (Xhorse XM38 / Autel IKEY Rojo)", 760.0),
                        ("Inserto de Emergencia TOY48 + Corte CNC Dolphin II", 95.0),
                        ("Batería de Litio CR2032 Instalada y Medición de Frecuencia RF", 35.0),
                        ("Estabilización Electrónica de Voltaje (Noco Genius 10)", 70.0),
                        ("Programación Sistema Smart 8A / 4A con Autel IM508S", 340.0)
                    ] # Total = Q1,300.00
                else:
                    desglose_items = [
                        ("Llave Metálica Automotriz Virgen (TR40 / TR47 / DA34 / HON-31)", 35.0),
                        ("Corte Computarizado CNC en Máquina Xhorse Dolphin II", 30.0)
                    ] # Total = Q65.00

            elif "MODERNIZAR" in situacion_llave:
                desglose_items = [
                    ("Control Universal Tipo Navaja (Keydiy Celeste/Rojo o Xhorse Wire Rojo)", 220.0),
                    ("Espada / Inserto Metálico + Corte CNC Exacto (Dolphin II)", 75.0),
                    ("Pin de Acero de Fijación + Traslado/Adaptación de tu Chip Actual", 35.0),
                    ("Batería de Litio CR2032 Nueva Instalada", 30.0),
                    ("Generación y Programación de Cierre Centralizado en el Vehículo", 65.0)
                ] # Total = Q425.00

            elif "PERDÍ TODAS LAS LLAVES" in situacion_llave:
                estilo_akl = st.selectbox(
                    "¿Qué tipo de llave usaba tu carro antes de perderla?",
                    [
                        "1. Llave con Chip de Corte Normal (Hilux, Corolla, Yaris, Frontier, L200, Mazda)",
                        "2. Llave con Chip de Regata / Alta Seguridad o Chip H (Honda HON66, Ford HU101, Toyota H)",
                        "3. Quiero que me entreguen de una vez Llave con Control Navaja o Control Original",
                        "4. Llave de Presencia (Encendido de Botón Smart Key - Honda, Mazda, Hyundai, Kia, Mitsu)",
                        "5. Llave de Presencia Toyota / Lexus (Encendido de Botón Smart Key 8A / 4A)",
                        "6. Carro o Pick-up Antiguo 100% Mecánico (Sin chip inmovilizador)"
                    ]
                )
                if estilo_akl.startswith("1."):
                    desglose_items = [
                        ("Apertura Técnica Sin Daño y Lectura de Alturas de Chapa con Ganzúa Lishi", 180.0),
                        ("Decodificación Mecánica y Corte de Llave desde Cero en CNC Dolphin II", 120.0),
                        ("Llave Automotriz + Chip Transponder Nuevo (Dedicado / XT27A)", 140.0),
                        ("Protección de Batería (Noco Genius 10) + Reseteo/Programación Inmovilizador OBD2", 260.0)
                    ] # Total = Q700.00
                elif estilo_akl.startswith("2."):
                    desglose_items = [
                        ("Apertura y Decodificación de Cilindro de Alta Seguridad con Lishi Especial", 240.0),
                        ("Corte CNC de Pista Interna desde Cero (Xhorse Dolphin II XP-005L)", 150.0),
                        ("Llave de Regata / Alta Seguridad + Chip Criptográfico (Chip H / ID47 / ID49)", 180.0),
                        ("Estabilizador Noco Genius 10 + Programación por Pérdida Total (Autel IM508S)", 330.0)
                    ] # Total = Q900.00
                elif estilo_akl.startswith("3."):
                    desglose_items = [
                        ("Apertura y Lectura Mecánica de Cilindro con Herramienta Lishi", 200.0),
                        ("Control Tipo Navaja / Original OEM + Inserto Cortado desde Cero en Dolphin II", 410.0),
                        ("Chip Transponder Nuevo + Pin de Acero + Batería de Litio CR2032", 160.0),
                        ("Programación Completa de Arranque y Control Remoto por OBD2 (Autel IM508S)", 330.0)
                    ] # Total = Q1,100.00
                elif estilo_akl.startswith("4."):
                    desglose_items = [
                        ("Apertura de Emergencia y Decodificación de Cerradura con Ganzúa Lishi", 250.0),
                        ("Smart Key de Proximidad (Xhorse Presencia Naranja) + Batería Litio CR2032", 720.0),
                        ("Inserto de Emergencia Cortado desde Cero por Código en CNC Dolphin II", 130.0),
                        ("Soporte de Voltaje Noco Genius 10 + Programación Inmovilizador desde Cero", 700.0)
                    ] # Total = Q1,800.00
                elif estilo_akl.startswith("5."):
                    desglose_items = [
                        ("Apertura Profesional y Lectura de Chapa TOY48/TR47 con Lishi", 250.0),
                        ("Smart Key Especial Toyota (Xhorse XM38) + Batería de Litio CR2032", 820.0),
                        ("Espadín de Emergencia Cortado por Código en CNC Dolphin II", 130.0),
                        ("Conexión de Arnés Inteligente Detrás de Guantera (Bypass Sin Desoldar)", 380.0),
                        ("Emulación y Programación de Módulo Smart Key con Autel IM508S + Noco 10", 520.0)
                    ] # Total = Q2,100.00
                else:
                    desglose_items = [
                        ("Apertura y Lectura de Combinación de Guardas con Ganzúa Lishi", 150.0),
                        ("Llave Metálica Virgen + Corte Exacto desde Cero en CNC Dolphin II", 150.0)
                    ] # Total = Q300.00

            elif "ABRIR" in situacion_llave:
                tipo_apertura = st.radio(
                    "Tipo de cerradura del vehículo:",
                    ["Cerradura Estándar (Llave normal dentada)", "Cerradura Alta Seguridad / Regata (Honda, Ford moderno, VW/BMW, Toyota botón)"]
                )
                if "Estándar" in tipo_apertura:
                    desglose_items = [
                        ("Apertura Técnica Profesional con Ganzúa Lishi (0% rayones, sin inflar puertas)", 175.0)
                    ]
                else:
                    desglose_items = [
                        ("Apertura de Alta Precisión en Cilindro de Regata con Lishi Especializado", 275.0)
                    ]

            else:
                sub_taller = st.selectbox(
                    "Selecciona el servicio de reparación o diagnóstico:",
                    [
                        "Cambio de Carcasa Nueva + Corte + Traslado de Placa/Chip (Q200)",
                        "Cambio de Batería de Litio Original + Medición de Frecuencia RF (Q35)",
                        "Diagnóstico Electrónico Completo Autel IM508S + Test Batería Topdon (Q150)",
                        "Cambio de Combinación de Switch/Chapa por Robo de Llave (Q400)",
                        "Rescate de Batería Muerta con Jumpstarter + Test Alternador (Q100)"
                    ]
                )
                if "Carcasa" in sub_taller:
                    desglose_items = [
                        ("Carcasa Nueva de Alta Resistencia (Honda / Toyota / Hyundai)", 110.0),
                        ("Corte Computarizado CNC en Dolphin II + Pin de Acero (si aplica)", 55.0),
                        ("Traslado Cuidadoso de Placa Electrónica, Chip Transponder y Limpieza", 35.0)
                    ]
                elif "Batería de Litio" in sub_taller:
                    desglose_items = [
                        ("Batería de Litio (CR2032 Maxell/Keyless, CR1616, CR2025 o CR2016)", 25.0),
                        ("Instalación + Comprobación de Emisión de Frecuencia con Key Tool Max Pro", 10.0)
                    ]
                elif "Diagnóstico" in sub_taller:
                    desglose_items = [
                        ("Escaneo General de Módulos (Motor, ABS, Airbag, BCM) con Autel IM508S", 100.0),
                        ("Prueba Certificada de Vida de Batería y Alternador con Topdon BT Mobile Elite", 50.0)
                    ]
                elif "Combinación" in sub_taller:
                    desglose_items = [
                        ("Juego de Guardas Nuevas (Honda/Toyota) y Reconfiguración de Cilindro", 260.0),
                        ("Llave Nueva Cortada a la Nueva Combinación en CNC Dolphin II", 140.0)
                    ]
                else:
                    desglose_items = [
                        ("Arranque de Emergencia con Jumpstarter Profesional", 60.0),
                        ("Diagnóstico de Sistema de Carga y Alternador con Topdon BT Mobile", 40.0)
                    ]

        # --- LÓGICA B: MOTOCICLETAS ---
        elif tipo_bien == "🏍️ Motocicleta / Cuatrimoto":
            marca_moto = st.selectbox("Marca de tu Moto:", ["Honda (HD75 / Navi / XR / Twister)", "Suzuki (SUZ12 / Gixxer / GN125)", "Yamaha (YM63 / YH48 / Fazer / Crux)", "Bajaj / Pulsar (Discover / NS200)", "Italika / Kymco / Kawasaki"])
            descripcion_vehiculo = f"Motocicleta {marca_moto}"
            serv_moto = st.radio("Servicio requerido para la moto:", ["Sacar copia de llave (Tengo muestra)", "Perdí todas las llaves de la moto (Hacer llave desde cero)"])
            if "copia" in serv_moto:
                precio_m = 45.0 if "Navi" in marca_moto else 35.0
                desglose_items = [
                    (f"Llave Virgen para {marca_moto}", 20.0),
                    ("Corte de Precisión en Máquina Duplicadora", precio_m - 20.0)
                ]
            else:
                desglose_items = [
                    ("Lectura Mecánica de Alturas de Switch / Tapón de Gasolina", 110.0),
                    (f"Llave Virgen para {marca_moto} + Corte Exacto desde Cero en Dolphin II", 90.0)
                ]

        # --- LÓGICA C: CAMIONES PESADOS ---
        elif tipo_bien == "🚛 Camión Pesado (Hino/Isuzu/Freightliner)":
            camion_sel = st.selectbox("Marca del Camión:", ["Freightliner (FRE-1)", "Hino Serie 300 / 500 (X274 / HN3)", "Isuzu NPR / NQR / ELF (X275 / B113)", "Kenworth (K1994 / B87)"])
            descripcion_vehiculo = f"Camión {camion_sel}"
            serv_camion = st.radio("Servicio para el camión:", ["Duplicado de llave metálica", "Hechura de llave desde cero (Pérdida total)", "Apertura de cabina sin daño"])
            if "Duplicado" in serv_camion:
                desglose_items = [
                    (f"Llave de Trabajo Pesado {camion_sel}", 45.0),
                    ("Corte Computarizado CNC en Dolphin II", 40.0)
                ] # Q85
            elif "cero" in serv_camion:
                desglose_items = [
                    ("Apertura y Lectura de Cilindro de Camión con Herramienta Lishi", 180.0),
                    (f"Llave Virgen {camion_sel} + Corte por Código en CNC Dolphin II", 120.0)
                ] # Q300
            else:
                desglose_items = [("Apertura Técnica de Cabina de Camión Sin Daño", 200.0)]

        # --- LÓGICA D: CASA / PORTÓN ELÉCTRICO ---
        else:
            descripcion_vehiculo = "Servicio Residencial / Portón Eléctrico"
            serv_casa = st.radio("Selecciona lo que necesitas:", ["Control para Portón Eléctrico (Xhorse Garage Rojo)", "Duplicado de Llave de Casa (Kwikset, Yale, Schlage, Alba)", "Promo 2 Copias de Llave de Casa"])
            if "Portón" in serv_casa:
                desglose_items = [
                    ("Control Universal Clonador de Portón (Xhorse Garage Rojo Alta Potencia)", 260.0),
                    ("Batería Instalada + Copia/Sincronización de Frecuencia con Key Tool Max Pro", 115.0)
                ] # Q375
            elif "Promo" in serv_casa:
                desglose_items = [("2x Llaves Residenciales (Yale / Kwikset / Schlage) Cortadas", 25.0)]
            else:
                desglose_items = [("1x Llave Residencial (Yale / Kwikset / Schlage / Alba) Cortada", 15.0)]

        st.write("---")
        st.markdown("#### Paso 2: Ubicación Exacta y Agenda de tu Cita")
        u1, u2 = st.columns(2)
        with u1:
            depto_sel = st.selectbox("Departamento:", list(ZONAS_ORIENTE.keys()))
        with u2:
            muni_sel = st.selectbox("Municipio / Ruta:", list(ZONAS_ORIENTE[depto_sel].keys()))
        
        costo_traslado = ZONAS_ORIENTE[depto_sel][muni_sel]
        if costo_traslado > 0:
            desglose_items.append((f"Traslado Unidad Móvil hasta {muni_sel} ({depto_sel})", costo_traslado))
        else:
            desglose_items.append((f"Atención en Zona Base ({muni_sel}) — Sin recargo de envío", 0.0))

        direccion_exacta = st.text_input("📍 Dirección exacta, aldea, gasolinera o punto de referencia:", placeholder="Ej. Frente a Gasolinera Shell salida a Ipala / Parque Central...")
        
        f1, f2 = st.columns(2)
        with f1:
            fecha_cita = st.date_input("📅 Fecha deseada:", min_value=date.today(), value=date.today())
        with f2:
            hora_cita = st.time_input("⏰ Hora preferida:", value=time(10, 0))

        n1, n2 = st.columns(2)
        with n1:
            nombre_cliente = st.text_input("👤 Tu Nombre:", placeholder="Ej. Carlos Morales")
        with n2:
            tel_cliente = st.text_input("📱 Tu Teléfono / WhatsApp:", placeholder="Ej. 5544-3322")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- COLUMNA DERECHA: RECIBO TRANSPARENTE "HASTA LA HORMIGA" ---
    with col_recibo:
        total_cotizacion = sum(monto for _, monto in desglose_items)
        fecha_str = fecha_cita.strftime("%d/%m/%Y")
        hora_str = hora_cita.strftime("%I:%M %p")

        if alerta_tecnica == "ROJO":
            st.error("⚠️ **NOTA TÉCNICA IMPORTANTE:** Este modelo reciente (2021-2026) utiliza seguridad avanzada (CAN-FD / BCM 40 pines / Código BA). Envíanos tu cotización por WhatsApp con foto de tu llave o VIN para confirmar disponibilidad de servidor antes de agendar.")
        elif alerta_tecnica == "AMARILLO":
            st.warning("⚡ **PROTECCIÓN ELECTRÓNICA INCLUIDA:** Este vehículo requiere estabilizador de voltaje **Noco Genius 10** conectado durante toda la programación (ya incluido en tu cotización).")

        html_lineas = ""
        texto_lineas_wa = ""
        for concepto, valor in desglose_items:
            html_lineas += f'<div class="receipt-line"><span>🔹 {concepto}</span><b>Q {valor:,.2f}</b></div>'
            texto_lineas_wa += f"• {concepto}: Q{valor:,.2f}\n"

        st.markdown(f"""
        <div class="receipt-box">
            <div class="receipt-header">
                <h3 style="margin:0; color:#F97316;">🧾 COTIZACIÓN OFICIAL DESGLOSADA</h3>
                <p style="margin:4px 0 0 0; font-size:13px; color:#94A3B8;">
                    <b>Cerrajería Automotriz Elías</b> | Tel/WhatsApp: +502 5191-6984<br>
                    <b>Vehículo/Bien:</b> {descripcion_vehiculo}<br>
                    <b>Ubicación:</b> {muni_sel}, {depto_sel} ({direccion_exacta if direccion_exacta else 'Por confirmar'})<br>
                    <b>Cita solicitada:</b> {fecha_str} a las {hora_str}
                </p>
            </div>
            {html_lineas}
            <div class="receipt-total">
                <span>PRECIO FINAL TODO INCLUIDO:</span>
                <span>Q {total_cotizacion:,.2f}</span>
            </div>
            <p style="font-size:12px; color:#94A3B8; margin-top:10px; margin-bottom:0;">
                ✅ Incluye mano de obra certificada, corte láser/CNC, materiales nuevos y garantía de funcionamiento.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Construcción del mensaje automático para WhatsApp (+502 5191 6984)
        mensaje_wa = (
            f"🔑 *NUEVA COTIZACIÓN Y CITA - CERRAJERÍA ELÍAS*\n\n"
            f"👤 *Cliente:* {nombre_cliente if nombre_cliente else 'Cliente Web'}\n"
            f"📱 *Teléfono:* {tel_cliente if tel_cliente else 'No indicado'}\n"
            f"🚗 *Vehículo/Servicio:* {descripcion_vehiculo}\n"
            f"📍 *Ubicación:* {muni_sel}, {depto_sel} ({direccion_exacta if direccion_exacta else 'Sin referencia'})\n"
            f"📅 *Fecha y Hora:* {fecha_str} a las {hora_str}\n\n"
            f"📋 *DESGLOSE COMPLETO DE MATERIALES Y TRABAJO:*\n"
            f"{texto_lineas_wa}\n"
            f"💰 *TOTAL FINAL A PAGAR: Q{total_cotizacion:,.2f}*\n\n"
            f"¿Me confirman disponibilidad para esta cita?"
        )
        wa_encoded = urllib.parse.quote(mensaje_wa)
        link_whatsapp = f"https://wa.me/50251916984?text={wa_encoded}"

        asunto_mail = urllib.parse.quote(f"Cotización y Cita: {descripcion_vehiculo} - Q{total_cotizacion:,.2f}")
        link_mailto = f"mailto:cerrajeriaelias@gmail.com?subject={asunto_mail}&body={wa_encoded}"

        st.markdown(f'<a class="btn-wa" href="{link_whatsapp}" target="_blank">📲 ENVIAR COTIZACIÓN Y CONFIRMAR CITA POR WHATSAPP</a>', unsafe_allow_html=True)
        st.markdown(f'<a class="btn-mail" href="{link_mailto}">📧 Enviar copia por Correo Electrónico</a>', unsafe_allow_html=True)

        st.download_button(
            label="📥 Descargar Recibo de Cotización en el Celular (.TXT)",
            data=mensaje_wa.encode("utf-8"),
            file_name=f"Cotizacion_Cerrajeria_Elias_{datetime.now().strftime('%d%m%Y_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )

# ==============================================================================
# PESTAÑA 2: CATÁLOGO DE CONTROLES Y COBERTURA EN ORIENTE
# ==============================================================================
with tab_catalogo:
    st.subheader("🚘 Nuestro Arsenal de Llaves, Controles y Tecnología en Oriente")
    c_cat1, c_cat2, c_cat3 = st.columns(3)
    with c_cat1:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#38BDF8;">📡 Llaves de Presencia (Smart Key)</h4>
            <p>Para vehículos que encienden con botón <b>Start/Stop</b>:</p>
            <ul>
                <li><b>Xhorse XM38 Toyota:</b> Hilux, RAV4, Corolla, Tacoma, 4Runner, Land Cruiser.</li>
                <li><b>Xhorse Presencia Naranja:</b> Honda CR-V/Civic, Mazda 3/CX-5, Hyundai, Kia, Nissan, Mitsubishi.</li>
                <li><b>Autel IKEY Rojo:</b> Rango extendido OEM.</li>
            </ul>
            <b>Duplicado: Q1,200 - Q1,300 | Desde cero: Q1,800 - Q2,100</b>
        </div>
        """, unsafe_allow_html=True)
    with c_cat2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#F97316;">🔪 Conversiones a Control Navaja</h4>
            <p>Transforma tu llave sencilla o control roto en una llave retráctil moderna:</p>
            <ul>
                <li><b>Xhorse Serie Roja / Azul / Supermodel Morado.</b></li>
                <li><b>Keydiy Serie Celeste y Roja</b> de alta durabilidad.</li>
                <li>Incluye corte CNC en <b>Dolphin II</b>, pin de acero y batería CR2032.</li>
            </ul>
            <b>Upgrade (usando tu chip): Q425 | Completa con chip nuevo: Q650</b>
        </div>
        """, unsafe_allow_html=True)
    with c_cat3:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#4ADE80;">🛡️ Llaves con Chip & Portones</h4>
            <p>Seguridad inmediata para no quedarte tirado:</p>
            <ul>
                <li><b>Llaves con Chip Originales:</b> Toyota 4D67, G y H; Honda ID46/ID47; Nissan; Mazda; Mitsu; Ford; Isuzu.</li>
                <li><b>Controles de Portón Eléctrico:</b> Xhorse Garage Rojo.</li>
                <li><b>Carcasas y Baterías Maxell/Keyless:</b> Cambio en 5 minutos.</li>
            </ul>
            <b>Duplicado Chip: Q300 - Q375 | Control Portón: Q375</b>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# PESTAÑA 3: PANEL INTERNO DE TALLER, INVENTARIO 2027 Y SEMÁFORO (ADMIN)
# ==============================================================================
with tab_admin:
    st.subheader("🔐 Panel Administrativo e Inventario 2027 (Uso Exclusivo Taller)")
    pin_acceso = st.text_input("Ingresa el PIN del Taller para desbloquear la contabilidad (Pista: últimos 4 dígitos de tu teléfono o 5191):", type="password")

    if pin_acceso in ["5191", "6984"]:
        st.success("✅ Acceso concedido. Bienvenido al Sistema Operativo de Cerrajería Automotriz Elías.")
        
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
    else:
        st.info("🔒 Ingresa el PIN `5191` o `6984` arriba para abrir el control de stock y descuentos en combo.")
