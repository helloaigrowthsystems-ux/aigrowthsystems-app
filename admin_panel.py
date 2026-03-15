# admin_panel.py — AI Growth Systems · Panel de Administración Completo
# Gestión de usuarios, planes, métricas y control total de la agencia

import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date, datetime


PLANES = {
    "demo":     {"label": "Demo",      "color": "#606070", "bg": "#141520", "icon": "🔍", "limite": 3},
    "gratuito": {"label": "Gratuito",  "color": "#8B8B9E", "bg": "#1A1B26", "icon": "⚪", "limite": 5},
    "pro":      {"label": "Pro",       "color": "#C9A84C", "bg": "#1E1A0A", "icon": "⭐", "limite": None},
    "business": {"label": "Business",  "color": "#E8C96A", "bg": "#1E1800", "icon": "🚀", "limite": None},
    "admin":    {"label": "Admin",     "color": "#3DD68C", "bg": "#0A1E14", "icon": "🔑", "limite": None},
}


def _plan_badge(plan):
    meta = PLANES.get(plan, PLANES["gratuito"])
    return (
        f"<span style='background:{meta['bg']};color:{meta['color']};"
        f"border:1px solid {meta['color']}44;border-radius:5px;"
        f"padding:2px 10px;font-size:0.72rem;font-weight:700;"
        f"font-family:DM Sans,sans-serif;letter-spacing:0.04em;'>"
        f"{meta['icon']} {meta['label']}</span>"
    )


