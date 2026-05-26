pip install streamlit openai
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="LLM Chat App")

st.title("🤖 LLM 질문 웹앱")

# -----------------------------
# API KEY 입력
# -----------------------------

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

api_key = st.text_input(
    "OpenAI API Key 입력",
    type="password",
    value=st.session_state.api_key
)

# session_state 저장
st.session_state.api_key = api_key


# -----------------------------
# 질문 입력
# -----------------------------

question = st.text_input("질문을 입력하세요")


# -----------------------------
# 캐시 함수
# -----------------------------

@st.cache_data(show_spinner=False)
def get_ai_response(api_key, question):

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content


# -----------------------------
# 버튼 클릭
# -----------------------------

if st.button("질문하기"):

    if not api_key:
        st.warning("API Key를 입력하세요.")
    
    elif not question:
        st.warning("질문을 입력하세요.")

    else:
        with st.spinner("응답 생성 중..."):
            answer = get_ai_response(api_key, question)

        st.success("응답 완료!")
        st.write(answer)
