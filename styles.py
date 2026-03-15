# styles.py — AI Growth Systems
# CSS centralizado. Importar con: from styles import inject_css, CSS_VARS
# Nunca volver a duplicar estilos en auth.py ni en otros módulos.

import streamlit as st

CSS_VARS = """
:root {
  --base:    #08090C;
  --surface: #0F1117;
  --surface2:#141520;
  --border:  #1E1F2E;
  --border2: #282938;
  --gold:    #C9A84C;
  --gold2:   #E8C96A;
  --text:    #EAEAF0;
  --text2:   #9090A8;
  --text3:   #505060;
  --green:   #3DD68C;
  --red:     #F87171;
  --amber:   #FBBF24;
  --radius:  12px;
  --radius2: 8px;
}
"""

FULL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&display=swap');

:root {
  --base:    #08090C;
  --surface: #0F1117;
  --surface2:#141520;
  --border:  #1E1F2E;
  --border2: #282938;
  --gold:    #C9A84C;
  --gold2:   #E8C96A;
  --text:    #EAEAF0;
  --text2:   #9090A8;
  --text3:   #505060;
  --green:   #3DD68C;
  --red:     #F87171;
  --amber:   #FBBF24;
  --radius:  12px;
  --radius2: 8px;
}

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', system-ui, sans-serif !important;
    background: var(--base) !important;
    color: var(--text) !important;
    -webkit-font-smoothing: antialiased;
}
.main .block-container {
    padding-top: 2rem !important;
    max-width: 1060px !important;
    background: transparent !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.4) !important;
}
section[data-testid="stSidebar"] * { color: var(--text2) !important; }

section[data-testid="stSidebar"] .stRadio > div > label {
    background: transparent !important;
    border: none !important;
    border-radius: var(--radius2) !important;
    padding: 7px 14px !important;
    margin-bottom: 1px !important;
    font-size: 0.83rem !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text3) !important;
    transition: all 0.18s ease !important;
    cursor: pointer !important;
    font-weight: 400 !important;
    letter-spacing: 0.01em !important;
}
section[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(201,168,76,0.07) !important;
    color: var(--gold2) !important;
    padding-left: 18px !important;
    border-left: 2px solid var(--gold) !important;
}
section[data-testid="stSidebar"] .stRadio > div > label > div:first-child {
    display: none !important;
}
/* Category separators */
section[data-testid="stSidebar"] .stRadio > div > label[aria-label^="—"] {
    font-size: 0.56rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.14em !important;
    color: var(--border2) !important;
    padding: 20px 14px 4px !important;
    pointer-events: none !important;
    cursor: default !important;
}
section[data-testid="stSidebar"] .stRadio > div > label[aria-label^="—"]:hover {
    background: transparent !important;
    color: var(--border2) !important;
    padding-left: 14px !important;
    border-left: none !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    border-radius: var(--radius2) !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.02em !important;
}
.stButton > button[kind="primary"] {
    background: var(--gold) !important;
    border: none !important;
    color: #0A0807 !important;
    box-shadow: 0 2px 16px rgba(201,168,76,0.25) !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--gold2) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(201,168,76,0.38) !important;
}
.stButton > button:not([kind="primary"]) {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    color: var(--text2) !important;
}
.stButton > button:not([kind="primary"]):hover {
    border-color: var(--gold) !important;
    color: var(--gold2) !important;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 9px !important;
    font-size: 0.875rem !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    caret-color: var(--gold);
    transition: all 0.18s !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color: var(--text3) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(201,168,76,0.12) !important;
    background: var(--surface) !important;
}
.stTextInput label, .stTextArea label {
    color: var(--text3) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 9px !important;
    color: var(--text) !important;
}
.stSelectbox label { color: var(--text3) !important; font-size: 0.78rem !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px !important;
    padding: 8px 18px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: var(--text3) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background: var(--surface2) !important;
    color: var(--gold2) !important;
}

