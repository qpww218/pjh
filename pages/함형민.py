import streamlit as st
import time

# 페이지 설정 (웹 브라우저 탭에 표시될 정보)
st.set_page_config(page_title="간편 심플 타이머", page_icon="⏱️", layout="centered")

# 세션 상태(Session State) 초기화 - 오타 수정 (str -> st)
if "total_seconds" not in st.session_state:
    st.session_state.total_seconds = 0
if "current_seconds" not in st.session_state:
    st.session_state.current_seconds = 0
if "is_running" not in st.session_state:
    st.session_state.is_running = False

# 앱 타이틀 및 설명
st.title("⏱️ 시각적 심플 타이머")
st.write("버튼을 눌러 시간을 추가하고 타이머를 시작해보세요!")

st.divider() # 파이썬 문법에 맞게 구분선 수정

### 1. 시간 설정 버튼 (1분 / 5분 / 10분 / 초기화)
cols = st.columns(4)

with cols[0]:
    if st.button("➕ 1분 추가", use_container_width=True):
        st.session_state.total_seconds += 60
        st.session_state.current_seconds += 60
        st.rerun()

with cols[1]:
    if st.button("➕ 5분 추가", use_container_width=True):
        st.session_state.total_seconds += 300
        st.session_state.current_seconds += 300
        st.rerun()

with cols[2]:
    if st.button("➕ 10분 추가", use_container_width=True):
        st.session_state.total_seconds += 600
        st.session_state.current_seconds += 600
        st.rerun()

with cols[3]:
    if st.button("🔄 초기화", use_container_width=True, type="secondary"):
        st.session_state.total_seconds = 0
        st.session_state.current_seconds = 0
        st.session_state.is_running = False
        st.rerun()

st.divider() # 구분선 수정

### 2. 타이머 화면 표시 및 진행 바를 위한 빈 공간(Placeholder) 생성
# 실시간으로 화면을 부드럽게 갱신하기 위해 container를 활용합니다.
timer_container = st.container()

with timer_container:
    if st.session_state.total_seconds > 0:
        # 실시간 변경될 텍스트와 게이지의 자리를 미리 잡아둡니다.
        time_text = st.empty()
        progress_bar = st.empty()
        
        mins, secs = divmod(st.session_state.current_seconds, 60)
        time_text.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
        
        progress_percentage = float(st.session_state.current_seconds / st.session_state.total_seconds)
        progress_bar.progress(max(0.0, min(1.0, progress_percentage)))
    else:
        st.info("위의 버튼을 눌러 먼저 타이머 시간을 설정해주세요.")

st.divider() # 구분선 수정

### 3. 타이머 제어 및 구동부
if st.session_state.total_seconds > 0:
    # 시작 / 일시정지 버튼
    if not st.session_state.is_running:
        if st.button("▶️ 타이머 시작", use_container_width=True, type="primary"):
            st.session_state.is_running = True
            st.rerun()
    else:
        if st.button("⏸️ 일시 정지", use_container_width=True):
            st.session_state.is_running = False
            st.rerun()

    # [핵심 수정] 타이머 실시간 구동 루프
    # while 루프 안에서 st.empty() 요소들만 갱신해 주어 새로고침 부담을 줄입니다.
    while st.session_state.is_running and st.session_state.current_seconds > 0:
        time.sleep(1)
        st.session_state.current_seconds -= 1
        
        # UI 요소 실시간 업데이트
        mins, secs = divmod(st.session_state.current_seconds, 60)
        time_text.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
        
        progress_percentage = float(st.session_state.current_seconds / st.session_state.total_seconds)
        progress_bar.progress(max(0.0, min(1.0, progress_percentage)))
        
        # 타이머가 도중에 종료되었을 때의 처리
        if st.session_state.current_seconds == 0:
            st.session_state.is_running = False
            st.balloons()
            st.success("🎉 설정하신 시간이 모두 완료되었습니다!")
            st.session_state.total_seconds = 0
            time.sleep(2) # 축하 메시지를 볼 수 있도록 잠시 대기 후
            st.rerun() # 최종 상태 리셋을 위한 rerun
