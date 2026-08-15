# AZGREEN — Smart Campus Waste Management Dashboard v2

Management interface for Monitoring + Analytics + Decision Support.

Architecture: **IoT Sensors → Smart Bins → Database → Dashboard + GIS → Analytics / Decisions**

Core pages: Overview, GIS Map, Smart Bin Management, Analytics, Collection Management, Recycling & Impact.
Advanced pages: Student Engagement, Machine Monitoring, AI/Future, Alerts.

All current CSV values are **Prototype / Simulated Data**. Do not claim Live/Real-time IoT, AI-powered predictions, or validated CO₂ impact until implemented and validated.

Run: `pip install -r requirements.txt` then `streamlit run app.py`

## GIS Coordinate Note
The dashboard uses the Al-Azhar University Nasr City campus reference point **30.0561242, 31.3169891** supplied via the project brief/user map link. The Smart Bin and Collection Point coordinates are simulated prototype coordinates re-anchored around this campus point while preserving their relative spatial pattern. They are not surveyed GPS measurements.
