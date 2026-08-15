import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen

from utils.ui import css, sidebar, header, footer
from utils.data import load_data, nearest_bins
from config import CAMPUS_NAME, CAMPUS_LAT, CAMPUS_LON

st.set_page_config(
    page_title="AZGREEN | GIS",
    page_icon="🗺️",
    layout="wide"
)

css()
sidebar()

bins, col, rec, mach, imp, pts, stu = load_data()

header(
    "GIS Map",
    "Al-Azhar University campus view — Smart Bins, collection points and spatial priorities"
)

# =========================================================
# FILTERS
# =========================================================

st.markdown("### Map Filters")

a, b, c = st.columns(3)

with a:
    s = st.multiselect(
        "Status",
        sorted(bins.status.dropna().unique().tolist())
    )

with b:
    ar = st.multiselect(
        "Area",
        sorted(bins.location.dropna().unique().tolist())
    )

with c:
    w = st.multiselect(
        "Waste Type",
        sorted(bins.waste_type.dropna().unique().tolist())
    )

df = bins.copy()

if s:
    df = df[df.status.isin(s)]

if ar:
    df = df[df.location.isin(ar)]

if w:
    df = df[df.waste_type.isin(w)]


# =========================================================
# FULL WIDTH GIS MAP
# =========================================================

st.markdown("### Campus Smart Waste Map")

mp = folium.Map(
    location=[CAMPUS_LAT, CAMPUS_LON],
    zoom_start=16,
    tiles="OpenStreetMap",
    control_scale=True
)

Fullscreen(position="topright").add_to(mp)


# ---------------------------------------------------------
# University Marker
# ---------------------------------------------------------

university_popup = (
    f"<b>{CAMPUS_NAME}</b><br>"
    f"Al-Azhar University Campus<br><br>"
    f"Coordinates: {CAMPUS_LAT:.7f}, {CAMPUS_LON:.7f}"
)

folium.Marker(
    [CAMPUS_LAT, CAMPUS_LON],
    tooltip="Al-Azhar University Campus",
    popup=folium.Popup(
        university_popup,
        max_width=340
    ),
    icon=folium.Icon(
        color="green",
        icon="university",
        prefix="fa"
    )
).add_to(mp)

folium.Circle(
    [CAMPUS_LAT, CAMPUS_LON],
    radius=650,
    color="#2E7D32",
    weight=2,
    fill=False,
    tooltip="Campus reference area"
).add_to(mp)


# ---------------------------------------------------------
# Smart Bin Markers — Color by Bin State
# ---------------------------------------------------------

def get_bin_color(status, fill_level, sensor_status):
    status_text = str(status).strip().lower()
    sensor_text = str(sensor_status).strip().lower()

    # Sensor problem has highest priority
    if sensor_text == "offline":
        return "gray"

    # Explicit critical states
    if status_text in {"urgent", "full", "critical", "needs collection"}:
        return "red"

    # Monitoring / nearly full states
    if status_text in {"monitor", "nearly full", "nearly_full"}:
        return "orange"

    # Fill-level fallback rule
    try:
        fill = float(fill_level)
        if fill >= 91:
            return "red"
        if fill >= 76:
            return "orange"
    except (TypeError, ValueError):
        pass

    return "green"


for _, r in df.iterrows():

    marker_color = get_bin_color(
        r.status,
        r.fill_level,
        r.sensor_status
    )

    popup_html = (
        f"<b>{r.bin_id}</b><br>"
        f"Location: {r.location}<br>"
        f"Waste: {r.waste_type}<br>"
        f"Capacity: {r.capacity_kg} kg<br>"
        f"Fill: {r.fill_level}%<br>"
        f"Status: {r.status}<br>"
        f"Sensor: {r.sensor_status}<br>"
        f"Last Collection: {r.last_collection.date()}<br>"
        f"Priority: {r.collection_priority}<br>"
        f"Coordinates: {r.latitude:.6f}, {r.longitude:.6f}"
    )

    folium.Marker(
        [r.latitude, r.longitude],
        tooltip=f"{r.bin_id} • {r.fill_level}%",
        popup=folium.Popup(
            popup_html,
            max_width=320
        ),
        icon=folium.Icon(
            color=marker_color,
            icon="trash",
            prefix="fa"
        )
    ).add_to(mp)


# ---------------------------------------------------------
# Collection Points
# ---------------------------------------------------------

for _, r in pts.iterrows():

    folium.CircleMarker(
        [r.latitude, r.longitude],
        radius=6,
        color="#157A3A",
        fill=True,
        fill_color="#66BB6A",
        fill_opacity=0.85,
        tooltip=f"{r.point_id} • {r.location}",
        popup=folium.Popup(
            f"<b>{r.point_id}</b><br>"
            f"{r.location}<br>"
            f"{r.point_type}",
            max_width=260
        )
    ).add_to(mp)


