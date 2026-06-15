import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la página (Tema oscuro/metálico para cerrajería)
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

# 2. Base de Datos en Memoria (Extraída de tu Excel)
if "inv_cerrajeria" not in st.session_state:
    # Muestra representativa de tu Excel. Puedes agregar el resto en la app.
    productos_cerrajeria = [
        {"Código": "15", "Marca/Línea": "XHORSE XT27A", "Categoría": "Chips", "Costo (Q)": 35.0, "Precio Venta (Q)": 120.0, "Stock": 71},
        {"Código": "0", "Marca/Línea": "XHORSE PRESENCIA (Naranja)", "Categoría": "Controles", "Costo (Q)": 250.0, "Precio Venta (Q)": 1100.0, "Stock": 26},
        {"Código": "0", "Marca/Línea": "XHORSE WIRE (Rojo) Navaja", "Categoría": "Controles", "Costo (Q)": 135.0, "Precio Venta (Q)": 800.0, "Stock": 26},
        {"Código": "0", "Marca/Línea": "XHORSE GARAGE", "Categoría": "Controles", "Costo (Q)": 135.0, "Precio Venta (Q)": 550.0, "Stock": 19},
        {"Código": "17", "Marca/Línea": "Toyota TR47 / TOY-02", "Categoría": "Espadas y Cabezas", "Costo (Q)": 25.0, "Precio Venta (Q)": 120.0, "Stock": 25},
        {"Código": "16", "Marca/Línea": "Honda HO01 / HOND-25", "Categoría": "Espadas y Cabezas", "Costo (Q)": 25.0, "Precio Venta (Q)": 120.0, "Stock": 28},
        {"Código": "21", "Marca/Línea": "Nissan DA34 / NSN14", "Categoría": "Espadas y Cabezas", "Costo (Q)": 25.0, "Precio Venta (Q)": 120.0, "Stock": 12},
        {"Código": "CR2032", "Marca/Línea": "Batería de Litio CR2032", "Categoría": "Baterías", "Costo (Q)": 15.0, "Precio Venta (Q)": 50.0, "Stock": 105},
        {"Código": "CR1616", "Marca/Línea": "Batería de Litio CR1616", "Categoría": "Baterías", "Costo (Q)": 15.0, "Precio Venta (Q)": 50.0, "Stock": 8}
    ]
    st.session_state.inv_cerrajeria = pd.DataFrame(productos_cerrajeria)

if "historial_trabajos" not in st.session_state:
    st.session_state.historial_trabajos = pd.DataFrame(columns=["Fecha", "Tipo", "Descripción", "Monto Cobrado (Q)"])

# 3. Catálogo de Servicios Intangibles (No descuentan stock, solo suman dinero)
servicios_fijos = {
    "Diagnóstico Autel": 100.0,
    "Apertura de Vehículo": 150.0,
    "Jumpstart / Encendido": 50.0,
    "Cambio de Carcasa (Mano de obra)": 230.0,
    "Reprogramación Controles": 150.0,
    "Llave Perdida - Moto": 100.0,
    "Llave Perdida - Con Chip": 550.0,
    "Llave Perdida - Espadín": 800.0,
    "Llave Perdida - Presencia": 1250.0,
    "Duplicado - Carro (Metálica)": 75.0,
    "Duplicado - Con Chip": 350.0
}

# 4. Navegación Lateral
st.sidebar.title("🛠️ Panel de Control")
menu = st.sidebar.radio("Navegación:", ["📝 Registrar Trabajo / Venta", "📦 Inventario de Insumos", "📋 Historial de Ingresos"])

ingresos_totales = st.session_state.historial_trabajos["Monto Cobrado (Q)"].sum() if not st.session_state.historial_trabajos.empty else 0.0
st.sidebar.write("---")
st.sidebar.success(f"### 💵 Ingresos Registrados:\n## Q {ingresos_totales:.2f}")

