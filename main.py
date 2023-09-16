import streamlit as st
import streamlit.components.v1 as components

st.sidebar.header('Trip Parameters')
max_time = st.sidebar.slider('Max Time for Trip (hours)', 1, 24, 12)
max_distance = st.sidebar.slider('Max Distance Traveled (km)', 10, 500, 100)
starting_point = st.sidebar.selectbox('Select Starting Point', ['Point A', 'Point B', 'Point C'])
weight_constraint = st.sidebar.number_input('Weight Constraint (kg)', min_value=0, value=50)

components.html('''
<h1> Trip </h1>''')

st.write('')

components.html('''
<iframe
  src="http://127.0.0.1/"
  height="600"
  style="width:100%;border:none;"
></iframe>''', height=600)

st.write('### User Inputs')
st.write(f'- Max Time for Trip: {max_time} hours')
st.write(f'- Max Distance Traveled: {max_distance} km')
st.write(f'- Starting Point: {starting_point}')
st.write(f'- Weight Constraint: {weight_constraint} kg')
st.write('Check out your scheduled plan: http://127.0.0.1/')