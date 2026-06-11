import streamlit as st
from google import genai
from google.genai import types

# -------------------------
# 페이지 설정
# -------------------------
st.set_page_config(
    page_title="수행평가 일정 알람 챗봇",
    page_icon="📚"
)

st.title("📚 수행평가 일정 알람 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반")

# -------------------------
# API 키 확인
# -------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("GEMINI_API_KEY가 Secrets에 설정되지 않았습니다.")
    st.stop()

# -------------------------
# Gemini 클라이언트
# -------------------------
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 초기화 오류: {e}")
    st.stop()

# -------------------------
# 세션 상태 초기화
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요! 📚\n\n"
                "수행평가, 시험, 과제 일정을 관리하는 챗봇입니다.\n"
                "예시:\n"
                "- 다음 주까지 해야 할 수행평가 정리해줘\n"
                "- 영어 수행평가 준비 계획 만들어줘\n"
                "- 시험 공부 일정 짜줘"
            )
        }
    ]

# -------------------------
# 채팅 기록 표시
# -------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# 사용자 입력
# -------------------------
user_input = st.chat_input("질문을 입력하세요")

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    try:

        # 대화 기록 구성
        history_text = ""

        for msg in st.session_state.messages:
            role = "사용자" if msg["role"] == "user" else "챗봇"
            history_text += f"{role}: {msg['content']}\n"

        prompt = f"""
당신은 학생들의 학습 도우미입니다.

역할:
- 수행평가 일정 관리
- 시험 준비 계획 제안
- 과제 일정 정리
- 학습 습관 조언

대화 기록:
{history_text}

답변:
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=800
            )
        )

        bot_reply = response.text

    except Exception as e:
        bot_reply = (
            "⚠️ 오류가 발생했습니다.\n\n"
            f"오류 내용: {str(e)}"
        )

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": bot_reply
        }
    )

# -------------------------
# 대화 초기화 버튼
# -------------------------
if st.button("대화 초기화"):
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "대화가 초기화되었습니다. 새로운 질문을 해보세요!"
        }
    ]
    st.rerun()
