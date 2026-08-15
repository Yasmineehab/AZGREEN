from pathlib import Path
import numpy as np, pandas as pd, streamlit as st
BASE=Path(__file__).resolve().parents[1]/"data"
@st.cache_data
def load_data():
 bins=pd.read_csv(BASE/"Bins.csv"); col=pd.read_csv(BASE/"Waste_Collection.csv"); rec=pd.read_csv(BASE/"Recycling.csv"); mach=pd.read_csv(BASE/"Machine.csv"); imp=pd.read_csv(BASE/"Impact.csv"); pts=pd.read_csv(BASE/"Collection_Points.csv"); stu=pd.read_csv(BASE/"Student_Engagement.csv")
 for df,cs in [(bins,['last_collection']),(col,['date']),(rec,['processing_date']),(imp,['date'])]:
  for c in cs: df[c]=pd.to_datetime(df[c],errors='coerce')
 return bins,col,rec,mach,imp,pts,stu
def metrics(bins,col,rec,imp,stu):
 total=col.weight_kg.sum()

 # Recyclable stream captured by the recycling process.
 recyclable=col.loc[
  col.waste_type.isin(['Plastic','Paper','Cardboard','Metal','Glass']),
  'weight_kg'
 ].sum()

 # Final recovered material from the recycling process.
 recycled=rec.output_weight.sum()

 # Diversion is calculated only from waste streams with an explicit
 # recovery destination in the collection data (recycling or composting).
 # The Impact sheet is a separate daily simulated dataset and must not be
 # used as the denominator for the collection-level KPI.
 diverted=col.loc[
  col.destination.isin(['Recycling Unit','Composting Unit']),
  'weight_kg'
 ].sum()

 # Overflow follows the project rule for a Full/Critical bin: 91-100%.
 overflow=int((bins.fill_level>=91).sum())

 return {
  'total':total,
  'recyclable':recyclable,
  'recycled':recycled,
  'diverted':diverted,
  'total_bins':len(bins),
  'available':int(bins.status.isin(['Normal','Monitor']).sum()),
  'nearly':int((bins.status=='Needs Collection').sum()),
  'full':int((bins.status=='Urgent').sum()),
  'online':int((bins.sensor_status=='Online').sum()),
  'offline':int((bins.sensor_status!='Online').sum()),
  'avg_fill':bins.fill_level.mean(),
  'diversion':diverted/total*100 if total else 0,
  'recycling_rate':recycled/recyclable*100 if recyclable else 0,
  'overflow':overflow,
  'operations':len(col),
  'co2':imp.co2_avoided_demo.sum(),
  'products':rec.output_weight.sum(),
  'students':int(stu.active_students.sum())
}
def nearest_bins(bins,lat,lon,waste):
 x=bins[(bins.status.isin(['Normal','Monitor']))&(bins.waste_type.isin([waste,'Mixed']))].copy()
 if x.empty:return x
 r=6371;p1=np.radians(lat);p2=np.radians(x.latitude);dp=np.radians(x.latitude-lat);dl=np.radians(x.longitude-lon);a=np.sin(dp/2)**2+np.cos(p1)*np.cos(p2)*np.sin(dl/2)**2;x['distance_km']=2*r*np.arcsin(np.sqrt(a));return x.sort_values('distance_km').head(5)