def mostrar_admin_panel(get_supabase, perfil_admin):
    """Panel de administración completo — solo para admin."""

    # ── CSS adicional admin ────────────────────────────────────────────────────
    st.markdown("""
<style>
.admin-section-title {
    font-family: 'Sora', sans-serif;
    font-size: 0.6rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--text3);
    margin: 24px 0 12px;
}
.user-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 10px;
    transition: border-color 0.2s, box-shadow 0.2s;
    position: relative;
}
.user-card:hover {
    border-color: var(--border2);
    box-shadow: 0 6px 24px rgba(0,0,0,0.3);
}
.plan-change-row {
    background: rgba(201,168,76,0.04);
    border: 1px solid rgba(201,168,76,0.12);
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 8px;
}
.stat-card-admin {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 22px;
    text-align: center;
}
.admin-badge {
    display: inline-block;
    background: rgba(61,214,140,0.1);
    color: #3DD68C;
    border: 1px solid rgba(61,214,140,0.25);
    border-radius: 6px;
    font-size: 0.6rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 2px 8px;
    margin-bottom: 8px;
    font-family: 'DM Sans', sans-serif;
}
</style>
""", unsafe_allow_html=True)

    # ── Header ─────────────────────────────────────────────────────────────────
    st.markdown("""
<div style='background:linear-gradient(135deg,#0A1E14,#0D1117 60%,#0A0F1E);
border-radius:16px;padding:22px 28px 18px;margin-bottom:22px;position:relative;overflow:hidden;
border:1px solid rgba(61,214,140,0.15);'>
<div style='position:absolute;top:0;left:0;right:0;height:1px;
background:linear-gradient(90deg,transparent,rgba(61,214,140,0.4),transparent);'></div>
<div class='admin-badge'>Solo Admin</div>
<div style='font-family:Sora,sans-serif;font-size:1.35rem;font-weight:700;
color:#EAEAF0;letter-spacing:-0.03em;margin-bottom:5px;'>Panel de Control · AI Growth Systems</div>
<div style='font-size:0.82rem;color:#506060;font-family:DM Sans,sans-serif;'>
Gestión completa de clientes, planes, métricas y configuración de la agencia</div>
</div>
""", unsafe_allow_html=True)

    # ── Cargar datos ───────────────────────────────────────────────────────────
    try:
        sb = get_supabase()
        res_usuarios = sb.table("usuarios").select("*").execute()
        usuarios = res_usuarios.data or []
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return

    df_u = pd.DataFrame(usuarios) if usuarios else pd.DataFrame()

    # ── TABS principales ───────────────────────────────────────────────────────
    tab_resumen, tab_usuarios, tab_planes, tab_buscar, tab_exportar = st.tabs([
        "  📊 Resumen  ",
        "  👥 Usuarios  ",
        "  🎯 Gestión de Planes  ",
        "  🔍 Buscar  ",
        "  📥 Exportar  ",
    ])

    # ════════════════════════════════════════════════════════════════════════════
    # TAB 1 — RESUMEN
    # ════════════════════════════════════════════════════════════════════════════
    with tab_resumen:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if df_u.empty:
            st.info("No hay usuarios registrados todavía.")
            return

        # Métricas globales
        total_u   = len(df_u)
        n_gratuito = len(df_u[df_u["plan"] == "gratuito"]) if "plan" in df_u else 0
        n_demo     = len(df_u[df_u["plan"] == "demo"])     if "plan" in df_u else 0
        n_pro      = len(df_u[df_u["plan"] == "pro"])      if "plan" in df_u else 0
        n_business = len(df_u[df_u["plan"] == "business"]) if "plan" in df_u else 0
        n_pagando  = n_pro + n_business
        mrr_est    = n_pro * 29 + n_business * 99  # estimación

        c1, c2, c3, c4, c5, c6 = st.columns(6)
        for col, val, lbl, sub_c in [
            (c1, total_u,   "Usuarios totales", "201,168,76"),
            (c2, n_pagando, "Clientes activos",  "61,214,140"),
            (c3, n_pro,     "Plan Pro",          "201,168,76"),
            (c4, n_business,"Plan Business",     "232,201,106"),
            (c5, n_gratuito,"Gratuito",          "80,80,100"),
            (c6, f"{mrr_est}€","MRR estimado",   "61,214,140"),
        ]:
            with col:
                st.markdown(
                    f"<div style='background:rgba({sub_c},0.07);border:1px solid rgba({sub_c},0.18);"
                    "border-radius:12px;padding:16px;text-align:center;margin-bottom:4px;'>"
                    f"<div style='font-family:Sora,sans-serif;font-size:1.6rem;font-weight:700;"
                    f"color:rgba({sub_c},1);letter-spacing:-0.03em;'>{val}</div>"
                    f"<div style='font-size:0.72rem;color:rgba({sub_c},0.7);margin-top:4px;font-weight:600;'>{lbl}</div>"
                    "</div>", unsafe_allow_html=True
                )

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        # Distribución de planes — visual
        st.markdown("<div class='admin-section-title'>Distribución de planes</div>", unsafe_allow_html=True)
        planes_data = {
            "Demo": n_demo,
            "Gratuito": n_gratuito,
            "Pro": n_pro,
            "Business": n_business,
        }
        total_dist = sum(planes_data.values()) or 1
        for plan_lbl, count in planes_data.items():
            pct = round(count / total_dist * 100)
            meta = list(PLANES.values())[list(PLANES.keys()).index(plan_lbl.lower())]
            color = meta["color"]
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:14px;margin-bottom:10px;'>"
                f"<div style='width:90px;font-size:0.82rem;color:var(--text2);font-weight:500;'>{plan_lbl}</div>"
                f"<div style='flex:1;background:var(--border);border-radius:4px;height:8px;overflow:hidden;'>"
                f"<div style='background:{color};width:{pct}%;height:100%;border-radius:4px;"
                f"transition:width 0.5s ease;'></div></div>"
                f"<div style='width:50px;text-align:right;font-size:0.82rem;color:{color};font-weight:700;'>{count}</div>"
                f"<div style='width:40px;text-align:right;font-size:0.75rem;color:var(--text3);'>{pct}%</div>"
                f"</div>",
                unsafe_allow_html=True
            )

        # Últimos registros
        st.markdown("<div class='admin-section-title'>Últimos usuarios registrados</div>", unsafe_allow_html=True)
        cols_show = [c for c in ["email", "nombre", "plan"] if c in df_u.columns]
        st.dataframe(df_u[cols_show].tail(10)[::-1], use_container_width=True, hide_index=True)

    # ════════════════════════════════════════════════════════════════════════════
    # TAB 2 — USUARIOS
    # ════════════════════════════════════════════════════════════════════════════
    with tab_usuarios:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if df_u.empty:
            st.info("No hay usuarios.")
            return

        # Filtro por plan
        filtro_plan = st.radio(
            "Filtrar por plan:",
            ["Todos", "Demo", "Gratuito", "Pro", "Business", "Admin"],
            horizontal=True, key="admin_filtro_plan"
        )

        df_filtrado = df_u.copy()
        if filtro_plan != "Todos":
            df_filtrado = df_u[df_u["plan"] == filtro_plan.lower()]

        st.markdown(
            f"<div style='font-size:0.8rem;color:var(--text3);margin-bottom:12px;'>"
            f"{len(df_filtrado)} usuario(s) encontrados</div>",
            unsafe_allow_html=True
        )

        cols_tabla = [c for c in ["email", "nombre", "plan", "usos_hoy", "fecha_usos", "usos_total"] if c in df_filtrado.columns]
        st.dataframe(df_filtrado[cols_tabla], use_container_width=True, hide_index=True)

    # ════════════════════════════════════════════════════════════════════════════
    # TAB 3 — GESTIÓN DE PLANES (LA CLAVE)
    # ════════════════════════════════════════════════════════════════════════════
    with tab_planes:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # Descripción
        st.markdown("""
<div style='background:rgba(201,168,76,0.05);border:1px solid rgba(201,168,76,0.15);
border-radius:12px;padding:16px 20px;margin-bottom:20px;'>
<div style='font-family:Sora,sans-serif;font-weight:700;font-size:0.9rem;color:var(--gold2);margin-bottom:6px;'>
🎯 Asignación manual de planes</div>
<div style='font-size:0.83rem;color:var(--text3);line-height:1.6;'>
Puedes cambiar el plan de cualquier usuario manualmente — ideal si conoces a alguien en una empresa
y quieres asignarle un plan business aunque esté pagando pro, o dar acceso especial a un contacto.
El usuario no recibe ninguna notificación automática.
</div>
</div>
""", unsafe_allow_html=True)

        # ── CAMBIO RÁPIDO POR EMAIL ──────────────────────────────────────────
        st.markdown("<div class='admin-section-title'>Cambio rápido por email</div>", unsafe_allow_html=True)

        with st.container():
            st.markdown("<div class='plan-change-row'>", unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns([3, 2, 1.5, 1.5])
            with c1:
                email_cambio = st.text_input(
                    "Email del usuario",
                    placeholder="usuario@empresa.com",
                    key="plan_email_rapido",
                    label_visibility="collapsed"
                )
            with c2:
                nuevo_plan_rapido = st.selectbox(
                    "Plan",
                    options=["demo", "gratuito", "pro", "business", "admin"],
                    format_func=lambda x: f"{PLANES[x]['icon']} {PLANES[x]['label']}",
                    key="plan_select_rapido",
                    label_visibility="collapsed"
                )
            with c3:
                motivo_rapido = st.text_input(
                    "Motivo (opcional)",
                    placeholder="Amigo, socio...",
                    key="plan_motivo_rapido",
                    label_visibility="collapsed"
                )
            with c4:
                st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
                if st.button("Actualizar plan →", type="primary", key="btn_plan_rapido", use_container_width=True):
                    if email_cambio:
                        _cambiar_plan_usuario(sb, email_cambio, nuevo_plan_rapido)
                    else:
                        st.warning("Introduce el email del usuario.")

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        # ── GESTIÓN VISUAL POR USUARIO ──────────────────────────────────────
        st.markdown("<div class='admin-section-title'>Gestión visual de usuarios</div>", unsafe_allow_html=True)

        # Búsqueda
        buscar_plan = st.text_input(
            "Buscar usuario",
            placeholder="Email o nombre...",
            key="plan_buscar",
            label_visibility="collapsed"
        )

        df_plan = df_u.copy()
        if buscar_plan:
            mask = df_plan.apply(
                lambda r: buscar_plan.lower() in str(r.get("email", "")).lower()
                or buscar_plan.lower() in str(r.get("nombre", "")).lower(),
                axis=1
            )
            df_plan = df_plan[mask]

        if df_plan.empty:
            st.markdown(
                "<div style='text-align:center;padding:32px;border:1px dashed var(--border2);"
                "border-radius:12px;color:var(--text3);font-size:0.875rem;'>"
                "No se encontraron usuarios con ese criterio.</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='font-size:0.78rem;color:var(--text3);margin-bottom:12px;'>"
                f"Mostrando {min(len(df_plan), 20)} de {len(df_plan)} usuarios</div>",
                unsafe_allow_html=True
            )

            # Mostrar hasta 20 usuarios
            for _, row in df_plan.head(20).iterrows():
                email_row  = row.get("email", "—")
                nombre_row = row.get("nombre", "—")
                plan_row   = row.get("plan", "gratuito")
                usos_row   = row.get("usos_hoy", 0)
                total_row  = row.get("usos_total", 0)
                fecha_row  = row.get("fecha_usos", "—")

                meta = PLANES.get(plan_row, PLANES["gratuito"])

                # Card de usuario con selector de plan inline
                uid_key = email_row.replace("@", "_at_").replace(".", "_")

                col_info, col_select, col_btn = st.columns([4, 2, 1.2])

                with col_info:
                    st.markdown(
                        f"<div style='background:var(--surface);border:1px solid var(--border);"
                        "border-radius:10px;padding:14px 16px;'>"
                        f"<div style='font-weight:600;font-size:0.875rem;color:var(--text);margin-bottom:4px;'>{nombre_row}</div>"
                        f"<div style='font-size:0.78rem;color:var(--text3);margin-bottom:8px;'>{email_row}</div>"
                        f"<div style='display:flex;gap:8px;align-items:center;'>"
                        f"{_plan_badge(plan_row)}"
                        f"<span style='font-size:0.72rem;color:var(--text3);'>· {total_row} acciones totales</span>"
                        f"</div></div>",
                        unsafe_allow_html=True
                    )

                with col_select:
                    plan_options = list(PLANES.keys())
                    current_idx  = plan_options.index(plan_row) if plan_row in plan_options else 0
                    nuevo_plan_u = st.selectbox(
                        f"Plan para {email_row}",
                        options=plan_options,
                        index=current_idx,
                        format_func=lambda x: f"{PLANES[x]['icon']} {PLANES[x]['label']}",
                        key=f"plan_sel_{uid_key}",
                        label_visibility="collapsed"
                    )

                with col_btn:
                    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
                    btn_disabled = (nuevo_plan_u == plan_row)
                    if st.button(
                        "Cambiar" if not btn_disabled else "Igual",
                        key=f"btn_plan_{uid_key}",
                        type="primary" if not btn_disabled else "secondary",
                        use_container_width=True,
                        disabled=btn_disabled
                    ):
                        _cambiar_plan_usuario(sb, email_row, nuevo_plan_u)

                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        # ── CAMBIOS MASIVOS ──────────────────────────────────────────────────
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown("<div class='admin-section-title'>Acciones masivas</div>", unsafe_allow_html=True)

        with st.expander("⚡ Cambiar plan a múltiples usuarios a la vez"):
            st.markdown(
                "<div style='font-size:0.82rem;color:var(--text3);margin-bottom:12px;'>"
                "Pega una lista de emails (uno por línea) y asigna el mismo plan a todos.</div>",
                unsafe_allow_html=True
            )
            emails_masivos = st.text_area(
                "Emails (uno por línea):",
                height=120,
                key="plan_masivo_emails",
                placeholder="usuario1@empresa.com\nusuario2@empresa.com\nusuario3@empresa.com"
            )
            plan_masivo = st.selectbox(
                "Plan a asignar:",
                options=list(PLANES.keys()),
                format_func=lambda x: f"{PLANES[x]['icon']} {PLANES[x]['label']}",
                key="plan_masivo_select"
            )
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("Aplicar a todos", type="primary", key="btn_masivo", use_container_width=True):
                    if emails_masivos.strip():
                        lista_emails = [e.strip() for e in emails_masivos.strip().split("\n") if e.strip()]
                        ok = 0
                        err = 0
                        for em in lista_emails:
                            exito = _cambiar_plan_usuario(sb, em, plan_masivo, silencioso=True)
                            if exito:
                                ok += 1
                            else:
                                err += 1
                        if ok > 0:
                            st.success(f"✅ {ok} usuario(s) actualizados a {PLANES[plan_masivo]['label']}")
                        if err > 0:
                            st.warning(f"⚠️ {err} email(s) no encontrados")
                    else:
                        st.warning("Pega al menos un email.")

    # ════════════════════════════════════════════════════════════════════════════
    # TAB 4 — BUSCAR USUARIO ESPECÍFICO
    # ════════════════════════════════════════════════════════════════════════════
    with tab_buscar:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.markdown(
            "<div style='font-size:0.84rem;color:var(--text3);margin-bottom:16px;'>"
            "Busca un usuario para ver su perfil completo, métricas y gestionar su cuenta.</div>",
            unsafe_allow_html=True
        )

        buscar_q = st.text_input(
            "Buscar",
            placeholder="Email exacto o nombre...",
            key="admin_buscar_q",
            label_visibility="collapsed"
        )

        if buscar_q and not df_u.empty:
            mask_b = df_u.apply(
                lambda r: buscar_q.lower() in str(r.get("email", "")).lower()
                or buscar_q.lower() in str(r.get("nombre", "")).lower(),
                axis=1
            )
            resultados = df_u[mask_b]

            if resultados.empty:
                st.warning(f"No se encontraron usuarios con '{buscar_q}'")
            else:
                for _, row in resultados.iterrows():
                    _mostrar_perfil_usuario(sb, row)

    # ════════════════════════════════════════════════════════════════════════════
    # TAB 5 — EXPORTAR
    # ════════════════════════════════════════════════════════════════════════════
    with tab_exportar:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if df_u.empty:
            st.info("No hay datos para exportar.")
            return

        st.markdown("<div class='admin-section-title'>Exportar datos de usuarios</div>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        with c1:
            # Todos los usuarios
            buf_all = BytesIO()
            df_u.to_excel(buf_all, index=False)
            buf_all.seek(0)
            st.download_button(
                "⬇ Todos los usuarios (Excel)",
                data=buf_all,
                file_name=f"usuarios_aigrowth_{date.today()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary", use_container_width=True
            )

        with c2:
            # Solo pagantes
            df_pagantes = df_u[df_u["plan"].isin(["pro", "business"])] if "plan" in df_u else pd.DataFrame()
            buf_pay = BytesIO()
            df_pagantes.to_excel(buf_pay, index=False)
            buf_pay.seek(0)
            st.download_button(
                f"⬇ Clientes activos ({len(df_pagantes)})",
                data=buf_pay,
                file_name=f"clientes_activos_{date.today()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        with c3:
            # Solo emails (para newsletter)
            if "email" in df_u.columns:
                emails_str = "\n".join(df_u["email"].dropna().tolist())
                st.download_button(
                    "⬇ Lista de emails (.txt)",
                    data=emails_str.encode("utf-8"),
                    file_name=f"emails_{date.today()}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown("<div class='admin-section-title'>Exportar por plan</div>", unsafe_allow_html=True)

        cols_exp = st.columns(len(PLANES))
        for col, (plan_key, meta) in zip(cols_exp, PLANES.items()):
            with col:
                df_p = df_u[df_u["plan"] == plan_key] if "plan" in df_u else pd.DataFrame()
                buf_p = BytesIO()
                df_p.to_excel(buf_p, index=False)
                buf_p.seek(0)
                st.download_button(
                    f"⬇ {meta['label']} ({len(df_p)})",
                    data=buf_p,
                    file_name=f"plan_{plan_key}_{date.today()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )


def _cambiar_plan_usuario(sb, email, nuevo_plan, silencioso=False):
    """Cambia el plan de un usuario por email. Retorna True si éxito."""
    try:
        # Buscar usuario por email
        res = sb.table("usuarios").select("id,email,nombre,plan").eq("email", email).execute()
        if not res.data:
            if not silencioso:
                st.error(f"No se encontró ningún usuario con el email: **{email}**")
            return False

        usuario = res.data[0]
        plan_anterior = usuario.get("plan", "—")

        # Actualizar plan
        sb.table("usuarios").update({"plan": nuevo_plan}).eq("id", usuario["id"]).execute()

        if not silencioso:
            meta_nuevo    = PLANES.get(nuevo_plan, PLANES["gratuito"])
            meta_anterior = PLANES.get(plan_anterior, PLANES["gratuito"])
            st.success(
                f"✅ Plan actualizado correctamente — "
                f"**{usuario.get('nombre', email)}** ({email}): "
                f"{meta_anterior['icon']} {meta_anterior['label']} → "
                f"{meta_nuevo['icon']} {meta_nuevo['label']}"
            )
            st.rerun()

        return True

    except Exception as e:
        if not silencioso:
            st.error(f"Error al actualizar plan: {e}")
        return False


def _mostrar_perfil_usuario(sb, row):
    """Muestra el perfil completo de un usuario con gestión de plan."""
    email_u  = row.get("email", "—")
    nombre_u = row.get("nombre", "—")
    plan_u   = row.get("plan", "gratuito")
    meta     = PLANES.get(plan_u, PLANES["gratuito"])
    uid_key  = email_u.replace("@", "_at_").replace(".", "_")

    with st.expander(f"{meta['icon']} {nombre_u} — {email_u}", expanded=True):
        c1, c2 = st.columns([2, 1])

        with c1:
            st.markdown(
                "<div style='background:var(--surface);border:1px solid var(--border);"
                "border-radius:12px;padding:18px 20px;'>"
                "<div style='font-family:Sora,sans-serif;font-size:0.62rem;font-weight:700;"
                "text-transform:uppercase;letter-spacing:0.1em;color:var(--text3);margin-bottom:12px;'>Datos de cuenta</div>"
                "<table style='width:100%;font-size:0.83rem;border-collapse:collapse;'>"
                f"<tr><td style='color:var(--text3);padding:7px 0;border-bottom:1px solid var(--border);'>Email</td>"
                f"<td style='text-align:right;color:var(--text2);padding:7px 0;border-bottom:1px solid var(--border);'>{email_u}</td></tr>"
                f"<tr><td style='color:var(--text3);padding:7px 0;border-bottom:1px solid var(--border);'>Nombre</td>"
                f"<td style='text-align:right;color:var(--text);font-weight:600;padding:7px 0;border-bottom:1px solid var(--border);'>{nombre_u}</td></tr>"
                f"<tr><td style='color:var(--text3);padding:7px 0;border-bottom:1px solid var(--border);'>Plan actual</td>"
                f"<td style='text-align:right;padding:7px 0;border-bottom:1px solid var(--border);'>{_plan_badge(plan_u)}</td></tr>"
                f"<tr><td style='color:var(--text3);padding:7px 0;border-bottom:1px solid var(--border);'>Acciones hoy</td>"
                f"<td style='text-align:right;color:var(--text2);padding:7px 0;border-bottom:1px solid var(--border);'>{row.get('usos_hoy', 0)}</td></tr>"
                f"<tr><td style='color:var(--text3);padding:7px 0;'>Acciones totales</td>"
                f"<td style='text-align:right;color:var(--gold);font-weight:600;padding:7px 0;'>{row.get('usos_total', 0)}</td></tr>"
                "</table></div>",
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                "<div style='background:rgba(201,168,76,0.05);border:1px solid rgba(201,168,76,0.15);"
                "border-radius:12px;padding:18px 20px;'>"
                "<div style='font-family:Sora,sans-serif;font-size:0.62rem;font-weight:700;"
                "text-transform:uppercase;letter-spacing:0.1em;color:var(--text3);margin-bottom:12px;'>Cambiar plan</div>",
                unsafe_allow_html=True
            )
            plan_options = list(PLANES.keys())
            current_idx  = plan_options.index(plan_u) if plan_u in plan_options else 0
            nuevo_p      = st.selectbox(
                "Nuevo plan",
                options=plan_options,
                index=current_idx,
                format_func=lambda x: f"{PLANES[x]['icon']} {PLANES[x]['label']}",
                key=f"perfil_plan_{uid_key}"
            )
            nota = st.text_input("Nota interna", placeholder="Motivo del cambio...", key=f"nota_{uid_key}")

            if st.button("Aplicar cambio de plan", type="primary", use_container_width=True, key=f"btn_perfil_{uid_key}"):
                if nuevo_p != plan_u:
                    _cambiar_plan_usuario(sb, email_u, nuevo_p)
                else:
                    st.info("El usuario ya tiene ese plan.")

            st.markdown("</div>", unsafe_allow_html=True)
