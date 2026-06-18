import streamlit as st

st.set_page_config(
    page_title="학급 운영 도우미",
    page_icon="🏫",
    layout="wide"
)

st.title("🏫 학급 운영 도우미")

st.markdown("""
### 반장과 선생님의 효율적인 학급 운영을 지원하는 웹앱입니다.

자리 배치, 발표자 선정, 시간 관리를 한곳에서 쉽고 빠르게 이용할 수 있습니다.
""")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🪑 자리 배치")
    st.write("학생들의 자리를 랜덤으로 배정합니다.")

with col2:
    st.subheader("🎤 발표자 선정")
    st.write("공정하게 발표자를 랜덤으로 선택합니다.")

with col3:
    st.subheader("⏰ 타이머")
    st.write("발표 시간과 모둠 활동 시간을 관리합니다.")

st.divider()

st.info("왼쪽 사이드바에서 원하는 기능을 선택해 주세요.")

st.markdown("""
### 📌 사용 방법

1. 사이드바에서 원하는 기능을 선택합니다.
2. 필요한 정보를 입력합니다.
3. 결과를 확인하고 학급 운영에 활용합니다.
""")
