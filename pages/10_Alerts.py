import streamlit as st
from utils.ui import css,sidebar,header,footer
from utils.data import load_data
st.set_page_config(page_title='AZGREEN | Alerts',page_icon='🔔',layout='wide');css();sidebar();bins,col,rec,mach,imp,pts,stu=load_data();header('Alerts','Management notification center driven by prototype rules');alerts=[]
for _,r in bins[bins.status=='Urgent'].sort_values('fill_level',ascending=False).iterrows():alerts.append(('🔴',f'Bin {r.bin_id} is Full / Collection Required',f'{r.location} • {r.fill_level}% • Critical'))
for _,r in bins[bins.status=='Needs Collection'].sort_values('fill_level',ascending=False).iterrows():alerts.append(('🟡',f'Bin {r.bin_id} is Nearly Full',f'{r.location} • {r.fill_level}% • High priority'))
for _,r in bins[bins.sensor_status!='Online'].iterrows():alerts.append(('⚫',f'Sensor {r.bin_id} requires maintenance',f'{r.location} • {r.sensor_status}'))
alerts += [('🔵','Batch traceability available','Recycling & Impact'),('🟣','AI prediction planned','Future Development')]
for icon,title,detail in alerts:st.markdown(f'<div class="card" style="margin-bottom:9px"><b>{icon} {title}</b><br><span style="color:#66756B;font-size:.8rem">{detail}</span></div>',unsafe_allow_html=True)
st.caption('Prototype alerts are generated from simulated data and simple rules.');footer()
