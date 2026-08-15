import streamlit as st
import plotly.express as px
from utils.ui import css, sidebar, header, footer
from utils.data import load_data

st.set_page_config(
    page_title='AZGREEN | Collection',
    page_icon='🚛',
    layout='wide'
)

css()
sidebar()

bins, col, rec, mach, imp, pts, stu = load_data()

header(
    'Collection Management',
    'Operational queue for bins requiring intervention'
)

# =========================================================
# DATA PREPARATION
# =========================================================

df = bins[
    [
        'bin_id',
        'location',
        'waste_type',
        'fill_level',
        'status',
        'last_collection',
        'collection_priority',
        'sensor_status'
    ]
].copy()

pending = (
    df[df.status.isin(['Needs Collection', 'Urgent'])]
    .sort_values('fill_level', ascending=False)
)

pending_count = len(pending)
critical_count = int((pending.collection_priority == 'Critical').sum())
high_count = int((pending.collection_priority == 'High').sum())
avg_pending_fill = (
    f'{pending.fill_level.mean():.0f}%'
    if len(pending)
    else '0%'
)

# =========================================================
# MANAGEMENT KPIs — EACH KPI IN ITS OWN CARD
# =========================================================

st.markdown('### Management KPIs')

k1, k2, k3, k4 = st.columns(4, gap='medium')

with k1:
    st.markdown(
        f'''
        <div class="card" style="min-height:120px;">
            <div style="font-size:14px;color:#4f6358;font-weight:600;">Pending</div>
            <div style="font-size:32px;font-weight:700;color:#1B4332;margin-top:8px;">{pending_count}</div>
            <div style="font-size:12px;color:#718078;margin-top:4px;">Bins requiring intervention</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f'''
        <div class="card" style="min-height:120px;">
            <div style="font-size:14px;color:#4f6358;font-weight:600;">Critical</div>
            <div style="font-size:32px;font-weight:700;color:#1B4332;margin-top:8px;">{critical_count}</div>
            <div style="font-size:12px;color:#718078;margin-top:4px;">Immediate collection priority</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f'''
        <div class="card" style="min-height:120px;">
            <div style="font-size:14px;color:#4f6358;font-weight:600;">High</div>
            <div style="font-size:32px;font-weight:700;color:#1B4332;margin-top:8px;">{high_count}</div>
            <div style="font-size:12px;color:#718078;margin-top:4px;">Schedule collection soon</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        f'''
        <div class="card" style="min-height:120px;">
            <div style="font-size:14px;color:#4f6358;font-weight:600;">Avg Pending Fill</div>
            <div style="font-size:32px;font-weight:700;color:#1B4332;margin-top:8px;">{avg_pending_fill}</div>
            <div style="font-size:12px;color:#718078;margin-top:4px;">Average fill of pending bins</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

# =========================================================
# COLLECTION TREND — THE EXISTING CHART, MOVED HERE
# =========================================================

h = col.merge(
    bins[['bin_id', 'location']],
    on='bin_id',
    how='left'
)

q = (
    h.groupby('date', as_index=False)['weight_kg']
    .sum()
    .sort_values('date')
)

st.markdown('### Collection Trend')

if len(q):
    fig = px.area(
        q,
        x='date',
        y='weight_kg',
        labels={
            'date': 'Date',
            'weight_kg': 'Collected Waste (kg)'
        }
    )

    fig.update_traces(
        line_color='#2E7D32',
        fillcolor='rgba(76, 175, 80, 0.20)',
        hovertemplate=(
            '<b>%{x}</b><br>'
            'Collected: %{y:.1f} kg'
            '<extra></extra>'
        )
    )

    fig.update_layout(
        height=340,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#1B4332'),
        xaxis=dict(showgrid=False),
        yaxis=dict(
            gridcolor='#DDEBDD',
            zeroline=False
        ),
        hoverlabel=dict(
            bgcolor='#1B4332',
            font_color='white'
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={'displayModeBar': False}
    )
else:
    st.info('No collection history is available.')

# =========================================================
# COLLECTION QUEUE
# =========================================================

st.markdown('### Collection Queue')
st.dataframe(
    pending,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# PRIORITY RULES
# =========================================================

st.markdown('### Priority Rules')
st.table({
    'Fill Level': ['<50%', '50–70%', '70–90%', '>90%'],
    'Priority': ['Low', 'Medium', 'High', 'Critical'],
    'Action': [
        'Monitor',
        'Monitor',
        'Schedule Collection',
        'Immediate Collection'
    ]
})

# =========================================================
# COLLECTION HISTORY
# =========================================================

st.markdown('### Collection History')

history = h[
    [
        'collection_id',
        'bin_id',
        'location',
        'waste_type',
        'weight_kg',
        'date',
        'collector',
        'destination',
        'batch_id'
    ]
].sort_values('date', ascending=False)

st.dataframe(
    history,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# FUTURE ROUTE OPTIMIZATION
# =========================================================

st.info(
    'Future: combine fill level + time since collection + waste type '
    '+ historical demand + GIS distance for route optimization.'
)

footer()