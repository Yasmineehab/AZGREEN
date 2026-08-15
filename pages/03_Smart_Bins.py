import streamlit as st
import plotly.express as px

from utils.ui import (
    css,
    sidebar,
    header,
    footer,
    STATUS_COLORS,
    PRIORITY_COLORS
)
from utils.data import load_data


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AZGREEN | Smart Bins",
    page_icon="🗑️",
    layout="wide"
)

css()
sidebar()

bins, col, rec, mach, imp, pts, stu = load_data()

header(
    "Smart Bin Management",
    "Operational inventory, sensor status and collection priority"
)


# =========================================================
# FILTERS
# =========================================================

a, b, c, d = st.columns(4)

with a:
    ar = st.multiselect(
        "Area",
        sorted(bins.location.dropna().unique())
    )

with b:
    s = st.multiselect(
        "Status",
        ["Normal", "Monitor", "Needs Collection", "Urgent"]
    )

with c:
    se = st.multiselect(
        "Sensor",
        ["Online", "Maintenance"]
    )

with d:
    w = st.multiselect(
        "Waste Type",
        sorted(bins.waste_type.dropna().unique())
    )


df = bins.copy()

if ar:
    df = df[df.location.isin(ar)]

if s:
    df = df[df.status.isin(s)]

if se:
    df = df[df.sensor_status.isin(se)]

if w:
    df = df[df.waste_type.isin(w)]


# =========================================================
# MANAGEMENT KPIs
# =========================================================

st.markdown("### Management KPIs")

k1, k2, k3, k4 = st.columns(4, gap="medium")


visible_bins = len(df)

average_fill = (
    df.fill_level.mean()
    if len(df)
    else 0
)

collection_required = int(
    df.status.isin(
        ["Needs Collection", "Urgent"]
    ).sum()
)

online_sensors = int(
    (df.sensor_status == "Online").sum()
)


with k1:
    st.markdown(
        f"""
        <div class="card">
            <div style="font-size:14px;opacity:.75;">
                Visible Bins
            </div>
            <div style="font-size:32px;font-weight:700;">
                {visible_bins}
            </div>
            <div style="font-size:12px;opacity:.65;">
                Active filtered inventory
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k2:
    st.markdown(
        f"""
        <div class="card">
            <div style="font-size:14px;opacity:.75;">
                Online Sensors
            </div>
            <div style="font-size:32px;font-weight:700;">
                {online_sensors}
            </div>
            <div style="font-size:12px;opacity:.65;">
                Sensors currently online
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k3:
    st.markdown(
        f"""
        <div class="card">
            <div style="font-size:14px;opacity:.75;">
                Collection Required
            </div>
            <div style="font-size:32px;font-weight:700;">
                {collection_required}
            </div>
            <div style="font-size:12px;opacity:.65;">
                Needs Collection + Urgent
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k4:
    st.markdown(
        f"""
        <div class="card">
            <div style="font-size:14px;opacity:.75;">
                Average Fill
            </div>
            <div style="font-size:32px;font-weight:700;">
                {average_fill:.0f}%
            </div>
            <div style="font-size:12px;opacity:.65;">
                Current average fill level
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CHARTS
# =========================================================

st.markdown("### Bin Monitoring Analytics")

x, y = st.columns(2, gap="large")


# ---------------------------------------------------------
# Fill Level by Bin
# ---------------------------------------------------------

with x:

    chart_df = df.sort_values(
        "fill_level",
        ascending=True
    )

    fig_fill = px.bar(
        chart_df,
        x="fill_level",
        y="bin_id",
        orientation="h",
        color="status",
        color_discrete_map=STATUS_COLORS,
        labels={
            "fill_level": "Fill Level (%)",
            "bin_id": "Smart Bin"
        },
        title="Fill Level by Smart Bin"
    )

    fig_fill.update_layout(
        showlegend=True,
        margin=dict(l=10, r=10, t=50, b=10),
        height=420
    )

    st.plotly_chart(
        fig_fill,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# ---------------------------------------------------------
# Collection Priority
# ---------------------------------------------------------

with y:

    q = (
        df.collection_priority
        .value_counts()
        .reindex(
            ["Low", "Medium", "High", "Critical"],
            fill_value=0
        )
    )

    fig_priority = px.pie(
        values=q.values,
        names=q.index,
        hole=0.55,
        color=q.index,
        color_discrete_map=PRIORITY_COLORS,
        title="Collection Priority Distribution"
    )

    fig_priority.update_layout(
        showlegend=True,
        margin=dict(l=10, r=10, t=50, b=10),
        height=420
    )

    st.plotly_chart(
        fig_priority,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# =========================================================
# SMART BIN TABLE
# =========================================================

st.markdown("### Smart Bin Inventory")

table_columns = [
    "bin_id",
    "location",
    "waste_type",
    "capacity_kg",
    "fill_level",
    "status",
    "sensor_status",
    "last_collection",
    "collection_priority"
]

table_df = (
    df[table_columns]
    .sort_values(
        "fill_level",
        ascending=False
    )
)

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# PROTOTYPE RULES
# =========================================================

st.info(
    "Prototype rules: "
    "<50% Low • "
    "50–70% Medium • "
    "70–90% High • "
    ">90% Critical. "
    "Validate thresholds with real collection data."
)


footer()