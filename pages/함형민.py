import streamlit as st
import time

# 페이지 설정
st.set_page_config(page_title="간편 심플 타이머", page_icon="⏱️", layout="centered")

# 세션 상태(Session State) 초기화
if "total_seconds" not in st.session_state:
    st.session_state.total_seconds = 0
if "current_seconds" not in st.session_state:
    st.session_state.current_seconds = 0
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "is_finished" not in st.session_state: # 타이머 종료 상태를 기억할 변수 추가
    st.session_state.is_finished = False

# 앱 타이틀 및 설명
st.title("⏱️ 시각적 심플 타이머")
st.write("버튼을 눌러 시간을 추가하고 타이머를 시작해보세요!")

st.divider()

### 1. 시간 설정 버튼 (1분 / 5분 / 10분 / 초기화)
cols = st.columns(4)

with cols[0]:
    if st.button("➕ 1분 추가", use_container_width=True):
        st.session_state.total_seconds += 60
        st.session_state.current_seconds += 60
        st.session_state.is_finished = False # 새 시간을 추가하면 완료 상태 해제
        st.rerun()

with cols[1]:
    if st.button("➕ 5분 추가", use_container_width=True):
        st.session_state.total_seconds += 300
        st.session_state.current_seconds += 300
        st.session_state.is_finished = False
        st.rerun()

with cols[2]:
    if st.button("➕ 10분 추가", use_container_width=True):
        st.session_state.total_seconds += 600
        st.session_state.current_seconds += 600
        st.session_state.is_finished = False
        st.rerun()

with cols[3]:
    if st.button("🔄 초기화", use_container_width=True, type="secondary"):
        st.session_state.total_seconds = 0
        st.session_state.current_seconds = 0
        st.session_state.is_running = False
        st.session_state.is_finished = False # 초기화 시 완전히 리셋
        st.rerun()

st.divider()

### 2. 타이머 화면 표시 및 진행 바 (항시 유지 영역)
timer_container = st.container()

with timer_container:
    # 시간이 설정되어 있거나, 혹은 이미 타이머가 완료된 상태라면 00:00을 계속 띄웁니다.
    if st.session_state.total_seconds > 0 or st.session_state.is_finished:
        time_text = st.empty()
        progress_bar = st.empty()
        
        # 시간 표시 (MM:SS)
        mins, secs = divmod(st.session_state.current_seconds, 60)
        time_text.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
        
        # 진행 바 표시 (0초일 때는 안전하게 0.0으로 고정)
        if st.session_state.total_seconds > 0:
            progress_percentage = float(st.session_state.current_seconds / st.session_state.total_seconds)
            progress_bar.progress(max(0.0, min(1.0, progress_percentage)))
        else:
            progress_bar.progress(0.0)
    else:
        st.info("위의 버튼을 눌러 먼저 타이머 시간을 설정해주세요.")

st.divider()

### 3. 타이머 제어 및 구동부
if st.session_state.total_seconds > 0:
    # 시작 / 일시정지 버튼 컨트롤
    if not st.session_state.is_running:
        if st.button("▶️ 타이머 시작", use_container_width=True, type
