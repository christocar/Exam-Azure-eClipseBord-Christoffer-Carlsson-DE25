import os

import pandas as pd
import requests
import streamlit as st
import altair as alt

# the one line that makes the same code work locally, in compose and in Azure
# only the value changes: localhost, the container name, or the azurewebsites URL
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("eClipseBord")
st.caption("Solar eclipse data from NASA's five millennium catalog")

# collapsed by default, the type codes mean nothing without an explanation
with st.expander("What do the eclipse types mean?"):
    st.markdown("""
    - **T — Total:** the moon completely covers the sun
    - **A — Annular:** the moon is too far away to cover the sun fully, leaving a ring of light
    - **P — Partial:** only part of the sun is covered
    - **H — Hybrid:** shifts between total and annular along the path
    """)

# a tuple as value gives a range slider with two handles
min_year, max_year = st.slider(
    "Year range", min_value=1900, max_value=3000, value=(2000, 2050)
)

# the backend does the counting, we just display it
counts = requests.get(
    f"{API_URL}/eclipses/count-by-type",
    params={"min_year": min_year, "max_year": max_year},
).json()

st.subheader("Eclipses by type")
# altair needs named columns to reference, so the dict becomes a dataframe
chart_data = pd.DataFrame({"type": list(counts.keys()), "count": list(counts.values())})

# using altair instead of st.bar_chart to control the label rotation
chart = alt.Chart(chart_data).mark_bar().encode(
    # labelAngle=0 keeps the type letters horizontal
    x=alt.X("type:N", title="Eclipse type", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("count:Q", title="Number of eclipses"),
)

st.altair_chart(chart, use_container_width=True)

# second call, this one for the raw rows in the table
eclipses = requests.get(
    f"{API_URL}/eclipses",
    params={"min_year": min_year, "max_year": max_year},
).json()

st.subheader(f"{len(eclipses)} eclipses")
st.dataframe(pd.DataFrame(eclipses), use_container_width=True)