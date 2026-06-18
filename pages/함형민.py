import pytz
print(pytz.__version__)

import streamlit as st
import time
from datetime import datetime
import pytz  # 대한민국 시간대를 정확히 가져오기 위한 라이브러리

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

# 앱 타이틀 및 설명
st.title("⏱️ 시각적 심플 타이머 & 대한민국 시계")
st.write("타이머가 비어있을 때는 현재 한국 시간을 보여줍니다. 버튼을 눌러 타이머를 시작해보세요!")

st.divider()

### 1. 시간 설정 버튼 (1분 / 5분 / 10분 / 초기화)
cols = st.columns(4)

with cols[0]:
    if st.button("➕ 1분 추가", use_container_width=True):
        st.session_state.total_seconds += 60
        st.session_state.current_seconds += 60
        st.session_state.is_finished = False
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
        st.session_state.is_finished = False
        st.rerun()

st.divider()

### 2. 메인 화면 표시 영역 (타이머 OR 실시간 시계)
timer_container = st.container()

with timer_container:
    time_text = st.empty()
    progress_bar = st.empty()
    status_text = st.empty()  # 현재 시계 모드인지 타이머 모드인지 알려주는 문구
    
    # 대한민국 시간대 설정
    kst = pytz.timezone('Asia/Seoul')

    # [Case 1] 타이머 시간 설정이 되어있거나 방금 막 종료된 상태
    if st.session_state.total_seconds > 0 or st.session_state.is_finished:
        status_text.write("⏳ 타이머 모드 작동 중")
        
        # 기본 타이머 시간 표시
        mins, secs = divmod(st.session_state.current_seconds, 60)
        time_text.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
        
        if st.session_state.total_seconds > 0:
            progress_percentage = float(st.session_state.current_seconds / st.session_state.total_seconds)
            progress_bar.progress(max(0.0, min(1.0, progress_percentage)))
        else:
            progress_bar.progress(0.0)

    # [Case 2] 대기 상태 ➔ 대한민국 실시간 시계 작동 (핵심 추가 변경)
    else:
        status_text.write("🇰🇷 현재 대한민국 표준시 (KST)")
        progress_bar.progress(0.0) # 시계 모드일 땐 게이지 비워두기
        
        # 사용자가 버튼을 누르기 전까지 무한 루프를 돌며 초단위로 현재 시각을 업데이트합니다.
        # Streamlit 구조상 버튼을 누르면 이 루프가 깨지고 상단부터 코드가 재실행됩니다.
        while st.session_state.total_seconds == 0 and not st.session_state.is_finished:
            now_kst = datetime.now(kst)
            current_time_str = now_kst.strftime("%H:%M:%S")
            time_text.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{current_time_str}</h1>", unsafe_allow_html=True)
            time.sleep(1)
            st.rerun()

st.divider()

### 3. 타이머 제어 및 구동부
if st.session_state.total_seconds > 0:
    # 시작 / 일시정지 버튼 컨트롤
    if not st.session_state.is_running:
        if st.button("▶️ 타이머 시작", use_container_width=True, type="primary"):
            st.session_state.is_running = True
            st.rerun()
    else:
        if st.button("⏸️ 일시 정지", use_container_width=True):
            st.session_state.is_running = False
            st.rerun()

    # 타이머 가동 루프
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
