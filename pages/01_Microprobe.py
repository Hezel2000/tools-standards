import streamlit as st
import pandas as pd
st.sidebar.button(f'''<a href='http://geoplatform.de'><button style="background-color:LightYellow;">Back to GeoPlatform</button></a>''', unsafe_allow_html=True)

df = pd.read_csv('data/epma_standards.csv')
elements = df.columns[10:129].tolist()

tab1, tab2 = st.tabs(['Elements', 'Holder Images'])

with tab1:
    colel1_1, colel1_2 = st.columns([1,3])
    with colel1_1:
        st.session_state.el1 = st.selectbox('Element', elements, index=8)
    with colel1_2:
        st.session_state.el1_range = st.slider('sel', .0, 100.0, (0., 100.))

    fil = (df[st.session_state.el1] > st.session_state.el1_range[0]) & (df[st.session_state.el1] < st.session_state.el1_range[1])
    st.dataframe(df[fil])

    with st.expander('The entire standards table'):
        st.dataframe(df)
    
with tab2:
    st.write('\test')