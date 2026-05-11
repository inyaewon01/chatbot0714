import streamlit as st
from openai import OpenAI

# 1. 제목 및 설명 설정
st.title("💬 챗봇")
st.write(
    "이 앱은 OpenAI의 GPT-3.5 모델을 사용하여 답변을 생성하는 간단한 챗봇입니다. "
    "앱을 사용하려면 [여기](https://platform.openai.com/account/api-keys)에서 OpenAI API 키를 발급받아 입력해야 합니다. "
)

# 2. OpenAI API 키 입력 받기
openai_api_key = st.text_input("OpenAI API 키", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해 주세요.", icon="🗝️")
else:
    # OpenAI 클라이언트 초기화
    client = OpenAI(api_key=openai_api_key)

    # 3. 세션 상태에 메시지 저장 공간 만들기
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 4. 저장된 기존 대화 내용 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. 채팅 입력창 만들기
    if prompt := st.chat_input("무엇을 도와드릴까요?"):

        # 사용자의 메시지 저장 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 6. OpenAI API를 통해 답변 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # 7. 답변을 화면에 스트리밍하고 세션에 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
