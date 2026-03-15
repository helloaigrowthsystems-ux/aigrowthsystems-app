# crm.py — AImpulsa v2 — CRM ligero con IA
import streamlit as st
import json
from datetime import date, datetime

# CRM guardado en session_state (en producción real → Supabase)
def _init_crm():
    if "crm_contactos" not in st.session_state:
        st.session_state.crm_contactos = []
    if "crm_oportunidades" not in st.session_state:
        st.session_state.crm_oportunidades = []

def mostrar_crm():
    _init_crm()
    st.markdown("### 👥 Contactos")
    col_form, col_lista = st.columns([1, 2])

    with col_form:
        st.markdown("**Añadir contacto:**")
        nombre = st.text_input("Nombre", key="crm_nombre")
        empresa = st.text_input("Empresa", key="crm_empresa")
        email = st.text_input("Email", key="crm_email")
        telefono = st.text_input("Teléfono", key="crm_tel")
        notas = st.text_area("Notas", key="crm_notas", height=80)
        if st.button("➕ Añadir contacto", type="primary", use_container_width=True):
            if nombre:
                st.session_state.crm_contactos.append({
                    "nombre": nombre, "empresa": empresa, "email": email,
                    "telefono": telefono, "notas": notas,
                    "fecha": str(date.today())
                })
                st.success(f"Contacto {nombre} añadido")
                st.rerun()

    with col_lista:
        if st.session_state.crm_contactos:
            import pandas as pd
            df = pd.DataFrame(st.session_state.crm_contactos)
            st.dataframe(df[["nombre","empresa","email","telefono","fecha"]], use_container_width=True)
            from io import BytesIO
            buf = BytesIO()
            df.to_excel(buf, index=False); buf.seek(0)
            st.download_button("📥 Exportar contactos", data=buf, file_name="contactos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            st.info("Aún no hay contactos. Añade el primero.")

    st.markdown("---")
    st.markdown("### 💼 Pipeline de ventas")
    estados = ["Prospecto", "Contactado", "Demo hecha", "Propuesta enviada", "Negociación", "Ganado", "Perdido"]

    col_op, col_pipe = st.columns([1, 2])
    with col_op:
        st.markdown("**Nueva oportunidad:**")
        contacto_sel = st.text_input("Empresa/Contacto", key="op_empresa")
        valor = st.number_input("Valor estimado (€)", min_value=0, key="op_valor")
        estado = st.selectbox("Estado", estados, key="op_estado")
        fecha_cierre = st.text_input("Fecha cierre estimada", placeholder="30/06/2026", key="op_fecha")
        if st.button("➕ Añadir oportunidad", use_container_width=True):
            if contacto_sel:
                st.session_state.crm_oportunidades.append({
                    "empresa": contacto_sel, "valor": valor, "estado": estado,
                    "fecha_cierre": fecha_cierre, "creada": str(date.today())
                })
                st.success("Oportunidad añadida")
                st.rerun()

    with col_pipe:
        if st.session_state.crm_oportunidades:
            import pandas as pd
            df_op = pd.DataFrame(st.session_state.crm_oportunidades)
            total_pipeline = df_op["valor"].sum()
            ganadas = df_op[df_op["estado"] == "Ganado"]["valor"].sum()
            c1, c2, c3 = st.columns(3)
            c1.metric("Pipeline total", f"{total_pipeline:,.0f}€")
            c2.metric("Ganadas", f"{ganadas:,.0f}€")
            c3.metric("Oportunidades", len(df_op))
            st.dataframe(df_op[["empresa","valor","estado","fecha_cierre"]], use_container_width=True)
        else:
            st.info("Sin oportunidades aún.")