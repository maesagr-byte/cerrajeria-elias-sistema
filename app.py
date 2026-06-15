import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la página
st.set_page_config(page_title="Cerrajería Automotriz Elias", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main-title { font-size:35px; font-weight:bold; color:#1C2833; margin-bottom:10px; }
    .sub-title { font-size:20px; color:#566573; margin-bottom:20px; }
    .metric-box { background-color:#EAEDED; padding:15px; border-radius:10px; border-left:5px solid #E67E22; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🔑 Cerrajería Automotriz Elias</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Sistema Integral de Inventario, Servicios y Facturación</div>', unsafe_allow_html=True)

# 2. Base de Datos Completa (Extraída de Excel Oficial)
if "inv_cerrajeria" not in st.session_state:
    productos_cerrajeria = [
        # --- RESIDENCIAL ---
        {"Código": "1", "Descripción": "Kwikset llave ND", "Categoría": "Residencial", "Costo (Q)": 3.84, "Precio (Q)": 15.0, "Stock": 20},
        {"Código": "2", "Descripción": "Schlage llave SC1", "Categoría": "Residencial", "Costo (Q)": 1.72, "Precio (Q)": 15.0, "Stock": 10},
        {"Código": "2", "Descripción": "Kwikset llave KW1", "Categoría": "Residencial", "Costo (Q)": 4.48, "Precio (Q)": 15.0, "Stock": 10},
        {"Código": "3", "Descripción": "Yale R8 Larga", "Categoría": "Residencial", "Costo (Q)": 2.50, "Precio (Q)": 15.0, "Stock": 13},
        {"Código": "3", "Descripción": "Yale Y1 Corta", "Categoría": "Residencial", "Costo (Q)": 2.90, "Precio (Q)": 15.0, "Stock": 35},
        {"Código": "1", "Descripción": "Philips Alba", "Categoría": "Residencial", "Costo (Q)": 2.50, "Precio (Q)": 15.0, "Stock": 6},
        {"Código": "3", "Descripción": "Yale Cabezona", "Categoría": "Residencial", "Costo (Q)": 2.50, "Precio (Q)": 15.0, "Stock": 3},

        # --- CARRO/CAMION ---
        {"Código": "5", "Descripción": "Toyota TR40 Metalica", "Categoría": "Carro/Camión", "Costo (Q)": 5.44, "Precio (Q)": 50.0, "Stock": 30},
        {"Código": "6", "Descripción": "Toyota TR47 Metalica", "Categoría": "Carro/Camión", "Costo (Q)": 4.32, "Precio (Q)": 50.0, "Stock": 14},
        {"Código": "7", "Descripción": "Honda -31 Metalica", "Categoría": "Carro/Camión", "Costo (Q)": 7.76, "Precio (Q)": 50.0, "Stock": 14},
        {"Código": "4", "Descripción": "Nissan DA34", "Categoría": "Carro/Camión", "Costo (Q)": 4.80, "Precio (Q)": 50.0, "Stock": 8},
        {"Código": "4", "Descripción": "Mazda MZ31", "Categoría": "Carro/Camión", "Costo (Q)": 7.50, "Precio (Q)": 50.0, "Stock": 2},
        {"Código": "4", "Descripción": "Mitsubishi Mit1", "Categoría": "Carro/Camión", "Costo (Q)": 7.50, "Precio (Q)": 50.0, "Stock": 1},
        {"Código": "8", "Descripción": "Freightleiner FRE-1", "Categoría": "Carro/Camión", "Costo (Q)": 6.88, "Precio (Q)": 50.0, "Stock": 10},
        {"Código": "9", "Descripción": "Hino X274 / HN3", "Categoría": "Carro/Camión", "Costo (Q)": 9.44, "Precio (Q)": 50.0, "Stock": 10},
        {"Código": "9", "Descripción": "Isuzu (IZ-DR) X275 /B113", "Categoría": "Carro/Camión", "Costo (Q)": 10.67, "Precio (Q)": 50.0, "Stock": 12},
        {"Código": "8", "Descripción": "Kenworth K1994 / B87", "Categoría": "Carro/Camión", "Costo (Q)": 7.20, "Precio (Q)": 50.0, "Stock": 5},

        # --- MOTO ---
        {"Código": "11", "Descripción": "Honda HD75 NP / X138", "Categoría": "Moto", "Costo (Q)": 6.51, "Precio (Q)": 20.0, "Stock": 28},
        {"Código": "12", "Descripción": "Yamaha YM63 / X248", "Categoría": "Moto", "Costo (Q)": 11.08, "Precio (Q)": 20.0, "Stock": 6},
        {"Código": "12", "Descripción": "Yamaha YH48 NP / YAMA-191", "Categoría": "Moto", "Costo (Q)": 10.40, "Precio (Q)": 20.0, "Stock": 10},
        {"Código": "10", "Descripción": "Suzuki X179 / SUZ12", "Categoría": "Moto", "Costo (Q)": 9.07, "Precio (Q)": 20.0, "Stock": 30},
        {"Código": "12", "Descripción": "Kawasaki X278 / KA33", "Categoría": "Moto", "Costo (Q)": 12.00, "Precio (Q)": 20.0, "Stock": 4},
        {"Código": "11", "Descripción": "Honda HD103", "Categoría": "Moto", "Costo (Q)": 10.00, "Precio (Q)": 20.0, "Stock": 5},
        {"Código": "11", "Descripción": "Honda HD109", "Categoría": "Moto", "Costo (Q)": 10.00, "Precio (Q)": 20.0, "Stock": 4},
        {"Código": "12", "Descripción": "Kymco KYM2", "Categoría": "Moto", "Costo (Q)": 10.00, "Precio (Q)": 20.0, "Stock": 2},
        {"Código": "13", "Descripción": "Pulsar MAPA", "Categoría": "Moto", "Costo (Q)": 25.00, "Precio (Q)": 50.0, "Stock": 5},
        {"Código": "13", "Descripción": "Bajaj BAJ-2DP", "Categoría": "Moto", "Costo (Q)": 15.00, "Precio (Q)": 30.0, "Stock": 2},
        {"Código": "13", "Descripción": "Bajaj Discover", "Categoría": "Moto", "Costo (Q)": 15.00, "Precio (Q)": 30.0, "Stock": 2},
        {"Código": "13", "Descripción": "Italika 1DP", "Categoría": "Moto", "Costo (Q)": 15.00, "Precio (Q)": 30.0, "Stock": 2},
        {"Código": "13", "Descripción": "Italika 1P", "Categoría": "Moto", "Costo (Q)": 15.00, "Precio (Q)": 30.0, "Stock": 2},
        {"Código": "13", "Descripción": "Italika IK-2P", "Categoría": "Moto", "Costo (Q)": 15.00, "Precio (Q)": 30.0, "Stock": 1},
        {"Código": "14", "Descripción": "Suzuki Cabeza plastica", "Categoría": "Moto", "Costo (Q)": 15.00, "Precio (Q)": 30.0, "Stock": 6},
        {"Código": "14", "Descripción": "Suzuki Plastica pequeñita 13AP", "Categoría": "Moto", "Costo (Q)": 20.00, "Precio (Q)": 25.0, "Stock": 2},
        {"Código": "14", "Descripción": "Honda Navy", "Categoría": "Moto", "Costo (Q)": 15.00, "Precio (Q)": 30.0, "Stock": 7},

        # --- SIN CHIP ---
        {"Código": "1", "Descripción": "Toyota TR47 (Sin Chip)", "Categoría": "Sin Chip", "Costo (Q)": 35.00, "Precio (Q)": 255.0, "Stock": 12},
        {"Código": "2", "Descripción": "Honda HON66 (Sin Chip)", "Categoría": "Sin Chip", "Costo (Q)": 35.00, "Precio (Q)": 255.0, "Stock": 10},
        {"Código": "1", "Descripción": "Mitsubishi MIT1 (Sin Chip)", "Categoría": "Sin Chip", "Costo (Q)": 35.00, "Precio (Q)": 255.0, "Stock": 3},
        {"Código": "2", "Descripción": "NISSAN NS (Sin Chip)", "Categoría": "Sin Chip", "Costo (Q)": 35.00, "Precio (Q)": 255.0, "Stock": 2},
        {"Código": "2", "Descripción": "Isuzu B111 (Sin Chip)", "Categoría": "Sin Chip", "Costo (Q)": 35.00, "Precio (Q)": 255.0, "Stock": 3},
        {"Código": "1", "Descripción": "Mazda MZ (Sin Chip)", "Categoría": "Sin Chip", "Costo (Q)": 35.00, "Precio (Q)": 255.0, "Stock": 3},
        {"Código": "3", "Descripción": "Ford HU101 (Sin Chip)", "Categoría": "Sin Chip", "Costo (Q)": 35.00, "Precio (Q)": 255.0, "Stock": 7},

        # --- CON CHIP ---
        {"Código": "4", "Descripción": "Toyota TR47 TEXAS ID 4D67", "Categoría": "Con Chip", "Costo (Q)": 70.00, "Precio (Q)": 360.0, "Stock": 5},
        {"Código": "5", "Descripción": "Toyota TR47 TEXAS ID 4D74 128 BITS H", "Categoría": "Con Chip", "Costo (Q)": 70.00, "Precio (Q)": 360.0, "Stock": 5},
        {"Código": "4", "Descripción": "Toyota TR47 TEXAS ID 4D72 80 BITS G", "Categoría": "Con Chip", "Costo (Q)": 70.00, "Precio (Q)": 360.0, "Stock": 12},
        {"Código": "5", "Descripción": "Toyota TR48 TEXAS ID 4D74 128 BITS H", "Categoría": "Con Chip", "Costo (Q)": 70.00, "Precio (Q)": 360.0, "Stock": 8},
        {"Código": "6", "Descripción": "Honda HON66 HO01 ID46", "Categoría": "Con Chip", "Costo (Q)": 70.00, "Precio (Q)": 360.0, "Stock": 12},
        {"Código": "6", "Descripción": "Honda HON66 HO01 ID47", "Categoría": "Con Chip", "Costo (Q)": 70.00, "Precio (Q)": 360.0, "Stock": 2},
        {"Código": "7", "Descripción": "Mitsubishi MIT3 ID46 A", "Categoría": "Con Chip", "Costo (Q)": 70.00, "Precio (Q)": 360.0, "Stock": 7},
        {"Código": "7", "Descripción": "Nissan DA34 ID46", "Categoría": "Con Chip", "Costo (Q)": 70.00, "Precio (Q)": 360.0, "Stock": 4},
        {"Código": "7", "Descripción": "Mazda H76 TEXAS 4D63 80 BITS", "Categoría": "Con Chip", "Costo (Q)": 70.00, "Precio (Q)": 360.0, "Stock": 4},

        # --- CARCASAS ---
        {"Código": "0", "Descripción": "Honda 4B 2005-2012", "Categoría": "Carcasas", "Costo (Q)": 105.00, "Precio (Q)": 300.0, "Stock": 2},
        {"Código": "0", "Descripción": "Honda 4B 2013+", "Categoría": "Carcasas", "Costo (Q)": 280.00, "Precio (Q)": 250.0, "Stock": 4},
        {"Código": "0", "Descripción": "Honda 4 botones placa -2012", "Categoría": "Carcasas", "Costo (Q)": 50.00, "Precio (Q)": 150.0, "Stock": 1},
        {"Código": "0", "Descripción": "Toyota Diamante 4B", "Categoría": "Carcasas", "Costo (Q)": 135.00, "Precio (Q)": 200.0, "Stock": 3},
        {"Código": "0", "Descripción": "Toyota 4B", "Categoría": "Carcasas", "Costo (Q)": 90.00, "Precio (Q)": 250.0, "Stock": 1},

        # --- CONTROLES ESPADIN ---
        {"Código": "8", "Descripción": "Nissan 3B Espadín", "Categoría": "Controles", "Costo (Q)": 200.00, "Precio (Q)": 550.0, "Stock": 1},
        {"Código": "8", "Descripción": "Toyota 3B Espadín", "Categoría": "Controles", "Costo (Q)": 200.00, "Precio (Q)": 550.0, "Stock": 2},
        {"Código": "8", "Descripción": "Toyota 4B Espadín", "Categoría": "Controles", "Costo (Q)": 200.00, "Precio (Q)": 550.0, "Stock": 1},
        {"Código": "8", "Descripción": "Honda 3B Espadín", "Categoría": "Controles", "Costo (Q)": 200.00, "Precio (Q)": 550.0, "Stock": 2},
        {"Código": "8", "Descripción": "Honda 4B Espadín", "Categoría": "Controles", "Costo (Q)": 200.00, "Precio (Q)": 550.0, "Stock": 5},

        # --- CONTROLES XHORSE ---
        {"Código": "0", "Descripción": "XHORSE PRESENCIA (Naranja)", "Categoría": "Xhorse", "Costo (Q)": 250.00, "Precio (Q)": 1100.0, "Stock": 26},
        {"Código": "0", "Descripción": "XHORSE WIRELESS (Azul)", "Categoría": "Xhorse", "Costo (Q)": 170.00, "Precio (Q)": 800.0, "Stock": 6},
        {"Código": "0", "Descripción": "XHORSE SUPERMODEL (Morado)", "Categoría": "Xhorse", "Costo (Q)": 170.00, "Precio (Q)": 800.0, "Stock": 4},
        {"Código": "0", "Descripción": "XHORSE GARAGE", "Categoría": "Xhorse", "Costo (Q)": 135.00, "Precio (Q)": 550.0, "Stock": 19},
        {"Código": "0", "Descripción": "XHORSE WIRE (Rojo) Navaja", "Categoría": "Xhorse", "Costo (Q)": 135.00, "Precio (Q)": 800.0, "Stock": 26},

        # --- CHIPS Y PINES ---
        {"Código": "15", "Descripción": "XHORSE XT27A", "Categoría": "Chips", "Costo (Q)": 35.00, "Precio (Q)": 120.0, "Stock": 71},
        {"Código": "15", "Descripción": "XHORSE ID46", "Categoría": "Chips", "Costo (Q)": 35.00, "Precio (Q)": 120.0, "Stock": 5},
        {"Código": "15", "Descripción": "XHORSE ID4C/T5", "Categoría": "Chips", "Costo (Q)": 35.00, "Precio (Q)": 120.0, "Stock": 5},
        {"Código": "15", "Descripción": "XHORSE ID46/ID4D/ID48/T5", "Categoría": "Chips", "Costo (Q)": 35.00, "Precio (Q)": 120.0, "Stock": 5},
        {"Código": "15", "Descripción": "XHORSE Honda G ID47", "Categoría": "Chips", "Costo (Q)": 35.00, "Precio (Q)": 120.0, "Stock": 2},
        {"Código": "15", "Descripción": "PINES", "Categoría": "Chips", "Costo (Q)": 5.00, "Precio (Q)": 15.0, "Stock": 225},

        # --- ESPADAS Y CABEZAS ---
        {"Código": "9", "Descripción": "Mitsubishi MIT6 / MIT-18P", "Categoría": "Espadas", "Costo (Q)": 20.0, "Precio (Q)": 120.0, "Stock": 10},
        {"Código": "9", "Descripción": "Mitsubishi MIT17-PT", "Categoría": "Espadas", "Costo (Q)": 20.0, "Precio (Q)": 120.0, "Stock": 10},
        {"Código": "9", "Descripción": "Toyota TOY43 / TOY15P", "Categoría": "Espadas", "Costo (Q)": 20.0, "Precio (Q)": 120.0, "Stock": 7},
        {"Código": "9", "Descripción": "Hyundai/Kia HIN6 / HI-4", "Categoría": "Espadas", "Costo (Q)": 20.0, "Precio (Q)": 120.0, "Stock": 10},
        {"Código": "9", "Descripción": "Mazda MAZ24R / MAZ-11D.P", "Categoría": "Espadas", "Costo (Q)": 20.0, "Precio (Q)": 120.0, "Stock": 9},
        {"Código": "9", "Descripción": "Isuzu ISU5 / TP00ISU-5.P3", "Categoría": "Espadas", "Costo (Q)": 20.0, "Precio (Q)": 120.0, "Stock": 10},
        {"Código": "9", "Descripción": "Honda HO01 / HOND-31", "Categoría": "Espadas", "Costo (Q)": 20.0, "Precio (Q)": 120.0, "Stock": 7},
        {"Código": "9", "Descripción": "Nissan DA34 / DAT-16", "Categoría": "Espadas", "Costo (Q)": 20.0, "Precio (Q)": 120.0, "Stock": 10},
        {"Código": "9", "Descripción": "Yamaha YH35R / YAMA-26", "Categoría": "Espadas", "Costo (Q)": 20.0, "Precio (Q)": 120.0, "Stock": 10},
        {"Código": "0", "Descripción": "Toyota 008L", "Categoría": "Espadas", "Costo (Q)": 20.0, "Precio (Q)": 120.0, "Stock": 6},
        {"Código": "0", "Descripción": "Mitsubishi 003L", "Categoría": "Espadas", "Costo (Q)": 20.0, "Precio (Q)": 120.0, "Stock": 8},
        {"Código": "0", "Descripción": "Nissan 059L", "Categoría": "Espadas", "Costo (Q)": 20.0, "Precio (Q)": 120.0, "Stock": 10},
        {"Código": "0", "Descripción": "Mazda 001L", "Categoría": "Espadas", "Costo (Q)": 20.0, "Precio (Q)": 120.0, "Stock": 10},
        {"Código": "0", "Descripción": "Hyundai 050L", "Categoría": "Espadas", "Costo (Q)": 20.0, "Precio (Q)": 120.0, "Stock": 9},
        {"Código": "0", "Descripción": "Suzuki 11", "Categoría": "Espadas", "Costo (Q)": 20.0, "Precio (Q)": 120.0, "Stock": 5},
        {"Código": "21", "Descripción": "Nissan DA34 / NSN14", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 12},
        {"Código": "22", "Descripción": "Hyundai HY15", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 2},
        {"Código": "22", "Descripción": "Kia KK12 / KIA-75", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 2},
        {"Código": "22", "Descripción": "Hyundai/Kia HY18R / HY-130", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 2},
        {"Código": "22", "Descripción": "Hyundai/Kia HY18 / HY-129", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 2},
        {"Código": "17", "Descripción": "Toyota TOY48 Short / TOY-77", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 13},
        {"Código": "19", "Descripción": "GM HU100 / GM-71", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 2},
        {"Código": "17", "Descripción": "Toyota TOY40 Long / TOY-13", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 2},
        {"Código": "23", "Descripción": "Jeep Dodge Fiat SIP22", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 1},
        {"Código": "19", "Descripción": "Ford 19", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 5},
        {"Código": "21", "Descripción": "Isuzu D-max", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 7},
        {"Código": "22", "Descripción": "Hyundai/Kia 15", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 2},
        {"Código": "23", "Descripción": "Dodge Jeep chrysler", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 4},
        {"Código": "23", "Descripción": "Jeep HU101", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 2},
        {"Código": "20", "Descripción": "Mitsubishi MIT11", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 5},
        {"Código": "23", "Descripción": "BMW HU58 4 TRACK", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 2},
        {"Código": "18", "Descripción": "Mazda MZ31/MZ34/FD-38", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 13},
        {"Código": "16", "Descripción": "Honda HO01/HOND-25", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 28},
        {"Código": "18", "Descripción": "Mazda MZ31/MZ34/MZ27", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 14},
        {"Código": "23", "Descripción": "VW/AUDI/PORSCHE HU66/BW-86", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 4},
        {"Código": "23", "Descripción": "BMW HU92 2 TRACK", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 2},
        {"Código": "17", "Descripción": "Toyota TR47/TOY-02", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 25},
        {"Código": "19", "Descripción": "GM GM-26V/GM10", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 1},
        {"Código": "20", "Descripción": "Mitsubishi MIT1/MIT-Y-13", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 5},
        {"Código": "19", "Descripción": "Chrysler Y157-Y159", "Categoría": "Espadas", "Costo (Q)": 25.0, "Precio (Q)": 120.0, "Stock": 10},

        # --- BATERIAS ---
        {"Código": "CR1616", "Descripción": "Batería de litio CR1616", "Categoría": "Baterías", "Costo (Q)": 15.0, "Precio (Q)": 50.0, "Stock": 8},
        {"Código": "CR1620", "Descripción": "Batería de litio CR1620", "Categoría": "Baterías", "Costo (Q)": 15.0, "Precio (Q)": 50.0, "Stock": 10},
        {"Código": "CR2032", "Descripción": "Batería de litio CR2032", "Categoría": "Baterías", "Costo (Q)": 15.0, "Precio (Q)": 50.0, "Stock": 105},
        {"Código": "CR2025", "Descripción": "Batería de litio CR2025", "Categoría": "Baterías", "Costo (Q)": 15.0, "Precio (Q)": 50.0, "Stock": 10},
        {"Código": "CR2016", "Descripción": "Batería de litio CR2016", "Categoría": "Baterías", "Costo (Q)": 15.0, "Precio (Q)": 50.0, "Stock": 10},
        {"Código": "CR1632", "Descripción": "Batería de litio CR1632", "Categoría": "Baterías", "Costo (Q)": 15.0, "Precio (Q)": 50.0, "Stock": 10}
    ]
    st.session_state.inv_cerrajeria = pd.DataFrame(productos_cerrajeria)

if "historial_trabajos" not in st.session_state:
    st.session_state.historial_trabajos = pd.DataFrame(columns=["Fecha", "Tipo", "Descripción", "Monto Cobrado (Q)"])

# 3. Catálogo de Servicios Intangibles (Tarifario Oficial)
servicios_fijos = {
    "Duplicado Casas (Metálica)": 15.0,
    "Duplicado Carros (Metálica)": 75.0,
    "Duplicado Motos (Metálica)": 50.0,
    "Duplicado Con Chip": 350.0,
    "Programación Control Navaja": 750.0,
    "Programación Control Espadín": 550.0,
    "Programación Control Presencia": 1000.0,
    "Diagnóstico con Scanner Autel": 100.0,
    "Cambio de Carcasas": 230.0,
    "Cambio de Baterías": 50.0,
    "Apertura de Vehículos": 150.0,
    "Jumpstart / Encendido": 50.0,
    "Llaves Perdidas - Moto": 100.0,
    "Llaves Perdidas - Llave con chip": 550.0,
    "Llaves Perdidas - Espadín": 800.0,
    "Llaves Perdidas - Navaja": 1000.0,
    "Llaves Perdidas - Presencia": 1250.0,
    "Reprogramación Controles": 150.0,
    "Limpieza": 50.0
}

# 4. Navegación Lateral
st.sidebar.title("🛠️ Panel de Control")
menu = st.sidebar.radio("Navegación:", ["📝 Registrar Trabajo / Venta", "📦 Inventario Completo", "📋 Historial de Ingresos"])

ingresos_totales = st.session_state.historial_trabajos["Monto Cobrado (Q)"].sum() if not st.session_state.historial_trabajos.empty else 0.0
st.sidebar.write("---")
st.sidebar.success(f"### 💵 Ingresos de Hoy:\n## Q {ingresos_totales:.2f}")

# ==========================================
# PANTALLA 1: REGISTRAR TRABAJO (SERVICIOS + PRODUCTOS)
# ==========================================
if menu == "📝 Registrar Trabajo / Venta":
    st.header("📝 Facturación y Salidas")
    
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.subheader("1. Cobrar Servicio (Mano de Obra)")
        servicio_sel = st.selectbox("Selecciona el servicio realizado:", ["Ninguno"] + list(servicios_fijos.keys()))
        precio_serv = 0.0
        if servicio_sel != "Ninguno":
            precio_serv = st.number_input("Precio del Servicio (Q):", value=servicios_fijos[servicio_sel], step=10.0)
            if st.button("🛠️ Registrar Servicio"):
                nuevo_ingreso = {"Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), "Tipo": "Servicio", "Descripción": servicio_sel, "Monto Cobrado (Q)": precio_serv}
                st.session_state.historial_trabajos = pd.concat([st.session_state.historial_trabajos, pd.DataFrame([nuevo_ingreso])], ignore_index=True)
                st.toast(f"✅ Servicio de {servicio_sel} registrado.", icon="🔧")
                st.rerun()

    with col_der:
        st.subheader("2. Vender Insumo (Descuenta Stock)")
        insumo_sel = st.selectbox("Selecciona la pieza a vender/usar:", st.session_state.inv_cerrajeria["Descripción"].tolist())
        
        datos_prod = st.session_state.inv_cerrajeria[st.session_state.inv_cerrajeria["Descripción"] == insumo_sel].iloc[0]
        precio_prod = datos_prod["Precio (Q)"]
        stock_prod = datos_prod["Stock"]
        
        st.info(f"📦 Existencias reales: **{stock_prod}** | 💵 Precio: **Q {precio_prod}**")
        
        precio_final_prod = st.number_input("Cobrar al cliente (Q):", value=precio_prod, step=10.0)
        cantidad = st.number_input("Cantidad utilizada:", min_value=1, max_value=int(stock_prod) if stock_prod > 0 else 1, value=1)
        
        if st.button("🛒 Registrar Venta de Insumo"):
            if stock_prod >= cantidad:
                st.session_state.inv_cerrajeria.loc[st.session_state.inv_cerrajeria["Descripción"] == insumo_sel, "Stock"] -= cantidad
                total_cobrado = precio_final_prod * cantidad
                nuevo_ingreso = {"Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), "Tipo": "Producto", "Descripción": f"{cantidad}x {insumo_sel}", "Monto Cobrado (Q)": total_cobrado}
                st.session_state.historial_trabajos = pd.concat([st.session_state.historial_trabajos, pd.DataFrame([nuevo_ingreso])], ignore_index=True)
                st.toast(f"✅ Insumo registrado. Stock restante: {stock_prod - cantidad}", icon="📦")
                st.rerun()
            else:
                st.error("❌ Stock insuficiente en el sistema.")

# ==========================================
# PANTALLA 2: INVENTARIO FÍSICO
# ==========================================
elif menu == "📦 Inventario Completo":
    st.header("📦 Control Total de Existencias")
    st.write("Tu inventario completo. Modifica precios, agrega mercancía nueva al final de la tabla y guarda los cambios.")
    
    inventario_editado = st.data_editor(
        st.session_state.inv_cerrajeria,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Costo (Q)": st.column_config.NumberColumn(format="Q %.2f"),
            "Precio (Q)": st.column_config.NumberColumn(format="Q %.2f"),
        }
    )
    
    if st.button("💾 Guardar Cambios en Inventario", type="primary"):
        st.session_state.inv_cerrajeria = inventario_editado
        st.success("✅ Base de datos actualizada con éxito.")
        st.rerun()

# ==========================================
# PANTALLA 3: HISTORIAL DE INGRESOS
# ==========================================
elif menu == "📋 Historial de Ingresos":
    st.header("📋 Contabilidad")
    
    if st.session_state.historial_trabajos.empty:
        st.info("Aún no hay trabajos facturados hoy.")
    else:
        st.dataframe(st.session_state.historial_trabajos.iloc[::-1], use_container_width=True, hide_index=True)
        
        csv_data = st.session_state.historial_trabajos.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Contabilidad (CSV)",
            data=csv_data,
            file_name=f"Ingresos_Cerrajeria_{datetime.now().strftime('%d_%m_%Y')}.csv",
            mime="text/csv",
            use_container_width=True
        )
