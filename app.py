import urllib.parse
import streamlit as st

st.set_page_config(page_title="아기자기 OC 캐릭터 생성기", page_icon="🎨")
st.title("🎨 OC 캐릭터 일러스트 생성기")
st.caption("캐릭터 설정을 입력하시면 무료 AI가 아기자기한 동화풍 일러스트로 그려드려요!")

user_description = st.text_area(
    "캐릭터 설정을 입력하세요", 
    placeholder="예: 무뚝뚝한 표정의 연노랑/하늘색 투톤 머리 남학생. 베이지색 니트 조끼를 입고 주머니에 작은 곰인형 키링이 들어있음.",
    height=150
)

if st.button("그림 그리기 ✨", type="primary"):
    if not user_description.strip():
        st.warning("캐릭터 설명을 입력해 주세요!")
    else:
        with st.spinner("아기자기한 화풍으로 캐릭터를 그리고 있어요... 🎨"):
            try:
                # 무료 이미지 생성 프롬프트 조합
                prompt = (
                    f"{user_description}, cute cozy storybook illustration, "
                    "soft line art, warm pastel colors, soft watercolor texture, "
                    "intricate details, highly detailed, master piece"
                )
                
                # URL 인코딩 및 Pollinations.ai 무료 이미지 링크 생성
                encoded_prompt = urllib.parse.quote(prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed=42&nologo=true"
                
                st.success("완성되었습니다!")
                st.image(image_url, caption="생성된 캐릭터 일러스트", use_container_width=True)
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
