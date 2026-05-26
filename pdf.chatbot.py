import streamlit as st
from openai import OpenAI

st.title("ChatPDF")

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store_id" not in st.session_state:
    st.session_state.vector_store_id = None

api_key = st.text_input(
    "OpenAI API Key 입력",
    value=st.session_state.api_key,
    type="password"
)

st.session_state.api_key = api_key

uploaded_file = st.file_uploader(
    "PDF 업로드",
    type="pdf"
)

if api_key and uploaded_file and st.session_state.vector_store_id is None:

    client = OpenAI(api_key=api_key)

    vector_store = client.vector_stores.create(
        name="pdf_store"
    )

    client.vector_stores.files.upload_and_poll(
        vector_store_id=vector_store.id,
        file=uploaded_file
    )

    st.session_state.vector_store_id = vector_store.id

    st.success("PDF 업로드 완료")

if st.button("Clear"):

    if st.session_state.vector_store_id:

        client = OpenAI(api_key=api_key)

        client.vector_stores.delete(
            st.session_state.vector_store_id
        )

    st.session_state.vector_store_id = None
    st.session_state.messages = []

    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("질문 입력"):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
        tools=[
            {
                "type": "file_search",
                "vector_store_ids": [
                    st.session_state.vector_store_id
                ]
            }
        ]
    )

    answer = response.output_text

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
