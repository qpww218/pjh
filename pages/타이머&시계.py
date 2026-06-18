import streamlit as st
import time
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="멀티 시계 & 타이머", page_icon="⏱️", layout="centered")

# 세션 상태(Session State) 초기화
if "total_seconds" not in st.session_state:
    st.session_state.total_seconds = 0
if "current_seconds" not in st.session_state:
    st.session_state.current_seconds = 0
if "is_running" not in st.session_state:
    st.session_state.is_running = False

st.title("⏱️ 스마트 시계 & 타이머")

---

### 1. [신규 기능] 현재 시간 표시 (12시 / 24시 기준 전환)
st.subheader("🕒 현재 시간")

# 토글 버튼으로 12시간제 / 24시간제 선택
time_format_option = st.radio(
    "시간 표시 형식을 선택하세요:",
    ("12시간 기준 (AM/PM)", "24시간 기준"),
    horizontal=True
)

# 현재 시간 가져오기
now = datetime.now()

if time_format_option == "12시간 기준 (AM/PM)":
    current_time_str = now.strftime("%p %I:%M:%S") # %p: AM/PM, %I: 12시간 형식
    # 조금 더 친숙한 한국어 표기를 원할 경우 치환
    current_time_str = current_time_str.replace("AM", "오전").replace("PM", "오후")
else:
    current_time_str = now.strftime("%H:%M:%S") # %H: 24시간 형식

# 현재 시간을 크게 표시
st.markdown(f"<h2 style='text-align: center; color: #4F8BF9;'>{current_time_str}</h2>", unsafe_allow_html=True)

---

### 2. 타이머 기능 (기존 요청 사항 유지)
st.subheader("⌛ 타이머 설정")

cols = st.columns(4)
with cols[0]:
    if st.button("➕ 1분 추가", use_container_width=True):
        st.session_state.total_seconds += 60
        st.session_state.current_seconds += 60

with cols[1]:
    if st.button("➕ 5분 추가", use_container_width=True):
        st.session_state.total_seconds += 300
        st.session_state.current_seconds += 300

with cols[2]:
    if st.button("➕ 10분 추가", use_container_width=True):
        st.session_state.total_seconds += 600
        st.session_state.current_seconds += 600

with cols[3]:
    if st.button("🔄 초기화", use_container_width=True, type="secondary"):
        st.session_state.total_seconds = 0
        st.session_state.current_seconds = 0
        st.session_state.is_running = False
        st.rerun()

# 타이머 화면 표시 및 진행 바
if st.session_state.total_seconds > 0:
    mins, secs = divmod(st.session_state.current_seconds, 60)
    timer_format = f"{mins:02d}:{secs:02d}"
    
    st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{timer_format}</h1>", unsafe_allow_html=True)
    
    # 진행 상황 바
    progress_percentage = float(st.session_state.current_seconds / st.session_state.total_seconds)
    progress_percentage = max(0.0, min(1.0, progress_percentage))
    st.progress(progress_percentage)
else:
    st.info("위의 버튼을 눌러 타이머 시간을 설정하면 타이머가 활성화됩니다.")

---

### 3. 타이머 제어 및 실시간 새로고침 (시계/타이머 공통)
if st.session_state.total_seconds > 0:
    if not st.session_state.is_running:
        if st.button("▶️ 타이머 시작", use_container_width=True, type="primary"):
            st.session_state.is_running = True
            st.rerun()
    else:
        if st.button("⏸️ 일시 정지", use_container_width=True):
            st.session_state.is_running = False
            st.rerun()

# 1초마다 화면을 새로고침하여 시계와 타이머를 실시간으로 업데이트
time.sleep(1)

if st.session_state.is_running and st.session_state.current_seconds > 0:
    st.session_state.current_seconds -= 1
    st.rerun()
elif st.session_state.is_running and st.session_state.current_seconds == 0:
    st.session_state.is_running = False
    st.balloons()
    st.success("🎉 설정하신 시간이 모두 완료되었습니다!")
    st.session_state.total_seconds = 0
else:
    # 타이머가 안 돌 때도 시계 초바늘이 가야 하므로 화면을 계속 리프레시해줍니다.
    st.rerun()
