import streamlit as st,plotly.express as px
from utils.ui import css,sidebar,header,footer
from utils.data import load_data
st.set_page_config(page_title='AZGREEN | Machine',page_icon='⚙️',layout='wide');css();sidebar();bins,col,rec,mach,imp,pts,stu=load_data();header('Machine Monitoring','Prototype telemetry for the shredder / processing machine');r=mach.iloc[-1];a,b,c,d=st.columns(4);a.metric('Machine Status',r.status);b.metric('Material',r.material);c.metric('Input',f'{r.input_weight:.1f} kg');d.metric('Processed',f'{r.processed_weight:.1f} kg');x,y=st.columns(2)
with x:st.plotly_chart(px.line(mach,y='temperature',markers=True,color_discrete_sequence=['#0B5D2A']),use_container_width=True,config={'displayModeBar':False})
with y:st.plotly_chart(px.line(mach,y='power_consumption',markers=True,color_discrete_sequence=['#72C287']),use_container_width=True,config={'displayModeBar':False})
st.warning('Prototype / Simulated Machine Data. Future ESP32/sensor telemetry can replace these values.');st.dataframe(mach.tail(20),use_container_width=True,hide_index=True);footer()
