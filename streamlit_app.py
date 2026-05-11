import streamlit as st
from openai import OpenAI

# 제목 및 설명 설정
st.title("💬 챗봇")
st.write(
    "이 앱은 OpenAI의 GPT-3.5 모델을 사용하여 답변을 생성하는 간단한 챗봇입니다. "
    "앱을 사용하려면 [여기](https://platform.openai.com/account/api-keys)에서 OpenAI API 키를 발급받아 입력해야 합니다. "
    "이 앱을 직접 만드는 방법이 궁금하다면 [단계별 튜토리얼](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)을 확인해 보세요."
)

# st.text_input을 통해 사용자로부터 OpenAI API 키를 입력받음
# 보안을 위해 API 키를 ./.streamlit/secrets.toml에 저장하고 st.secrets로 접근하는 방법도 있습니다.
# 참고: https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API 키", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해 주세요.", icon="🗝️")
else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 채팅 메시지를 저장할 세션 상태(session state) 변수 생성
    # 이를 통해 앱이 재실행되어도 대화 내용이 유지됩니다.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # st.chat_message를 사용하여 기존 채팅 메시지를 화면에 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자가 메시지를 입력할 수 있는 채팅 입력창 생성
    if prompt := st.chat_input("무엇을 도와드릴까요?"):

        # 현재 입력받은 메시지를 세션 상태에 저장하고 화면에 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API를 사용하여 답변 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # st.write_stream을 사용하여 답변을 스트리밍 방식으로 화면에 표시하고 세션 상태에 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

### 💡 주요 변경 사항:

* **st.title & st.write**: 앱의 제목과 설명을 한국어로 번역했습니다.
* **st.text_input**: API 키 입력창의 라벨을 "OpenAI API 키"로 변경했습니다.
* **st.info**: 키가 없을 때 나타나는 안내 문구를 수정했습니다.
* **st.chat_input**: 채팅창의 플레이스홀더를 "무엇을 도와드릴까요?"로 변경했습니다.
* **주석**: 코드의 각 기능을 설명하는 주석도 이해하기 쉽게 한국어로 풀어서 작성했습니다.
