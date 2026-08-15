import streamlit as st
import plotly.express as px

from utils.ui import (
    css,
    sidebar,
    header,
    footer,
    STATUS_COLORS
)
from utils.data import load_data, metrics


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AZGREEN | Analytics",
    page_icon="📈",
    layout="wide"
)

css()
sidebar()

bins, col, rec, mach, imp, pts, stu = load_data()

m = metrics(
    bins,
    col,
    rec,
    imp,
    stu
)

header(
    "Analytics",
    "Waste generation, collection trends, utilization and management KPIs"
)


# =========================================================
# FILTERS
# =========================================================

st.markdown("### Analytics Filters")

a, b, c = st.columns(3)

with a:
    types = st.multiselect(
        "Waste Type",
        sorted(col.waste_type.dropna().unique())
    )

with b:
    areas = st.multiselect(
        "Area",
        sorted(bins.location.dropna().unique())
    )

with c:
    gran = st.selectbox(
        "Trend",
        ["Daily", "Weekly", "Monthly"]
    )


# =========================================================
# FILTERED DATA
# =========================================================

df = col.merge(
    bins[["bin_id", "location"]],
    on="bin_id",
    how="left"
)

if types:
    df = df[df.waste_type.isin(types)]

if areas:
    df = df[df.location.isin(areas)]


# =========================================================
# MANAGEMENT KPIs
# =========================================================

st.markdown("### Management KPIs")

k1, k2, k3, k4, k5, k6 = st.columns(
    6,
    gap="medium"
)


def kpi_card(container, title, value, description):
    with container:

        # Native Streamlit bordered card
        with st.container(border=True):

            st.markdown(
                f"""
                <div style="
                    color:#66756C;
                    font-size:14px;
                    margin-bottom:4px;
                    font-weight:500;
                ">
                    {title}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div style="
                    color:#176B3A;
                    font-size:30px;
                    font-weight:700;
                    line-height:1.2;
                    margin:4px 0 6px 0;
                ">
                    {value}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.caption(description)


# =========================================================
# KPI CARDS
# =========================================================

kpi_card(
    k1,
    "Diversion Rate",
    f'{m["diversion"]:.1f}%',
    "Waste diverted from disposal"
)

kpi_card(
    k2,
    "Recycling Rate",
    f'{m["recycling_rate"]:.1f}%',
    "Estimated recycling performance"
)

kpi_card(
    k3,
    "Bin Utilization",
    f'{m["avg_fill"]:.0f}%',
    "Average Smart Bin fill level"
)

kpi_card(
    k4,
    "Overflow Incidents",
    m["overflow"],
    "Priority overflow events"
)

kpi_card(
    k5,
    "Collection Operations",
    m["operations"],
    "Recorded collection operations"
)

kpi_card(
    k6,
    "Student Participation",
    f'{m["students"]:,}',
    "Prototype student engagement"
)


# =========================================================
# WASTE ANALYTICS
# =========================================================

st.markdown("### Waste Analytics")

x, y = st.columns(2, gap="large")


# ---------------------------------------------------------
# Chart 1 — Waste Type Distribution
# ---------------------------------------------------------

with x:

    q = (
        df.groupby(
            "waste_type",
            as_index=False
        )["weight_kg"]
        .sum()
        .sort_values(
            "weight_kg",
            ascending=True
        )
    )

    fig = px.bar(
        q,
        x="weight_kg",
        y="waste_type",
        orientation="h",
        labels={
            "weight_kg": "Waste Collected (kg)",
            "waste_type": "Waste Type"
        },
        title="Waste Collected by Type",
        color="weight_kg",
        color_continuous_scale=[
            "#E8F5E9",
            "#A5D6A7",
            "#66BB6A",
            "#2E7D32",
            "#145A32"
        ]
    )

    fig.update_coloraxes(showscale=False)

    fig.update_layout(
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        ),
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# ---------------------------------------------------------
# Chart 2 — Waste by Area
# ---------------------------------------------------------

with y:

    q = (
        df.groupby(
            "location",
            as_index=False
        )["weight_kg"]
        .sum()
        .sort_values(
            "weight_kg",
            ascending=True
        )
    )

    fig = px.bar(
        q,
        x="weight_kg",
        y="location",
        orientation="h",
        labels={
            "weight_kg": "Waste Collected (kg)",
            "location": "Area"
        },
        title="Waste Collected by Area",
        color="weight_kg",
        color_continuous_scale=[
            "#E8F5E9",
            "#A5D6A7",
            "#66BB6A",
            "#2E7D32",
            "#145A32"
        ]
    )

    fig.update_coloraxes(showscale=False)

    fig.update_layout(
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        ),
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# =========================================================
# COLLECTION TREND
# =========================================================

st.markdown("### Collection Trend")

if gran == "Daily":

    q = (
        df.groupby(
            df.date.dt.date,
            as_index=False
        )["weight_kg"]
        .sum()
    )

elif gran == "Weekly":

    q = (
        df.groupby(
            df.date.dt.to_period("W").astype(str),
            as_index=False
        )["weight_kg"]
        .sum()
    )

else:

    q = (
        df.groupby(
            df.date.dt.to_period("M").astype(str),
            as_index=False
        )["weight_kg"]
        .sum()
    )

q.columns = [
    "period",
    "weight_kg"
]


fig = px.line(
    q,
    x="period",
    y="weight_kg",
    markers=True,
    labels={
        "period": "Period",
        "weight_kg": "Waste Collected (kg)"
    },
    title=f"{gran} Waste Collection Trend"
)

fig.update_traces(
    line=dict(
        color="#2E7D32",
        width=3
    ),
    marker=dict(
        color="#145A32",
        size=8
    )
)

fig.update_layout(
    margin=dict(
        l=10,
        r=10,
        t=50,
        b=10
    ),
    height=430
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)


# =========================================================
# OPERATIONAL ANALYTICS
# =========================================================

st.markdown("### Operational Analytics")

x, y = st.columns(2, gap="large")


# ---------------------------------------------------------
# Chart 4 — Bin Utilization
# ---------------------------------------------------------

with x:

    bin_chart = bins.sort_values(
        "fill_level",
        ascending=True
    )

    fig = px.bar(
        bin_chart,
        x="fill_level",
        y="bin_id",
        orientation="h",
        color="status",
        color_discrete_map=STATUS_COLORS,
        labels={
            "fill_level": "Fill Level (%)",
            "bin_id": "Smart Bin"
        },
        title="Smart Bin Utilization"
    )

    fig.update_layout(
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        ),
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# ---------------------------------------------------------
# Chart 5 — Collection Operations by Area
# ---------------------------------------------------------

with y:

    q = (
        df.groupby(
            "location",
            as_index=False
        )["collection_id"]
        .count()
        .sort_values(
            "collection_id",
            ascending=True
        )
    )

    fig = px.bar(
        q,
        x="location",
        y="collection_id",
        labels={
            "location": "Area",
            "collection_id": "Collection Operations"
        },
        title="Collection Operations by Area",
        color="collection_id",
        color_continuous_scale=[
            "#E8F5E9",
            "#A5D6A7",
            "#66BB6A",
            "#2E7D32",
            "#145A32"
        ]
    )

    fig.update_coloraxes(showscale=False)

    fig.update_layout(
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        ),
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# =========================================================
# FOOTER
# =========================================================

footer()