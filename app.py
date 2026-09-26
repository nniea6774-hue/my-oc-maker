import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="아기자기 OC 캐릭터 생성기", page_icon="🎨")
st.title("🎨 OC 캐릭터 일러스트 생성기")
st.caption("캐릭터 설정을 입력하시면 아기자기한 동화풍 일러스트로 그려드려요!")

# Streamlit Secrets에서 API Key 가져오기
api_key = st.secrets.get("OPENAI_API_KEY")

user_description = st.text_area(
    "캐릭터 설정을 입력하세요", 
    placeholder="예: 무뚝뚝한 표정의 연노랑/하늘색 투톤 머리 남학생. 베이지색 니트 조끼를 입고 주머니에 작은 곰인형 키링이 들어있음.",
    height=150
)

if st.button("그림 그리기 ✨", type="primary"):
    if not api_key:
        st.error("서버에 API Key가 설정되지 않았습니다. Secrets 설정을 확인해 주세요.")
    elif not user_description.strip():
        st.warning("캐릭터 설명을 입력해 주세요!")
    else:
        with st.spinner("아기자기한 화풍으로 캐릭터를 그리고 있어요... 🎨"):
            try:
                client = OpenAI(api_key=api_key)
                
                # 1. 한국어 설정을 영문 프롬프트로 변환
                translate_prompt = f"""
                Translate and enrich the following Korean character description into a detailed English prompt for image generation.
                
                [Character Description]
                {user_description}
                
                [Style Guidelines]
                - Style: Cute cozy storybook illustration, soft line art, warm pastel color palette.
                - Details: Fine line art, delicate patterns, tiny accessories, cozy and warm lighting.
                - Format: Return ONLY the final English prompt text.
                """
                
                llm_res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": translate_prompt}]
                )
                eng_prompt = llm_res.choices[0].message.content

                # 2. 이미지 생성
                img_res = client.images.generate(
                    model="dall-e-3",
                    prompt=f"{eng_prompt}, cute cozy storybook illustration, soft watercolor texture, intricate small details, warm lighting",
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                
                image_url = img_res.data[0].url
                st.success("완성되었습니다!")
                st.image(image_url, caption="생성된 캐릭터 일러스트", use_container_width=True)
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
