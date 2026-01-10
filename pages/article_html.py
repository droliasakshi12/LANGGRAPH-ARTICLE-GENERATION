import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from typing import TypedDict
from docx import Document
from langgraph.graph import StateGraph, START, END
import streamlit.components.v1 as component
import time

load_dotenv(dotenv_path=r"my_api_key.env")
os.environ['OPENAI_API_KEY'] = os.getenv("openai_api")

if 'login' not in st.session_state:
    st.session_state['login'] = False


elif st.session_state['login'] == True:

    # creating state
    class htmlstate(TypedDict):
        topic: str
        html: str

    model = ChatOpenAI(model="gpt-4.1-mini")

    def generate_html_content(state: htmlstate):
        prompt = f"""
            You are a professional html generator.
            convert the content in complete professional html article on {state['topic']}
            you have to provide me the html code for the content shared.

            DESGIN
            White page background for whole content
            Centered white container (max-width: 900px)
            Font: Segoe UI, Arial, sans-serif
            Blue h1, h2, h3 headings
            Section boxes with a left blue border

            RULES
            - must be in the format of article.
            - keep it attractive but professional
            - do not include anything extra keep the content as it is.
            - keep the image in the image tag when required.
            """
        response = model.invoke(prompt).content
        return {"html": response}

    st.title("GENERATE HTML")

    # reading the file
    upload_file = st.file_uploader("choose file")

    file_data = []
    if upload_file is not None:
        doc = Document(upload_file)

        for para in doc.paragraphs:
            file_data.append(para.text)
    else:
        st.warning("please upload the file first")

    content = "\n".join(file_data)
    st.markdown(content)  # reading the data from file

    # creating graph
    graph = StateGraph(htmlstate)

    # creating nodes
    graph.add_node("generate_html", generate_html_content)

    # creating edge
    graph.add_edge(START, "generate_html")
    graph.add_edge("generate_html", END)

    workflow = graph.compile()
    # initiating state
    initiate_state = {
        "topic": content
    }

    generate = st.button("GENERATE HTML", use_container_width=True)

    if generate:
        with st.spinner('GENERATING RESPONSE....'):
            time.sleep(5)
        # compiling and invoking state
            final_output = workflow.invoke(initiate_state)
            html_output = final_output['html']

        # creating session state
        st.session_state['html_output'] = html_output

        # reading the content
        st.markdown(st.session_state['html_output'], unsafe_allow_html=True)
        # shows the preview for html
        component.html(
            st.session_state['html_output'], height=800, scrolling=True)

    try:
        # creating a button to insert the data into file
        insert_into_file = st.button(
            "INSERT INTO FILE", use_container_width=True)

        if insert_into_file:
            html_file_name = upload_file.name.replace(".docx", ".html")
            if "html_output" not in st.session_state:
                st.warning("please generate the content first")

            else:
                with open(f"{html_file_name}", 'w', encoding="utf-8") as file:
                    file.write(st.session_state['html_output'])

            st.success("data inserted successfully!!")

            # creating a dwonload button to download the file
            st.download_button(
                label="DOWNLOAD HTML",
                data=st.session_state['html_output'],
                file_name=f'{html_file_name}.html',
                mime="text/html",
                icon=":material/download:",
                width='stretch'
            )

    except Exception as e:
        st.error(e)

    article = st.button("GENERATE ARTICLE", use_container_width=True)

    if article:
        st.switch_page("pages/article_generation.py")

else:
    st.switch_page("password.py")
