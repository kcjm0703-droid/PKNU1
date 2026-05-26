import streamlit as st
from openai import OpenAI

st.title("LLM 웹 앱")

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

api_key = st.text_input(
    "OpenAI API Key 입력",
    value=st.session_state.api_key,
    type="password"
)

st.session_state.api_key = api_key

question = st.text_input("질문 입력")

@st.cache_data

def get_response(api_key, question):
    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-5-mini",
        input=question
    )

    return response.output_text

if st.button("질문하기"):
    if not api_key:
        st.warning("API Key를 입력하세요.")

    elif not question:
        st.warning("질문을 입력하세요.")

    else:
        answer = get_response(api_key, question)
        st.write(answer)
