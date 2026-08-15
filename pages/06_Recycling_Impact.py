import streamlit as st
import plotly.express as px

from utils.ui import css, sidebar, header, footer
from utils.data import load_data, metrics


st.set_page_config(
    page_title="AZGREEN | Recycling & Impact",
    page_icon="♻️",
    layout="wide",
)

css()

# Green card styling for bordered Streamlit containers.
# This gives KPI / journey cards a soft green tint, border, and shadow
# without exposing raw HTML on the page.
st.markdown(
    """
    <style>
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F5FBF6 100%);
        border: 1px solid #D7E9DB !important;
        border-radius: 16px !important;
        box-shadow: 0 5px 16px rgba(27, 67, 50, 0.08);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 8px 22px rgba(27, 67, 50, 0.13);
        transform: translateY(-1px);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMetricLabel"] {
        color: #5A6B61 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMetricValue"] {
        color: #1B4332 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] .stCaption {
        color: #6A7B72 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

sidebar()

bins, col, rec, mach, imp, pts, stu = load_data()
m = metrics(bins, col, rec, imp, stu)

header(
    "Recycling & Environmental Impact",
    "Trace material recovery and report prototype sustainability indicators",
)

# =========================================================
# TOP RECYCLING KPIs
# =========================================================

st.markdown("### Recycling KPIs")

kpi_data = [
    ("Collected", f"{rec.input_weight.sum():,.1f} kg"),
    ("Sorted", f"{rec.sorted_weight.sum():,.1f} kg"),
    ("Processed", f"{rec.processed_weight.sum():,.1f} kg"),
    ("Final Recovered", f"{rec.output_weight.sum():,.1f} kg"),
    ("Diversion Rate", f"{m['diversion']:.1f}%"),
]

kpi_cols = st.columns(5, gap="medium")

for col_container, (label, value) in zip(kpi_cols, kpi_data):
    with col_container:
        with st.container(border=True):
            st.metric(label, value)


# =========================================================
# RECYCLING ANALYTICS
# =========================================================

st.markdown("### Recycling Analytics")

left, right = st.columns(2, gap="large")

with left:
    q = (
        rec.groupby("material", as_index=False)
        .agg(
            input=("input_weight", "sum"),
            output=("output_weight", "sum"),
        )
    )

    fig_material = px.bar(
        q,
        x="material",
        y=["input", "output"],
        barmode="group",
        labels={
            "material": "Material",
            "value": "Weight (kg)",
            "variable": "Stage",
        },
        color_discrete_sequence=["#0B5D2A", "#72C287"],
    )

    fig_material.update_layout(
        height=360,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=20, b=10),
        font=dict(color="#1B4332"),
        legend_title_text="",
    )

    st.plotly_chart(
        fig_material,
        use_container_width=True,
        config={"displayModeBar": False},
    )

with right:
    fig_impact = px.line(
        imp,
        x="date",
        y=["waste_diverted", "recycled_material"],
        markers=True,
        labels={
            "date": "Date",
            "value": "Weight (kg)",
            "variable": "Metric",
        },
        color_discrete_sequence=["#0B5D2A", "#72C287"],
    )

    fig_impact.update_layout(
        height=360,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=20, b=10),
        font=dict(color="#1B4332"),
        legend_title_text="",
    )

    st.plotly_chart(
        fig_impact,
        use_container_width=True,
        config={"displayModeBar": False},
    )


# =========================================================
# MATERIAL JOURNEY
# =========================================================

st.markdown("### Material Journey")

journey = st.columns([1, 0.35, 1, 0.35, 1, 0.35, 1], gap="small")

journey_steps = [
    ("Collected", "Input"),
    ("Sorted", "Material"),
    ("Processed", "Material"),
    ("Final Product", "Recovered"),
]

# Step 1
with journey[0]:
    with st.container(border=True):
        st.markdown("#### Collected")
        st.caption("Input")

# Arrow 1
with journey[1]:
    st.markdown(
        "<div style='text-align:center; font-size:28px; "
        "font-weight:700; color:#2E7D32; padding-top:22px;'>→</div>",
        unsafe_allow_html=True,
    )

# Step 2
with journey[2]:
    with st.container(border=True):
        st.markdown("#### Sorted")
        st.caption("Material")

# Arrow 2
with journey[3]:
    st.markdown(
        "<div style='text-align:center; font-size:28px; "
        "font-weight:700; color:#2E7D32; padding-top:22px;'>→</div>",
        unsafe_allow_html=True,
    )

# Step 3
with journey[4]:
    with st.container(border=True):
        st.markdown("#### Processed")
        st.caption("Material")

# Arrow 3
with journey[5]:
    st.markdown(
        "<div style='text-align:center; font-size:28px; "
        "font-weight:700; color:#2E7D32; padding-top:22px;'>→</div>",
        unsafe_allow_html=True,
    )

# Step 4
with journey[6]:
    with st.container(border=True):
        st.markdown("#### Final Product")
        st.caption("Recovered")


# =========================================================
# ENVIRONMENTAL IMPACT KPIs
# =========================================================

st.markdown("### Environmental Impact")

impact_data = [
    ("Waste Diverted", f"{m['diverted']:,.0f} kg"),
    ("Materials Recovered", f"{m['recycled']:,.0f} kg"),
    ("CO₂e Avoided (Demo)", f"{m['co2']:,.0f} kg"),
]

impact_cols = st.columns(3, gap="large")

for col_container, (label, value) in zip(impact_cols, impact_data):
    with col_container:
        with st.container(border=True):
            st.metric(label, value)

st.warning(
    "CO₂e is Estimated/Simulated. "
    "A documented scientific conversion factor is required "
    "before claiming validated real-world impact."
)

footer()