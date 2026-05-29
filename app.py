import streamlit as st

st.set_page_config(
    page_title="키 크는 법 앱",
    page_icon="📏"
)

st.title("📏 키 크는 법 알려주는 앱")

st.write("생활 습관을 입력하면 키 성장 팁을 알려줍니다.")

sleep = st.slider("하루 수면 시간", 0, 12, 8)
exercise = st.selectbox(
    "운동 여부",
    ["거의 안 함", "가끔 함", "매일 함"]
)

st.subheader("결과")

if sleep >= 8 and exercise == "매일 함":
    st.success("좋은 습관입니다! 수면과 운동을 꾸준히 유지하세요.")
elif sleep < 6:
    st.warning("수면 시간이 부족합니다. 충분한 수면이 중요합니다.")
else:
    st.info("균형 잡힌 식사와 규칙적인 운동을 추천합니다.")

st.markdown("---")
st.caption("※ 실제 키 성장은 유전, 영양, 수면 등 다양한 영향을 받습니다.")