# ==========================================
# PANTALLA 1: REGISTRAR TRABAJO (SERVICIOS + PRODUCTOS)
# ==========================================
if menu == "📝 Registrar Trabajo / Venta":
    st.header("📝 Nuevo Trabajo Realizado")
    st.write("En la cerrajería puedes cobrar por un servicio (ej. Apertura), vender un insumo físico (ej. Batería), o ambas cosas.")
    
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.subheader("1. Cobrar un Servicio")
        servicio_sel = st.selectbox("Selecciona el servicio realizado:", ["Ninguno"] + list(servicios_fijos.keys()))
        precio_serv = 0.0
        if servicio_sel != "Ninguno":
            precio_serv = st.number_input("Precio del Servicio (Q):", value=servicios_fijos[servicio_sel], step=10.0)
            if st.button("🛠️ Cobrar Solo Servicio"):
                nuevo_ingreso = {"Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), "Tipo": "Servicio", "Descripción": servicio_sel, "Monto Cobrado (Q)": precio_serv}
                st.session_state.historial_trabajos = pd.concat([st.session_state.historial_trabajos, pd.DataFrame([nuevo_ingreso])], ignore_index=True)
                st.toast(f"✅ Servicio de {servicio_sel} registrado.", icon="🔧")
                st.rerun()

    with col_der:
        st.subheader("2. Vender Insumo (Descuenta Stock)")
        insumo_sel = st.selectbox("Selecciona el producto a vender/usar:", st.session_state.inv_cerrajeria["Marca/Línea"].tolist())
        
        datos_prod = st.session_state.inv_cerrajeria[st.session_state.inv_cerrajeria["Marca/Línea"] == insumo_sel].iloc[0]
        precio_prod = datos_prod["Precio Venta (Q)"]
        stock_prod = datos_prod["Stock"]
        
        st.info(f"📦 En inventario: **{stock_prod}** | 💵 Precio sugerido: **Q {precio_prod}**")
        
        precio_final_prod = st.number_input("Cobrar al cliente (Q):", value=precio_prod, step=10.0)
        cantidad = st.number_input("Cantidad a usar/vender:", min_value=1, max_value=int(stock_prod) if stock_prod > 0 else 1, value=1)
        
        if st.button("🛒 Registrar Venta de Insumo"):
            if stock_prod >= cantidad:
                # Descontar inventario
                st.session_state.inv_cerrajeria.loc[st.session_state.inv_cerrajeria["Marca/Línea"] == insumo_sel, "Stock"] -= cantidad
                # Registrar ingreso
                total_cobrado = precio_final_prod * cantidad
                nuevo_ingreso = {"Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), "Tipo": "Producto", "Descripción": f"{cantidad}x {insumo_sel}", "Monto Cobrado (Q)": total_cobrado}
                st.session_state.historial_trabajos = pd.concat([st.session_state.historial_trabajos, pd.DataFrame([nuevo_ingreso])], ignore_index=True)
                st.toast(f"✅ Insumo registrado. Stock restante: {stock_prod - cantidad}", icon="📦")
                st.rerun()
            else:
                st.error("❌ Stock insuficiente para esta operación.")

# ==========================================
# PANTALLA 2: INVENTARIO FÍSICO
# ==========================================
elif menu == "📦 Inventario de Insumos":
    st.header("📦 Control de Stock y Precios")
    st.write("Haz doble clic en cualquier celda para editar (precios, stock, nombres). Para agregar los productos que faltan de tu Excel, simplemente desplázate hacia abajo en la tabla y escribe en la fila vacía al final.")
    
    inventario_editado = st.data_editor(
        st.session_state.inv_cerrajeria,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Costo (Q)": st.column_config.NumberColumn(format="Q %.2f"),
            "Precio Venta (Q)": st.column_config.NumberColumn(format="Q %.2f"),
        }
    )
    
    if st.button("💾 Guardar Base de Datos", type="primary"):
        st.session_state.inv_cerrajeria = inventario_editado
        st.success("✅ Base de datos de llaves, chips y equipos actualizada.")
        st.rerun()

# ==========================================
# PANTALLA 3: HISTORIAL DE INGRESOS
# ==========================================
elif menu == "📋 Historial de Ingresos":
    st.header("📋 Contabilidad de Trabajos")
    
    if st.session_state.historial_trabajos.empty:
        st.info("No hay ingresos registrados aún.")
    else:
        st.dataframe(st.session_state.historial_trabajos.iloc[::-1], use_container_width=True, hide_index=True)
        
        # Opción para exportar el reporte
        csv_data = st.session_state.historial_trabajos.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Reporte de Ingresos (CSV)",
            data=csv_data,
            file_name=f"Ingresos_Cerrajeria_{datetime.now().strftime('%d_%m_%Y')}.csv",
            mime="text/csv",
            use_container_width=True
        )
