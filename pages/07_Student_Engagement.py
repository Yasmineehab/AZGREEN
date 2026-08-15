import streamlit as st,plotly.express as px
from utils.ui import css,sidebar,header,footer
from utils.data import load_data
st.set_page_config(page_title='AZGREEN | Student Engagement',page_icon='🎓',layout='wide');css();sidebar();bins,col,rec,mach,imp,pts,stu=load_data();header('Student Engagement','Prototype of the future student-facing participation layer',True)
a,b,c,d=st.columns(4);a.metric('Active Students',f'{stu.active_students.sum():,}');b.metric('Recycling Actions',f'{stu.recycling_actions.sum():,}');c.metric('Points Earned',f'{stu.points_earned.sum():,}');d.metric('Waste Diverted',f'{stu.waste_diverted_kg.sum():,.1f} kg')
x,y=st.columns(2)
with x:st.plotly_chart(px.bar(stu.sort_values('active_students'),x='active_students',y='area',orientation='h'),use_container_width=True,config={'displayModeBar':False})
with y:st.plotly_chart(px.bar(stu.sort_values('points_earned'),x='points_earned',y='area',orientation='h'),use_container_width=True,config={'displayModeBar':False})
st.markdown('<div class="journey"><div class="step"><b>Student App</b><br>Open</div><div class="arrow">→</div><div class="step"><b>Nearest Suitable Bin</b><br>Find</div><div class="arrow">→</div><div class="step"><b>Waste Sorting</b><br>Dispose</div><div class="arrow">→</div><div class="step"><b>Points / Rewards</b><br>Engage</div></div>',unsafe_allow_html=True);st.info('Future: student app → nearest suitable bin → verified recycling action → points/rewards → management analytics.');st.dataframe(stu.sort_values('points_earned',ascending=False),use_container_width=True,hide_index=True);footer()
