"""
Módulo app.py
Interfaz Gráfica Comercial — Isoglobaltech Facturación & Proformas
Desarrollada con Streamlit
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import List

from src.cliente import Cliente
from src.cliente_mayorista import ClienteMayorista
from src.cliente_minorista import ClienteMinorista
from src.producto import Producto
from src.producto_fisico import ProductoFisico
from src.producto_digital import ProductoDigital
from src.item_proforma import ItemProforma
from src.proforma import Proforma


# --- Configuración de la Página Streamlit ---
st.set_page_config(
    page_title="Isoglobaltech | Sistema Comercial",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Estilos CSS Personalizados Modernos ---
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        opacity: 0.9;
    }
    .product-badge-fisico {
        background-color: #E0F2FE;
        color: #0369A1;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .product-badge-digital {
        background-color: #F3E8FF;
        color: #7E22CE;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .client-badge-mayorista {
        background-color: #DCFCE7;
        color: #15803D;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .client-badge-minorista {
        background-color: #FEF9C3;
        color: #A16207;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .invoice-box {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.5rem;
        font-family: 'Courier New', Courier, monospace;
        white-space: pre-wrap;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- Inicialización del Estado de Sesión (State) ---
def inicializar_estado():
    if "catalogo" not in st.session_state:
        st.session_state.catalogo = [
            ProductoFisico(
                codigo="FIS-01",
                nombre="Laptop Dell Inspiron 15 (16GB RAM)",
                precio_base=850.00,
                peso_kg=2.40,
                tarifa_envio_kg=3.50,
                stock=15,
            ),
            ProductoFisico(
                codigo="FIS-02",
                nombre="Teclado Mecánico Inalámbrico RGB",
                precio_base=75.00,
                peso_kg=0.95,
                tarifa_envio_kg=3.00,
                stock=30,
            ),
            ProductoFisico(
                codigo="FIS-03",
                nombre="Monitor Gamer 27\" 165Hz IPS",
                precio_base=280.00,
                peso_kg=4.50,
                tarifa_envio_kg=3.00,
                stock=8,
            ),
            ProductoDigital(
                codigo="DIG-01",
                nombre="Masterclass Arquitectura Cloud & POO",
                precio_base=120.00,
                tamano_mb=3500.0,
                enlace_descarga="https://cursos.uees.edu.ec/descargas/ia-poo",
                porcentaje_tarifa_servicio=0.08,
                stock=100,
            ),
            ProductoDigital(
                codigo="DIG-02",
                nombre="Licencia JetBrains All Products (1 Año)",
                precio_base=199.00,
                tamano_mb=850.0,
                enlace_descarga="https://jetbrains.com/activate/uees",
                porcentaje_tarifa_servicio=0.05,
                stock=50,
            ),
            ProductoDigital(
                codigo="DIG-03",
                nombre="Suscripción Anual Antivirus Endpoint",
                precio_base=45.00,
                tamano_mb=150.0,
                enlace_descarga="https://cloudsecurity.uees.edu.ec/dl",
                porcentaje_tarifa_servicio=0.04,
                stock=200,
            ),
        ]

    if "clientes_registrados" not in st.session_state:
        st.session_state.clientes_registrados = [
            ClienteMayorista(
                cedula="0992345678001",
                nombre="Importadora Tecnológica del Pacífico S.A.",
                email="compras@pacifico-tech.com",
                telefono="042881234",
                razon_social="Importadora Tecnológica del Pacífico S.A.",
                porcentaje_descuento=0.15,
                monto_minimo_volumen=500.0,
                porcentaje_adicional_volumen=0.05,
            ),
            ClienteMayorista(
                cedula="1790123456001",
                nombre="Corporación Digital Andina Cía. Ltda.",
                email="gerencia@andina-digital.ec",
                telefono="022998877",
                razon_social="Corporación Digital Andina",
                porcentaje_descuento=0.18,
                monto_minimo_volumen=600.0,
                porcentaje_adicional_volumen=0.07,
            ),
            ClienteMinorista(
                cedula="0928374651",
                nombre="Carlos Andrés Mendoza",
                email="carlos.mendoza@gmail.com",
                telefono="0987654321",
                puntos_fidelidad=60,
                porcentaje_descuento=0.05,
                valor_por_punto=0.05,
            ),
            ClienteMinorista(
                cedula="0911223344",
                nombre="Valeria Sofía Herrera",
                email="valeria.herrera@hotmail.com",
                telefono="0991234567",
                puntos_fidelidad=120,
                porcentaje_descuento=0.05,
                valor_por_punto=0.05,
            ),
        ]

    if "carrito_items" not in st.session_state:
        # Formato: lista de dicts con {"codigo": str, "cantidad": int}
        st.session_state.carrito_items = []

    if "historial_facturas" not in st.session_state:
        st.session_state.historial_facturas = []


inicializar_estado()


# --- Barra Lateral: Navegación y Resumen General ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shop.png", width=64)
    st.markdown("### **ISOGLOBALTECH**")
    st.caption("Sistema Comercial & Facturación v3.0")
    st.markdown("---")

    menu_opcion = st.radio(
        "Módulos del Sistema:",
        [
            "📝 Nueva Factura / Proforma",
            "📦 Catálogo de Productos",
            "➕ Registrar Producto",
            "👥 Directorio de Clientes",
            "📊 Historial de Facturas",
        ],
        index=0,
    )

    st.markdown("---")
    st.markdown("#### **Resumen Operativo**")
    total_prods = len(st.session_state.catalogo)
    stock_total = sum(p.stock for p in st.session_state.catalogo)
    facturas_emitidas = len(st.session_state.historial_facturas)
    total_ventas = sum(f["total"] for f in st.session_state.historial_facturas) if facturas_emitidas > 0 else 0.0

    st.metric("Total Productos", f"{total_prods}")
    st.metric("Unidades en Stock", f"{stock_total}")
    st.metric("Facturas Emitidas", f"{facturas_emitidas}")
    st.metric("Ventas Totales ($)", f"${total_ventas:,.2f}")


# ==============================================================================
# MÓDULO 1: EMITIR FACTURA / PROFORMA
# ==============================================================================
if menu_opcion == "📝 Nueva Factura / Proforma":
    st.markdown('<div class="main-header">📝 Emisión de Factura / Proforma Comercial</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Registre clientes, configure ítems con cálculo automático de descuentos e impuestos.</div>', unsafe_allow_html=True)

    col_izq, col_der = st.columns([1, 1], gap="medium")

    # --- PANEL IZQUIERDO: SELECCIÓN Y DATOS DEL CLIENTE ---
    with col_izq:
        st.markdown("#### **1. Datos del Cliente**")

        modo_cliente = st.radio(
            "Origen del Cliente:",
            ["Seleccionar Cliente Existente", "Registrar Nuevo Cliente en la Factura"],
            horizontal=True,
        )

        cliente_actual: Cliente = None

        if modo_cliente == "Seleccionar Cliente Existente":
            opciones_cli = [
                f"{c.nombre} ({c.tipo_cliente()} - {c.cedula})"
                for c in st.session_state.clientes_registrados
            ]
            idx_sel = st.selectbox("Seleccionar Cliente del Directorio:", range(len(opciones_cli)), format_func=lambda x: opciones_cli[x])
            cliente_actual = st.session_state.clientes_registrados[idx_sel]

            # Ficha del cliente seleccionado
            with st.container(border=True):
                st.markdown(f"**Cliente:** {cliente_actual.nombre}")
                st.markdown(f"**Identificación:** `{cliente_actual.cedula}` | **Email:** `{cliente_actual.email}`")
                st.markdown(f"**Teléfono:** `{cliente_actual.telefono}`")
                if isinstance(cliente_actual, ClienteMayorista):
                    st.markdown(f'<span class="client-badge-mayorista">MAYORISTA</span> — Razón Social: **{cliente_actual.razon_social}**', unsafe_allow_html=True)
                    st.caption(f"Descuento base: {cliente_actual.porcentaje_descuento*100:.0f}% | Bono compras >= ${cliente_actual.monto_minimo_volumen:.2f}: +{cliente_actual.porcentaje_adicional_volumen*100:.0f}%")
                elif isinstance(cliente_actual, ClienteMinorista):
                    st.markdown(f'<span class="client-badge-minorista">MINORISTA</span> — Puntos Fidelidad: **{cliente_actual.puntos_fidelidad} pts**', unsafe_allow_html=True)
                    st.caption(f"Descuento membresía: {cliente_actual.porcentaje_descuento*100:.0f}% | Saldo en puntos: ${cliente_actual.puntos_fidelidad * cliente_actual.valor_por_punto:.2f}")

        else:
            tipo_nuevo = st.selectbox("Tipo de Cliente a Registrar:", ["Mayorista", "Minorista"])
            c1, c2 = st.columns(2)
            with c1:
                n_cedula = st.text_input("Cédula / RUC *", placeholder="0999999999001")
                n_nombre = st.text_input("Nombre Completo *", placeholder="Juan Pérez o Empresa S.A.")
            with c2:
                n_email = st.text_input("Correo Electrónico *", placeholder="contacto@dominio.com")
                n_telefono = st.text_input("Teléfono / Celular *", placeholder="0991234567")

            if tipo_nuevo == "Mayorista":
                c3, c4 = st.columns(2)
                with c3:
                    n_rs = st.text_input("Razón Social", placeholder="Distribuidora del Norte S.A.")
                    n_desc_base = st.number_input("Descuento Base (%)", min_value=0.0, max_value=100.0, value=15.0, step=1.0) / 100.0
                with c4:
                    n_monto_vol = st.number_input("Monto Mínimo Volumen ($)", min_value=0.0, value=500.0, step=50.0)
                    n_desc_vol = st.number_input("Bono Volumen Adicional (%)", min_value=0.0, max_value=100.0, value=5.0, step=1.0) / 100.0

                if n_cedula and n_nombre and n_email and n_telefono:
                    try:
                        cliente_actual = ClienteMayorista(
                            cedula=n_cedula,
                            nombre=n_nombre,
                            email=n_email,
                            telefono=n_telefono,
                            razon_social=n_rs if n_rs else n_nombre,
                            porcentaje_descuento=n_desc_base,
                            monto_minimo_volumen=n_monto_vol,
                            porcentaje_adicional_volumen=n_desc_vol,
                        )
                    except Exception as err:
                        st.error(f"Error en datos de cliente: {err}")
            else:
                c3, c4 = st.columns(2)
                with c3:
                    n_pts = st.number_input("Puntos de Fidelidad Iniciales", min_value=0, value=0, step=10)
                with c4:
                    n_desc_min = st.number_input("Descuento Base Fidelidad (%)", min_value=0.0, max_value=100.0, value=5.0, step=1.0) / 100.0

                if n_cedula and n_nombre and n_email and n_telefono:
                    try:
                        cliente_actual = ClienteMinorista(
                            cedula=n_cedula,
                            nombre=n_nombre,
                            email=n_email,
                            telefono=n_telefono,
                            puntos_fidelidad=n_pts,
                            porcentaje_descuento=n_desc_min,
                            valor_por_punto=0.05,
                        )
                    except Exception as err:
                        st.error(f"Error en datos de cliente: {err}")

    # --- PANEL DERECHO: SELECCIÓN DE PRODUCTOS Y CARRITO ---
    with col_der:
        st.markdown("#### **2. Agregar Productos al Carrito**")

        productos_disponibles = [p for p in st.session_state.catalogo if p.stock > 0]

        if not productos_disponibles:
            st.warning("⚠️ No hay productos con stock disponible en el catálogo.")
        else:
            opciones_prod = [
                f"{p.codigo} - {p.nombre} (${p.calcular_precio_final():.2f} | Stock: {p.stock})"
                for p in productos_disponibles
            ]
            idx_prod_sel = st.selectbox(
                "Seleccionar Producto:",
                range(len(opciones_prod)),
                format_func=lambda x: opciones_prod[x],
            )
            prod_seleccionado = productos_disponibles[idx_prod_sel]

            col_p1, col_p2, col_p3 = st.columns([1.5, 1, 1])
            with col_p1:
                tipo_tag = "Físico (con Envío)" if isinstance(prod_seleccionado, ProductoFisico) else "Digital (Descarga)"
                st.caption(f"Tipo: **{tipo_tag}** | Precio Unitario Final: **${prod_seleccionado.calcular_precio_final():.2f}**")
            with col_p2:
                cant_agregar = st.number_input("Cantidad:", min_value=1, max_value=prod_seleccionado.stock, value=1, step=1)
            with col_p3:
                st.write("")
                st.write("")
                if st.button("➕ Agregar al Carrito", use_container_width=True):
                    # Verificar si ya existe en el carrito temporal
                    existente = next((item for item in st.session_state.carrito_items if item["codigo"] == prod_seleccionado.codigo), None)
                    if existente:
                        total_deseado = existente["cantidad"] + cant_agregar
                        if total_deseado <= prod_seleccionado.stock:
                            existente["cantidad"] = total_deseado
                            st.success(f"Se actualizaron {cant_agregar} unidades.")
                        else:
                            st.error(f"Excede el stock disponible ({prod_seleccionado.stock}).")
                    else:
                        st.session_state.carrito_items.append({
                            "codigo": prod_seleccionado.codigo,
                            "cantidad": cant_agregar,
                        })
                        st.success(f"Producto agregado.")
                    st.rerun()

    # --- SECCIÓN INFERIOR: TABLA DE CARRITO Y LIQUIDACIÓN EN VIVO ---
    st.markdown("---")
    st.markdown("#### **3. Detalle de la Factura / Carrito de Compras**")

    if not st.session_state.carrito_items:
        st.info("🛒 El carrito está vacío. Agregue productos desde la sección superior.")
    else:
        # Construir proforma temporal para cálculos en vivo usando POO y Polimorfismo
        temp_cliente = cliente_actual if cliente_actual else ClienteMinorista(
            cedula="0999999999", nombre="Consumidor Final", email="final@isoglobaltech.com", telefono="0999999999"
        )

        proforma_temporal = Proforma(
            numero_proforma=f"PROF-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            cliente=temp_cliente,
            fecha=datetime.now(),
            porcentaje_iva=0.15,
        )

        filas_tabla = []
        for idx_cart, item_c in enumerate(st.session_state.carrito_items):
            prod_obj = next((p for p in st.session_state.catalogo if p.codigo == item_c["codigo"]), None)
            if prod_obj:
                cant = item_c["cantidad"]
                precio_u = prod_obj.calcular_precio_final()
                subtotal_linea = round(precio_u * cant, 2)
                tipo_p = "Físico" if isinstance(prod_obj, ProductoFisico) else "Digital"

                # Agregar al objeto proforma temporal para usar sus métodos de cálculo
                nuevo_item = ItemProforma(producto=prod_obj, cantidad=cant)
                proforma_temporal._Proforma__items.append(nuevo_item)

                filas_tabla.append({
                    "Ítem": idx_cart + 1,
                    "Código": prod_obj.codigo,
                    "Descripción": prod_obj.nombre,
                    "Tipo": tipo_p,
                    "Cantidad": cant,
                    "P. Unitario ($)": f"${precio_u:.2f}",
                    "Subtotal ($)": f"${subtotal_linea:.2f}",
                })

        df_carrito = pd.DataFrame(filas_tabla)
        st.dataframe(df_carrito, use_container_width=True, hide_index=True)

        # Acciones del carrito
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if st.button("🗑️ Vaciar Carrito", use_container_width=True):
                st.session_state.carrito_items = []
                st.rerun()

        # Resumen Financiero con Polimorfismo en Vivo
        st.markdown("##### **Liquidación Comercial**")
        sub_bruto = proforma_temporal.calcular_subtotal_neto()
        descuento = proforma_temporal.calcular_descuento()
        sub_neto = proforma_temporal.calcular_subtotal_con_descuento()
        iva = proforma_temporal.calcular_iva()
        total = proforma_temporal.calcular_total()

        c_m1, c_m2, c_m3, c_m4, c_m5 = st.columns(5)
        with c_m1:
            st.metric("Subtotal Bruto", f"${sub_bruto:.2f}")
        with c_m2:
            st.metric(f"Descuento ({temp_cliente.tipo_cliente()})", f"-${descuento:.2f}")
        with c_m3:
            st.metric("Base Imponible", f"${sub_neto:.2f}")
        with c_m4:
            st.metric("IVA (15%)", f"${iva:.2f}")
        with c_m5:
            st.metric("Total a Pagar", f"${total:.2f}")

        # Botón de Emisión Final
        st.markdown("---")
        if st.button("🚀 **EMITIR FACTURA Y DESCONTAR INVENTARIO**", type="primary", use_container_width=True):
            if not cliente_actual:
                st.error("❌ Complete los datos válidos del cliente antes de emitir la factura.")
            else:
                # Crear la proforma oficial y descontar stock mediante POO
                proforma_oficial = Proforma(
                    numero_proforma=f"FAC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                    cliente=cliente_actual,
                    fecha=datetime.now(),
                    porcentaje_iva=0.15,
                )

                try:
                    for item_c in st.session_state.carrito_items:
                        p_obj = next((p for p in st.session_state.catalogo if p.codigo == item_c["codigo"]), None)
                        if p_obj:
                            proforma_oficial.agregar_item(p_obj, item_c["cantidad"])

                    # Si es cliente nuevo no registrado en directorio, agregarlo
                    if cliente_actual not in st.session_state.clientes_registrados:
                        st.session_state.clientes_registrados.append(cliente_actual)

                    # Si es cliente minorista, acumular puntos por la compra
                    puntos_ganados = 0
                    if isinstance(cliente_actual, ClienteMinorista):
                        puntos_ganados = cliente_actual.acumular_puntos(proforma_oficial.calcular_total())

                    # Registrar en historial
                    factura_doc = proforma_oficial.generar_proforma_texto()
                    st.session_state.historial_facturas.append({
                        "numero": proforma_oficial.numero_proforma,
                        "fecha": proforma_oficial.fecha.strftime("%d/%m/%Y %H:%M:%S"),
                        "cliente": cliente_actual.nombre,
                        "tipo_cliente": cliente_actual.tipo_cliente(),
                        "items_count": proforma_oficial.contar_items(),
                        "subtotal_bruto": proforma_oficial.calcular_subtotal_neto(),
                        "descuento": proforma_oficial.calcular_descuento(),
                        "total": proforma_oficial.calcular_total(),
                        "texto_factura": factura_doc,
                    })

                    # Vaciar carrito
                    st.session_state.carrito_items = []

                    st.success(f"🎉 ¡Factura **{proforma_oficial.numero_proforma}** emitida exitosamente!")
                    if puntos_ganados > 0:
                        st.info(f"🎁 Cliente acumuló **{puntos_ganados}** nuevos puntos Club Isoglobaltech (Saldo actual: {cliente_actual.puntos_fidelidad} pts).")

                    # Mostrar factura generada
                    st.markdown("#### **Comprobante Oficial Emitido:**")
                    st.markdown(f'<div class="invoice-box">{factura_doc}</div>', unsafe_allow_html=True)

                    st.download_button(
                        label="📥 Descargar Factura (.txt)",
                        data=factura_doc,
                        file_name=f"{proforma_oficial.numero_proforma}.txt",
                        mime="text/plain",
                    )

                except Exception as ex_emision:
                    st.error(f"❌ Error al procesar la factura: {ex_emision}")


# ==============================================================================
# MÓDULO 2: CATÁLOGO DE PRODUCTOS
# ==============================================================================
elif menu_opcion == "📦 Catálogo de Productos":
    st.markdown('<div class="main-header">📦 Catálogo de Productos e Inventario</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Consulta de existencias, precios base, tarifas logísticas y precios finales polimórficos.</div>', unsafe_allow_html=True)

    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        filtro_texto = st.text_input("🔍 Buscar por Código o Nombre:", placeholder="Ej: Laptop, Dell, FIS-01, DIG-02...")
    with col_f2:
        filtro_tipo = st.selectbox("Filtrar por Categoría:", ["Todos", "Físicos", "Digitales"])

    # Filtrado
    lista_filtrada = st.session_state.catalogo
    if filtro_tipo == "Físicos":
        lista_filtrada = [p for p in lista_filtrada if isinstance(p, ProductoFisico)]
    elif filtro_tipo == "Digitales":
        lista_filtrada = [p for p in lista_filtrada if isinstance(p, ProductoDigital)]

    if filtro_texto:
        term = filtro_texto.strip().lower()
        lista_filtrada = [p for p in lista_filtrada if term in p.codigo.lower() or term in p.nombre.lower()]

    # Renderizar tarjetas de catálogo
    if not lista_filtrada:
        st.info("No se encontraron productos coincidentes con los filtros.")
    else:
        for p in lista_filtrada:
            with st.container(border=True):
                col_c1, col_c2, col_c3, col_c4 = st.columns([1, 3, 2, 1.5])
                with col_c1:
                    if isinstance(p, ProductoFisico):
                        st.markdown('<span class="product-badge-fisico">FÍSICO</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="product-badge-digital">DIGITAL</span>', unsafe_allow_html=True)
                    st.markdown(f"### `{p.codigo}`")

                with col_c2:
                    st.markdown(f"**{p.nombre}**")
                    if isinstance(p, ProductoFisico):
                        st.caption(f"📦 Peso: {p.peso_kg} kg | Tarifa Envío: ${p.tarifa_envio_kg:.2f}/kg | Costo Flete: **${p.costo_envio:.2f}**")
                    elif isinstance(p, ProductoDigital):
                        st.caption(f"💾 Tamaño: {p.tamano_mb} MB | Tarifa Servicio: {p.porcentaje_tarifa_servicio*100:.1f}% | Enlace: `{p.enlace_descarga}`")

                with col_c3:
                    st.markdown(f"Precio Base: **${p.precio_base:.2f}**")
                    st.markdown(f"Precio Final Unitario: **${p.calcular_precio_final():.2f}**")

                with col_c4:
                    if p.stock > 5:
                        st.success(f"Stock: {p.stock} uds")
                    elif p.stock > 0:
                        st.warning(f"Stock Bajo: {p.stock} uds")
                    else:
                        st.error("Agotado (0 uds)")


# ==============================================================================
# MÓDULO 3: REGISTRAR NUEVO PRODUCTO
# ==============================================================================
elif menu_opcion == "➕ Registrar Producto":
    st.markdown('<div class="main-header">➕ Registro de Nuevo Producto</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Incorpore nuevos ítems físicos o digitales al catálogo comercial con validación de atributos.</div>', unsafe_allow_html=True)

    with st.form("form_nuevo_producto", clear_on_submit=True):
        tipo_prod = st.radio("Tipo de Producto a Registrar:", ["Producto Físico (Tangible con Envío)", "Producto Digital (Software / Descarga)"], horizontal=True)

        c1, c2 = st.columns(2)
        with c1:
            cod = st.text_input("Código de Producto *", placeholder="FIS-04 / DIG-04").strip().upper()
            nom = st.text_input("Nombre / Descripción *", placeholder="Ej: Mouse Ergonómico Logitech")
        with c2:
            prec = st.number_input("Precio Base ($) *", min_value=0.01, value=50.00, step=5.0)
            stk = st.number_input("Stock Inicial (unidades) *", min_value=1, value=20, step=1)

        if "Físico" in tipo_prod:
            c3, c4 = st.columns(2)
            with c3:
                peso = st.number_input("Peso en Kilogramos (kg) *", min_value=0.01, value=1.20, step=0.1)
            with c4:
                tarifa_flete = st.number_input("Tarifa de Envío por Kg ($)", min_value=0.0, value=2.50, step=0.5)
        else:
            c3, c4 = st.columns(2)
            with c3:
                tam_mb = st.number_input("Tamaño de Descarga (MB) *", min_value=0.1, value=500.0, step=50.0)
                tarifa_srv = st.number_input("Tarifa Servicio Digital (%)", min_value=0.0, max_value=100.0, value=5.0, step=1.0) / 100.0
            with c4:
                enlace = st.text_input("Enlace de Descarga / Licenciamiento *", placeholder="https://isoglobaltech.com/descargas/app")

        enviar = st.form_submit_button("💾 Guardar Producto en Catálogo", type="primary", use_container_width=True)

        if enviar:
            if not cod or not nom:
                st.error("❌ El código y el nombre del producto son campos obligatorios.")
            elif any(p.codigo == cod for p in st.session_state.catalogo):
                st.error(f"❌ Ya existe un producto registrado con el código '{cod}'.")
            else:
                try:
                    if "Físico" in tipo_prod:
                        nuevo = ProductoFisico(
                            codigo=cod,
                            nombre=nom,
                            precio_base=prec,
                            peso_kg=peso,
                            tarifa_envio_kg=tarifa_flete,
                            stock=stk,
                        )
                    else:
                        if not enlace:
                            st.error("❌ Debe ingresar el enlace de descarga para productos digitales.")
                            st.stop()
                        nuevo = ProductoDigital(
                            codigo=cod,
                            nombre=nom,
                            precio_base=prec,
                            tamano_mb=tam_mb,
                            enlace_descarga=enlace,
                            porcentaje_tarifa_servicio=tarifa_srv,
                            stock=stk,
                        )

                    st.session_state.catalogo.append(nuevo)
                    st.success(f"✅ ¡Producto '{nuevo.nombre}' registrado con éxito! Precio final calculado: ${nuevo.calcular_precio_final():.2f}")
                except Exception as err_prod:
                    st.error(f"❌ Error de validación: {err_prod}")


# ==============================================================================
# MÓDULO 4: DIRECTORIO DE CLIENTES
# ==============================================================================
elif menu_opcion == "👥 Directorio de Clientes":
    st.markdown('<div class="main-header">👥 Directorio de Clientes Registrados</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Gestión de cartera de clientes Mayoristas y Minoristas.</div>', unsafe_allow_html=True)

    c_may, c_min = st.tabs(["🏢 Clientes Mayoristas", "👤 Clientes Minoristas"])

    with c_may:
        may_list = [c for c in st.session_state.clientes_registrados if isinstance(c, ClienteMayorista)]
        if not may_list:
            st.info("No hay clientes mayoristas registrados.")
        else:
            for cm in may_list:
                with st.container(border=True):
                    col_m1, col_m2, col_m3 = st.columns([2, 2, 2])
                    with col_m1:
                        st.markdown(f"**{cm.nombre}**")
                        st.caption(f"Razón Social: {cm.razon_social}")
                        st.markdown(f"RUC: `{cm.cedula}`")
                    with col_m2:
                        st.markdown(f"📧 `{cm.email}`")
                        st.markdown(f"📞 `{cm.telefono}`")
                    with col_m3:
                        st.markdown(f"🏷️ Descuento Base: **{cm.porcentaje_descuento*100:.0f}%**")
                        st.markdown(f"📦 Bono Volumen (>= ${cm.monto_minimo_volumen:.2f}): **+{cm.porcentaje_adicional_volumen*100:.0f}%**")

    with c_min:
        min_list = [c for c in st.session_state.clientes_registrados if isinstance(c, ClienteMinorista)]
        if not min_list:
            st.info("No hay clientes minoristas registrados.")
        else:
            for cn in min_list:
                with st.container(border=True):
                    col_n1, col_n2, col_n3 = st.columns([2, 2, 2])
                    with col_n1:
                        st.markdown(f"**{cn.nombre}**")
                        st.markdown(f"Cédula: `{cn.cedula}`")
                    with col_n2:
                        st.markdown(f"📧 `{cn.email}`")
                        st.markdown(f"📞 `{cn.telefono}`")
                    with col_n3:
                        st.markdown(f"🎁 Puntos Fidelidad: **{cn.puntos_fidelidad} pts**")
                        st.markdown(f"💰 Saldo Canjeable: **${cn.puntos_fidelidad * cn.valor_por_punto:.2f}**")
                        st.markdown(f"🏷️ Descuento Membresía: **{cn.porcentaje_descuento*100:.0f}%**")


# ==============================================================================
# MÓDULO 5: HISTORIAL DE FACTURAS
# ==============================================================================
elif menu_opcion == "📊 Historial de Facturas":
    st.markdown('<div class="main-header">📊 Historial de Facturas & Proformas Emitidas</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Consulta, auditoría y reimpresión de comprobantes emitidos en la sesión.</div>', unsafe_allow_html=True)

    if not st.session_state.historial_facturas:
        st.info("Aún no se han emitido facturas en esta sesión.")
    else:
        df_hist = pd.DataFrame([
            {
                "N° Factura": f["numero"],
                "Fecha": f["fecha"],
                "Cliente": f["cliente"],
                "Tipo": f["tipo_cliente"],
                "Ítems": f["items_count"],
                "Subtotal Bruto": f"${f['subtotal_bruto']:.2f}",
                "Descuento": f"-${f['descuento']:.2f}",
                "Total Facturado": f"${f['total']:.2f}",
            }
            for f in st.session_state.historial_facturas
        ])

        st.dataframe(df_hist, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("#### **Reimpresión / Visualización de Comprobante**")
        num_sel = st.selectbox(
            "Seleccione una factura para ver el detalle completo:",
            [f["numero"] for f in st.session_state.historial_facturas]
        )

        fact_elegida = next(f for f in st.session_state.historial_facturas if f["numero"] == num_sel)
        st.markdown(f'<div class="invoice-box">{fact_elegida["texto_factura"]}</div>', unsafe_allow_html=True)

        st.download_button(
            label=f"📥 Descargar {fact_elegida['numero']}.txt",
            data=fact_elegida["texto_factura"],
            file_name=f"{fact_elegida['numero']}.txt",
            mime="text/plain",
        )
