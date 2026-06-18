import streamlit as st
import time
from datetime import datetime
import pytz

# 페이지 설정
st.set_page_config(page_title="간편 심플 타이머 & 시계", page_icon="⏱️", layout="centered")

# 세션 상태(Session State) 초기화
if "total_seconds" not in st.session_state:
    st.session_state.total_seconds = 0
if "current_seconds" not in st.session_state:
    st.session_state.current_seconds = 0
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "is_finished" not in st.session_state:
    st.session_state.is_finished = False
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "시계"  # 기본 모드는 '시계'로 설정

# 앱 타이틀
st.title("⏱️ 시각적 심플 타이머 & 시계")

st.divider()

### 1. [기능 추가] 상단 모드 선택 버튼
mode_cols = st.columns(2)

with mode_cols[0]:
    # 시계 모드 버튼 (현재 시계 모드면 강조)
    if st.button("⏱️ 시계 보기", use_container_width=True, type="primary" if st.session_state.current_mode == "시계" else "secondary"):
        st.session_state.current_mode = "시계"
        # 시계로 돌아갈 때는 작동 중이던 타이머 리셋
        st.session_state.total_seconds = 0
        st.session_state.current_seconds = 0
        st.session_state.is_running = False
        st.session_state.is_finished = False
        st.rerun()

with mode_cols[1]:
    # 타이머 모드 버튼 (현재 타이머 모드면 강조)
    if st.button("⏳ 타이머 모드 전환", use_container_width=True, type="primary" if st.session_state.current_mode == "타이머" else "secondary"):
        st.session_state.current_mode = "タイマー" # 내부 구분을 위해 타이머로 변경
        st.session_state.current_mode = "타이머"
        st.rerun()

st.divider()

### 2. 시간 설정 버튼 (타이머 모드일 때만 유효하게 작동)
st.write("### ⚙️ 타이머 시간 추가 버튼")
cols = st.columns(4)

with cols[0]:
    if st.button("➕ 1분 추가", use_container_width=True):
        st.session_state.current_mode = "타이머" # 버튼 누르면 자동으로 타이머 모드로 전환
        st.session_state.total_seconds += 60
        st.session_state.current_seconds += 60
        st.session_state.is_finished = False
        st.rerun()

with cols[1]:
    if st.button("➕ 5분 추가", use_container_width=True):
        st.session_state.current_mode = "타or머"
        st.session_state.current_mode = "타이머"
        st.session_state.total_seconds += 300
        st.session_state.current_seconds += 300
        st.session_state.is_finished = False
        st.rerun()

with cols[2]:
    if st.button("➕ 10분 추가", use_container_width=True):
        st.session_state.current_mode = "타이머"
        st.session_state.total_seconds += 600
        st.session_state.current_seconds += 600
        st.session_state.is_finished = False
        st.rerun()

with cols[3]:
    if st.button("🔄 초기화", use_container_width=True, type="secondary"):
        st.session_state.total_seconds = 0
        st.session_state.current_seconds = 0
        st.session_state.is_running = False
        st.session_state.is_finished = False
        st.rerun()

st.divider()

### 3. 메인 화면 표시 영역
timer_container = st.container()

with timer_container:
    time_text = st.empty()
    progress_bar = st.empty()
    status_text = st.empty()
    
    kst = pytz.timezone('Asia/Seoul')

    # [A] 타이머 모드일 때 (버튼을 눌렀거나 시간이 진행 중일 때)
    if st.session_state.current_mode == "타이머":
        status_text.write("⏳ 타이머 모드 대기/작동 중")
        
        # 시간이 설정되어 있지 않아도 기본적으로 00:00을 띄워둠
        mins, secs = divmod(st.session_state.current_seconds, 60)
        time_text.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
        
        if st.session_state.total_seconds > 0:
            progress_percentage = float(st.session_state.current_seconds / st.session_state.total_seconds)
            progress_bar.progress(max(0.0, min(1.0, progress_percentage)))
        else:
            progress_bar.progress(0.0)

    # [B] 시계 모드일 때 (시간이 실시간으로 흘러감)
    else:
        status_text.write("🇰🇷 현재 대한민국 표준시 (KST)")
        progress_bar.progress(0.0)
        
        # 다른 버튼을 눌러서 세션 상태가 바뀌기 전까지 실시간으로 시계 구동
        while st.session_state.current_mode == "시계":
            now_kst = datetime.now(kst)
            current_time_str = now_kst.strftime("%H:%M:%S")
            time_text.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{current_time_str}</h1>", unsafe_allow_html=True)
            time.sleep(1)
            st.rerun()

st.divider()

### 4. 타이머 제어 및 구동부 (타이머 모드이고 시간이 설정됐을 때만 노출)
if st.session_state.current_mode == "타이머" and st.session_state.total_seconds > 0:
    if not st.session_state.is_running:
        if st.button("▶️ 타이머 시작", use_container_width=True, type="primary"):
            st.session_state.is_running = True
            st.rerun()
    else:
        if st.button("⏸️ 일시 정지", use_container_width=True):
            st.session_state.is_running = False
            st.rerun()

    # 타이머 카운트다운 루프
    while st.session_state.is_running and st.session_state.current_seconds > 0:
        time.sleep(1)
        st.session_state.current_seconds -= 1
        
        mins, secs = divmod(st.session_state.current_seconds, 60)
        time_text.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
        
        progress_percentage = float(st.session_state.current_seconds / st.session_state.total_seconds)
        progress_bar.progress(max(0.0, min(1.0, progress_percentage)))
        
        if st.session_state.current_seconds == 0:
            st.session_state.is_running = False
            st.session_state.is_finished = True
            st.session_state.total_seconds = 0
            st.balloons()
            st.success("🎉 설정하신 시간이 모두 완료되었습니다!")
            st.rerun()
