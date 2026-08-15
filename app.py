import streamlit as st
import plotly.express as px

from utils.ui import css, sidebar, header, footer, STATUS_COLORS
from utils.data import load_data, metrics

st.set_page_config(
    page_title="AZGREEN | Overview",
    page_icon="🌿",
    layout="wide"
)

css()
sidebar()

bins, col, rec, mach, imp, pts, stu = load_data()
m = metrics(bins, col, rec, imp, stu)

header(
    "AZGREEN",
    "Smart Campus Waste Management — Executive Management Overview"
)


# =========================================================
# AZGREEN CARD STYLE
# =========================================================

st.markdown(
    """
<style>
.az-card-title {
    font-size: 0.82rem;
    color: #607068;
    font-weight: 600;
    margin-bottom: 6px;
}

.az-card-value {
    font-size: 1.65rem;
    line-height: 1.15;
    font-weight: 800;
    color: #173F2A;
    margin-bottom: 5px;
}

.az-card-subtitle {
    font-size: 0.72rem;
    color: #7B8B82;
}

.az-icon {
    font-size: 1.55rem;
    color: #0B5D2A;
    background: #EAF5EC;
    border-radius: 12px;
    padding: 8px 10px;
    display: inline-block;
    margin-bottom: 10px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #DCEBDD !important;
    border-radius: 16px !important;
    background: linear-gradient(145deg, #FFFFFF 0%, #F7FBF8 100%) !important;
    box-shadow: 0 5px 16px rgba(27, 67, 50, 0.07);
}
</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SECTION TITLE HELPER
# =========================================================

def section_title(title):
    st.markdown(
        f"### {title}"
    )


# =========================================================
# MANAGEMENT KPI CARD
# =========================================================

def management_kpi(label, value, subtitle, icon_name):
    with st.container(border=True):
        st.markdown(
            f":material/{icon_name}:",
            help=label
        )
        st.markdown(
            f'<div class="az-card-title">{label}</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="az-card-value">{value}</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="az-card-subtitle">{subtitle}</div>',
            unsafe_allow_html=True
        )


# =========================================================
# 1. MANAGEMENT KPIs
# =========================================================

section_title("Management KPIs")

kpi_cols = st.columns(6, gap="medium")

management_kpis = [
    (
        "Waste Diversion Rate",
        f"{m['diversion']:.1f}%",
        "Overall diverted waste",
        "autorenew"
    ),
    (
        "Recycling Rate",
        f"{m['recycling_rate']:.1f}%",
        "Recyclable material processed",
        "recycling"
    ),
    (
        "Average Bin Fill",
        f"{m['avg_fill']:.0f}%",
        "Current campus snapshot",
        "delete_outline"
    ),
    (
        "Overflow Incidents",
        m["overflow"],
        "Bins at or above 90%",
        "warning"
    ),
    (
        "Collection Operations",
        m["operations"],
        "Recorded operations",
        "local_shipping"
    ),
    (
        "Student Participation",
        f"{m['students']:,}",
        "Active participation records",
        "school"
    )
]

for col_slot, item in zip(kpi_cols, management_kpis):
    with col_slot:
        management_kpi(*item)


# =========================================================
# 2. TWO PRIMARY CHARTS — DIRECTLY UNDER MANAGEMENT KPIs
# =========================================================

section_title("Waste Analytics")

chart_left, chart_right = st.columns(2, gap="large")

# ---------------------------------------------------------
# Waste by Type
# ---------------------------------------------------------

with chart_left:
    with st.container(border=True):
        st.markdown("**Waste by Type**")

        q = col.groupby(
            "waste_type",
            as_index=False
        )["weight_kg"].sum()

        fig = px.bar(
            q,
            x="waste_type",
            y="weight_kg",
            title="Collected Waste by Type"
        )
        fig.update_traces(marker_color="#2E8B57")
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=45, b=10)
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

# ---------------------------------------------------------
# Bin Status by Area
# ---------------------------------------------------------

with chart_right:
    with st.container(border=True):
        st.markdown("**Bin Status by Area**")

        q = bins.groupby(
            ["location", "status"],
            as_index=False
        ).size()

        fig = px.bar(
            q,
            x="location",
            y="size",
            color="status",
            color_discrete_map=STATUS_COLORS,
            barmode="stack",
            title="System State Distribution"
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=45, b=10)
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )


# =========================================================
# 3. OPERATIONAL OVERVIEW
# =========================================================

section_title("Operational Overview")

overview_left, overview_right = st.columns(2, gap="large")


# ---------------------------------------------------------
# System Snapshot
# ---------------------------------------------------------

# with overview_right:
#     with st.container(border=True):

#         st.markdown("**System Snapshot**")

#         snapshot_cols = st.columns(3)

#         with snapshot_cols[0]:
#             st.metric(
#                 "Waste Diverted",
#                 f"{m['diverted']:,.0f} kg"
#             )

#         with snapshot_cols[1]:
#             st.metric(
#                 "Recovered Material",
#                 f"{m['recycled']:,.0f} kg"
#             )

#         with snapshot_cols[2]:
#             st.metric(
#                 "CO₂e Avoided",
#                 f"{m['co2']:,.0f} kg"
#             )

#         st.caption(
#             "Environmental impact values are prototype / simulated "
#             "unless otherwise documented."
#         )


# =========================================================
# 4. DATA ARCHITECTURE
# =========================================================

section_title("Data Architecture")

arch_cols = st.columns(5, gap="small")

architecture = [
    ("IoT Sensors", "sensors"),
    ("Smart Bins", "delete_outline"),
    ("Database", "storage"),
    ("Dashboard + GIS", "map"),
    ("Analytics / Decisions", "insights")
]

for slot, (label, icon_name) in zip(arch_cols, architecture):
    with slot:
        with st.container(border=True):
            st.markdown(
                f":material/{icon_name}:"
            )
            st.markdown(
                f"**{label}**"
            )

st.caption(
    "Additional sources: collection records • GIS • "
    "student interactions • manual entry."
)


# =========================================================
# 5. SYSTEM STATES — LAST
# =========================================================

section_title("System States")

state_cols = st.columns(7, gap="small")

system_states = [
    ("Total Smart Bins", m["total_bins"], "Campus inventory", "delete_outline"),
    ("Available Bins", m["available"], "Normal + monitor", "check_circle"),
    ("Nearly Full", m["nearly"], "Needs collection", "schedule"),
    ("Full / Collection", m["full"], "Urgent intervention", "priority_high"),
    ("Online Sensors", m["online"], "Simulated connectivity", "sensors"),
    ("Offline / Maintenance", m["offline"], "Inspection required", "build"),
    ("Recyclable Waste", f"{m['recyclable']:,.0f} kg", "Demo total", "recycling")
]

for slot, (label, value, subtitle, icon_name) in zip(
    state_cols,
    system_states
):
    with slot:
        with st.container(border=True):

            st.markdown(
                f":material/{icon_name}:"
            )

            st.markdown(
                f'<div class="az-card-title">{label}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="az-card-value">{value}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="az-card-subtitle">{subtitle}</div>',
                unsafe_allow_html=True
            )


# =========================================================
# DISCLAIMER
# =========================================================

st.warning(
    "All displayed dashboard numbers are prototype / simulated "
    "except where otherwise documented."
)

footer()