import streamlit as st


if 'login' not in st.session_state:
    st.session_state['login'] = False

if st.session_state['login'] == True:

    article = st.button("GENERATE ARTICLE", use_container_width=True)
    html = st.button("GENERATE HTML", use_container_width=True)

    if article:
        st.switch_page("pages/article_generation.py")
        
    elif html:
        st.switch_page("pages/article_html.py")
else:
    st.switch_page("password.py")