/* ── Alerts ── */
.stAlert { border-radius: 9px !important; font-family: 'DM Sans', sans-serif !important; }
[data-testid="stSuccess"] { background: rgba(61,214,140,0.07) !important; color: #3DD68C !important; border-left: 2px solid #3DD68C !important; }
[data-testid="stWarning"] { background: rgba(251,191,36,0.07) !important;  color: #FBBF24 !important; border-left: 2px solid #FBBF24 !important; }
[data-testid="stError"]   { background: rgba(248,113,113,0.07) !important; color: #F87171 !important; border-left: 2px solid #F87171 !important; }

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] { color: var(--text3) !important; font-size: 0.72rem !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; }
[data-testid="stMetricValue"] { color: var(--text) !important; font-family: 'Sora', sans-serif !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"] { font-size: 0.75rem !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius2) !important;
    color: var(--text2) !important;
    font-size: 0.83rem !important;
}
.streamlit-expanderContent {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
}

/* ── Chat ── */
[data-testid="stChatMessage"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
}

/* ── Progress / spinner ── */
.stSpinner > div { border-top-color: var(--gold) !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--base); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--text3); }

/* ── Animations ── */
@keyframes fadeUp  { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }
@keyframes floatUp { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }
@keyframes glow    { 0%,100% { filter: drop-shadow(0 0 8px rgba(201,168,76,0.6)); } 50% { filter: drop-shadow(0 0 20px rgba(201,168,76,1)); } }
@keyframes pulse   { 0%,100% { opacity: 1; } 50% { opacity: 0.6; } }

/* ── Upgrade banner (aparece cuando el usuario choca con límite) ── */
.upgrade-banner {
    background: linear-gradient(135deg, rgba(201,168,76,0.08), rgba(232,201,106,0.04));
    border: 1px solid rgba(201,168,76,0.25);
    border-radius: var(--radius);
    padding: 20px 24px;
    text-align: center;
    animation: fadeUp 0.3s ease;
}
.upgrade-banner h3 {
    font-family: 'Sora', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--gold2);
    margin-bottom: 8px;
}
.upgrade-banner p {
    font-size: 0.83rem;
    color: var(--text3);
    line-height: 1.65;
    margin-bottom: 14px;
}

/* ── Onboarding stepper ── */
.onboarding-step {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 28px 32px;
    max-width: 560px;
    margin: 0 auto;
    animation: fadeUp 0.4s ease;
}
.onboarding-step-number {
    display: inline-flex;
    width: 28px; height: 28px;
    background: rgba(201,168,76,0.12);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 50%;
    align-items: center; justify-content: center;
    font-size: 0.72rem; font-weight: 700;
    color: var(--gold);
    margin-bottom: 16px;
}

/* ── Stripe checkout card ── */
.pricing-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px 26px;
    transition: border-color 0.2s, transform 0.2s;
    position: relative;
    overflow: hidden;
}
.pricing-card:hover {
    border-color: rgba(201,168,76,0.35);
    transform: translateY(-2px);
}
.pricing-card.featured {
    border-color: rgba(201,168,76,0.4);
    background: linear-gradient(135deg, #0D0F1C, #141829);
}
.pricing-card.featured::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}

