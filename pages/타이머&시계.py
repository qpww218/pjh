import streamlit as st
import time

# 페이지 설정 (웹 브라우저 탭에 표시될 정보)
st.set_page_config(page_title="간편 심플 타이머", page_icon="⏱️", layout="centered")

# 세션 상태(Session State) 초기화 - 새로고침되어도 데이터가 유지되도록 설정
if "total_seconds" not in str.session_state:
    st.session_state.total_seconds = 0
if "current_seconds" not in str.session_state:
    st.session_state.current_seconds = 0
if "is_running" not in str.session_state:
    st.session_state.is_running = False

# 앱 타이틀 및 설명
st.title("⏱️ 시각적 심플 타이머")
st.write("버튼을 눌러 시간을 추가하고 타이머를 시작해보세요!")

---

### 1. 시간 설정 버튼 (1분 / 5분 / 10분 / 초기화)
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

---

### 2. 타이머 화면 표시 및 진행 바
if st.session_state.total_seconds > 0:
    # 남은 시간을 MM:SS 형식으로 변환
    mins, secs = divmod(st.session_state.current_seconds, 60)
    time_format = f"{mins:02d}:{secs:02d}"
    
    # 시간을 큼직하게 시각화 (Metric)
    st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{time_format}</h1>", unsafe_allow_html=True)
    
    # 진행 상황 바 (Progress Bar) 계산 및 표시
    # 0.0 ~ 1.0 사이의 값이어야 하므로 예외 처리 포함
    progress_percentage = float(st.session_state.current_seconds / st.session_state.total_seconds)
    progress_percentage = max(0.0, min(1.0, progress_percentage)) # 안전장치
    
    st.progress(progress_percentage)
else:
    st.info("위의 버튼을 눌러 먼저 타이머 시간을 설정해주세요.")

---

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

    # 타이머가 작동 중일 때 실시간 시간 감소 로직
    if st.session_state.is_running and st.session_state.current_seconds > 0:
        time.sleep(1)
        st.session_state.current_seconds -= 1
        st.rerun()
        
    # 타이머가 종료되었을 때 구동
    elif st.session_state.is_running and st.session_state.current_seconds == 0:
        st.session_state.is_running = False
        st.balloons() # 축하 효과
        st.success("🎉 설정하신 시간이 모두 완료되었습니다!")
        # 완료 후 자동 초기화
        st.session_state.total_seconds = 0
