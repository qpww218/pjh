import streamlit as st
import random
import time

# 페이지 설정 (기본 레이아웃을 넓게 설정)
st.set_page_config(
    page_title="클래스 마스터 - 발표자 뽑기",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 수월한 수업을 위한 발표자 뽑기 도우미")
st.caption("반장과 선생님이 수업 시간에 공정하고 재미있게 발표자를 선정할 수 있는 도구입니다.")
st.markdown("---")

# 세션 상태(Session State) 초기화 - 새로고침해도 이력이 유지되도록 함
if 'history' not in st.session_state:
    st.session_state.history = []

# 화면을 좌우 2컬럼으로 분할
col1, col2 = st.columns([1, 1], gap="large")

# --- 왼쪽 컬럼: 명단 입력 및 추첨 제어 ---
with col1:
    st.subheader("👥 학생 명단 설정")
    
    # 예시 명단 기본 제공
    default_students = "김철수, 이영희, 박민수, 최지원, 정다은, 강하늘, 홍길동, 임꺽정"
    
    student_input = st.text_area(
        "우리 반 학생 이름을 입력하세요 (쉼표 또는 줄바꿈으로 구분):",
        value=default_students,
        height=150,
        help="이름을 변경하거나 새로 붙여넣은 뒤 가공됩니다."
    )
    
    # 입력된 문자열을 리스트로 변환 및 공백 제거
    # 쉼표(,)나 줄바꿈(\n) 모두 대응할 수 있도록 처리
    raw_list = student_input.replace("\n", ",").split(",")
    students = [name.strip() for name in raw_list if name.strip()]
    
    # 현재 등록 인원 표시
    st.metric(label="현재 등록된 학생 수", value=f"{len(students)} 명")
    
    st.markdown("---")
    st.subheader("🎲 추첨하기")
    
    if not students:
        st.error("⚠️ 학생 이름을 최소 1명 이상 입력해주세요.")
    else:
        # 한번에 뽑을 인원 설정 (최대치는 현재 학생 수)
        num_to_pick = st.number_input(
            "한 번에 뽑을 발표자 수:", 
            min_value=1, 
            max_value=len(students), 
            value=1
        )
        
        # 추첨 버튼
        if st.button("🚀 발표자 추첨 시작!", use_container_width=True, type="primary"):
            st.markdown("### 🥁 두구두구두구... 결과는?")
            
            # 효과적인 연출을 위한 텍스트 플레이스홀더 생성
            roll_placeholder = st.empty()
            
            # 긴장감을 주는 무작위 이름 롤링 효과 (0.8초간 진행)
            for _ in range(8):
                random_name = random.choice(students)
                roll_placeholder.markdown(f"<h2 style='text-align: center; color: #7f8c8d;'>🎲 {random_name} ...</h2>", unsafe_allow_html=True)
                time.sleep(0.1)
            
            # 실제 당첨자 선정
            selected_students = random.sample(students, num_to_pick)
            result_text = ", ".join(selected_students)
            
            # 화면에 최종 결과 크게 표시
            roll_placeholder.markdown(
                f"<div style='background-color: #e8f4f8; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #3498db;'>"
                f"<h1 style='color: #2980b9; margin: 0;'>🎉 {result_text} 🎉</h1>"
                f"</div>", 
                unsafe_allow_html=True
            )
            
            # 효과 축하 폭죽
            st.balloons()
            
            # 히스토리에 기록 기록 (최신 항목이 위로 가도록 저장 시간 포함)
            current_time = time.strftime('%H:%M:%S')
            st.session_state.history.append(f"⏱️ [{current_time}] 당첨: {result_text}")

# --- 오른쪽 컬럼: 실시간 추첨 이력 확인 ---
with col2:
    st.subheader("📜 이번 교시 발표자 이력")
    st.write("누가 언제 뽑혔는지 실시간으로 확인하고 중복을 방지할 수 있습니다.")
    
    if st.session_state.history:
        # 지우기 버튼
        if st.button("🗑️ 이력 초기화", size="small"):
            st.session_state.history = []
            st.rerun()
            
        st.markdown("---")
        # 최근 이력이 가장 위로 오도록 역순 출력
        for record in reversed(st.session_state.history):
            st.info(record)
    else:
        st.write("아직 추첨한 이력이 없습니다. 왼쪽에서 버튼을 눌러보세요!")
