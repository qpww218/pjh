import streamlit as st
import random
import time

st.set_page_config(
    page_title="학급 운영 도우미",
    page_icon="🏫",
    layout="wide"
)

# 세션 상태 초기화
if "selected_students" not in st.session_state:
    st.session_state.selected_students = []

st.title("🏫 학급 운영 도우미")

st.markdown("""
반장과 선생님의 효율적인 학급 운영을 돕는 웹앱입니다.

### 제공 기능
- 🪑 자리 배치
- 🎤 발표자 선정
- ⏰ 타이머
""")

tab1, tab2, tab3 = st.tabs([
    "🪑 자리 배치",
    "🎤 발표자 선정",
    "⏰ 타이머"
])

# ---------------------------
# 자리 배치
# ---------------------------
with tab1:

    st.header("🪑 랜덤 자리 배치")

    names_text = st.text_area(
        "학생 명단 입력 (한 줄에 한 명)",
        height=200,
        key="seat_students"
    )

    col1, col2 = st.columns(2)

    with col1:
        rows = st.number_input(
            "행 수",
            min_value=1,
            value=5
        )

    with col2:
        cols = st.number_input(
            "열 수",
            min_value=1,
            value=6
        )

    if st.button("자리 배치 생성"):

        students = [
            name.strip()
            for name in names_text.split("\n")
            if name.strip()
        ]

        if len(students) == 0:
            st.warning("학생 명단을 입력해주세요.")
        else:

            random.shuffle(students)

            total_seats = rows * cols

            while len(students) < total_seats:
                students.append("빈자리")

            st.subheader("배치 결과")

            index = 0

            for r in range(rows):

                cols_data = st.columns(cols)

                for c in range(cols):
                    with cols_data[c]:
                        st.info(students[index])
                    index += 1

# ---------------------------
# 발표자 선정
# ---------------------------
with tab2:

    st.header("🎤 발표자 선정")

    names_text = st.text_area(
        "학생 명단 입력",
        height=200,
        key="speaker_students"
    )

    students = [
        name.strip()
        for name in names_text.split("\n")
        if name.strip()
    ]

    if st.button("발표자 뽑기"):

        remaining = [
            s for s in students
            if s not in st.session_state.selected_students
        ]

        if len(students) == 0:
            st.warning("학생 명단을 입력해주세요.")

        elif len(remaining) == 0:
            st.warning("모든 학생이 이미 선택되었습니다.")

        else:
            selected = random.choice(remaining)

            st.session_state.selected_students.append(selected)

            st.success(f"🎉 발표자: {selected}")

    if st.session_state.selected_students:

        st.subheader("선택된 발표자")

        for student in st.session_state.selected_students:
            st.write("•", student)

        if st.button("발표자 기록 초기화"):
            st.session_state.selected_students = []
            st.rerun()

# ---------------------------
# 타이머
# ---------------------------
with tab3:

    st.header("⏰ 타이머")

    minutes = st.number_input(
        "시간(분)",
        min_value=1,
        value=1
    )

    if st.button("타이머 시작"):

        timer_placeholder = st.empty()

        total_seconds = int(minutes * 60)

        for sec in range(total_seconds, -1, -1):

            mins = sec // 60
            secs = sec % 60

            timer_placeholder.metric(
                "남은 시간",
                f"{mins:02d}:{secs:02d}"
            )

            time.sleep(1)

        st.success("⏰ 시간 종료!")