/* ── Sidebar brand ── */
.sb-wrap { padding: 20px 14px 10px; }
.sb-mark { font-size: 1.05rem; vertical-align: middle; animation: glow 3s ease-in-out infinite; }
.sb-name {
    font-family: 'Sora', sans-serif; font-size: 0.86rem; font-weight: 700;
    color: #EAEAF0 !important; vertical-align: middle; margin-left: 9px; letter-spacing: -0.01em;
}
.sb-sub { font-size: 0.57rem; color: #282938 !important; margin-top: 5px; letter-spacing: 0.13em; font-weight: 600; text-transform: uppercase; font-family: 'DM Sans', sans-serif; }
</style>
"""

LOGIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');
:root {
  --base:#08090C; --surface:#0F1117; --surface2:#141520;
  --border:#1E1F2E; --border2:#282938;
  --gold:#C9A84C; --gold2:#E8C96A;
  --text:#EAEAF0; --text2:#9090A8; --text3:#505060;
  --green:#3DD68C; --red:#F87171;
}
html, body, [class*="css"] { font-family:'DM Sans',system-ui,sans-serif !important; background:var(--base) !important; color:var(--text) !important; -webkit-font-smoothing:antialiased; }
.main .block-container { max-width:520px !important; padding-top:2rem !important; background:transparent !important; }
section[data-testid="stSidebar"] { display:none !important; }
.stTabs [data-baseweb="tab-list"] { background:var(--surface) !important; border-radius:10px !important; padding:4px !important; border:1px solid var(--border) !important; gap:2px !important; }
.stTabs [data-baseweb="tab"] { border-radius:7px !important; padding:8px 18px !important; font-size:0.82rem !important; font-weight:500 !important; color:var(--text3) !important; font-family:'DM Sans',sans-serif !important; }
.stTabs [aria-selected="true"] { background:var(--surface2) !important; color:var(--gold2) !important; }
.stTextInput input { background:var(--surface2) !important; border:1px solid var(--border2) !important; border-radius:9px !important; font-size:0.875rem !important; color:var(--text) !important; font-family:'DM Sans',sans-serif !important; caret-color:var(--gold); transition:all 0.18s !important; }
.stTextInput input::placeholder { color:var(--text3) !important; }
.stTextInput input:focus { border-color:var(--gold) !important; box-shadow:0 0 0 3px rgba(201,168,76,0.12) !important; background:var(--surface) !important; }
.stTextInput label { color:var(--text3) !important; font-size:0.78rem !important; font-weight:500 !important; letter-spacing:0.03em !important; }
.stButton > button { font-family:'DM Sans',sans-serif !important; font-weight:600 !important; font-size:0.875rem !important; border-radius:9px !important; transition:all 0.2s !important; letter-spacing:0.02em !important; }
.stButton > button[kind="primary"] { background:var(--gold) !important; border:none !important; color:#0A0807 !important; box-shadow:0 2px 16px rgba(201,168,76,0.3) !important; }
.stButton > button[kind="primary"]:hover { background:var(--gold2) !important; transform:translateY(-1px) !important; box-shadow:0 6px 24px rgba(201,168,76,0.4) !important; }
.stButton > button:not([kind="primary"]) { background:var(--surface2) !important; border:1px solid var(--border2) !important; color:var(--text2) !important; }
.stButton > button:not([kind="primary"]):hover { border-color:var(--gold) !important; color:var(--gold2) !important; }
.stSelectbox > div > div { background:var(--surface2) !important; border:1px solid var(--border2) !important; border-radius:9px !important; color:var(--text) !important; }
.stSelectbox label { color:var(--text3) !important; font-size:0.78rem !important; }
.stAlert { border-radius:9px !important; font-family:'DM Sans',sans-serif !important; }
[data-testid="stSuccess"] { background:rgba(61,214,140,0.07) !important; color:#3DD68C !important; border-left:2px solid #3DD68C !important; }
[data-testid="stWarning"] { background:rgba(251,191,36,0.07) !important; color:#FBBF24 !important; border-left:2px solid #FBBF24 !important; }
[data-testid="stError"]   { background:rgba(248,113,113,0.07) !important; color:#F87171 !important; border-left:2px solid #F87171 !important; }
@keyframes glow   { 0%,100%{filter:drop-shadow(0 0 8px rgba(201,168,76,0.6));} 50%{filter:drop-shadow(0 0 20px rgba(201,168,76,1));} }
@keyframes fadeUp { from{opacity:0;transform:translateY(14px);} to{opacity:1;transform:translateY(0);} }
</style>
"""

def inject_css():
    """Inyecta el CSS global. Llamar una vez al inicio de app.py."""
    st.markdown(FULL_CSS, unsafe_allow_html=True)

def inject_login_css():
    """CSS específico para la pantalla de login."""
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)
