import streamlit as st
import streamlit.components.v1 as components
import os
import json

st.sidebar.header('Set Clean-Up Quest Parameters')
max_time = st.sidebar.slider('Upper Time Bound for Trip (hours)', 1, 6, 3)
max_distance = st.sidebar.slider('Upper Distance Bound (miles)', 10, 500, 100)
starting_point = st.sidebar.selectbox('Select Starting Point', ['ISS (ZARYA)', 'CSS (TIANHE)', 'AURORASAT'])
weight_constraint = st.sidebar.number_input('Weight Constraint (kg)', min_value=450, value=4500)

iframe_key = 'unique_key_for_iframe'


st.title('JEDI - Junk Elimination and Debris Interception')

st.write('')

components.html('''
<iframe
  id="unique_key_for_iframe"
  src="http://127.0.0.1/"
  height="600"
  style="width:100%;border:none;"
></iframe>''', height=600)

if st.sidebar.button("Submit"):
  with open("./src/pub/api/parameters.json", "w") as f:
    json.dump({"max_dist": min(max_distance/0.621371, 400*max_time), "starting_point": starting_point, "weight_constraint": int(weight_constraint/404.347)}, f)
  os.system("cd src && cd pub && cd api && python mid_mapper.py")
  with open("./src/pub/api/output.json", "r") as f:
    out = json.load(f)
  st.sidebar.info("Please refresh to view the path!")

  col1, col2 = st.columns(2)
  with col1:
    st.info("Distance to be Travelled: "+str(round(out['total_distance_navigated']*0.621371, 2))+'miles')
    st.warning("Cleaned up "+str(out['num_debris_picked'])+" debris!")
  with col2:
    st.success("Salvaged about "+str(out['salvage_value'])+"k USD worth of debris")
    st.info("Time Period for Trip: "+str(round(round(out['time_taken'], 4)*60, 2))+'mins')
  _, col, _ = st.columns(3)
  with col:
    st.error("Picked up about "+str(round(out['num_debris_picked']*404.347*2.20462, 2))+" pounds of debris!!!")
  components.html(f'<script>document.getElementById("{iframe_key}").src = "http://127.0.0.1/";</script>')

    
if st.sidebar.button("Reset"):
  with open("./src/pub/api/latest.json", "r") as f:
    data = json.load(f)
  data['l'] = [row for row in data['l'] if row[3]!='green']
  with open("./src/pub/api/latest.json", "w") as f:
    json.dump(data, f)
if st.sidebar.button("Scrape Data"):
  os.system("cd src && cd pub && cd api && python scraper.py")