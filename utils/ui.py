import base64
from pathlib import Path
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

GREEN_PALETTE = [
    '#0B5D2A',
    '#157A3A',
    '#2E8B57',
    '#4FAE6A',
    '#72C287',
    '#98D5A6',
    '#BFE6C7',
]
STATUS_COLORS = {
    'Normal': '#2E8B57',
    'Monitor': '#72C287',
    'Needs Collection': '#4FAE6A',
    'Urgent': '#0B5D2A',
}
PRIORITY_COLORS = {
    'Low': '#BFE6C7',
    'Medium': '#72C287',
    'High': '#2E8B57',
    'Critical': '#0B5D2A',
}

GREEN_SCALE = [
    [0.00, '#EAF7EE'],
    [0.15, '#CFEAD7'],
    [0.35, '#A8D8B5'],
    [0.55, '#72C287'],
    [0.72, '#4FAE6A'],
    [0.88, '#2E8B57'],
    [1.00, '#0B5D2A'],
]

def configure_charts():
    """Apply one AZGREEN green-only visual language to all Plotly charts."""
    px.defaults.color_discrete_sequence = GREEN_PALETTE
    px.defaults.color_continuous_scale = GREEN_SCALE
    template = go.layout.Template(
        layout=go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter, sans-serif', color='#17321F'),
            colorway=GREEN_PALETTE,
            legend=dict(bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=10, r=10, t=40, b=10),
            xaxis=dict(showgrid=False, zeroline=False, linecolor='#D7E5D9'),
            yaxis=dict(gridcolor='#E1EAE3', zeroline=False, linecolor='#D7E5D9'),
            hoverlabel=dict(bgcolor='#173F2A', font_color='white')
        )
    )
    px.defaults.template = template


def css():
    configure_charts()
    st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:Inter,sans-serif}
.stApp{background:#F7FAF7;color:#17321F}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#004225,#004225);border-right:1px solid #084B22}
[data-testid="stSidebar"] *{color:#fff!important}
/* Hide Streamlit's automatic multipage navigation so the AZGREEN logo stays at the very top. */
[data-testid="stSidebarNav"]{display:none!important}
.block-container{max-width:1500px;padding-top:4rem}
.title{font-size:2.1rem;font-weight:800;color:#0B5D2A}
.sub{color:#627269}
.tag{display:inline-block;margin-top:.6rem;padding:.35rem .7rem;border-radius:999px;background:#EAF7EE;color:#146B34;font-size:.75rem;font-weight:700}
.kpi{background:#fff;border:1px solid #DCE8DE;border-radius:16px;padding:1rem;min-height:120px;box-shadow:0 6px 20px rgba(27,67,50,.08);animation:up .45s}
.kl{font-size:.76rem;color:#65756B;font-weight:700}.kv{font-size:1.5rem;font-weight:800;margin-top:.35rem;color:#173F2A}.kn{font-size:.72rem;color:#18813D;margin-top:.2rem}
.card{background:#fff;border:1px solid #DCE8DE;border-radius:16px;padding:1rem;box-shadow:0 6px 20px rgba(27,67,50,.08)}
.card:hover,.kpi:hover{box-shadow:0 9px 24px rgba(27,67,50,.11)}
.step{min-width:145px;padding:.75rem;text-align:center;background:#fff;border:1px solid #DCE8DE;border-radius:12px;box-shadow:0 4px 14px rgba(27,67,50,.06)}
.journey{display:flex;align-items:stretch;overflow:auto}.arrow{padding:0 .4rem;display:flex;align-items:center;color:#2E7D32;font-size:1.3rem}
/* Native Streamlit bordered containers use the same AZGREEN white-card language everywhere. */
div[data-testid="stVerticalBlockBorderWrapper"]{background:#fff!important;border:1px solid #DCE8DE!important;border-radius:16px!important;box-shadow:0 6px 20px rgba(27,67,50,.08)!important}
.alert{padding:.65rem;border-bottom:1px solid #EDF2EE;font-size:.82rem}
.arch{display:flex;gap:8px;justify-content:center;align-items:center;flex-wrap:wrap}.abox{padding:.7rem .9rem;border-radius:12px;background:#EAF7EE;border:1px solid #CDE9D5;color:#125E2E;font-weight:700}.arr{color:#5A9D6E;font-weight:800}
.foot{margin-top:2rem;padding:1rem;text-align:center;color:#5B7563;background:#EFF8F1;border-radius:12px}
@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
</style>""",unsafe_allow_html=True)

def sidebar():
    with st.sidebar:
        # Keep the existing AZGREEN logo exactly as provided and place it first.
        p=Path('assets/white_logo.png')
        if p.exists():
            b64=base64.b64encode(p.read_bytes()).decode()
            st.markdown(
                f"<div style='text-align:center;padding:0 8px 12px 8px'><img src='data:image/png;base64,{b64}' style='width:88%;max-width:245px;display:block;margin:0 auto'></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown('<h2 style="text-align:center">AZGREEN</h2>',unsafe_allow_html=True)
        # st.markdown('<div style="background:#ffffff22;border:1px solid #ffffff33;border-radius:10px;padding:8px;text-align:center;font-size:.72rem;font-weight:700">PROTOTYPE • SIMULATED DATA</div>',unsafe_allow_html=True)
        # st.caption('Smart Campus Waste Management System')
        st.markdown('### Management')
        for p,l in [
            ('app.py','Overview'),
            ('pages/02_GIS_Map.py','GIS Map'),
            ('pages/03_Smart_Bins.py','Smart Bin Management'),
            ('pages/04_Analytics.py','Analytics'),
            ('pages/05_Collection.py','Collection Management'),
            ('pages/06_Recycling_Impact.py','Recycling & Impact')
        ]:
            st.page_link(p,label=l)
        # st.markdown('### Advanced / Prototype')
        # for p,l in [
        #     ('pages/07_Student_Engagement.py','Student Engagement'),
        #     ('pages/08_Machine_Monitoring.py','Machine Monitoring'),
        #     ('pages/09_AI_Future.py','AI / Future'),
        #     ('pages/10_Alerts.py','Alerts')
        # ]:
        #     st.page_link(p,label=l)

def header(t,s,future=False):
    tag='Future Development' if future else 'Prototype / Simulated Data'
    st.markdown(f"<div class='title'>{t}</div><div class='sub'>{s}</div><span class='tag'>{tag} • Not Live University Measurements</span>",unsafe_allow_html=True)

def kpi(l,v,n='',i=''):
    st.markdown(f"<div class='kpi'><div class='kl'>{i} {l}</div><div class='kv'>{v}</div><div class='kn'>{n}</div></div>",unsafe_allow_html=True)

def footer():
    st.markdown('<div class="foot">🌿 <b>AZGREEN</b> — Smart Campus Waste Management • Prototype Dashboard v2</div>',unsafe_allow_html=True)
