import os

import pandas as pd
import requests
import streamlit as st
import altair as alt

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("eClipseBord")
st.caption("Solar eclipse data from NASA's five millennium catalog")

with st.expander("What do the eclipse types mean?"):
    st.markdown("""
    - **T — Total:** the moon completely covers the sun
    - **A — Annular:** the moon is too far away to cover the sun fully, leaving a ring of light
    - **P — Partial:** only part of the sun is covered
    - **H — Hybrid:** shifts between total and annular along the path
    """)

min_year, max_year = st.slider(
    "Year range", min_value=1900, max_value=3000, value=(2000, 2050)
)

counts = requests.get(
    f"{API_URL}/eclipses/count-by-type",
    params={"min_year": min_year, "max_year": max_year},
).json()

st.subheader("Eclipses by type")
chart_data = pd.DataFrame({"type": list(counts.keys()), "count": list(counts.values())})

chart = alt.Chart(chart_data).mark_bar().encode(
    x=alt.X("type:N", title="Eclipse type", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("count:Q", title="Number of eclipses"),
)

st.altair_chart(chart, use_container_width=True)

eclipses = requests.get(
    f"{API_URL}/eclipses",
    params={"min_year": min_year, "max_year": max_year},
).json()

st.subheader(f"{len(eclipses)} eclipses")
st.dataframe(pd.DataFrame(eclipses), use_container_width=True)