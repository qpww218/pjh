import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="스마트 자리배치",
    page_icon="🪑",
    layout="wide"
)

st.title("🪑 스마트 자리배치 앱")

st.sidebar.header("설정")

rows = st.sidebar.number_input(
    "행(Row)",
    min_value=1,
    max_value=10,
    value=5
)

cols = st.sidebar.number_input(
    "열(Column)",
    min_value=1,
    max_value=10,
    value=6
)

student_text = st.text_area(
    "학생 명단 입력 (한 줄에 한 명)",
    height=250
)

if st.button("🎲 자리배치 생성"):

    students = [
        s.strip()
        for s in student_text.split("\n")
        if s.strip()
    ]

    total_seats = rows * cols

    if len(students) > total_seats:
        st.error(
            f"학생 수({len(students)})가 좌석 수({total_seats})보다 많습니다."
        )

    else:

        random.shuffle(students)

        while len(students) < total_seats:
            students.append("")

        data = []

        idx = 0

        for r in range(rows):

            row_data = []

            for c in range(cols):
                row_data.append(students[idx])
                idx += 1

            data.append(row_data)

        df = pd.DataFrame(
            data,
            columns=[f"{i+1}열" for i in range(cols)]
        )

        st.subheader("📚 교탁")

        st.dataframe(
            df,
            use_container_width=True,
            height=400
        )

        csv = df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            "⬇️ CSV 다운로드",
            csv,
            "seat_arrangement.csv",
            "text/csv"
        )