# ---------------------------------------------------------
# Render Full Width
# ---------------------------------------------------------

st_folium(
    mp,
    use_container_width=True,
    height=620
)


# =========================================================
# MAP NOTES / LEGEND
# =========================================================

st.markdown("### Map Legend")

legend_col1, legend_col2, legend_col3, legend_col4 = st.columns(4)

with legend_col1:
    st.markdown(
        """
        <div class="card">
        🏫 <b>University</b><br>
        Al-Azhar University Campus
        </div>
        """,
        unsafe_allow_html=True
    )

with legend_col2:
    st.markdown(
        """
        <div class="card">
        🟢 <b>Available / Normal</b><br>
        Normal fill level
        </div>
        """,
        unsafe_allow_html=True
    )

with legend_col3:
    st.markdown(
        """
        <div class="card">
        🟠 <b>Nearly Full / Monitor</b><br>
        Monitoring required
        </div>
        """,
        unsafe_allow_html=True
    )

with legend_col4:
    st.markdown(
        """
        <div class="card">
        🔴 <b>Urgent / Full</b><br>
        Collection required
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class="card" style="margin-top:10px;">
    ⚫ <b>Offline</b> = sensor inspection required
    &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;
    🟩 <b>Collection Points</b> = waste collection locations
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DETAILS SECTION
# =========================================================

st.markdown("---")

left, right = st.columns(2, gap="large")


# =========================================================
# LEFT — BIN DETAILS
# =========================================================

with left:

    st.markdown("### Bin Details")

    if len(df):

        sid = st.selectbox(
            "Select Smart Bin",
            df.bin_id.tolist()
        )

        r = df[df.bin_id == sid].iloc[0]

        details = [
            ("Location", r.location),
            ("Waste Type", r.waste_type),
            ("Capacity", f"{r.capacity_kg} kg"),
            ("Fill Level", f"{r.fill_level}%"),
            ("Status", r.status),
            ("Sensor", r.sensor_status),
            ("Priority", r.collection_priority),
            ("Last Collection", str(r.last_collection.date())),
        ]

        for label, value in details:

            st.markdown(
                f"""
                <div class="card" style="margin-bottom:8px;">
                    <b>{label}</b><br>
                    {value}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.warning(
            "No Smart Bins match the selected filters."
        )


# =========================================================
# RIGHT — STUDENT FEATURE
# =========================================================

with right:

    st.markdown(
        "### Nearest Suitable Bin — Student Feature"
    )

    st.info(
        "Prototype feature: the student selects their "
        "current campus area instead of entering coordinates. "
        "Future versions can detect the user's location "
        "automatically using device GPS."
    )

    # -----------------------------------------------------
    # Student chooses location inside campus
    # -----------------------------------------------------

    student_area = st.selectbox(
        "Where are you on campus?",
        sorted(
            bins.location.dropna().unique().tolist()
        )
    )

    student_waste = st.selectbox(
        "What type of waste do you have?",
        sorted(
            bins.waste_type.dropna().unique().tolist()
        )
    )

    # -----------------------------------------------------
    # Calculate representative location of selected area
    # -----------------------------------------------------

    area_bins = bins[
        bins.location == student_area
    ]

    if len(area_bins):

        area_lat = float(
            area_bins.latitude.mean()
        )

        area_lon = float(
            area_bins.longitude.mean()
        )

        nearest = nearest_bins(
            bins,
            area_lat,
            area_lon,
            student_waste
        )

        if len(nearest):

            nearest = nearest[
                [
                    "bin_id",
                    "location",
                    "waste_type",
                    "fill_level",
                    "status",
                    "distance_km"
                ]
            ].copy()

            nearest["distance_km"] = (
                nearest["distance_km"]
                .round(3)
            )

            st.markdown(
                "#### Recommended Smart Bin"
            )

            first = nearest.iloc[0]

            st.success(
                f"Recommended Bin: **{first.bin_id}**"
            )

            st.markdown(
                f"""
                <div class="card">

                <b>Location:</b> {first.location}<br>
                <b>Waste Type:</b> {first.waste_type}<br>
                <b>Fill Level:</b> {first.fill_level}%<br>
                <b>Status:</b> {first.status}<br>
                <b>Distance:</b> {first.distance_km} km

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                "#### Other Suitable Bins"
            )

            st.dataframe(
                nearest,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "No suitable available bin found "
                "for this waste type under the prototype rules."
            )

    else:

        st.warning(
            "No location data is available for the selected area."
        )


footer()