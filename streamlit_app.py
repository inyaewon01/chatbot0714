import streamlit as st
from openai import OpenAI

# 1. 앱 제목 및 설정
st.set_page_config(page_title="오늘의 코디 챗봇", page_icon="👕")
st.title("👕 기온별 옷차림 추천 챗봇")
st.write(
    "오늘의 기온을 알려주시면 가장 적절한 옷차림을 추천해 드립니다. "
    "OpenAI API 키를 입력하고 대화를 시작해 보세요!"
)

# 2. OpenAI API 키 입력 받기
openai_api_key = st.text_input("OpenAI API 키", type="password")

if not openai_api_key:
    st.info("오른쪽 또는 아래에 OpenAI API 키를 입력해 주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 3. 세션 상태 초기화 (대화 기록 및 시스템 설정)
    if "messages" not in st.session_state:
        # 시스템 메시지를 통해 AI에게 역할을 부여합니다.
        st.session_state.messages = [
            {
                "role": "system", 
                "content": (
                    "너는 한국의 기온별 옷차림 가이드를 완벽하게 숙지한 패션 스타일리스트야. "
                    "사용자가 기온(도)을 말하면, 해당 날씨에 적합한 상의, 하의, 외투, 액세서리를 친절하게 추천해줘. "
                    "예를 들어 4도 이하면 패딩, 12~16도면 자켓이나 가디건 등을 추천하는 식이야. "
                    "사용자가 온도를 말하지 않아도 날씨 관련 질문을 하면 친절히 답해줘."
                )
            }
        ]

    # 4. 저장된 대화 내용 표시 (시스템 메시지는 제외하고 표시)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 5. 채팅 입력창
    if prompt := st.chat_input("오늘 기온은 몇 도인가요? (예: 지금 15도야)"):

        # 사용자의 메시지 저장 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 6. OpenAI API를 통해 답변 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True,
        )

        # 7. 답변 스트리밍 및 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
